from .models import Project, Profile, Role

def get_projects(request):
    admin_projects = []
    normal_projects = []
    #print(request.user.is_authenticated)
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        projects = profile.get_user_projects()
        admin_projects = profile.get_user_projects(admin=True)
        normal_projects = profile.get_user_projects(admin=False)
        # print("Admin")
        # print(admin_projects)
        # print("Normal")
        # print(normal_projects)
        
    return {'admin_projects': admin_projects, 'normal_projects': normal_projects}
