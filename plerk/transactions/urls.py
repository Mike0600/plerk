#Django restframework
from email.mime import base
from unicodedata import name
from rest_framework import routers

#Django
from django.urls import path, include

#Views
from . import views

router = routers.DefaultRouter()

router.register('transactions', viewset=views.TransactionsListView)
router.register('companies', viewset=views.CompanysListView)

urlpatterns = [
    path('', include(router.urls)),
    path('resume-service/', views.ListResumeService.as_view()),
    path('company-service/', views.ListCompanyService.as_view()),
    path('month-service/', views.MonthResumeService.as_view()),
    path('api/auth/', include('djoser.urls.authtoken'))
]