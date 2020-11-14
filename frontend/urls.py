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
    url(r'^update_property_table/$', views.DataView.update_property_table, name='update_property_table'),
    url(r'^delete_property_table/$', views.DataView.delete_property_table, name='delete_property_table'),
    url(r'^update_amenities_table/$', views.DataView.update_amenities_table, name='update_amenities_table'),
    url(r'^delete_amenities_table/$', views.DataView.delete_amenities_table, name='delete_amenities_table'),
    url(r'^update_lease_table/$', views.DataView.update_lease_table, name='update_lease_table'),
    url(r'^delete_lease_table/$', views.DataView.delete_lease_table, name='delete_lease_table'),
    url(r'^update_apartment_table/$', views.DataView.update_apartment_table, name='update_apartment_table'),
    url(r'^delete_apartment_table/$', views.DataView.delete_apartment_table, name='delete_apartment_table'),
    url(r'^update_provides_table/$', views.DataView.update_provides_table, name='update_provides_table'),
    url(r'^delete_provides_table/$', views.DataView.delete_provides_table, name='delete_provides_table'),
    url(r'^update_manages_table/$', views.DataView.update_manages_table, name='update_manages_table'),
    url(r'^delete_manages_table/$', views.DataView.delete_manages_table, name='delete_manages_table'),
    url(r'^get_apt_info/$', views.DataView.get_apt_info, name='get_apt_info'),
    url(r'^add/$', views.AddView.add, name='add'), # Add this /about/ route
    url(r'^upload/$', views.AddView.upload, name='upload'),
    # url(r'^finishreal/$', views.FinishRealPageView.as_view()), # Add this /about/ route
    # url(r'^index_copy/$', views.IndexCopyPageView.as_view()), # Add this /about/ route
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)