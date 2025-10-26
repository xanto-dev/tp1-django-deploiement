from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import PermisAnimalSerializer, PermisConstructionSerializer, BonTravailAqueducSerializer, RegistreGESSerializer
from .models import PermisAnimal, PermisConstruction, BonTravailAqueduc, RegistreGES

from django.db.models import Count, Sum
from django.db.models.functions import TruncYear


from drf_yasg.utils import swagger_auto_schema
@swagger_auto_schema(tags=['PermisAnimal'], responses={200: PermisAnimalSerializer(many=True)})


class RegistreGESViewSet(viewsets.ModelViewSet):
    queryset = RegistreGES.objects.all()                
    serializer_class = RegistreGESSerializer             

    def list(self, request):
        registres_ges = self.get_queryset()              
        serializer = self.get_serializer(registres_ges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class BonTravailAqueducViewSet(viewsets.ModelViewSet):
    queryset = BonTravailAqueduc.objects.all()                
    serializer_class = BonTravailAqueducSerializer             

    def list(self, request):
        bons_travail = self.get_queryset()              
        serializer = self.get_serializer(bons_travail, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class PermisAnimalViewSet(viewsets.ModelViewSet):
    queryset = PermisAnimal.objects.all()               
    serializer_class = PermisAnimalSerializer            

    def list(self, request):
        permis_animals = PermisAnimal.objects.all()
        serializer = self.get_serializer(permis_animals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PermisConstructionViewSet(viewsets.ModelViewSet):
    queryset = PermisConstruction.objects.all()                
    serializer_class = PermisConstructionSerializer             

    def list(self, request):
        permis_constructions = self.get_queryset()              
        serializer = self.get_serializer(permis_constructions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



"""def statistiques(request):
    # Nombre total par modèle
    total_animaux = PermisAnimal.objects.count()
    total_construction = PermisConstruction.objects.count()

    # Répartition thématique : exemple par type de permis
    repartition_types_animaux = (
        PermisAnimal.objects.values('animal_type_permis')
        .annotate(nombre=Count('id'))
        .order_by('-nombre')
    )

    # Tendances temporelles : nombre de permis par année
    tendances_construction = (
        PermisConstruction.objects
        .annotate(annee=TruncYear('date_emission'))
        .values('annee')
        .annotate(total=Count('id'))
        .order_by('annee')
    )

    context = {
        'total_animaux': total_animaux,
        'total_construction': total_construction,
        'repartition_types_animaux': repartition_types_animaux,
        'tendances_construction': tendances_construction,
    }
    return render(request, 'statistiques.html', context)"""
def statistiques(request):
    # ==== PERMIS ====
    total_animaux = PermisAnimal.objects.count()
    total_construction = PermisConstruction.objects.count()

    repartition_types_animaux = (
        PermisAnimal.objects.values('animal_type_permis')
        .annotate(nombre=Count('id'))
        .order_by('-nombre')
    )

    tendances_construction = (
        PermisConstruction.objects
        .annotate(annee=TruncYear('date_emission'))
        .values('annee')
        .annotate(total=Count('id'))
        .order_by('annee')
    )

    # ==== AQUEDUC ====
    total_aqueduc = BonTravailAqueduc.objects.count()

    repartition_secteur_aqueduc = (
        BonTravailAqueduc.objects
        .values('secteur')
        .annotate(nombre=Count('id'))
        .order_by('-nombre')
    )

    tendances_aqueduc = (
        BonTravailAqueduc.objects
        .annotate(annee=TruncYear('date_realisee'))
        .values('annee')
        .annotate(total=Count('id'))
        .order_by('annee')
    )

    # ==== REGISTRE GES ====
    total_ges = RegistreGES.objects.count()

    repartition_region_ges = (
        RegistreGES.objects
        .values('region')
        .annotate(nombre=Count('id'))
        .order_by('-nombre')
    )

    tendances_ges = (
        RegistreGES.objects
        .values('annee')
        .annotate(emissions_totales=Sum('em_tot'))
        .order_by('annee')
    )

    context = {
        # Données permis
        'total_animaux': total_animaux,
        'total_construction': total_construction,
        'repartition_types_animaux': repartition_types_animaux,
        'tendances_construction': tendances_construction,
        # Données aqueduc
        'total_aqueduc': total_aqueduc,
        'repartition_secteur_aqueduc': repartition_secteur_aqueduc,
        'tendances_aqueduc': tendances_aqueduc,
        # Données GES
        'total_ges': total_ges,
        'repartition_region_ges': repartition_region_ges,
        'tendances_ges': tendances_ges,
    }
    return render(request, 'statistiques.html', context)

def home(request):
    return render(request, 'base1.html')


