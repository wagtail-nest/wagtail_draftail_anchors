from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class WagtailDraftailAnchorsAppConfig(AppConfig):
    name = "wagtail_draftail_anchors"
    label = "wagtaildraftailanchors"
    verbose_name = _("Wagtail Draftail Anchors")
