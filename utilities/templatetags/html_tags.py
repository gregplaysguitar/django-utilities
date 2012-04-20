from BeautifulSoup import BeautifulSoup, Comment
from django import template


register = template.Library()


def sanitise_html(value, valid_tags='p i strong b u a h1 h2 h3 pre br img'):
    valid_tags = valid_tags.split()
    valid_attrs = 'href src'.split()
    soup = BeautifulSoup(value)
    for comment in soup.findAll(
        text=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        tag.attrs = [(attr, val) for attr, val in tag.attrs if attr in valid_attrs]
    return soup.renderContents().decode('utf8').replace('javascript:', '')

register.filter('sanitise', sanitise_html)
