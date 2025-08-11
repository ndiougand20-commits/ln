from django.shortcuts import render
from main.models import About, Service, Realisation, Lifestyle, MembreEquipe

def index(request):
    about = About.objects.first()
    services = Service.objects.all().order_by('ordre')
    realisations = Realisation.objects.all()[:6]  # latest 6
    lifestyles = Lifestyle.objects.all()[:6]  # latest 6
    equipe = MembreEquipe.objects.all().order_by('ordre')

    context = {
        'about': about,
        'services': services,
        'realisations': realisations,
        'lifestyles': lifestyles,
        'equipe': equipe,
    }
    return render(request, 'index.html', context)
