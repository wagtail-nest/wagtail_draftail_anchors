from django.conf import settings
from django.utils.html import format_html
from django.utils.module_loading import import_string
from draftjs_exporter.dom import DOM

from wagtail import VERSION as wagtail_version
from wagtail.admin.rich_text.converters.contentstate_models import Block
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    BlockElementHandler,
    InlineEntityElementHandler,
)

if wagtail_version >= (3, 0):
    from wagtail.rich_text import LinkHandler
else:
    from wagtail.core.rich_text import LinkHandler


# We can't use "anchor", as Wagtail uses this internally for links whose hrefs
# start with "#"
ANCHOR_TARGET_IDENTIFIER = "anchor-target"


def render_span(attrs):
    return format_html('<span id="{}">', attrs["id"])


def render_a(attrs):
    return format_html('<a href="#{id}" id="{id}" data-id="{id}">', id=attrs["id"])


class AnchorIdentifierLinkHandler(LinkHandler):
    identifier = ANCHOR_TARGET_IDENTIFIER

    @classmethod
    def get_renderer(cls):
        renderer = getattr(cls, "_renderer", None)
        if renderer is None:
            renderer = getattr(settings, "DRAFTAIL_ANCHORS_RENDERER", render_a)
            if isinstance(renderer, str):
                renderer = import_string(renderer)
            cls._renderer = renderer
        return renderer

    @classmethod
    def expand_db_attributes(cls, attrs):
        renderer = cls.get_renderer()
        return renderer(attrs)


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
            # Add a custom linktype so we can handle the DB -> HTML transformation
            "linktype": ANCHOR_TARGET_IDENTIFIER,
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

        elem_data = {
            "id": block_data.get("anchor") or block_data.get("id"),
        }

        if block_data.get("anchor"):
            elem_data["anchor"] = block_data.get("anchor")

        # Here, we want to display the block's content so we pass the `children` prop as the last parameter.
        return DOM.create_element(
            self.tag,
            elem_data,
            props["children"]
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
            data={
                "id": attrs.get("id", ""),
                "anchor": attrs.get("anchor", "")
            },
        )
