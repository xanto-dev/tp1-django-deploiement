# testApp/models.py
from django.db import models

class PermisAnimal(models.Model):
    permis_numero = models.CharField(max_length=50, unique=True)
    permis_date_debut = models.DateField(null=True, blank=True)
    permis_date_fin = models.DateField(null=True, blank=True)
    gardien_territoire = models.CharField(max_length=255, null=True, blank=True)
    animal_type_permis = models.CharField(max_length=100, null=True, blank=True)
    animal_nom = models.CharField(max_length=100, null=True, blank=True)
    animal_categorie = models.CharField(max_length=100, null=True, blank=True)
    animal_race_primaire = models.CharField(max_length=100, null=True, blank=True)
    animal_race_croise = models.CharField(max_length=100, null=True, blank=True)
    animal_sexe = models.CharField(max_length=20, null=True, blank=True)
    animal_couleur = models.CharField(max_length=100, null=True, blank=True)
    animal_date_naissance = models.DateField(null=True, blank=True)
    animal_vaccination = models.BooleanField(default=False)
    animal_sterilisation = models.BooleanField(default=False)
    animal_poids_kg = models.FloatField(default=0)
    animal_micropuce = models.BooleanField(default=False)
    animal_pot_dangereux = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.animal_nom} ({self.animal_type_permis})"


class PermisConstruction(models.Model):
    no_permis = models.CharField(max_length=50, unique=True)
    type_permis = models.CharField(max_length=10, null=True, blank=True)
    type_permis_descr = models.CharField(max_length=255, null=True, blank=True)
    categorie_batiment = models.CharField(max_length=255, null=True, blank=True)
    type_batiment = models.CharField(max_length=255, null=True, blank=True)
    date_emission = models.DateField(null=True, blank=True)
    structure = models.CharField(max_length=100, null=True, blank=True)
    cout_permis = models.FloatField(null=True, blank=True)
    nombre_etages = models.IntegerField(null=True, blank=True)
    nombre_logements = models.IntegerField(null=True, blank=True)
    sup_ca = models.FloatField(null=True, blank=True)
    lots = models.CharField(max_length=500, null=True, blank=True)
    entrepreneur = models.CharField(max_length=255, null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    exville_code = models.CharField(max_length=10, null=True, blank=True)
    exville_descr = models.CharField(max_length=100, null=True, blank=True)
    occupation_debut = models.DateField(null=True, blank=True)
    occupation_fin = models.DateField(null=True, blank=True)
    adresse_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.no_permis} - {self.adresse}"

class BonTravailAqueduc(models.Model):
    probleme = models.CharField(max_length=100, blank=True, null=True)
    date_realisee = models.DateField(blank=True, null=True)
    secteur = models.CharField(max_length=20, blank=True, null=True)
    district = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.probleme or 'Inconnu'} - Secteur {self.secteur or '?'}"
    

class RegistreGES(models.Model):
    num_sago = models.CharField(max_length=100, blank=True, null=True)  # NUM_SAGO : Identifiant de l'établissement
    annee = models.IntegerField(blank=True, null=True)  # Annee : Année des données
    entreprise = models.CharField(max_length=255, blank=True, null=True)  # Entreprise : Nom de l'entreprise
    etablissement = models.CharField(max_length=255, blank=True, null=True)  # Etablissement : Nom de l'établissement
    scian = models.CharField(max_length=255, blank=True, null=True)  # SCIAN : Code et description du secteur d'activité
    adresse = models.TextField(blank=True, null=True)  # Adresse : Adresse complète (inclut ville, code postal si présent)
    region = models.CharField(max_length=100, blank=True, null=True)  # Region : Région administrative
    mun = models.CharField(max_length=100, blank=True, null=True)  # Mun : Municipalité (équivalent à ville)
    em_tot = models.FloatField(blank=True, null=True)  # Em_tot : Émissions totales en t CO2 eq.
    em_bio_comb = models.FloatField(blank=True, null=True)  # Em_bio_comb : Émissions biogènes de combustion
    em_bio_aut = models.FloatField(blank=True, null=True)  # Em_bio_aut : Autres émissions biogènes
    em_exc_bio = models.FloatField(blank=True, null=True)  # Em_exc_bio : Émissions non biogènes
    co2_t = models.FloatField(blank=True, null=True)  # CO2(t) : CO2 en tonnes
    ch4_t = models.FloatField(blank=True, null=True)  # CH4(t) : CH4 en tonnes
    n2o_t = models.FloatField(blank=True, null=True)  # N2O(t) : N2O en tonnes
    hfc_32_t = models.FloatField(blank=True, null=True)  # HFC-32(t) : HFC-32 en tonnes (optionnel)
    hfc_125_t = models.FloatField(blank=True, null=True)  # HFC-125(t) : HFC-125 en tonnes (optionnel)
    hfc_134a_t = models.FloatField(blank=True, null=True)  # HFC-134a(t) : HFC-134a en tonnes (optionnel)
    hfc_143a_t = models.FloatField(blank=True, null=True)  # HFC-143a(t) : HFC-143a en tonnes (optionnel)
    hfc_227ea_t = models.FloatField(blank=True, null=True)  # HFC-227ea(t) : HFC-227ea en tonnes (optionnel)
    hfc_245fa_t = models.FloatField(blank=True, null=True)  # HFC-245fa(t) : HFC-245fa en tonnes (optionnel)
    hfc_365mfc_t = models.FloatField(blank=True, null=True)  # HFC-365mfc(t) : HFC-365mfc en tonnes (optionnel)
    sf6_t = models.FloatField(blank=True, null=True)  # SF6(t) : SF6 en tonnes (optionnel)
    cf4_t = models.FloatField(blank=True, null=True)  # CF4(t) : CF4 en tonnes (optionnel)
    c2f6_t = models.FloatField(blank=True, null=True)  # C2F6(t) : C2F6 en tonnes (optionnel)
    c_c4f8_t = models.FloatField(blank=True, null=True)  # c-C4F8(t) : c-C4F8 en tonnes (optionnel)
    hfc_23_t = models.FloatField(blank=True, null=True)  # HFC-23(t) : HFC-23 en tonnes (optionnel)
    hfc_43_10mee_t = models.FloatField(blank=True, null=True)  # HFC-43-10mee(t) : HFC-43-10mee en tonnes (optionnel)
    note = models.TextField(blank=True, null=True)  # Note : Notes supplémentaires (e.g., validation)
    latitude = models.FloatField(blank=True, null=True)  # Latitude : Extrait de properties["Latitude"] (mis à null si absent)
    longitude = models.FloatField(blank=True, null=True)  # Longitude : Extrait de properties["Longitude"] (mis à null si absent)
    coord_x = models.FloatField(blank=True, null=True)  # Coordonnée X (longitude) extraite de geometry.coordinates
    coord_y = models.FloatField(blank=True, null=True)  # Coordonnée Y (latitude) extraite de geometry.coordinates

    def __str__(self):
        return f"{self.etablissement} - {self.annee}"