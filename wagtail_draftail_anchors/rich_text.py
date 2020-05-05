from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.contentstate_models import Block 
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler, BlockElementHandler


def anchor_identifier_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.
    Converts the ANCHOR entities into <a> tags.
    """
    return DOM.create_element('a', {
        'data-id':props['fragment'].lstrip('#'),
        'id':props['fragment'].lstrip('#'),
        'href': '#{}'.format(props['fragment'].lstrip('#')),
    }, props['children'])


class AnchorIndentifierEntityElementHandler(InlineEntityElementHandler):
    """
    Database HTML to Draft.js ContentState.
    Converts the <a> tags into ANCHOR IDENTIFIER entities, with the right data.
    """
    # In Draft.js entity terms, anchors identifier are "mutable".
    mutability = 'MUTABLE'

    def get_attribute_data(self, attrs):
        """
        Take the ``fragment`` value from the ``href`` HTML attribute.
        """
        return {
            'fragment': attrs['href'].lstrip('#'),
            'data-id': attrs['id'],
        }


class FragmentBlockConverter:
    """
    Draft.js ContentState to database HTML.
    Converts the fragments in block data to html ids.
    """
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, props):
        block_data = props['block']['data']

        # Here, we want to display the block's content so we pass the `children` prop as the last parameter.
        return DOM.create_element(self.tag, {
            'id': block_data.get('fragment')
            }, props['children'])


class DataBlock(Block):
    """
    ContentState block representation with block data
    """
    def __init__(self, *args, **kwargs):
        self.data = kwargs.pop('data')
        super().__init__(*args, **kwargs)

    def as_dict(self):
        return dict(data=self.data, **super().as_dict())


class FragmentBlockHandler(BlockElementHandler):
    """HTML to Draft.js ContentState for anchor blocks with a fragment"""
    def create_block(self, name, attrs, state, contentstate):
        return DataBlock(self.block_type, depth=state.list_depth, data={'fragment': attrs.pop('id')})