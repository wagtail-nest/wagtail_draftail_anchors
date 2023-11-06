from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page


class HomePage(Page):
    body = RichTextField(blank=True)
    stream = StreamField(
        [
            ("richtext", blocks.RichTextBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
        FieldPanel("stream"),
    ]
