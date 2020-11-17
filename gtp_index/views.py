# import pdb  # pdb.set_trace()
from django.shortcuts import render, redirect
from sf.models import Participant
from gtp.models import TeamMember
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .forms import ParticipantCreateForm, ParticipantEditForm, TeamMemberCreateForm, TeamMemberEditForm, AuthForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.models import Group


def is_superuser(request):
    """ Проверяет является ли пользователь superuser. """
    if request.user.is_superuser:
        return True
    else:
        return False


def get_group(request):
    """ Проверяет является ли пользователь superuser, тогда ему всё разрешено, или в каких группах состоит пользователь.
    :param request:
    :return: Либо 'superuser' либо список групп. """
    if is_superuser(request):
        return 'superuser'
    else:
        query_set = Group.objects.filter(user=request.user)
        list_group = ''
        for group in query_set:
            list_group += group.name
        return list_group


def user_belongs_to_group(request, group_name):
    """ Проверяет входит ли пользователь в группу. """
    # query_set = Group.objects.filter(user=request.user)
    if request.user.groups.filter(name=group_name).exists():
        return True
    else:
        return False


def not_authorized(request):
    """ Страница для неавторизованных пользователей, которые не включены ни в какую группу,
    поэтому не имеют гикаких прав и должны обратиться к администратору.
    :param request:
    :return: """
    template = 'not_authorized.html'
    context = {
        'user_name': 'None',
        'group_name': 'None'
    }
    return render(request, template, context=context)


class GSLoginView(LoginView):
    """ Страница Login. """
    template_name = 'gs_login.html'
    form_class = AuthForm
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url


class GSLogoutView(LogoutView):
    """ Logout - перенаправление на главную страницу. """
    next_page = reverse_lazy('index')


def index(request):
    """ Главная страница. Здесь проверяется авторизация пользователя и в зависимости от его группы,
    происходит перенаправление на необходимую страницу.
    :param request:
    :return: """
    # Если пользователь не аутентифицирован, то перенаправлять на страницу входа
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('gs_login'))
    # суперпользователь, то ему можно всё и показывать всё
    if request.user.is_superuser:
        template = 'index.html'
        context = {
            'user_name': request.user,
            'group_name': 'superuser'
        }
        return render(request, template, context)
    # sf_admin_group (Администраторы Друзей Школы)
    elif request.user.groups.filter(name='sf_admin_group').exists():
        return HttpResponseRedirect(reverse('sf_list'))
    # sf_user_group (участники Друзей Школы)
    elif request.user.groups.filter(name='sf_user_group').exists():
        print(f"request.user={request.user}")
        if request.user.username.endswith('@givinschool.org'):
            try:
                user_ = Participant.objects.get(login=request.user)
            except Participant.DoesNotExist:
                raise Http404("Такой участник не существует")
            print(f"user_name={user_}")
            return HttpResponseRedirect(reverse('sf_user_page', args=[user_.id]))
        else:
            messages.success(request,
                             "Пользователь должен быть из домена @givinschool.org. Обратитесь к Администратору.")
            return HttpResponseRedirect(reverse('gs_login'))
    # gs_admin_group (Администраторы Основной комманды)
    elif request.user.groups.filter(name='gs_admin_group').exists():
        return HttpResponseRedirect(reverse('team_list'))
    # gs_user_group (участники Основной комманды)
    elif request.user.groups.filter(name='gs_user_group').exists():
        print(f"request.user={request.user}")
        if request.user.username.endswith('@givinschool.org'):
            try:
                user_ = TeamMember.objects.get(login=request.user)
            except TeamMember.DoesNotExist:
                raise Http404("Такой участник не существует")
            print(f"user_name={user_}")
            return HttpResponseRedirect(reverse('team_user_page', args=[user_.id]))
        else:
            messages.success(request,
                             "Пользователь должен быть из домена @givinschool.org. Обратитесь к Администратору.")
            return HttpResponseRedirect(reverse('gs_login'))
    # иначе все остальные (пользователи без группы не имеют прав и должны обратиться к администратору)
    else:
        return HttpResponseRedirect(reverse('not_authorized'))


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


class ParticipantCreateView(SuccessMessageMixin, CreateView):
    """ Страница показывает список ДШ и обеспечивает создание новых членов ДШ. """
    model = Participant
    template_name = 'sf_list.html'
    form_class = ParticipantCreateForm
    success_url = reverse_lazy('sf_list')
    success_message = "Участник создан"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or user_belongs_to_group(request, "sf_admin_group"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        kwargs['sf_list'] = Participant.objects.all().order_by('last_name')
        kwargs['user_name'] = self.request.user
        kwargs['group_name'] = get_group(self.request)
        return super().get_context_data(**kwargs)

    def form_valid(self, form_class):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form_class.send_email()
        # print("test test")
        # TODO Здесь нужно вызывать процедуру создания участника
        #      from_list_create_sf_participants(list_, database, logger)
        return super(ParticipantCreateView, self).form_valid(form_class)


class ParticipantEditView(SuccessMessageMixin, UpdateView):
    """ Страница редактирования участника ДШ. """
    model = Participant
    template_name = 'sf_list.html'
    form_class = ParticipantEditForm
    success_url = reverse_lazy('sf_list')
    success_message = "Участник изменён"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or user_belongs_to_group(request, "sf_admin_group"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

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


class ParticipantDetailView(DetailView):
    """ Страница детальной информации об участнике ДШ. """
    model = Participant
    template_name = 'sf_user.html'
    context_object_name = 'the_participant'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or user_belongs_to_group(request, "sf_user_group") or user_belongs_to_group(
                request, "sf_admin_group"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        kwargs['user_name'] = self.request.user
        kwargs['group_name'] = get_group(self.request)
        return super().get_context_data(**kwargs)


class ParticipantDeleteView(DeleteView):
    """ Страница удаления участника ДШ.
    (Класс DeleteView в отличие от функции sf_participant_delete работает методом POST!!!) """
    model = Participant
    template_name = 'sf_list.html'
    success_url = reverse_lazy('sf_list')
    success_message = "Участник удалён"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or user_belongs_to_group(request, "sf_admin_group"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().post(request)


class TeamMemberCreateView(SuccessMessageMixin, CreateView):
    """ Страница показывает список команды и обеспечивает создание новых членов команды. """
    model = TeamMember
    template_name = 'team_list.html'
    form_class = TeamMemberCreateForm
    success_url = reverse_lazy('team_list')
    success_message = "Участник создан"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or user_belongs_to_group(request, "gs_admin_group"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        kwargs['team_list'] = TeamMember.objects.all().order_by('last_name')
        kwargs['user_name'] = self.request.user
        kwargs['group_name'] = get_group(self.request)
        return super().get_context_data(**kwargs)

    def form_valid(self, form_class):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form_class.send_email()
        # print("test test")
        # TODO Здесь нужно вызывать процедуру создания участника
        #      from_list_create_sf_participants(list_, database, logger)
        return super(TeamMemberCreateView, self).form_valid(form_class)


class TeamMemberEditView(SuccessMessageMixin, UpdateView):
    """ Страница редактирования участника команды. """
    model = TeamMember
    template_name = 'team_list.html'
    form_class = TeamMemberEditForm
    success_url = reverse_lazy('team_list')
    success_message = "Участник изменён"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or user_belongs_to_group(request, "gs_admin_group"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

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


class TeamMemberDetailView(DetailView):
    """ Страница детальной информации о члене команды. """
    model = TeamMember
    template_name = 'team_user.html'
    context_object_name = 'the_member'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or user_belongs_to_group(request, "gs_user_group") or user_belongs_to_group(
                request, "gs_admin_group"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        kwargs['user_name'] = self.request.user
        kwargs['group_name'] = get_group(self.request)
        return super().get_context_data(**kwargs)


class TeamMemberDeleteView(DeleteView):
    """ Страница удаления участника команды.
    (Класс DeleteView в отличие от функции sf_participant_delete работает методом POST!!!) """
    model = TeamMember
    template_name = 'team_list.html'
    success_url = reverse_lazy('team_list')
    success_message = "Участник удалён"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or user_belongs_to_group(request, "gs_admin_group"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().post(request)
