from django.shortcuts import render, redirect
from sf.models import Participant
from gtp.models import TeamMember
from django.views.generic import DetailView, CreateView
from .forms import ParticipantCreateForm, ParticipantEditForm, TeamMemberCreateForm, TeamMemberEditForm
from django.urls import reverse, reverse_lazy


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

# Переделка функции на класс, но пока оставляю функцию
# class ParticipantCreateView(CreateView):
#     model = Participant
#     template_name = 'sf_list.html'
#     form_class = ParticipantCreateForm
#     success_url = reverse_lazy('sf_list')
#
#     def get_context_data(self, **kwargs):
#         kwargs['sf_list'] = Participant.objects.all().order_by('last_name')
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         # form.send_email()
#         print("test test")
#         return super(ParticipantCreateView, self).form_valid(form)

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
    participant = Participant.objects.get(pk=pk)
    success_edit = False
    if request.method == 'POST':
        form = ParticipantCreateForm(request.POST, instance=participant)
        if form.is_valid():
            # TODO Здесь нужно вызывать процедуру ОБНОВЛЕНИЯ участника
            #  from_list_create_sf_participants(list_, database, logger)
            form.save()
            success_edit = True
    template = "sf_list.html"

    context = {
        'participant': participant,
        'edit': True,
        'form': ParticipantEditForm(instance=participant),
        'success_edit': success_edit
    }
    return render(request, template, context)


# Удаление участника
def sf_participant_delete(request, pk):
    participant = Participant.objects.get(pk=pk)
    participant.delete()
    return redirect(reverse('sf_list'))


# Список основной команды
def team_list(request):
    success_create = False
    if request.method == 'POST':
        form = TeamMemberCreateForm(request.POST)
        if form.is_valid():
            # TODO Здесь нужно вызывать процедуру создания участника
            #  from_list_create_sf_participants(list_, database, logger)
            form.save()
            success_create = True
    template = "team_list.html"
    context = {
        'team_list': TeamMember.objects.all().order_by('last_name'),
        'form': TeamMemberCreateForm(),
        'success_create': success_create
    }
    return render(request, template, context)


# Редактирование участника команды
def team_member_edit(request, pk):
    team_member = TeamMember.objects.get(pk=pk)
    success_edit = False
    if request.method == 'POST':
        form = TeamMemberCreateForm(request.POST, instance=team_member)
        if form.is_valid():
            # TODO Здесь нужно вызывать процедуру ОБНОВЛЕНИЯ участника
            #  from_list_create_sf_participants(list_, database, logger)
            form.save()
            success_edit = True
    template = "team_list.html"

    context = {
        'team_member': team_member,
        'edit': True,
        'form': TeamMemberEditForm(instance=team_member),
        'success_edit': success_edit
    }
    return render(request, template, context)


# Удаление участника команды
def team_member_delete(request, pk):
    team_member = TeamMember.objects.get(pk=pk)
    team_member.delete()
    return redirect(reverse('team_list'))
