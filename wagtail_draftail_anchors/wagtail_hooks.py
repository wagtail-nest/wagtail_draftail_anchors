from django.utils.html import format_html_join
from django.conf import settings

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler, BlockElementHandler
from wagtail.core import hooks

from .rich_text import AnchorIndentifierEntityElementHandler, anchor_identifier_entity_decorator, FragmentBlockConverter, FragmentBlockHandler


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
            js=['wagtaildraftailanchors/js/wagtail-draftail-anchor.js'],
            css={'all': ['wagtaildraftailanchors/css/wagtail-draftail-anchor.css']}
            )
    )

    features.register_converter_rule('contentstate', feature_name, {
        # Note here that the conversion is more complicated than for blocks and inline styles.
        # 'from_database_format': {'a[data-anchor][id]': AnchorIndentifierEntityElementHandler(type_)},
        'from_database_format': {'a[data-id]': AnchorIndentifierEntityElementHandler(type_)},
        'to_database_format': {'entity_decorators': {type_: anchor_identifier_entity_decorator}},
    })

    features.register_converter_rule('contentstate', 'h1', {
        'from_database_format': {'h1': FragmentBlockHandler('header-one')},
        'to_database_format': {'block_map': {'header-one': FragmentBlockConverter('h1')}},
    })

    features.register_converter_rule('contentstate', 'h2', {
        'from_database_format': {'h2': FragmentBlockHandler('header-two')},
        'to_database_format': {'block_map': {'header-two': FragmentBlockConverter('h2')}},
    })

    features.register_converter_rule('contentstate', 'h3', {
        'from_database_format': {'h3': FragmentBlockHandler('header-three')},
        'to_database_format': {'block_map': {'header-three': FragmentBlockConverter('h3')}},
    })

    features.register_converter_rule('contentstate', 'h4', {
        'from_database_format': {'h4': FragmentBlockHandler('header-four')},
        'to_database_format': {'block_map': {'header-four': FragmentBlockConverter('h4')}},
    })

    features.register_converter_rule('contentstate', 'h5', {
        'from_database_format': {'h5': FragmentBlockHandler('header-five')},
        'to_database_format': {'block_map': {'header-five': FragmentBlockConverter('h5')}},
    })

    features.register_converter_rule('contentstate', 'h6', {
        'from_database_format': {'h6': FragmentBlockHandler('header-six')},
        'to_database_format': {'block_map': {'header-six': FragmentBlockConverter('h6')}},
    })
