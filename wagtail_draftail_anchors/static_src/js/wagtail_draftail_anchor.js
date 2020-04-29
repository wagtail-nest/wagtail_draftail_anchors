const React = window.React;
const RichUtils = window.DraftJS.RichUtils;
const TooltipEntity = window.draftail.TooltipEntity;
const Icon = window.wagtail.components.Icon;
const EditorState = window.DraftJS.EditorState;


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
    let icon = <Icon name="link" />;
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
