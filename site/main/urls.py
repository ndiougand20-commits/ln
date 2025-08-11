from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reservation/', views.reservation, name='reservation'),
    path('equipe/', views.equipe, name='equipe'),
    path('services/', views.services, name='services'),
    path('realisations/', views.realisations, name='realisations'),
    path('realisations/<int:pk>/', views.realisation_detail, name='realisation_detail'),
    path('lifestyle/', views.lifestyle, name='lifestyle'),
    path('lifestyle/<int:pk>/', views.lifestyle_detail, name='lifestyle_detail'),
    path('rendezvous/', views.rendezvous, name='rendezvous'),
    path('contact/', views.contact, name='contact'),
    path('api/service-autocomplete/', views.service_autocomplete, name='service_autocomplete'),
]
