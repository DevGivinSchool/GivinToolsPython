from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from gtp_index.models import Article
from django.views.generic import ListView, DetailView


# Create your views here.
# def index(request):
#     list_articles = Article.objects.all()
#     context = {
#         'list_articles': list_articles
#     }
#     template = 'index.html'
#     return render(request, template, context=context)


class HomeListView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'list_articles'


# def detail_page(request, id):
#     get_article = Article.objects.get(id=id)
#     context = {
#         'get_article': get_article
#     }
#     template = 'detail.html'
#     return render(request, template, context=context)

class HomeDetailView(DetailView):
    model = Article
    template_name = 'detail.html'
    context_object_name = 'get_article'


def my_view(request):
    # t = loader.get_template('gtp_index/index.html')
    # context = {'foo': 'bar'}
    # return HttpResponse(t.render(context, request))
    return render(request, 'index.html', context={'foo': 'bar'})
