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
from rest_framework import status
from .models import Profile, Project, Role, User, Ticket, State
from .forms import RegisterForm, ProfilePicForm, NewProjectForm, UserDeleteForm, TicketForm, UserUpdate
from bootstrap_modal_forms.generic import BSModalCreateView
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.authtoken.models import Token

# Create your views here.
import json

class Redirect(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'landing'

class Landing(LoginRequiredMixin,View): 
    login_url = 'login'
    landing_template = "landing.html"
    landing_empty_template = "landing_none_selected.html"

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            project = get_object_or_404(Project, pk=kwargs['pk'])
            context = {'project': project, 
                'template_name': self.landing_template, 
                'ticket_form': TicketForm(), 
                'project_profiles': [ role.profile for role in project.roles.all()]}
            return render(request, self.landing_template, context)
        else:
            return render(request, self.landing_empty_template)

    def post(self, request, *args, **kwargs):
        form = TicketForm(request.POST)
        project = get_object_or_404(Project, pk=kwargs['pk'])
        context = {'project': project, 
                'template_name': self.landing_template, 
                'project_profiles': [ role.profile for role in project.roles.all()]}

        if form.is_valid():
            title = form.cleaned_data.get('title')
            type = form.cleaned_data.get('type')
            state = project.ticket_template.states.all()[0]
            description = form.cleaned_data.get('description')
            assignees = form.cleaned_data.get('assignees')

            ticket = Ticket(project=project, title=title, type=type, state=state, description=description)
            ticket.save()
            ticket.assignees.set(assignees)
            context['ticket_form'] = TicketForm() 
            return render(request, self.landing_template, context)
        context['ticket_form'] = form
        return render(request, self.landing_template, context)



class Account(LoginRequiredMixin,View):
    login_url = 'login'
    template_name = "user/account.html"

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        token = Token.objects.get(user=request.user)
        form = UserUpdate()
        context = {"profile":profile, "user_token":token, 'form':form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserUpdate(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            profile = Profile.objects.get(user=request.user)
            context = {"profile":profile}
            return render(request, self.template_name, context)
        profile = Profile.objects.get(user=request.user)
        context = {"profile":profile, 'form':form}
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
            return redirect('landing')
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
class UpdateTicketState(View):
    login_url = 'login'
    
    def post(self, request, *args, **kwargs):
        try:
            state_name = json.loads(request.body)['state']
            ticket = Ticket.objects.get(pk=kwargs.get('pk'))
            print(ticket.project.name)
            state = ticket.project.ticket_template.states.get(state_name=state_name)
            print(state.state_name)
            ticket.state = state
            ticket.save()
            return HttpResponse({'':''},status=status.HTTP_200_OK,
            content_type='application/json')
        except:
            return HttpResponse({'':''},status=status.HTTP_404_NOT_FOUND,
            content_type='application/json')

class AccessSettings(LoginRequiredMixin,View):
    login_url = 'login'
    template_name = "project/management/container.html"

    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_id)
        profile = Profile.objects.get(user=request.user)
        role = Role.objects.get(profile= profile, project= project).role
        # users = User.objects.all().filter(profile= profile)
        # is_admin = role =='is_admin'
        ticket_project = {'states': [{'state_name':'New','color':'#ff0000'}, {'state_name':'To-Do','color':'#ff9500'}, {'state_name':'Doing','color':'#fffb00'}, {'state_name':'Done','color':'#00ff00'}, {'state_name':'Extra','color':'#fb00ff'}], 'types': [{'type_name': 'Bug','color':'#ff9500'}, {'type_name': 'Feature','color':'#0077ff'}], 'attributes': [{'name': 'Example'}, {'name': 'Example 2'}], 'relationships': [{'title': 'Null Pointer on update'}, {'title': 'Ticket Edit Wireframe'}]}
        #ticket_project = {'states': [], 'types': [], 'attributes': [], 'relationships': []}
        print(role)
        context = {'project': project, 'role':role}
        return render(request, self.template_name, context)
    
    def add_user_to_project(request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        if request.method == "POST":
            form = AddUserForm(request.POST)
            if form.is_valid():
                project.users.add(form.cleaned_data["user"])
                return redirect("access")
        else:
            form = AddUserForm()
        return render(request, "add_user.html", {"project": project, "form": form})
