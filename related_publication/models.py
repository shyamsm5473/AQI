"""
related_publication/models.py
──────────────────────────────────────────────────────────────────────────────
Publication model for the IIIT Lucknow AQI research portal.

Fields mirror the frontend data-keys used in the JS engine so that
JSON serialisation in the API views is a direct 1-to-1 mapping with
no adapter layer required.
"""

from django.db import models


class Publication(models.Model):
    """
    Persistent representation of an academic publication entry.

    All fields that are marked optional (blank=True) may be sent as
    empty strings from the frontend without causing validation errors.
    """

    # ------------------------------------------------------------------
    # Mandatory fields (mirrors the "*" labels in the Add-form UI)
    # ------------------------------------------------------------------
    authors = models.TextField(
        help_text="Comma-separated list of author names."
    )
    title = models.CharField(
        max_length=512,
        help_text="Full title of the paper / book chapter."
    )
    journal = models.CharField(
        max_length=512,
        help_text="Journal name, volume, and issue info."
    )
    year = models.CharField(
        max_length=10,
        help_text="Four-digit publication year (stored as text to allow '2024–25')."
    )

    # ------------------------------------------------------------------
    # Optional fields (blank=True so empty strings are accepted)
    # ------------------------------------------------------------------
    link = models.URLField(
        max_length=2048,
        blank=True,
        default="",
        help_text="DOI link or full URL to the published paper."
    )
    publisher = models.CharField(
        max_length=256,
        blank=True,
        default="",
        help_text="Publisher tag, e.g. IEEE, Elsevier, Springer."
    )
    impact = models.CharField(
        max_length=64,
        blank=True,
        default="",
        help_text="Impact factor indicator value, e.g. '4.7'."
    )

    # ------------------------------------------------------------------
    # Auto-managed timestamps
    # ------------------------------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]   # Newest entries appear first
        verbose_name = "Publication"
        verbose_name_plural = "Publications"

    def __str__(self):
        return f"[{self.year}] {self.title[:80]}"

    def to_dict(self):
        """
        Return a plain Python dict that is safe for JsonResponse serialisation.
        This acts as the canonical serialiser for all API views — no DRF needed.
        """
        return {
            "id":        self.pk,
            "authors":   self.authors,
            "title":     self.title,
            "journal":   self.journal,
            "year":      self.year,
            "link":      self.link,
            "publisher": self.publisher,
            "impact":    self.impact,
        }
