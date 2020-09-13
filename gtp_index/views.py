from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from gtp_index.models import Article, Participant
from django.views.generic import ListView, DetailView


# Create your views here.
# def index(request):
#     list_articles = Article.objects.all()
#     context = {
#         'list_articles': list_articles
#     }
#     template = 'sf_list.html'
#     return render(request, template, context=context)

def index(request):
    template = "index.html"
    context = {}
    return render(request, template, context)


class HomeListView(ListView):
    model = Article
    template_name = 'sf_list.html'
    context_object_name = 'list_articles'


class ParticipantListView(ListView):
    model = Participant
    template_name = 'sf_list.html'
    context_object_name = 'participant_list'


class ParticipantDetailView(DetailView):
    model = Participant
    template_name = 'sf_detail.html'
    context_object_name = 'the_participant'


# def detail_page(request, id):
#     get_article = Article.objects.get(id=id)
#     context = {
#         'get_article': get_article
#     }
#     template = 'sf_detail.html'
#     return render(request, template, context=context)


class HomeDetailView(DetailView):
    model = Article
    template_name = 'sf_detail.html'
    context_object_name = 'get_article'


def my_view(request):
    # t = loader.get_template('gtp_index/sf_list.html')
    # context = {'foo': 'bar'}
    # return HttpResponse(t.render(context, request))
    return render(request, 'sf_list.html', context={'foo': 'bar'})


def sf_edit(request):
    template = "sf_edit.html"
    context = {
        'sf_list': Participant.objects.all().order_by('last_name')
    }
    return render(request, template, context)
