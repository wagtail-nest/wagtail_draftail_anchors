from draftjs_exporter.dom import DOM

from wagtail.admin.rich_text.converters.contentstate_models import Block
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    BlockElementHandler,
    InlineEntityElementHandler,
)


def anchor_identifier_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.
    Converts the ANCHOR entities into <a> tags.
    """
    return DOM.create_element(
        "a",
        {
            "data-id": props["anchor"].lstrip("#"),
            "id": props["anchor"].lstrip("#"),
            "href": "#{}".format(props["anchor"].lstrip("#")),
        },
        props["children"],
    )


class AnchorIndentifierEntityElementHandler(InlineEntityElementHandler):
    """
    Database HTML to Draft.js ContentState.
    Converts the <a> tags into ANCHOR IDENTIFIER entities, with the right data.
    """

    # In Draft.js entity terms, anchors identifier are "mutable".
    mutability = "MUTABLE"

    def get_attribute_data(self, attrs):
        """
        Take the ``anchor`` value from the ``href`` HTML attribute.
        """
        return {
            "anchor": attrs["href"].lstrip("#"),
            "data-id": attrs["id"],
        }


class AnchorBlockConverter:
    """
    Draft.js ContentState to database HTML.
    Converts the anchors in block data to html ids.
    """

    def __init__(self, tag):
        self.tag = tag

    def __call__(self, props):
        block_data = props["block"]["data"]

        # Here, we want to display the block's content so we pass the `children` prop as the last parameter.
        return DOM.create_element(
            self.tag, {"id": block_data.get("anchor")}, props["children"]
        )


class DataBlock(Block):
    """
    ContentState block representation with block data
    """

    def __init__(self, *args, **kwargs):
        self.data = kwargs.pop("data")
        super().__init__(*args, **kwargs)

    def as_dict(self):
        return dict(data=self.data, **super().as_dict())


class AnchorBlockHandler(BlockElementHandler):
    """HTML to Draft.js ContentState for anchor blocks with a anchor"""

    def create_block(self, name, attrs, state, contentstate):
        return DataBlock(
            self.block_type,
            depth=state.list_depth,
            data={"anchor": attrs.get("id", "")},
        )
