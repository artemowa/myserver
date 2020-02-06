from . import views

URLS = {
    '/': views.index(),
    '/blog': views.blog(),
}
