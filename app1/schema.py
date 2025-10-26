import graphene
from graphene_django.types import DjangoObjectType
from .models import PermisAnimal, PermisConstruction, BonTravailAqueduc, RegistreGES



# type GraphQL pour RegistreGES
class RegistreGESType(DjangoObjectType):
    class Meta:
        model = RegistreGES
        fields = "__all__"


# Type GraphQL pour BonTravailAqueduc
class BonTravailAqueducType(DjangoObjectType):
    class Meta:
        model = BonTravailAqueduc
        fields = "__all__"


#Type GraphQL pour PermisAnimal
class PermisAnimalType(DjangoObjectType):
    class Meta:
        model = PermisAnimal
        fields = "__all__"

# Type GraphQL pour PermisConstruction
class PermisConstructionType(DjangoObjectType):
    class Meta:
        model = PermisConstruction
        fields = "__all__"



# Définition des queries pour récupérer les données des modèles
class Query(graphene.ObjectType):
    all_permis_animaux = graphene.List(PermisAnimalType)
    all_permis_constructions = graphene.List(PermisConstructionType)
    all_bons_travail_aqueduc = graphene.List(BonTravailAqueducType)
    all_registres_ges = graphene.List(RegistreGESType)

    # Requête pour tous les animaux
    def resolve_all_permis_animaux(root, info, **kwargs):
        return PermisAnimal.objects.all()

    # Requête pour toutes les constructions
    def resolve_all_permis_constructions(root, info, **kwargs):
        return PermisConstruction.objects.all()
    
    # Requête pour tous les bons de travail aqueduc
    def resolve_all_bons_travail_aqueduc(root, info, **kwargs):
        return BonTravailAqueduc.objects.all()
    
    # Requête pour tous les registres GES
    def resolve_all_registres_ges(root, info, **kwargs):
        return RegistreGES.objects.all()
    






# Définition des mutations

#mutations pour creer un registre GES
class CreateRegistreGES(graphene.Mutation):
    class Arguments:
        num_sago = graphene.String(required=True)
        annee = graphene.Int(required=True)
        entreprise = graphene.String(required=True)

    registre_ges = graphene.Field(RegistreGESType)

    def mutate(self, info, num_sago, annee, entreprise):
        registre = RegistreGES.objects.create(
            num_sago=num_sago,
            annee=annee,
            entreprise=entreprise
        )
        return CreateRegistreGES(registre_ges=registre)


# mutation pour supprimer un registre GES
class DeleteRegistreGES(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            registre = RegistreGES.objects.get(pk=id)
            registre.delete()
            return DeleteRegistreGES(ok=True, message="Registre GES supprimé avec succès.")
        except RegistreGES.DoesNotExist:
            return DeleteRegistreGES(ok=False, message="Registre GES introuvable.")
        

# mutation pour mettre à jour un registre GES
class UpdateRegistreGES(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        num_sago = graphene.String(required=False)
        annee = graphene.Int(required=False)
        entreprise = graphene.String(required=False)

    registre_ges = graphene.Field(RegistreGESType)
    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, num_sago=None, annee=None, entreprise=None):
        try:
            registre = RegistreGES.objects.get(pk=id)

            if num_sago is not None:
                registre.num_sago = num_sago
            if annee is not None:
                registre.annee = annee
            if entreprise is not None:
                registre.entreprise = entreprise

            registre.save()

            return UpdateRegistreGES(
                registre_ges=registre,
                ok=True,
                message="Registre GES mis à jour avec succès."
            )
        except RegistreGES.DoesNotExist:
            return UpdateRegistreGES(
                registre_ges=None,
                ok=False,
                message="Registre GES introuvable."
            )




# mutation pour creer un bon de travail aqueduc
class CreateBonTravailAqueduc(graphene.Mutation):
    class Arguments:
        probleme = graphene.String(required=True)
        date_realisee = graphene.Date(required=True)
        secteur = graphene.String(required=True)
        district = graphene.String(required=True)

    bon_travail_aqueduc = graphene.Field(BonTravailAqueducType)

    def mutate(self, info, probleme, date_realisee, secteur, district):
        bon_travail = BonTravailAqueduc.objects.create(
            probleme=probleme,
            date_realisee=date_realisee,
            secteur=secteur,
            district=district
        )
        return CreateBonTravailAqueduc(bon_travail_aqueduc=bon_travail)
    
# mutation pour supprimer un bon de travail aqueduc
class DeleteBonTravailAqueduc(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            bon_travail = BonTravailAqueduc.objects.get(pk=id)
            bon_travail.delete()
            return DeleteBonTravailAqueduc(ok=True, message="Bon de travail aqueduc supprimé avec succès.")
        except BonTravailAqueduc.DoesNotExist:
            return DeleteBonTravailAqueduc(ok=False, message="Bon de travail aqueduc introuvable.")
        
# mutation pour mettre à jour un bon de travail aqueduc
class UpdateBonTravailAqueduc(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        probleme = graphene.String(required=False)
        date_realisee = graphene.Date(required=False)
        secteur = graphene.String(required=False)
        district = graphene.String(required=False)

    bon_travail_aqueduc = graphene.Field(BonTravailAqueducType)
    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, probleme=None, date_realisee=None, secteur=None, district=None):
        try:
            bon_travail = BonTravailAqueduc.objects.get(pk=id)

            if probleme is not None:
                bon_travail.probleme = probleme
            if date_realisee is not None:
                bon_travail.date_realisee = date_realisee
            if secteur is not None:
                bon_travail.secteur = secteur
            if district is not None:
                bon_travail.district = district

            bon_travail.save()

            return UpdateBonTravailAqueduc(
                bon_travail_aqueduc=bon_travail,
                ok=True,
                message="Bon de travail aqueduc mis à jour avec succès."
            )
        except BonTravailAqueduc.DoesNotExist:
            return UpdateBonTravailAqueduc(
                bon_travail_aqueduc=None,
                ok=False,
                message="Bon de travail aqueduc introuvable."
            )



# Mutation pour créer un permis animal
class CreatePermisAnimal(graphene.Mutation):
    class Arguments:
        animal_nom = graphene.String(required=True)
        animal_type_permis = graphene.String(required=True)
        permis_numero = graphene.String(required=True)

    permis_animal = graphene.Field(PermisAnimalType)

    def mutate(self, info, nom, espece, numero):
        permis = PermisAnimal.objects.create(nom=nom, espece=espece, numero=numero)
        return CreatePermisAnimal(permis_animal=permis)

# Mutation pour supprimer un permis animal
class DeletePermisAnimal(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)  # L'identifiant du permis à supprimer

    ok = graphene.Boolean()  # Pour indiquer si la suppression a réussi
    message = graphene.String()  # Message de confirmation ou d'erreur

    def mutate(self, info, id):
        try:
            permis = PermisAnimal.objects.get(pk=id)
            permis.delete()
            return DeletePermisAnimal(ok=True, message="Permis supprimé avec succès.")
        except PermisAnimal.DoesNotExist:
            return DeletePermisAnimal(ok=False, message="Permis introuvable.")

# Mutation pour mettre à jour un permis animal
class UpdatePermisAnimal(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)             # L'ID du permis à modifier
        animal_nom = graphene.String(required=False)       # Nouveau nom (facultatif)
        animal_type_permis = graphene.String(required=False)    # Nouvelle espèce (facultatif)
        permis_numero = graphene.String(required=False)    # Nouveau numéro (facultatif)

    permis_animal = graphene.Field(PermisAnimalType)
    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, animal_nom=None, animal_type_permis=None, permis_numero=None):
        try:
            permis = PermisAnimal.objects.get(pk=id)

            # Met à jour seulement les champs fournis
            if animal_nom is not None:
                permis.animal_nom = animal_nom
            if animal_type_permis is not None:
                permis.animal_type_permis = animal_type_permis
            if permis_numero is not None:
                permis.permis_numero = permis_numero

            permis.save()

            return UpdatePermisAnimal(
                permis_animal=permis,
                ok=True,
                message="Permis animal mis à jour avec succès."
            )
        except PermisAnimal.DoesNotExist:
            return UpdatePermisAnimal(
                permis_animal=None,
                ok=False,
                message="Permis introuvable."
            )


# Mutation pour créer un permis de construction
class CreatePermisConstruction(graphene.Mutation):
    class Arguments:
        no_permis = graphene.String(required=True)
        type_permis = graphene.String(required=True)
        adresse = graphene.String(required=True)
        cout_permis = graphene.Float(required=True)
        

    permis_construction = graphene.Field(PermisConstructionType)
    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, no_permis, type_permis, adresse, cout_permis, **kwargs):
        try:
            permis = PermisConstruction.objects.create(
                no_permis=no_permis,
                type_permis=type_permis,
                adresse=adresse,
                cout_permis=cout_permis,
                **kwargs  # Inclut les champs facultatifs s'ils sont fournis
            )
            return CreatePermisConstruction(
                permis_construction=permis,
                ok=True,
                message="Permis de construction créé avec succès."
            )
        except Exception as e:
            return CreatePermisConstruction(
                permis_construction=None,
                ok=False,
                message=f"Erreur lors de la création du permis : {str(e)}"
            )


# Mutation pour mettre à jour un permis de construction
class UpdatePermisConstruction(graphene.Mutation):
    class Arguments:
        no_permis = graphene.String(required=True)  # Champ requis pour identifier
        type_permis = graphene.String(required=False)
        adresse = graphene.String(required=False)
        cout_permis = graphene.Float(required=False)
        type_permis_descr = graphene.String(required=False)
        categorie_batiment = graphene.String(required=False)
        type_batiment = graphene.String(required=False)
        date_emission = graphene.Date(required=False)
        structure = graphene.String(required=False)
        nombre_etages = graphene.Int(required=False)
        nombre_logements = graphene.Int(required=False)
        sup_ca = graphene.Float(required=False)
        lots = graphene.String(required=False)
        entrepreneur = graphene.String(required=False)
        exville_code = graphene.String(required=False)
        exville_descr = graphene.String(required=False)
        occupation_debut = graphene.Date(required=False)
        occupation_fin = graphene.Date(required=False)
        adresse_details = graphene.String(required=False)

    permis_construction = graphene.Field(PermisConstructionType)
    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, no_permis, **kwargs):
        try:
            permis = PermisConstruction.objects.get(no_permis=no_permis)

            # Met à jour seulement les champs fournis
            for key, value in kwargs.items():
                if value is not None:
                    setattr(permis, key, value)

            permis.save()

            return UpdatePermisConstruction(
                permis_construction=permis,
                ok=True,
                message="Permis de construction mis à jour avec succès."
            )
        except PermisConstruction.DoesNotExist:
            return UpdatePermisConstruction(
                permis_construction=None,
                ok=False,
                message="Permis de construction introuvable."
            )
        except Exception as e:
            return UpdatePermisConstruction(
                permis_construction=None,
                ok=False,
                message=f"Erreur lors de la mise à jour du permis : {str(e)}"
            )


# Mutation pour supprimer un permis de construction
class DeletePermisConstruction(graphene.Mutation):
    class Arguments:
        no_permis = graphene.String(required=True)  # Champ requis pour identifier

    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, no_permis):
        try:
            permis = PermisConstruction.objects.get(no_permis=no_permis)
            permis.delete()
            return DeletePermisConstruction(
                ok=True,
                message="Permis de construction supprimé avec succès."
            )
        except PermisConstruction.DoesNotExist:
            return DeletePermisConstruction(
                ok=False,
                message="Permis de construction introuvable."
            )



# Définition des mutations globales
class Mutation(graphene.ObjectType):
    create_permis_animal = CreatePermisAnimal.Field()
    delete_permis_animal = DeletePermisAnimal.Field()
    update_permis_animal = UpdatePermisAnimal.Field()

    create_bon_travail_aqueduc = CreateBonTravailAqueduc.Field()
    update_bon_travail_aqueduc = UpdateBonTravailAqueduc.Field()
    delete_bon_travail_aqueduc = DeleteBonTravailAqueduc.Field()

    create_permis_construction = CreatePermisConstruction.Field()
    update_permis_construction = UpdatePermisConstruction.Field()
    delete_permis_construction = DeletePermisConstruction.Field()

    create_registre_ges = CreateRegistreGES.Field()
    update_registre_ges = UpdateRegistreGES.Field()
    delete_registre_ges = DeleteRegistreGES.Field()

    

# Schéma global
schema = graphene.Schema(query=Query, mutation=Mutation)
