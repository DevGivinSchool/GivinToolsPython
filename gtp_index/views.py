from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from gtp_index.models import Article, Participant
from django.views.generic import ListView, DetailView
from .forms import ParticipantCreateForm, ParticipantEditForm
from django.urls import reverse


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


# class HomeListView(ListView):
#     model = Article
#     template_name = 'sf_list.html'
#     context_object_name = 'list_articles'

# Список ДШ
# class ParticipantListView(ListView):
#     model = Participant
#     template_name = 'sf_list.html'
#     context_object_name = 'participant_list'


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


# class HomeDetailView(DetailView):
#     model = Article
#     template_name = 'sf_detail.html'
#     context_object_name = 'get_article'


# def my_view(request):
#     # t = loader.get_template('gtp_index/sf_list.html')
#     # context = {'foo': 'bar'}
#     # return HttpResponse(t.render(context, request))
#     return render(request, 'sf_list.html', context={'foo': 'bar'})

# Список ДШ
def sf_list(request):
    success_create = False
    if request.method == 'POST':
        form = ParticipantCreateForm(request.POST)
        if form.is_valid():
            # TODO Здесь нужно вызывать процедуру создания участника
            #  from_list_create_sf_participants(list_, database, logger)
            form.save()
            success_create = True
    template = "sf_list.html"
    context = {
        'sf_list': Participant.objects.all().order_by('last_name'),
        'form': ParticipantCreateForm(),
        'success_create': success_create
    }
    return render(request, template, context)


# Редактирование участника
def sf_participant_edit(request, pk):
    get_participant = Participant.objects.get(pk=pk)
    success_edit = False
    if request.method == 'POST':
        form = ParticipantCreateForm(request.POST, instance=get_participant)
        if form.is_valid():
            # TODO Здесь нужно вызывать процедуру ОБНОВЛЕНИЯ участника
            #  from_list_create_sf_participants(list_, database, logger)
            form.save()
            success_edit = True
    template = "sf_edit.html"

    context = {
        'get_participant': get_participant,
        'edit': True,
        'form': ParticipantEditForm(instance=get_participant),
        'success_edit': success_edit
    }
    return render(request, template, context)


# Удаление участника
def sf_participant_delete(request, pk):
    get_participant = Participant.objects.get(pk=pk)
    get_participant.delete()
    return redirect(reverse('sf_edit'))


# Список основной команды
def team_list(request):
    success_create = False
    if request.method == 'POST':
        form = ParticipantCreateForm(request.POST)
        if form.is_valid():
            # TODO Здесь нужно вызывать процедуру создания участника
            #  from_list_create_sf_participants(list_, database, logger)
            form.save()
            success_create = True
    template = "team_list.html"
    context = {
        'team_list': Participant.objects.all().order_by('last_name'),
        'form': ParticipantCreateForm(),
        'success_create': success_create
    }
    return render(request, template, context)