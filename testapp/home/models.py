from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    body = RichTextField(
        features=["anchor-identifier", "h2", "h3", "bold", "italic", "link"],
        blank=True,
        null=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]