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
    url(r'^update_managers_table/$', views.DataView.update_managers_table, name='update_managers_table'),
    url(r'^delete_managers_table/$', views.DataView.delete_managers_table, name='delete_managers_table'),
    url(r'^update_lease_tenants_table/$', views.DataView.update_lease_tenants_table, name='update_lease_tenants_table'),
    url(r'^delete_lease_tenants_table/$', views.DataView.delete_lease_tenants_table, name='delete_lease_tenants_table'),
    url(r'^add/$', views.AddView.add, name='add'), # Add this /about/ route
    # url(r'^finishreal/$', views.FinishRealPageView.as_view()), # Add this /about/ route
    # url(r'^index_copy/$', views.IndexCopyPageView.as_view()), # Add this /about/ route
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)