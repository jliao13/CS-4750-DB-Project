from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from frontend import views

urlpatterns = [
    url(r'^$', views.LoginView.as_view()),
    url(r'^data/$', views.DataView.as_view()), # Add this /about/ route
    url(r'^add/$', views.AddView.as_view()), # Add this /about/ route
    # url(r'^finishreal/$', views.FinishRealPageView.as_view()), # Add this /about/ route
    # url(r'^index_copy/$', views.IndexCopyPageView.as_view()), # Add this /about/ route
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)