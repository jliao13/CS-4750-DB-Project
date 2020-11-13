from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from frontend import views

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='loginPage'),
    url(r'^login/$', views.LoginView.login, name='login'),
    url(r'^create/$', views.LoginView.create, name='create'),
    url(r'^logout/$', views.LoginView.logout, name='logout'),
    url(r'^data/$', views.DataView.as_view(), name='data'), # Add this /about/ route
    url(r'^add/$', views.AddView.add, name='add'), # Add this /about/ route
    url(r'^upload/$', views.AddView.upload, name='upload'),
    # url(r'^finishreal/$', views.FinishRealPageView.as_view()), # Add this /about/ route
    # url(r'^index_copy/$', views.IndexCopyPageView.as_view()), # Add this /about/ route
    path('delete/<int:property_id>&<int:apartment_number>', views.DataView.delete),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)