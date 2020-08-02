from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.base import RedirectView
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils.translation import ugettext as _
from django.contrib.auth import logout
# from .forms import UserDeleteForm
from .models import Profile, Project, Role
from .forms import RegisterForm, ProfilePicForm, NewProjectForm, UserDeleteForm
from bootstrap_modal_forms.generic import BSModalCreateView
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.


# We need to handle three different cases
# 1. User is logged in with atleast one project
# 2. User is logged in without any projects
# 3. User is not logged in
class Redirect(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'landingNoneSelected'


class Landing(LoginRequiredMixin,View): 
    login_url = 'login'
    landing_template = "landing.html"
    landing_empty_template = "landing_none_selected.html"

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            project = get_object_or_404(Project, pk=kwargs['pk'])
            context = {'project': project, 'template_name': self.landing_template}
            return render(request, self.landing_template, context)
        else:
            return render(request, self.landing_empty_template)


class Account(LoginRequiredMixin,View):
    login_url = 'login'
    template_name = "user/account.html"

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        context = {"profile":profile}
        return render(request, self.template_name, context)

    def post(self, request):
        error_message =""
        try:
            response = request.POST
            user = request.user
            user.first_name = response['fname']
            user.last_name = response['lname']
            user.username = response['username']
            user.email = response['email']
            user.save()
        except:
            error_message = "Username already exists!"

        profile = Profile.objects.get(user=request.user)
        context = {"profile":profile, "error":error_message}

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
            return redirect('landingNoneSelected')
        context = {'form': form}
        return render(request, self.template_name, context)

class UploadAvatar(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request):
        form = ProfilePicForm(request.POST, request.FILES)
        m = Profile.objects.get(user=request.user)
        if form.is_valid():
            m.avatar = form.cleaned_data['image']
            m.save()
            return redirect('account')
        m.avatar = None #Delete profile
        m.save()
        return redirect('account')

class UploadProjectAvatar(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'project/management/container.html'
    
    def post(self, request, *args, **kwargs):
        project_id = kwargs.get('pk')
        #print(project_id)
        form = ProfilePicForm(request.POST, request.FILES)
        project = get_object_or_404(Project, pk=project_id)
        if form.is_valid():
            project.avatar = form.cleaned_data['image']
            project.save()
            return render(request, self.template_name, {'project':project})
        project.avatar = None #Delete profile
        project.save()
        return render(request, self.template_name, {'project':project})

class ProjectSettings(LoginRequiredMixin,View):
    login_url = 'login'
    template_name = "project/management/container.html"

    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_id)
        profile = Profile.objects.get(user=request.user)
        role = Role.objects.get(profile= profile, project= project).role
        # is_admin = role =='is_admin'
        print(role)
        context = {'project': project, 'role':role}
        return render(request, self.template_name, context)
   
    def post(self, request, *args, **kwargs):
        project_id = kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_id)
        response = request.POST
        #For Update Project in Detatil Tab
        if response.get('section') =='edit_project':
            project.name = response['title']
            project.description = response['description']
            project.save()
            return render(request, self.template_name, {'project': project})
        #For Upload Profile Picture
        if response.get('section') == 'upload_pic':
            project_id = kwargs.get('pk')
            print(project_id)
            form = ProfilePicForm(request.POST, request.FILES)
            project = get_object_or_404(Project, pk=project_id)
            if form.is_valid():
                project.avatar = form.cleaned_data['image']
                project.save()
                return render(request, self.template_name, {'project':project})
            project.avatar = None #Delete profile
            project.save()
        if response.get('section') =='delete_project':
            project.delete()   
            return redirect('landingNoneSelected')
        return render(request, self.template_name, {'project':project})

class CreateProject(LoginRequiredMixin, BSModalCreateView):
    login_url = 'login' 
    template_name = 'landing.html'
    form_class = NewProjectForm
    #success_message = 'Success: Project was created.'
    #success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(request.POST)
        #Processes request if valid
        if form.is_valid():
            # form.save()
            name = form.cleaned_data.get('name')
            project = Project(name=name)
            project.save(user=request.user)
            #context = {'project': project, 'new_project_form': form}
            #Redirect to new project
            return redirect('landing', pk=project.pk) #render(request, self.template_name, context)

        #If invalid, show form is not working because you would need to 
        #reload previous page and pass POST data as well.
        #Decided to redirect to previous page for now
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
        #context = {'project': Project.objects.get(pk=kwargs.get('pk')),'new_project_form': form}
        #return redirect('landing', pk=kwargs.get('pk'), form=form )
        #return render(request, self.template_name, context)

def deleteuser(request):
    if request.method == 'POST':
        delete_form = UserDeleteForm(request.POST, instance=request.user)
        user = request.user
        user.is_active = False
        user.save()
        messages.info(request, 'Your account has been deleted.')
        return redirect('login')
    else:
        delete_form = UserDeleteForm(instance=request.user)

    context = {
        'delete_form': delete_form
    }

    return render(request, 'user/delete.html', context)
