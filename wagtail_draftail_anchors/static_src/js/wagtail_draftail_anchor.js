const React = window.React;
const RichUtils = window.DraftJS.RichUtils;
const TooltipEntity = window.draftail.TooltipEntity;
const Icon = window.wagtail.components.Icon;
const EditorState = window.DraftJS.EditorState;
const Portal = window.wagtail.components.Portal;
const Tooltip = window.draftail.Tooltip;
const slugify = require('slugify')

// Implement the new APIs.

const DECORATORS = [];
const CONTROLS = [];

const registerDecorator = (decorator) => {
    DECORATORS.push(decorator);
    return DECORATORS;
};

const registerControl = (control) => {
    CONTROLS.push(control);
    return CONTROLS;
};

// Override the existing initEditor to hook the new APIs into it.
// This works in Wagtail 2.0 but will definitely break in a future release.
const initEditor = window.draftail.initEditor;

const initEditorOverride = (selector, options, currentScript) => {
    const overrides = {
        decorators: DECORATORS,
        controls: CONTROLS,
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

        const fragment = window.prompt('Fragment identifier:');

        // Uses the Draft.js API to create a new entity with the right data.
        if (fragment) {
            const contentWithEntity = content.createEntity(
                entityType.type,
                'MUTABLE',
                {
                    fragment: fragment,
                },
            );
            const entityKey = contentWithEntity.getLastCreatedEntityKey();
            const selection = editorState.getSelection();
            const nextState = RichUtils.toggleLink(
                editorState,
                selection,
                entityKey,
            );
    
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
    const url = data.fragment || null;
    let icon = <Icon name="anchor" />;
    let label = `#${url}`;
  
    return {
      url,
      icon,
      label,
    };
  };

const AnchorIdentifier = props => {
    const { entityKey, contentState } = props;
    const data = contentState.getEntity(entityKey).getData();

    return (
        <TooltipEntity
          {...props}
          {...getAnchorIdentifierAttributes(data)}
        />
    );
};


window.draftail.registerPlugin({
    type: 'ANCHOR-IDENTIFIER',
    source: AnchorIdentifierSource,
    decorator: AnchorIdentifier,
});

class BasicTooltipDecorator extends React.Component {
    constructor(props) {
      super(props);
  
      this.state = {
        showTooltipAt: null,
      };
  
      this.openTooltip = this.openTooltip.bind(this);
      this.closeTooltip = this.closeTooltip.bind(this);
    }
  
    openTooltip(e) {
      const trigger = e.target.closest('[data-draftail-trigger]');
  
      // Click is within the tooltip.
      if (!trigger) {
        return;
      }
  
      const container = trigger.closest('[data-draftail-editor-wrapper]');
      const containerRect = container.getBoundingClientRect();
      const rect = trigger.getBoundingClientRect();
  
      this.setState({
        showTooltipAt: {
          container: container,
          top: rect.top - containerRect.top - (document.documentElement.scrollTop || document.body.scrollTop),
          left: rect.left - containerRect.left - (document.documentElement.scrollLeft || document.body.scrollLeft),
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
      const fragment = `#${slugify(this.props.decoratedText)}`;
      const icon = "icon-anchor";
      const { showTooltipAt } = this.state;
  
      // Contrary to what JSX A11Y says, this should be a button but it shouldn't be focusable.
      /* eslint-disable springload/jsx-a11y/interactive-supports-focus */
      return (
        <a
          href=''
          name={fragment}
          role="button"
          // Use onMouseUp to preserve focus in the text even after clicking.
          onMouseUp={this.openTooltip}
          className="TooltipEntity"
          data-draftail-trigger
        >
          <Icon icon={icon} className="TooltipEntity__icon" />
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
                {fragment}
              </Tooltip>
            </Portal>
          )}
        </a>
      );
    }
  };

// Note: these aren't very good regexes, don't use them!
const HANDLE_REGEX = /\@[\w]+/g;
const HASHTAG_REGEX = /\#[\w\u0590-\u05ff]+/g;
function handleStrategy(contentBlock, callback, contentState) {
  findWithRegex(HANDLE_REGEX, contentBlock, callback);
}
function hashtagStrategy(contentBlock, callback, contentState) {
  findWithRegex(HASHTAG_REGEX, contentBlock, callback);
}
function findWithRegex(regex, contentBlock, callback) {
  const text = contentBlock.getText();
  let matchArr, start;
  while ((matchArr = regex.exec(text)) !== null) {
    start = matchArr.index;
    callback(start, start + matchArr[0].length);
  }
}

const HashtagSpan = props => {
    return (
      <span style={{ color: "#007d7e" }}>
        {props.children}
      </span>
    );
  };

function headingStrategy(contentBlock, callback, contentState) {
    if (contentBlock.getType() == 'header-two') {
        callback(0, contentBlock.getLength());
    };
  }

const HeadingTest = props => {
    return (
      <span style={{ color: "#007d7e" }}>
        {props.children}
      </span>
    );
  };

registerDecorator({
    strategy: hashtagStrategy,
    component: HashtagSpan,
  });

registerDecorator({
    strategy: headingStrategy,
    component: BasicTooltipDecorator,
  });