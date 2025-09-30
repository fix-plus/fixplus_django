from django.db import models

from src.common.models import BaseModel


class Brand(BaseModel):
    title = models.CharField(max_length=100, null=False)
    fa_title = models.CharField(max_length=100, null=False)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    # Invoice template fields (fixed per brand)
    header_image = models.ImageField(upload_to='brands/headers/', blank=True, null=True)  # Header image for invoice
    footer_image = models.ImageField(upload_to='brands/footers/', blank=True, null=True)  # Footer image for invoice
    logo_image = models.ImageField(upload_to='brands/logos/', blank=True, null=True)  # Logo image for invoice
    stamp_image = models.ImageField(upload_to='brands/stamps/', blank=True, null=True)  # Stamp image for invoice
    repair_address = models.TextField(blank=True)  # Repair agency address
    phone_numbers = models.TextField(blank=True)  # Agency phone numbers (comma-separated)
    right_text1 = models.CharField(max_length=255, blank=True)  # Right top text 1 (e.g., company name)
    right_text2 = models.CharField(max_length=255, blank=True)  # Right top text 2 (e.g., service center)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title}-{self.fa_title}"