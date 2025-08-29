from wagtail import VERSION as wagtail_version
import wagtail.admin.rich_text.editors.draftail.features as draftail_features

if wagtail_version >= (3, 0):
    from wagtail import hooks
else:
    from wagtail.core import hooks

from .rich_text import (
    AnchorBlockConverter,
    AnchorBlockHandler,
    AnchorIndentifierEntityElementHandler,
    AnchorIdentifierLinkHandler,
    anchor_identifier_entity_decorator,
)


class AnchorFeature(draftail_features.EntityFeature):
    """Registers anchors both as entities and plugins."""

    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self.js = ["wagtaildraftailanchors/js/wagtail-draftail-anchor.js"]

    def construct_options(self, options):
        if "plugins" not in options:
            options["plugins"] = []

        options["plugins"].append(self.data)

        return super().construct_options(options)


@hooks.register('register_icons')
def register_icons(icons):
    icons.append('wagtaildraftailanchors/icons/anchor.svg')
    return icons


@hooks.register("register_rich_text_features")
def register_rich_text_anchor_identifier_feature(features):
    features.default_features.insert(0, "anchor-identifier")
    """
    Registering the `anchor-identifier` feature, which uses the `ANCHOR-IDENTIFIER` Draft.js entity type,
    and is stored as HTML with a `<a data-anchor href="#my-anchor" id="my-anchor">` tag.
    """
    feature_name = "anchor-identifier"
    type_ = "ANCHOR-IDENTIFIER"

    control = {
        "type": type_,
        "label": "",
        "icon": "anchor",
        "description": "Anchor Identifier",
    }

    features.register_editor_plugin(
        "draftail",
        feature_name,
        AnchorFeature(control),
    )

    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            # Note here that the conversion is more complicated than for blocks and inline styles.
            # 'from_database_format': {'a[data-anchor][id]': AnchorIndentifierEntityElementHandler(type_)},
            "from_database_format": {
                "a[data-id]": AnchorIndentifierEntityElementHandler(type_)
            },
            "to_database_format": {
                "entity_decorators": {type_: anchor_identifier_entity_decorator}
            },
        },
    )

    features.register_converter_rule(
        "contentstate",
        "h1",
        {
            "from_database_format": {"h1": AnchorBlockHandler("header-one")},
            "to_database_format": {
                "block_map": {"header-one": AnchorBlockConverter("h1")}
            },
        },
    )

    features.register_converter_rule(
        "contentstate",
        "h2",
        {
            "from_database_format": {"h2": AnchorBlockHandler("header-two")},
            "to_database_format": {
                "block_map": {"header-two": AnchorBlockConverter("h2")}
            },
        },
    )

    features.register_converter_rule(
        "contentstate",
        "h3",
        {
            "from_database_format": {"h3": AnchorBlockHandler("header-three")},
            "to_database_format": {
                "block_map": {"header-three": AnchorBlockConverter("h3")}
            },
        },
    )

    features.register_converter_rule(
        "contentstate",
        "h4",
        {
            "from_database_format": {"h4": AnchorBlockHandler("header-four")},
            "to_database_format": {
                "block_map": {"header-four": AnchorBlockConverter("h4")}
            },
        },
    )

    features.register_converter_rule(
        "contentstate",
        "h5",
        {
            "from_database_format": {"h5": AnchorBlockHandler("header-five")},
            "to_database_format": {
                "block_map": {"header-five": AnchorBlockConverter("h5")}
            },
        },
    )

    features.register_converter_rule(
        "contentstate",
        "h6",
        {
            "from_database_format": {"h6": AnchorBlockHandler("header-six")},
            "to_database_format": {
                "block_map": {"header-six": AnchorBlockConverter("h6")}
            },
        },
    )

    features.register_link_type(AnchorIdentifierLinkHandler)
