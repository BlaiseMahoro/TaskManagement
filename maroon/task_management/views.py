from django.shortcuts import render
from django.views.generic import DetailView, ListView, ListView, TemplateView, View
from django.views.generic.base import RedirectView
from django.http import HttpResponse

# Create your views here.

class Redirect(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'landing'

class Landing(View): #Will later add: LoginRequredMixin
    #login_url = 'login'
    template_name = "landing.html"

    def get(self, request):
        project = "Project one"
        project_2 = "Project two"
        context = {
            'some_value' : project, 
            'some_other_value' : project_2,
        }
        return render(request, self.template_name, context)
