from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from gtp_index.models import Article


# Create your views here.
def index(request):
    list_articles = Article.objects.all()
    context = {
        'list_articles': list_articles
    }
    template = 'index.html'
    return render(request, template, context=context)


def detail_page(request, id):
    get_article = Article.objects.get(id=id)
    context = {
        'get_article': get_article
    }
    template = 'detail.html'
    return render(request, template, context=context)


def my_view(request):
    # t = loader.get_template('gtp_index/index.html')
    # context = {'foo': 'bar'}
    # return HttpResponse(t.render(context, request))
    return render(request, 'index.html', context={'foo': 'bar'})
