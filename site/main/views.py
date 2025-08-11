from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, Reservation, MembreEquipe

from .models import About, Service

from django.contrib import messages
from .models import ContactMessage

from .models import Lifestyle

def index(request):
    about = About.objects.first()
    services = Service.objects.all()
    from .models import Realisation, MembreEquipe
    realisations = Realisation.objects.all()
    membres = MembreEquipe.objects.all()
    lifestyles = Lifestyle.objects.all()

    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message_text = request.POST.get('message')

        if not (nom and email and sujet and message_text):
            messages.error(request, "Veuillez remplir tous les champs du formulaire de contact.")
        else:
            contact_message = ContactMessage(
                nom=nom,
                email=email,
                sujet=sujet,
                message=message_text
            )
            contact_message.save()
            messages.success(request, "Votre message a été envoyé avec succès.")

    return render(request, 'index.html', {'about': about, 'services': services, 'realisations': realisations, 'membres': membres, 'lifestyles': lifestyles})

def reservation(request):
    services = Service.objects.all()
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        service_id = request.POST.get('service')
        date = request.POST.get('date')
        message_text = request.POST.get('message')

        if not (nom and email and service_id and date):
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Veuillez remplir tous les champs obligatoires.'})
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return render(request, 'reservation.html', {'services': services})

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Service sélectionné invalide.'})
            messages.error(request, "Service sélectionné invalide.")
            return render(request, 'reservation.html', {'services': services})

        reservation = Reservation(
            nom=nom,
            email=email,
            service=service,
            date=date,
            message=message_text or ''
        )
        reservation.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        messages.success(request, "Votre réservation a été envoyée avec succès.")
        return redirect('reservation')

    return render(request, 'reservation.html', {'services': services})

def equipe(request):
    membres = MembreEquipe.objects.all()
    return render(request, 'equipe.html', {'membres': membres})

def services(request):
    services_list = Service.objects.all()
    return render(request, 'services.html', {'services': services_list})

def realisations(request):
    from .models import Realisation
    realisations_list = Realisation.objects.all()
    return render(request, 'realisations.html', {'realisations': realisations_list})

def realisation_detail(request, pk):
    from .models import Realisation
    try:
        realisation = Realisation.objects.get(pk=pk)
        medias = realisation.medias.all()
    except Realisation.DoesNotExist:
        realisation = None
        medias = None
    return render(request, 'realisation_detail.html', {'realisation': realisation, 'medias': medias})

def lifestyle(request):
    from .models import Lifestyle
    lifestyles = Lifestyle.objects.all()
    return render(request, 'lifestyle.html', {'lifestyles': lifestyles})

def lifestyle_detail(request, pk):
    from .models import Lifestyle
    try:
        lifestyle = Lifestyle.objects.get(pk=pk)
        medias = lifestyle.medias.all()
    except Lifestyle.DoesNotExist:
        lifestyle = None
        medias = None
    return render(request, 'lifestyle_detail.html', {'lifestyle': lifestyle, 'medias': medias})

from django.http import JsonResponse

def rendezvous(request):
    from .models import RendezVous
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        objet = request.POST.get('objet')
        date = request.POST.get('date')
        heure = request.POST.get('heure')
        message_text = request.POST.get('message')

        if not (nom and email and telephone and objet and date and heure):
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Veuillez remplir tous les champs obligatoires.'})
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return render(request, 'rendezvous.html')

        rendezvous = RendezVous(
            nom=nom,
            email=email,
            telephone=telephone,
            objet=objet,
            date=date,
            heure=heure,
            message=message_text or ''
        )
        rendezvous.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        messages.success(request, "Votre demande de rendez-vous a été envoyée avec succès.")
        return redirect('rendezvous')

    return render(request, 'rendezvous.html')

def contact(request):
    return render(request, 'contact.html')

from django.http import JsonResponse

def service_autocomplete(request):
    query = request.GET.get('q', '')
    services = Service.objects.filter(nom__icontains=query).values_list('nom', flat=True)[:10]
    return JsonResponse(list(services), safe=False)
