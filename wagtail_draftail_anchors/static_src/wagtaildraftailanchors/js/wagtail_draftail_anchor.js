const React = window.React;
const RichUtils = window.DraftJS.RichUtils;
const Modifier = window.DraftJS.Modifier;
const SelectionState = window.DraftJS.SelectionState;
const TooltipEntity = window.draftail.TooltipEntity;
const Icon = window.wagtail.components.Icon;
const EditorState = window.DraftJS.EditorState;
const Portal = window.wagtail.components.Portal;
const Tooltip = window.draftail.Tooltip;
import slugify from "slugify";

// Implement the new APIs.

const DECORATORS = [];
const CONTROLS = [];
const DRAFT_PLUGINS = [];

const registerDecorator = (decorator) => {
  DECORATORS.push(decorator);
  return DECORATORS;
};

const registerControl = (control) => {
  CONTROLS.push(control);
  return CONTROLS;
};

const registerDraftPlugin = (plugin) => {
  DRAFT_PLUGINS.push(plugin);
  return DRAFT_PLUGINS;
};

// Override the existing initEditor to hook the new APIs into it.
// This works in Wagtail 2.0 but will definitely break in a future release.
const initEditor = window.draftail.initEditor;

const initEditorOverride = (selector, options, currentScript) => {
  const overrides = {
    decorators: DECORATORS.concat(options.decorators || []),
    controls: CONTROLS.concat(options.controls || []),
    plugins: DRAFT_PLUGINS.concat(options.plugins || []),
  };

  const newOptions = Object.assign({}, options, overrides);

  return initEditor(selector, newOptions, currentScript);
};

window.draftail.registerControl = registerControl;
window.draftail.registerDecorator = registerDecorator;
window.draftail.initEditor = initEditorOverride;

class AnchorIdentifierSource extends React.Component {
  componentDidMount() {
    const { editorState, entityType, onComplete } = this.props;

    const content = editorState.getCurrentContent();

    const anchor = window.prompt("Anchor identifier:");

    // Uses the Draft.js API to create a new entity with the right data.
    if (anchor) {
      const contentWithEntity = content.createEntity(
        entityType.type,
        "MUTABLE",
        {
          anchor: slugify(anchor.toLowerCase()),
        }
      );
      const entityKey = contentWithEntity.getLastCreatedEntityKey();
      const selection = editorState.getSelection();
      const nextState = RichUtils.toggleLink(editorState, selection, entityKey);

      onComplete(nextState);
    } else {
      onComplete(editorState);
    }
  }

  render() {
    return null;
  }
}

const getAnchorIdentifierAttributes = (data) => {
  const url = data.anchor || null;
  let icon = <Icon name="anchor" />;
  let label = `#${url}`;

  return {
    url,
    icon,
    label,
  };
};

const AnchorIdentifier = (props) => {
  const { entityKey, contentState } = props;
  const data = contentState.getEntity(entityKey).getData();

  return <TooltipEntity {...props} {...getAnchorIdentifierAttributes(data)} />;
};

window.draftail.registerPlugin({
  type: "ANCHOR-IDENTIFIER",
  source: AnchorIdentifierSource,
  decorator: AnchorIdentifier,
});

const CopyAnchorButton = ({identifier}) => {
  const [didCopy, setDidCopy] = React.useState(false);

  const copyText = (event) => {
    // Prevent the button click event from submitting the page form
    event.preventDefault();
    navigator.clipboard.writeText(identifier);
    setDidCopy(true);
  }

  const classes = `button button-small ${didCopy ? "button-secondary" : ""}`;
  return (
    <button
      class={classes}
      style={{ marginLeft: "1rem" }}
      aria-label="Copy anchor identifier"
      aria-live="polite"
      role="button"
      onClick={copyText}
    >
      {didCopy ? "Copied" : "Copy"}
    </button>
  );
}

class UneditableAnchorDecorator extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      showTooltipAt: null,
    };

    this.openTooltip = this.openTooltip.bind(this);
    this.closeTooltip = this.closeTooltip.bind(this);
  }

  openTooltip(e) {
    const trigger = e.target.closest("[data-draftail-trigger]");

    // Click is within the tooltip.
    if (!trigger) {
      return;
    }

    const container = trigger.closest("[data-draftail-editor-wrapper]");
    const containerRect = container.getBoundingClientRect();
    const rect = trigger.getBoundingClientRect();

    this.setState({
      showTooltipAt: {
        container: container,
        top:
          rect.top -
          containerRect.top -
          (document.documentElement.scrollTop || document.body.scrollTop),
        left:
          rect.left -
          containerRect.left -
          (document.documentElement.scrollLeft || document.body.scrollLeft),
        width: rect.width,
        height: rect.height,
      },
    });
  }

  closeTooltip() {
    this.setState({ showTooltipAt: null });
  }

  render() {
    const children = this.props.children;

    const slugified = slugify(this.props.decoratedText.toLowerCase());
    const anchor = `#${slugified}`;
    const content = [
      anchor,
      <CopyAnchorButton identifier={slugified} />,
    ];
    const { showTooltipAt } = this.state;

    // Contrary to what JSX A11Y says, this should be a button but it shouldn't be focusable.
    /* eslint-disable springload/jsx-a11y/interactive-supports-focus */
    return (
      <a
        href=""
        name={anchor}
        role="button"
        // Use onMouseUp to preserve focus in the text even after clicking.
        onMouseUp={this.openTooltip}
        className="TooltipEntity"
        data-draftail-trigger
      >
        <sub>
          <Icon name="anchor" className="TooltipEntity__icon" />
        </sub>
        {children}
        {showTooltipAt && (
          <Portal
            node={showTooltipAt.container}
            onClose={this.closeTooltip}
            closeOnClick
            closeOnType
            closeOnResize
          >
            <Tooltip target={showTooltipAt} direction="top">
              {content}
            </Tooltip>
          </Portal>
        )}
      </a>
    );
  }
}

function headingStrategy(contentBlock, callback, contentState) {
  if (contentBlock.getType().includes("header")) {
    callback(0, contentBlock.getLength());
  }
}

registerDraftPlugin({
  decorators: [
    {
      strategy: headingStrategy,
      component: UneditableAnchorDecorator,
    },
  ],
  onChange: (editorState, PluginFunctions) => {
    // if content has been modified, update all heading blocks's data with
    // a slugified version of their contents as 'anchor', for use
    // in generating anchor links consistently with their displayed form
    let content = editorState.getCurrentContent();
    if (content == PluginFunctions.getEditorState().getCurrentContent()) {
      return editorState;
    }
    const blocks = content.getBlockMap();
    const selection = editorState.getSelection();
    let newEditorState = editorState;
    for (let [key, block] of blocks.entries()) {
      if (block.getType().includes("header")) {
        let blockSelection = SelectionState.createEmpty(key);
        let newData = new Map();
        newData.set("anchor", slugify(block.getText().toLowerCase()));
        content = Modifier.mergeBlockData(content, blockSelection, newData);
      }
    }
    newEditorState = EditorState.push(
      editorState,
      content,
      editorState.getLastChangeType()
    );
    newEditorState = EditorState.acceptSelection(newEditorState, selection);
    return newEditorState;
  },
});
