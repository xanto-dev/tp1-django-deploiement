import os
import sys
import re
from django.core.management.base import BaseCommand
import requests
from datetime import datetime

try:
    from app1.models import RegistreGES
except Exception:
    RegistreGES = None

URL = "https://www.donneesquebec.ca/recherche/dataset/fff64fdd-2b42-4b65-af59-16f89e3507b6/resource/0b51c18f-fde5-4ef9-9ca6-943b49ca6e16/download/registreges.geojson"

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
    help = "Importe les données du registre des GES depuis Données Québec"

    def handle(self, *args, **options):
        global RegistreGES
        if RegistreGES is None:
            try:
                _ensure_django_setup()
                from app1.models import RegistreGES as _RegistreGES
                RegistreGES = _RegistreGES
            except Exception as e:
                self.stderr.write(f"❌ Impossible d'initialiser Django : {e}")
                return

        self.stdout.write("📡 Téléchargement des données...")
        try:
            response = requests.get(URL)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            self.stderr.write(f"❌ Erreur lors du téléchargement des données : {e}")
            return

        features = data.get("features", [])
        if not features:
            self.stderr.write("❌ Aucune donnée 'features' trouvée dans le GeoJSON")
            return

        self.stdout.write(f"✅ {len(features)} éléments reçus")

        for feature in features:
            try:
                # Vérification que feature est valide
                if not isinstance(feature, dict):
                    self.stderr.write(f"⚠️ Entrée invalide, ignorée : {feature}")
                    continue

                # Vérification des propriétés
                properties = feature.get("properties")
                if not properties:
                    self.stderr.write(f"⚠️ Propriétés manquantes pour une entrée, ignorée")
                    continue

                # Vérification de la géométrie
                geometry = feature.get("geometry", {})
                coordinates = geometry.get("coordinates", [None, None]) if geometry and geometry != "null" else [None, None]

                # Création ou mise à jour de l'enregistrement (clé unique : num_sago + annee)
                RegistreGES.objects.update_or_create(
                    num_sago=properties.get("NUM_SAGO"),
                    annee=self.safe_int(properties.get("Annee")),
                    defaults={
                        "entreprise": properties.get("Entreprise"),
                        "etablissement": properties.get("Etablissement"),
                        "scian": properties.get("SCIAN"),
                        "adresse": properties.get("Adresse"),
                        "region": properties.get("Region"),
                        "mun": properties.get("Mun"),
                        "em_tot": self.safe_float(properties.get("Em_tot")),
                        "em_bio_comb": self.safe_float(properties.get("Em_bio_comb")),
                        "em_bio_aut": self.safe_float(properties.get("Em_bio_aut")),
                        "em_exc_bio": self.safe_float(properties.get("Em_exc_bio")),
                        "co2_t": self.safe_float(properties.get("CO2(t)")),
                        "ch4_t": self.safe_float(properties.get("CH4(t)")),
                        "n2o_t": self.safe_float(properties.get("N2O(t)")),
                        "hfc_32_t": self.safe_float(properties.get("HFC-32(t)")),
                        "hfc_125_t": self.safe_float(properties.get("HFC-125(t)")),
                        "hfc_134a_t": self.safe_float(properties.get("HFC-134a(t)")),
                        "hfc_143a_t": self.safe_float(properties.get("HFC-143a(t)")),
                        "hfc_227ea_t": self.safe_float(properties.get("HFC-227ea(t)")),
                        "hfc_245fa_t": self.safe_float(properties.get("HFC-245fa(t)")),
                        "hfc_365mfc_t": self.safe_float(properties.get("HFC-365mfc(t)")),
                        "sf6_t": self.safe_float(properties.get("SF6(t)")),
                        "cf4_t": self.safe_float(properties.get("CF4(t)")),
                        "c2f6_t": self.safe_float(properties.get("C2F6(t)")),
                        "c_c4f8_t": self.safe_float(properties.get("c-C4F8(t)")),
                        "hfc_23_t": self.safe_float(properties.get("HFC-23(t)")),
                        "hfc_43_10mee_t": self.safe_float(properties.get("HFC-43-10mee(t)")),
                        "note": properties.get("Note"),
                        "latitude": self.safe_float(properties.get("Latitude")),  # Mis à null si absent
                        "longitude": self.safe_float(properties.get("Longitude")),  # Mis à null si absent
                        "coord_x": coordinates[0] if coordinates and isinstance(coordinates, list) and len(coordinates) >= 2 else None,
                        "coord_y": coordinates[1] if coordinates and isinstance(coordinates, list) and len(coordinates) >= 2 else None,
                    },
                )
            except Exception as e:
                # Afficher un message d'erreur plus détaillé
                num_sago = properties.get("NUM_SAGO") if properties else "inconnu"
                self.stderr.write(f"❌ Erreur pour l'entrée NUM_SAGO={num_sago}: {e}")
                continue

        self.stdout.write(self.style.SUCCESS("✅ Importation du registre des GES terminée avec succès"))

    def safe_int(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def safe_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

if __name__ == "__main__":
    try:
        _ensure_django_setup()
        from app1.models import RegistreGES  # noqa
        Command().handle()
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)