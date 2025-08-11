from django.db import models

class About(models.Model):
    titre = models.CharField(max_length=200)
    texte = models.TextField()
    image = models.ImageField(upload_to='about_images/')

    def __str__(self):
        return self.titre

class Service(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='service_images/')
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return self.nom

class Realisation(models.Model):
    titre = models.CharField(max_length=200)
    image_couverture = models.ImageField(upload_to='realisations_cover/', blank=True, null=True)
    description = models.TextField()
    categorie = models.CharField(max_length=100)

    def __str__(self):
        return self.titre

class Media(models.Model):
    TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]
    realisation = models.ForeignKey(Realisation, related_name='medias', on_delete=models.CASCADE)
    media = models.FileField(upload_to='realisations_media/')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.realisation.titre} - {self.type}"

class Lifestyle(models.Model):
    titre = models.CharField(max_length=200)
    image_couverture = models.ImageField(upload_to='lifestyle_cover/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.titre

class LifestyleMedia(models.Model):
    TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]
    lifestyle = models.ForeignKey(Lifestyle, related_name='medias', on_delete=models.CASCADE)
    media = models.FileField(upload_to='lifestyle_media/')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.lifestyle.titre} - {self.type}"

class MembreEquipe(models.Model):
    nom = models.CharField(max_length=200)
    poste = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='equipe_photos/')
    biographie = models.TextField(blank=True)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return self.nom

class Reservation(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('refuse', 'Refusé'),
    ]
    nom = models.CharField(max_length=200)
    email = models.EmailField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    message = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"Réservation de {self.nom} pour {self.service.nom} le {self.date}"

class RendezVous(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('refuse', 'Refusé'),
    ]
    nom = models.CharField(max_length=200)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    objet = models.CharField(max_length=200)
    date = models.DateField()
    heure = models.TimeField()
    message = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"Rendez-vous de {self.nom} le {self.date} à {self.heure}"

class ContactMessage(models.Model):
    nom = models.CharField(max_length=200)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.nom} - {self.sujet} ({self.date_envoi.strftime('%Y-%m-%d %H:%M')})"
