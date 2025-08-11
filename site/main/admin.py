from django.contrib import admin
from django.utils.html import format_html
from .models import About, Service, Realisation, Media, Lifestyle, LifestyleMedia, MembreEquipe, Reservation, RendezVous, ContactMessage

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('titre', 'image_preview')
    search_fields = ('titre',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return ""
    image_preview.short_description = 'Image'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'image_preview')
    search_fields = ('nom',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return ""
    image_preview.short_description = 'Image'

class MediaInline(admin.TabularInline):
    model = Media
    extra = 1

@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'image_couverture_preview')
    list_filter = ('categorie',)
    search_fields = ('titre',)
    inlines = [MediaInline]

    def image_couverture_preview(self, obj):
        if obj.image_couverture:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image_couverture.url)
        return ""
    image_couverture_preview.short_description = 'Image de couverture'

class LifestyleMediaInline(admin.TabularInline):
    model = LifestyleMedia
    extra = 1

@admin.register(Lifestyle)
class LifestyleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'image_couverture_preview')
    search_fields = ('titre',)
    inlines = [LifestyleMediaInline]

    def image_couverture_preview(self, obj):
        if obj.image_couverture:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image_couverture.url)
        return ""
    image_couverture_preview.short_description = 'Image de couverture'

@admin.register(MembreEquipe)
class MembreEquipeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'poste', 'ordre', 'photo_preview')
    list_editable = ('ordre',)
    search_fields = ('nom', 'poste')
    ordering = ('ordre',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.photo.url)
        return ""
    photo_preview.short_description = 'Photo'

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'service', 'date', 'statut')
    list_filter = ('statut', 'service')
    search_fields = ('nom', 'email')
    list_editable = ('statut',)
    actions = ['export_as_pdf']

    def export_as_pdf(self, request, queryset):
        from django.http import HttpResponse
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import simpleSplit
        import io

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y = height - 50

        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Liste des réservations")
        y -= 30

        p.setFont("Helvetica", 12)
        line_height = 14
        margin = 50
        max_width = width - 2 * margin

        for reservation in queryset:
            lines = []
            lines.append(f"Nom: {reservation.nom}")
            lines.append(f"Email: {reservation.email}")
            lines.append(f"Service: {reservation.service.nom}")
            lines.append(f"Date: {reservation.date}")
            lines.append(f"Statut: {reservation.statut}")
            lines.append("Message:")
            wrapped_message = simpleSplit(reservation.message or "", "Helvetica", 12, max_width)
            lines.extend(wrapped_message)
            lines.append("")  # empty line for spacing

            for line in lines:
                if y < 50:
                    p.showPage()
                    y = height - 50
                    p.setFont("Helvetica", 12)
                p.drawString(margin, y, line)
                y -= line_height

        p.save()
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reservations.pdf"'
        return response

    export_as_pdf.short_description = "Exporter la sélection en PDF"

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'objet', 'date', 'heure', 'statut')
    list_filter = ('statut',)
    search_fields = ('nom', 'email', 'telephone', 'objet')
    list_editable = ('statut',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoi')
    search_fields = ('nom', 'email', 'sujet')
    list_filter = ('date_envoi',)
