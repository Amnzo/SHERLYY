
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
def is_superuser(user):
    return user.is_superuser

urlpatterns = [

    #------------Famille-------------------,
    path('', login_required(categorie_list, login_url='bl_login'), name='categorie_list'),
    path('add_categorie/', user_passes_test(is_superuser, login_url='bl_login')(add_categorie), name='add_categorie'),
    path('edit_categorie/<int:id>/', user_passes_test(is_superuser, login_url='bl_login')(edit_categorie), name='edit_categorie'),
    #path('fetch-related-products/', fetch_related_products, name='fetch_related_products'),
    path('fetch-related-products/', login_required(fetch_related_products, login_url='bl_login'), name='fetch_related_products'),
    #path('fetch_related_products_in_liste/', login_required(fetch_related_products_in_liste, login_url='bl_login'), name='fetch_related_products_in_liste'),
    #------------SOCIETE-------------------,
    path('company/', user_passes_test(is_superuser, login_url='bl_login')(login_required(company, login_url='bl_login')), name='company'),
    path('parametrage/', user_passes_test(is_superuser, login_url='bl_login')(login_required(parametrage, login_url='bl_login')), name='parametrage'),
    #------------Commande-------------------,
    path('commande_list/', login_required(commande_list, login_url='bl_login'), name='commande_list'),
    path('add_commande/', login_required(add_commande, login_url='bl_login'), name='add_commande'),
    path('edit_commande/<int:bl_id>/', user_passes_test(is_superuser, login_url='bl_login')(edit_commande), name='edit_commande'),
    path('deleted_commande/', user_passes_test(is_superuser, login_url='bl_login')(deleted_commande), name='deleted_commande'),
    path('delete_commande/<int:id>/', user_passes_test(is_superuser, login_url='bl_login')(delete_commande), name='delete_commande'),
    path('delete_confirmation/<int:id>/', user_passes_test(is_superuser, login_url='bl_login')(delete_confirmation), name='delete_confirmation'),
    #------------Produit-----------------------
    #path('product_list', login_required(products_list, login_url='bl_login'), name='product_list'),
    path('product_list/', user_passes_test(is_superuser, login_url='bl_login')(products_list), name='product_list'),
    path('add_product/', user_passes_test(is_superuser, login_url='bl_login')(add_product), name='add_product'),
    path('edit_product/<int:id>/', user_passes_test(is_superuser, login_url='bl_login')(edit_product), name='edit_product'),
    #------------Utilisateur-------------------,
    path('add_user/', user_passes_test(is_superuser, login_url='bl_login')(add_user), name='add_user'),
    path('list_user/', user_passes_test(is_superuser, login_url='bl_login')(list_user), name='list_user'),
    path('profile/', user_passes_test(is_superuser, login_url='bl_login')(profile), name='profile'),
    path('profile_user/<int:id>/', user_passes_test(is_superuser, login_url='bl_login')(profile_user), name='profile_user'),
    path('facture/', user_passes_test(is_superuser, login_url='bl_login')(facture), name='facture'),
    path('generate_facture/', user_passes_test(is_superuser, login_url='bl_login')(generate_facture), name='generate_facture'),
    path('generate_zip/', user_passes_test(is_superuser, login_url='bl_login')(generate_zip), name='generate_zip'),
    path('edit_facture/', user_passes_test(is_superuser, login_url='bl_login')(edit_facture), name='edit_facture'),
    path('generate_pdf/<int:bl_id>/', user_passes_test(is_superuser, login_url='bl_login')(generate_pdf), name='page'),
    path('email/', user_passes_test(is_superuser, login_url='bl_login')(test_email), name='email'),
    path('periode/', user_passes_test(is_superuser, login_url='bl_login')(periode), name='periode'),
    path('hotmail/',hotmail,name="hotmail"),
#-----PROFILE-----------------------------------------------------------------------

    path('bl_login/', bl_custom_login, name='bl_login'),
    path('bl_logout/', bl_custom_logout, name='bl_logout'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
