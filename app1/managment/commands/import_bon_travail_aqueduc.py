import os
import sys
import re
from django.core.management.base import BaseCommand
import requests
from datetime import datetime

# Tentative d'import du modèle avant setup complet
try:
    from app1.models import BonTravailAqueduc
except Exception:
    BonTravailAqueduc = None

URL = "https://www.donneesquebec.ca/recherche/dataset/e439ae64-b284-4e30-b1ec-9c0855954942/resource/7ed8bf0b-b6dd-4d8d-8fd9-0c652b062c02/download/bon-travail-aqueduc.json"


def _ensure_django_setup():
    """Configure Django si ce n'est pas déjà fait."""
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
            "DJANGO_SETTINGS_MODULE n'est pas défini. Exécute ce script via manage.py."
        )

    django.setup()


class Command(BaseCommand):
    help = "Importe les données de bon travail aqueduc depuis Données Québec"

    def handle(self, *args, **options):
        global BonTravailAqueduc
        if BonTravailAqueduc is None:
            try:
                _ensure_django_setup()
                from app1.models import BonTravailAqueduc as _BonTravailAqueduc
                BonTravailAqueduc = _BonTravailAqueduc
            except Exception as e:
                self.stderr.write(f"❌ Impossible d'initialiser Django: {e}")
                return

        self.stdout.write("📡 Téléchargement des données...")
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        self.stdout.write(f"✅ {len(data)} éléments reçus")

        for item in data:
            try:
                BonTravailAqueduc.objects.create(
                    probleme=item.get("probleme", ""),
                    date_realisee=self.parse_date(item.get("date-realisee")),
                    secteur=item.get("secteur", ""),
                    district=item.get("district", ""),
                )
            except Exception as e:
                self.stderr.write(f"❌ Erreur pour {item}: {e}")

        self.stdout.write(self.style.SUCCESS("✅ Importation terminée avec succès"))

    def parse_date(self, date_str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None


if __name__ == "__main__":
    try:
        _ensure_django_setup()
        from app1.models import BonTravailAqueduc  # noqa
        Command().handle()
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)
