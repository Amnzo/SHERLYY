from django.http import HttpResponse
from django.shortcuts import render
from sherly_app.models import Famille,Produit,Image,Banniere,Societe
import random
def vitrine(request):
    familles = Famille.objects.all()
    company = Societe.objects.first()
    banners=Banniere.objects.all()
    return render(request, 'vitrine/home.html', {'familles': familles,'banners':banners,'company':company })
    #return HttpResponse("VITRINE")

def more(request, product_id):
    # Récupérer les détails du produit en fonction de product_id (à implémenter selon votre modèle)
    familles = Famille.objects.all()
    company = Societe.objects.first()
    product = Produit.objects.get(id=product_id)  # Remplacez VotreModele par le nom de votre modèle de produit

    context = {
        'product': product,
        'familles':familles,
        'company':company

    }
    return render(request, 'vitrine/more.html', context)


def associate_random_images(request):
    produits = Produit.objects.all()

    for produit in produits:
        # Obtenez toutes les images sauf la première pour ce produit
        #images_supprimer = Image.objects.filter(produit=produit).exclude(pk=produit.image.pk)
        images_supprimer = Image.objects.filter(produit=produit).exclude(pk=produit.image_set.first().pk)

        # Supprimez les images
        images_supprimer.delete()

        # Supprimez les images
        images_supprimer.delete()
    return HttpResponse("NETOYAGE")



def maintenance_page(request):
    message = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Page de maintenance</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }
            .maintenance-message {
                background-color: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            .icon {
                width: 100px; /* Taille de l'image */
                margin-bottom: 20px; /* Espace sous l'image */
            }
        </style>
    </head>
    <body>
        <div class="maintenance-message">
            <img src="https://cdn-icons-png.flaticon.com/512/4411/4411553.png" alt="Icône de maintenance" class="icon">
            <h1>Sitio en mantenimiento</h1>
            <p>El sitio web está temporalmente en mantenimiento. Estaremos de vuelta pronto. Gracias por su paciencia.</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(message)
