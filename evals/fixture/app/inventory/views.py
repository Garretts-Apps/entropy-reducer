"""HTML for the storefront page."""
from html import escape


def render_item(item):
    return '<li class="item"><span class="name">' + escape(item["name"]) + "</span> " + price_tag(item) + "</li>"


def render_featured_item(item):
    return '<li class="item featured">' + price_tag(item) + "<strong>" + escape(item["name"]) + "</strong></li>"


def price_tag(item):
    return '<span class="price">$' + format(item["price"], ".2f") + "</span>"


def render_page(items):
    rows = [
        render_featured_item(item) if item["featured"] else render_item(item)
        for item in items
    ]
    return "<ul>" + "".join(rows) + "</ul>"
