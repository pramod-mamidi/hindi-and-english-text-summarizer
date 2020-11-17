from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.TempView,name="Home"),
    path('summarizer/', views.Organiser,name='summarizer'),
    path('EngSummarizer/',views.EngOrganiser,name='EngSummarizer')
]
