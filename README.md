# Wagtail Draftail Anchors

Adds the ability to add and edit anchors in the Draftail rich text editor, as well as automatically adding
(slug-form) anchor ids to all headings.

## Installation

Install using `pip`:

```
pip install wagtail-draftail-anchors
```

Add `'wagtail_draftail_anchors'` to `INSTALLED_APPS` below `wagtail.admin`.

Add `'anchor-identifier'` to the features of any rich text field where you have overridden the default feature list. The feature must be added before any heading('h1',...,'h6') feature:

```
body = RichTextField(features=['anchor-identifier', 'h2', 'h3', 'bold', 'italic', 'link'])
```