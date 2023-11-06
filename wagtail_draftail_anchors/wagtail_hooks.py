from wagtail import hooks
from wagtail.admin.rich_text.editors.draftail.features import ControlFeature


@hooks.register("register_rich_text_features")
def register_sentences_counter(features):
    feature_name = "sentences"
    features.default_features.append(feature_name)

    features.register_editor_plugin(
        "draftail",
        feature_name,
        ControlFeature({
            "type": feature_name,
        },
        js=["wagtail-draftail-anchor.js"],
        ),
    )
