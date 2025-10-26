import os
import sys
import re
from django.core.management.base import BaseCommand
import requests
from datetime import datetime

# Try to import the model; if running standalone this may fail until django.setup() is called.
try:
    from app1.models import PermisAnimal
except Exception:
    PermisAnimal = None

URL = "https://www.donneesquebec.ca/recherche/dataset/e302c3f1-f562-449f-975f-40eb7c9d3b01/resource/b6eedf12-a543-4d61-bcaf-b05bea9e75e2/download/permis-animaux.json"


def _ensure_django_setup():
    """
    Ensure DJANGO_SETTINGS_MODULE is set and django.setup() has been called.
    Tries to detect the settings module from a nearby manage.py if not already set.
    """
    import django
    if django.conf.settings.configured:
        return

    # Try to find project root (assumes this file is at app1/managment/commands/import_data.py)
    current = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current, "..", "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Try to read manage.py to extract DJANGO_SETTINGS_MODULE
    manage_py = os.path.join(project_root, "manage.py")
    if os.path.exists(manage_py):
        try:
            with open(manage_py, "r", encoding="utf-8") as f:
                content = f.read()
                m = re.search(
                    r"os\.environ\.setdefault\(['\"]DJANGO_SETTINGS_MODULE['\"],\s*['\"]([^'\"]+)['\"]\)",
                    content,
                )
                if m:
                    os.environ.setdefault("DJANGO_SETTINGS_MODULE", m.group(1))
        except Exception:
            pass

    # If still not set, leave it to the user to set DJANGO_SETTINGS_MODULE in env
    if "DJANGO_SETTINGS_MODULE" not in os.environ:
        raise RuntimeError(
            "DJANGO_SETTINGS_MODULE n'est pas défini. Définissez la variable d'environnement ou exécutez via manage.py."
        )

    django.setup()


class Command(BaseCommand):
    help = "Importe les permis d'animaux depuis l'API Tourinsoft"

    def handle(self, *args, **options):
        # If the model wasn't importable at module import time, ensure Django is set up and import it now.
        global PermisAnimal
        if PermisAnimal is None:
            try:
                _ensure_django_setup()
                from app1.models import PermisAnimal as _PermisAnimal

                PermisAnimal = _PermisAnimal
            except Exception as e:
                self.stderr.write(f"❌ Impossible d'initialiser Django ou d'importer le modèle: {e}")
                return

        self.stdout.write("📡 Téléchargement des données...")
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        items = data
        self.stdout.write(f"✅ {len(items)} éléments reçus")

        for item in items:
            try:
                PermisAnimal.objects.update_or_create(
                    permis_numero=item.get("Permis_Numéro"),
                    defaults={
                        "permis_date_debut": self.parse_date(item.get("Permis_Date_de_début")),
                        "permis_date_fin": self.parse_date(item.get("Permis_Date_de_fin")),
                        "gardien_territoire": item.get("Gardien_Territoire_ex_villes", ""),
                        "animal_type_permis": item.get("Animal_Type_de_permis", ""),
                        "animal_nom": item.get("Animal_Nom", ""),
                        "animal_categorie": item.get("Animal_Catégorie_race_primaire_de_chiens", ""),
                        "animal_race_primaire": item.get("Animal_Race_primaire_des_chiens", ""),
                        "animal_race_croise": item.get("Animal_Race_croisé_des_chiens", ""),
                        "animal_sexe": item.get("Animal_Sexe", ""),
                        "animal_couleur": item.get("Animal_Couleur", ""),
                        "animal_date_naissance": self.parse_date(item.get("Animal_Date_de_naissance")),
                        "animal_vaccination": bool(item.get("Animal_Vaccination")),
                        "animal_sterilisation": bool(item.get("Animal_Stérilisation")),
                        "animal_poids_kg": float(item.get("Animal_Poids_kg", 0) or 0),
                        "animal_micropuce": bool(item.get("Animal_Micropuce")),
                        "animal_pot_dangereux": bool(item.get("Animal_Potentiellement_dangereux")),
                    },
                )
            except Exception as e:
                self.stderr.write(f"❌ Erreur pour {item.get('Permis_Numéro')}: {e}")

        self.stdout.write(self.style.SUCCESS("✅ Importation terminée avec succès"))

    def parse_date(self, date_str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None


if __name__ == "__main__":
    # Allow running the command file directly: detect/manage.py, set up Django and run.
    try:
        _ensure_django_setup()
        # import model to ensure it's available
        from app1.models import PermisAnimal  # noqa: F401
        Command().handle()
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)