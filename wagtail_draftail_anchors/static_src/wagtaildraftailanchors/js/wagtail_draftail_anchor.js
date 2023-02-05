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
    const { editorState, entityType, onComplete, entity } = this.props;

    const content = editorState.getCurrentContent();

    let anchor_id = "";
    if (entity) {
      anchor_id = entity.data.anchor;
    }
    const anchor = window.prompt("Anchor identifier:", anchor_id);

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

class HeaderAnchorDecorator extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      showTooltipAt: null,
    };

    this.onEdit = this.onEdit.bind(this);
    this.onRemove = this.onRemove.bind(this);
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

  getBlock(editorState){
    const block_key = editorState.getSelection().getFocusKey();
    return this.props.contentState.getBlockForKey(block_key);
  }

  getData(editorState) {
    const block = this.getBlock(editorState);
    return block.getData();
  }

  onRemove(e) {
    e.preventDefault();
    e.stopPropagation();
    this.setState({ showTooltipAt: null });
  }

  onEdit(e) {
    e.preventDefault();
    e.stopPropagation();

    const editorState = this.props.getEditorState();
    const data = this.getData(editorState);
    const block = this.getBlock(editorState);
    const anchor = window.prompt('Anchor Link:', data.get("anchor") || data.get("id") || slugify(block.getText().toLowerCase()));

    this.setState({ showTooltipAt: null });

    let newEditorState = editorState;

    let newData = new Map();
    newData.set("anchor", anchor);

    let content = editorState.getCurrentContent();
    const selection = editorState.getSelection();
    content = Modifier.mergeBlockData(content, selection, newData);

    newEditorState = EditorState.push(
      editorState,
      content,
      editorState.getLastChangeType()
    );
    newEditorState = EditorState.acceptSelection(newEditorState, selection);
    this.props.setEditorState(newEditorState);
  }

  render() {
    const children = this.props.children;

    const { showTooltipAt } = this.state;

    const editorState = this.props.getEditorState();
    const data = this.getData(editorState);
    const block = this.getBlock(editorState);
    // try to get custom anchor first, then id and only then build it from the text
    const anchor = data.get("anchor") || data.get("id") || slugify(block.getText().toLowerCase());
    const url = `#${anchor}`;

    // Contrary to what JSX A11Y says, this should be a button but it shouldn't be focusable.
    /* eslint-disable springload/jsx-a11y/interactive-supports-focus */
    return (
      <a
        href=""
        role="button"
        // Use onMouseUp to preserve focus in the text even after clicking.
        onMouseUp={this.openTooltip}
        className="TooltipEntity"
        data-draftail-trigger
      >
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
              <span className="Tooltip__link">
                {url}
              </span>
              <button
                className="button Tooltip__button"
                onClick={this.onEdit}
              >
                Edit
              </button>

              <button
                className="button button-secondary no Tooltip__button"
                onClick={this.onRemove}
              >
                Cancel
              </button>
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
      component: HeaderAnchorDecorator,
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
        const blockSelection = SelectionState.createEmpty(key);
        const data = block.getData()
        // do not change if there is a custom anchor
        if (data.get("anchor")){
          continue;
        }
        let newData = new Map();
        newData.set("id", slugify(block.getText().toLowerCase()));
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
