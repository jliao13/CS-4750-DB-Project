from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class LoginView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'login.html', context=None)

# Add this view
class DataView(TemplateView):
    template_name = "data.html"

class AddView(TemplateView):
    template_name = "add.html"

# class FinishRealPageView(TemplateView):
#     template_name = "finishreal.html"

# class IndexCopyPageView(TemplateView):
#     template_name = "index_copy.html"