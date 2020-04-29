from django.utils.html import format_html_join
from django.conf import settings

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.core import hooks

from .rich_text import AnchorIndentifierEntityElementHandler, anchor_identifier_entity_decorator


@hooks.register('register_rich_text_features')
def register_rich_text_anchor_identifier_feature(features):
    features.default_features.append('anchor-identifier')
    """
    Registering the `anchor-identifier` feature, which uses the `ANCHOR-IDENTIFIER` Draft.js entity type,
    and is stored as HTML with a `<a data-anchor href="#my-anchor" id="my-anchor">` tag.
    """
    feature_name = 'anchor-identifier'
    type_ = 'ANCHOR-IDENTIFIER'

    control = {
        'type': type_,
        'label': '',
        'icon': 'icon icon-anchor',
        'description': 'Anchor Identifier',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.EntityFeature(
            control,
            js=['js/wagtail-draftail-anchor.js'],
            css={'all': ['css/wagtail-draftail-anchor.css']}
            )
    )

    features.register_converter_rule('contentstate', feature_name, {
        # Note here that the conversion is more complicated than for blocks and inline styles.
        # 'from_database_format': {'a[data-anchor][id]': AnchorIndentifierEntityElementHandler(type_)},
        'from_database_format': {'a[data-id]': AnchorIndentifierEntityElementHandler(type_)},
        'to_database_format': {'entity_decorators': {type_: anchor_identifier_entity_decorator}},
    })