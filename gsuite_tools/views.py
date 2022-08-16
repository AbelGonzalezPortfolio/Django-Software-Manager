from django.views import View
from django.shortcuts import render

# Create your views here.
class Index(View):
    template_name = "gsuite_tools/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
