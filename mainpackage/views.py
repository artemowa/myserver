from http.base import HttpTemplateResponse


def index():
    return HttpTemplateResponse('templates/index.html')


def blog():
    return HttpTemplateResponse('templates/blog.html')
