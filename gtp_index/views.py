# import pdb  # pdb.set_trace()
from django.shortcuts import render, redirect
from sf.models import Participant
from gtp.models import TeamMember
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .forms import ParticipantCreateForm, ParticipantEditForm, TeamMemberCreateForm, TeamMemberEditForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages


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

class SuccessMessageMixin:
    """Выводит сообщения об успешных действиях."""

    @property
    def success_message(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


# Список ДШ создание участника ДШ
class ParticipantCreateView(SuccessMessageMixin, CreateView):
    model = Participant
    template_name = 'sf_list.html'
    form_class = ParticipantCreateForm
    success_url = reverse_lazy('sf_list')
    success_message = "Участник создан"

    def get_context_data(self, **kwargs):
        kwargs['sf_list'] = Participant.objects.all().order_by('last_name')
        return super().get_context_data(**kwargs)

    def form_valid(self, form_class):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form_class.send_email()
        # print("test test")
        # TODO Здесь нужно вызывать процедуру создания участника
        #      from_list_create_sf_participants(list_, database, logger)
        return super(ParticipantCreateView, self).form_valid(form_class)


# Список ДШ
# def sf_list(request):
#     success_create = False
#     if request.method == 'POST':
#         form = ParticipantCreateForm(request.POST)
#         if form.is_valid():
#             # TODO Здесь нужно вызывать процедуру создания участника
#             #  from_list_create_sf_participants(list_, database, logger)
#             form.save()
#             success_create = True
#     template = "sf_list.html"
#     context = {
#         'sf_list': Participant.objects.all().order_by('last_name'),
#         'form': ParticipantCreateForm(),
#         'success_create': success_create
#     }
#     return render(request, template, context)

# Редактирование участника
class ParticipantEditView(SuccessMessageMixin, UpdateView):
    model = Participant
    template_name = 'sf_list.html'
    form_class = ParticipantEditForm
    success_url = reverse_lazy('sf_list')
    success_message = "Участник изменён"

    def get_context_data(self, **kwargs):
        kwargs['edit'] = True
        return super().get_context_data(**kwargs)

    def form_valid(self, form_class):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form_class.send_email()
        # print("test test")
        # TODO Здесь нужно вызывать процедуру создания участника
        #      from_list_create_sf_participants(list_, database, logger)
        return super(ParticipantEditView, self).form_valid(form_class)


# Редактирование участника
# def sf_participant_edit(request, pk):
#     participant = Participant.objects.get(pk=pk)
#     success_edit = False
#     if request.method == 'POST':
#         form = ParticipantCreateForm(request.POST, instance=participant)
#         if form.is_valid():
#             # TODO Здесь нужно вызывать процедуру ОБНОВЛЕНИЯ участника
#             #  from_list_create_sf_participants(list_, database, logger)
#             form.save()
#             success_edit = True
#     template = "sf_list.html"
#
#     context = {
#         'participant': participant,
#         'edit': True,
#         'form': ParticipantEditForm(instance=participant),
#         'success_edit': success_edit
#     }
#     return render(request, template, context)

# Удаление участника
# Класс DeleteView в отличие от функции sf_participant_delete работает методом POST!!!
class ParticipantDeleteView(DeleteView):
    model = Participant
    template_name = 'sf_list.html'
    success_url = reverse_lazy('sf_list')
    success_message = "Участник удалён"

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().post(request)


# # Удаление участника
# def sf_participant_delete(request, pk):
#     participant = Participant.objects.get(pk=pk)
#     participant.delete()
#     return redirect(reverse('sf_list'))


# Список основной команды
class TeamMemberCreateView(SuccessMessageMixin, CreateView):
    model = TeamMember
    template_name = 'team_list.html'
    form_class = TeamMemberCreateForm
    success_url = reverse_lazy('team_list')
    success_message = "Участник создан"

    def get_context_data(self, **kwargs):
        kwargs['team_list'] = TeamMember.objects.all().order_by('last_name')
        return super().get_context_data(**kwargs)

    def form_valid(self, form_class):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form_class.send_email()
        # print("test test")
        # TODO Здесь нужно вызывать процедуру создания участника
        #      from_list_create_sf_participants(list_, database, logger)
        return super(TeamMemberCreateView, self).form_valid(form_class)


# Редактирование участника команды
class TeamMemberEditView(SuccessMessageMixin, UpdateView):
    model = TeamMember
    template_name = 'team_list.html'
    form_class = TeamMemberEditForm
    success_url = reverse_lazy('team_list')
    success_message = "Участник изменён"

    def get_context_data(self, **kwargs):
        kwargs['edit'] = True
        return super().get_context_data(**kwargs)

    def form_valid(self, form_class):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form_class.send_email()
        # print("test test")
        # TODO Здесь нужно вызывать процедуру создания участника
        #      from_list_create_sf_participants(list_, database, logger)
        return super(TeamMemberEditView, self).form_valid(form_class)


# Удаление участника команды
class TeamMemberDeleteView(DeleteView):
    model = TeamMember
    template_name = 'team_list.html'
    success_url = reverse_lazy('team_list')
    success_message = "Участник удалён"

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().post(request)


# Список основной команды
# def team_list(request):
#     success_create = False
#     if request.method == 'POST':
#         form = TeamMemberCreateForm(request.POST)
#         if form.is_valid():
#             # TODO Здесь нужно вызывать процедуру создания участника
#             #  from_list_create_sf_participants(list_, database, logger)
#             form.save()
#             success_create = True
#     template = "team_list.html"
#     context = {
#         'team_list': TeamMember.objects.all().order_by('last_name'),
#         'form': TeamMemberCreateForm(),
#         'success_create': success_create
#     }
#     return render(request, template, context)


# # Редактирование участника команды
# def team_member_edit(request, pk):
#     team_member = TeamMember.objects.get(pk=pk)
#     success_edit = False
#     if request.method == 'POST':
#         form = TeamMemberCreateForm(request.POST, instance=team_member)
#         if form.is_valid():
#             # TODO Здесь нужно вызывать процедуру ОБНОВЛЕНИЯ участника
#             #  from_list_create_sf_participants(list_, database, logger)
#             form.save()
#             success_edit = True
#     template = "team_list.html"
#
#     context = {
#         'team_member': team_member,
#         'edit': True,
#         'form': TeamMemberEditForm(instance=team_member),
#         'success_edit': success_edit
#     }
#     return render(request, template, context)


# Удаление участника команды
# def team_member_delete(request, pk):
#     team_member = TeamMember.objects.get(pk=pk)
#     team_member.delete()
#     return redirect(reverse('team_list'))
