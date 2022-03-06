"""SpendingApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from Record.views import add_record, show_record, edit_record, update_record, \
    delete_record, record_chart, group_record

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('add_transaction/', add_record, name='add transaction'),
    path('show/', show_record, name='show'),
    path('edit/<int:id>', edit_record, name='edit'),
    path('update/<int:id>', update_record, name='update'),
    path('delete/<int:id>', delete_record, name='delete'),
    path('get_chart/', record_chart, name='chart'),
    path('group_record/', group_record, name='group record'),
]
