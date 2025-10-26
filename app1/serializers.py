from rest_framework import serializers
from .models import PermisAnimal, PermisConstruction, BonTravailAqueduc, RegistreGES


class BonTravailAqueducSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonTravailAqueduc
        fields = [
            "id",
            "probleme",
            "date_realisee",
            "secteur",
            "district",
        ]




class PermisAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermisAnimal
        fields = [
            "id",
            "permis_numero",
            "permis_date_debut",
            "permis_date_fin",
            "gardien_territoire",
            "animal_type_permis",
            "animal_nom",
            "animal_categorie",
            "animal_race_primaire",
            "animal_race_croise",
            "animal_sexe",
            "animal_couleur",
            "animal_date_naissance",
            "animal_vaccination",
            "animal_sterilisation",
            "animal_poids_kg",
            "animal_micropuce",
            "animal_pot_dangereux",
        ]

class PermisConstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermisConstruction
        fields = [
            "id",
            "no_permis",
            "type_permis",
            "type_permis_descr",
            "categorie_batiment",
            "type_batiment",
            "date_emission",
            "structure",
            "cout_permis",
            "nombre_etages",
            "nombre_logements",
            "sup_ca",
            "lots",
            "entrepreneur",
            "adresse",
            "exville_code",
            "exville_descr",
            "occupation_debut",
            "occupation_fin",
            "adresse_details",
        ]

class RegistreGESSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistreGES
        fields = [
            'num_sago',
            'annee',
            'entreprise',
            'etablissement',
            'scian',
            'adresse',
            'region',
            'mun',
            'em_tot',
            'em_bio_comb',
            'em_bio_aut',
            'em_exc_bio',
            'co2_t',
            'ch4_t',
            'n2o_t',
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
            'note',
            'latitude',
            'longitude',
            'coord_x',
            'coord_y',
        ]