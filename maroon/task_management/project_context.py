from .models import Project, Profile, Role
from .forms import NewProjectForm
from django.shortcuts import reverse

#http://kkabardi.me/post/dynamic-menu-navigation-django/
def get_projects(request):
    admin_projects = []
    normal_projects = []
    form_redirect = reverse('create_project')
    #print(request.user.is_authenticated)
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        projects = profile.get_user_projects()
        admin_projects = profile.get_user_projects(admin=True)
        normal_projects = profile.get_user_projects(admin=False)    
        
    return {'admin_projects': admin_projects, 
        'normal_projects': normal_projects, 
        'form_redirect': form_redirect,
        'new_project_form': NewProjectForm()}
