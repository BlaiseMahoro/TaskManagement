from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, ListView, TemplateView, View
from django.views.generic.base import RedirectView
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from .models import Profile
from .forms import RegisterForm, ProfilePicForm
# Create your views here.


class Redirect(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'landing'


class Landing(LoginRequiredMixin,View):  # Will later add: LoginRequredMixin
    login_url = 'login'
    template_name = "landing.html"

    def get(self, request):
        project = "Project one"
        project_2 = "Project two"
        context = {
            'some_value': project,
            'some_other_value': project_2,
        }
        return render(request, self.template_name, context)


class Account(LoginRequiredMixin,View):  # Will later add: LoginRequredMixin
    login_url = 'login'
    template_name = "user/account.html"

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        context = {"profile":profile}
        return render(request, self.template_name, context)
    


class Register(View):
    template_name = "registration/register.html"

    def get(self, request):
        form = RegisterForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user) #authenticate user and redirect them to landing page
            return redirect('landing')
        context = {'form': form}
        return render(request, self.template_name, context)

class UploadAvatar(View):
    template_name = 'user/avatar.html'

    def get(self, request):
        form = ProfilePicForm()
        return render(request, self.template_name,{})

    def post(self, request):
        if request.method == 'POST':
            form = ProfilePicForm(request.POST, request.FILES)
            if form.is_valid():
                m = Profile.objects.get(user=request.user)
                m.avatar = form.cleaned_data['image']
                m.save()
                return redirect('account')
        return render(request, self.template_name,{})

class Project(LoginRequiredMixin,View):
    login_url = 'login'
    template_name = "project/management/container.html"

    def get(self, request):
        project = "Project one"
        project_2 = "Project two"
        ticket_project = {'states': [{'state_name':'New','color':'red'}, {'state_name':'To-Do','color':'orange'}, {'state_name':'Doing','color':'yellow'}, {'state_name':'Done','color':'green'}], 'types': [{'type_name': 'Bug'}, {'type_name': 'Feature'}], 'attributes': [{'name': 'Example'}, {'name': 'Example 2'}], 'relationships': [{'title': 'Null Pointer on update'}, {'title': 'Ticket Edit Wireframe'}]}
        context = {
            'some_value': project,
            'some_other_value': project_2,
            'project': ticket_project
        }
        return render(request, self.template_name, context)
    