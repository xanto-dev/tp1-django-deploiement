import os
import sys
import re
from django.core.management.base import BaseCommand
import requests
from datetime import datetime

# Tentative d'import du modèle
try:
    from app1.models import PermisConstruction
except Exception:
    PermisConstruction = None

URL = "https://www.donneesquebec.ca/recherche/dataset/c7808c42-e401-49f0-8049-df3c809d5982/resource/2c06a590-f783-40a3-a62e-597287bd4feb/download/permis-de-construction.json"


def _ensure_django_setup():
    """S’assure que Django est initialisé correctement"""
    import django
    if django.conf.settings.configured:
        return

    current = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current, "..", "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

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

    if "DJANGO_SETTINGS_MODULE" not in os.environ:
        raise RuntimeError(
            "DJANGO_SETTINGS_MODULE n'est pas défini. Exécute le script via manage.py ou définis-le manuellement."
        )

    django.setup()


class Command(BaseCommand):
    help = "Importe les permis de construction depuis le portail Données Québec"

    def handle(self, *args, **options):
        global PermisConstruction
        if PermisConstruction is None:
            try:
                _ensure_django_setup()
                from app1.models import PermisConstruction as _PermisConstruction
                PermisConstruction = _PermisConstruction
            except Exception as e:
                self.stderr.write(f"❌ Impossible d'initialiser Django : {e}")
                return

        self.stdout.write("📡 Téléchargement des données...")
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        self.stdout.write(f"✅ {len(data)} éléments reçus")

        for item in data:
            try:
                PermisConstruction.objects.update_or_create(
                    no_permis=item.get("NO_PERMIS"),
                    defaults={
                        "type_permis": item.get("TYPE_PERMIS"),
                        "type_permis_descr": item.get("TYPE_PERMIS_DESCR"),
                        "categorie_batiment": item.get("CATEGORIE_BATIMENT"),
                        "type_batiment": item.get("TYPE_BATIMENT"),
                        "date_emission": self.parse_date(item.get("DATE_EMISSION")),
                        "structure": item.get("STRUCTURE"),
                        "cout_permis": float(item.get("COUT_PERMIS", 0) or 0),
                        "nombre_etages": self.safe_int(item.get("NOMBRE_ETAGES")),
                        "nombre_logements": self.safe_int(item.get("NOMBRE_LOGEMENTS")),
                        "sup_ca": float(item.get("SUP_CA", 0) or 0),
                        "lots": item.get("LOTS"),
                        "entrepreneur": item.get("ENTREPRENEUR"),
                        "adresse": item.get("ADRESSE"),
                        "exville_code": item.get("EXVILLE_CODE"),
                        "exville_descr": item.get("EXVILLE_DESCR"),
                        "occupation_debut": self.parse_date(item.get("OCCUPATION_DEBUT")),
                        "occupation_fin": self.parse_date(item.get("OCCUPATION_FIN")),
                        "adresse_details": item.get("ADRESSE_DETAILS"),
                    },
                )
            except Exception as e:
                self.stderr.write(f"❌ Erreur pour {item.get('NO_PERMIS')}: {e}")

        self.stdout.write(self.style.SUCCESS("✅ Importation des permis de construction terminée avec succès"))

    def parse_date(self, date_str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None

    def safe_int(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None


if __name__ == "__main__":
    try:
        _ensure_django_setup()
        from app1.models import PermisConstruction  # noqa
        Command().handle()
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)
