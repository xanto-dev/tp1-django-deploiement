from django.contrib import admin
from .models import PermisAnimal, PermisConstruction, BonTravailAqueduc, RegistreGES


# Enregistrement du modèle PermisAnimal dans l’admin
@admin.register(PermisAnimal)
class PermisAnimalAdmin(admin.ModelAdmin):
    # ✅ colonnes visibles dans la liste principale
    list_display = (
        'permis_numero', 
        'animal_nom', 
        'animal_type_permis', 
        'animal_categorie',
        'animal_sexe', 
        'animal_couleur',
        'animal_vaccination',
        'animal_sterilisation'
    )

    # ✅ champs de recherche en haut
    search_fields = ('permis_numero', 'animal_nom', 'animal_categorie', 'animal_race_primaire')

    # ✅ filtres latéraux
    list_filter = ('animal_vaccination', 'animal_sterilisation', 'animal_pot_dangereux', 'animal_type_permis')

    # ✅ organisation du formulaire d’édition
    fieldsets = (
        ("Informations sur le permis", {
            "fields": (
                'permis_numero', 
                'permis_date_debut', 
                'permis_date_fin', 
                'gardien_territoire'
            )
        }),
        ("Informations sur l’animal", {
            "fields": (
                'animal_nom', 
                'animal_type_permis', 
                'animal_categorie', 
                'animal_race_primaire', 
                'animal_race_croise', 
                'animal_sexe', 
                'animal_couleur', 
                'animal_date_naissance', 
                'animal_poids_kg'
            )
        }),
        ("Santé et sécurité", {
            "fields": (
                'animal_vaccination', 
                'animal_sterilisation', 
                'animal_micropuce', 
                'animal_pot_dangereux'
            )
        }),
    )

# Enregistrement du modèle PermisConstruction
@admin.register(PermisConstruction)
class PermisConstructionAdmin(admin.ModelAdmin):
    # Colonnes visibles dans la liste principale
    list_display = (
        'no_permis',
        'adresse',
        'type_permis',
        'categorie_batiment',
        'type_batiment',
        'date_emission',
        'cout_permis',
        'nombre_logements',
        'entrepreneur',
    )

    # Champs de recherche en haut
    search_fields = (
        'no_permis',
        'adresse',
        'type_permis',
        'categorie_batiment',
        'entrepreneur',
    )

    # Filtres latéraux
    list_filter = (
        'type_permis',
        'categorie_batiment',
        'date_emission',
        'exville_code',
    )

    # Organisation du formulaire d’édition
    fieldsets = (
        ("Informations générales", {
            "fields": (
                'no_permis',
                'type_permis',
                'type_permis_descr',
                'date_emission',
                'cout_permis',
            )
        }),
        ("Détails du bâtiment", {
            "fields": (
                'categorie_batiment',
                'type_batiment',
                'structure',
                'nombre_etages',
                'nombre_logements',
                'sup_ca',
            )
        }),
        ("Localisation", {
            "fields": (
                'adresse',
                'lots',
                'exville_code',
                'exville_descr',
                'adresse_details',
            )
        }),
        ("Période d'occupation", {
            "fields": (
                'occupation_debut',
                'occupation_fin',
            )
        }),
        ("Entrepreneur", {
            "fields": (
                'entrepreneur',
            )
        }),
    )


# Enregistrement du modèle BonTravailAqueduc dans l’admin
@admin.register(BonTravailAqueduc)
class BonTravailAqueducAdmin(admin.ModelAdmin):
    # ✅ Colonnes visibles dans la liste principale
    list_display = (
        'probleme',
        'date_realisee',
        'secteur',
        'district',
    )

    # ✅ Champs de recherche (barre du haut)
    search_fields = ('probleme', 'secteur', 'district')

    # ✅ Filtres latéraux
    list_filter = ('secteur', 'district', 'probleme')

    # ✅ Organisation du formulaire d’édition
    fieldsets = (
        ("Information sur le problème", {
            "fields": ('probleme', 'date_realisee')
        }),
        ("Localisation", {
            "fields": ('secteur', 'district')
        }),
    )

# Enregistrement du modèle RegistreGES dans l’admin
@admin.register(RegistreGES)
class RegistreGESAdmin(admin.ModelAdmin):
    # Champs à afficher dans la liste
    list_display = (
        'num_sago',
        'annee',
        'entreprise',
        'etablissement',
        'region',
        'mun',
        'em_tot',
        'latitude',
        'longitude',
        'coord_x',
        'coord_y',
    )

    # Champs sur lesquels filtrer
    list_filter = (
        'annee',
        'region',
        'mun',
        'scian',
    )

    # Champs pour la recherche
    search_fields = (
        'num_sago',
        'entreprise',
        'etablissement',
        'adresse',
        'scian',
    )

    # Tri par défaut
    ordering = ('-annee', 'num_sago')

    # Champs en lecture seule (par exemple, pour éviter la modification accidentelle)
    readonly_fields = (
        'num_sago',
        'annee',
        'latitude',
        'longitude',
        'coord_x',
        'coord_y',
    )

    # Organisation des champs dans le formulaire de détail
    fieldsets = (
        ('Informations Générales', {
            'fields': ('num_sago', 'annee', 'entreprise', 'etablissement', 'scian', 'adresse', 'region', 'mun')
        }),
        ('Coordonnées', {
            'fields': ('latitude', 'longitude', 'coord_x', 'coord_y')
        }),
        ('Émissions', {
            'fields': (
                'em_tot',
                'em_bio_comb',
                'em_bio_aut',
                'em_exc_bio',
                'co2_t',
                'ch4_t',
                'n2o_t',
            )
        }),
        ('Gaz Optionnels', {
            'fields': (
                'hfc_32_t',
                'hfc_125_t',
                'hfc_134a_t',
                'hfc_143a_t',
                'hfc_227ea_t',
                'hfc_245fa_t',
                'hfc_365mfc_t',
                'sf6_t',
                'cf4_t',
                'c2f6_t',
                'c_c4f8_t',
                'hfc_23_t',
                'hfc_43_10mee_t',
            ),
            'classes': ('collapse',),  # Section pliable pour les gaz optionnels
        }),
        ('Notes', {
            'fields': ('note',),
        }),
    )