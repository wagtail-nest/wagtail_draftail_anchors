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

## Configuration

### Rendered representation of anchors

By default, `anchor-identifier` rich text entities will be rendered as HTML `anchor` elements, e.g.:

``` html
<a href="#my-element" id="my-element" data-id="my-element">My element</a>
```

This package provides an alternative renderer that renders `anchor-identifier` entities as HTML `span` elements, e.g.:

``` html
<span id="my-element">My element</span>
```

The desired renderer can be specified using the `DRAFTAIL_ANCHORS_RENDERER` setting. To use the `span` renderer, configure your application as follows:

``` python
DRAFTAIL_ANCHORS_RENDERER = "wagtail_draftail_anchors.rich_text.render_span"
```

It is possible to define your own renderer. It should be a callable that takes a `dict` of attributes, and returns a string containing the opening tag of the HTML element that represents the anchor target. The `dict` passed to the renderer, for an anchor with an identifier of `"my-anchor"`, would look like the following:

``` python
{"data-id": "my-anchor", "href": "#my-anchor", "id": "my-anchor", "linktype": "my-anchor"}
```

If you define your own renderer, you should set the value of `DRAFTAIL_ANCHORS_RENDERER` to your custom renderer's import path.

See `render_span` and `render_a` in `wagtail_draftail_anchors.rich_text` for examples.
