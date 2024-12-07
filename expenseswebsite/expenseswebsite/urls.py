
from django.contrib import admin
from django.urls import path, include,  re_path

from . import views

urlpatterns = [

    path('authentication/', include('authentication.urls')),

    re_path(r'^$', views.dashboard, name='dashboard'),

    path('dashboard/data/', views.dashboard_data, name='dashboard_data'),
    


    path('expenses/', include('expenses.urls')),

    path('admin/', admin.site.urls),

    
    path('preferences/', include('userpreferences.urls')),
    path('income/', include('userincome.urls')),
  
]
