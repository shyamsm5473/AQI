"""
seed_publications.py
──────────────────────────────────────────────────────────────────────────────
One-time seed script: loads the 3 original publications (previously hard-coded
in the localCacheStore JS array) into the Django database.

Run from the project root:
    python seed_publications.py
"""

import os
import django

# ── Bootstrap Django ──────────────────────────────────────────────────────────
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iiitl_project.settings")
django.setup()

from related_publication.models import Publication

SEED_DATA = [
    {
        "authors":   "Pulkit Dwivedi, Soumendu Chakraborty",
        "title":     "FrTrGAN: Single image dehazing using the frequency component of transmission maps in the generative adversarial network",
        "journal":   "Computer Vision and Image Understanding, Elsevier",
        "year":      "2025",
        "link":      "https://doi.org/10.1016/j.cviu.2025.104336",
        "publisher": "Elsevier",
        "impact":    "",
    },
    {
        "authors":   "Pulkit Dwivedi, Soumendu Chakraborty",
        "title":     "A comprehensive qualitative and quantitative survey on image dehazing based on deep neural networks",
        "journal":   "Neurocomputing, Vol-610, 128582, Elsevier",
        "year":      "2024",
        "link":      "https://doi.org/10.1016/j.neucom.2024.128582",
        "publisher": "Elsevier",
        "impact":    "",
    },
    {
        "authors":   "Pulkit Dwivedi, Soumendu Chakraborty",
        "title":     "Single image dehazing using extended local dark channel prior",
        "journal":   "Image and Vision Computing, Volume 136, 104747, Elsevier",
        "year":      "2023",
        "link":      "https://doi.org/10.1016/j.imavis.2023.104747",
        "publisher": "Elsevier",
        "impact":    "4.7",
    },
]


def run():
    if Publication.objects.exists():
        print(f"[SEED] Database already contains {Publication.objects.count()} record(s). Skipping seed.")
        return

    created = []
    for entry in SEED_DATA:
        pub = Publication.objects.create(**entry)
        created.append(pub)
        print(f"  [+] Created: [{pub.year}] {pub.title[:60]}…")

    print(f"\n[SEED] Done. {len(created)} publication(s) inserted into the database.")


if __name__ == "__main__":
    run()
