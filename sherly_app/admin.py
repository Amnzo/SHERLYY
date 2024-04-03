from django.contrib import admin

from .models import *

# Register your models here.
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('designation', 'famille', 'conditionnement_count', 'prix', 'reference', 'is_active', 'total_products')
    list_filter = ('is_active',)  # Add a filter for is_active field
    search_fields = ('designation', 'reference')  # Add fields for searching

    def total_products(self, obj):
        """
        Custom method to display the total number of products.
        """
        return Produit.objects.count()

    total_products.short_description = 'Total Products'  # Set the column header

admin.site.register(Produit, ProduitAdmin)
admin.site.register(Famille)
admin.site.register(Image)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_number', 'mois_concerne')
admin.site.register(Invoice,InvoiceAdmin)

admin.site.register(Societe)
admin.site.register(Facture)
admin.site.register(Banniere)

class Bon_CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_de_cmd', 'no_cmde')  # Add the fields you want to display in the list

admin.site.register(Bon_Commande, Bon_CommandeAdmin)

class Bon_LivraisonAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_de_bl', 'no_bl')  # Add the fields you want to display in the list

admin.site.register(Bon_Livraison, Bon_LivraisonAdmin)
admin.site.register(EmailSettings)
admin.site.register(TABLE_BL)




