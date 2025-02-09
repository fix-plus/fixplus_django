import json
import os
import uuid
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from src.parametric.models import Brand, DeviceType, TimingSetting


# Load default brand name elements from JSON file
brand_json_file_path = os.path.join(os.path.dirname(__file__), 'default_objects', 'brand_names.json')
with open(brand_json_file_path, 'r', encoding='utf-8') as json_file:
    default_brand_elements = json.load(json_file)

# Load default device type elements from JSON file
device_json_file_path = os.path.join(os.path.dirname(__file__), 'default_objects', 'device_types.json')
with open(device_json_file_path, 'r', encoding='utf-8') as json_file:
    default_device_elements = json.load(json_file)


@receiver(post_migrate)
def create_default_parametric_data(sender, app_config, **kwargs):
    if app_config.name == 'src.parametric':  # Replace 'parametric' with your app name
        # Create default BrandNameParametric objects
        if not Brand.objects.exists():
            for element in default_brand_elements:
                Brand.objects.create(
                    title=element["title"],
                    fa_title=element["fa_title"]
                )
        # Create default DeviceTypeParametric objects
        if not DeviceType.objects.exists():
            for element in default_device_elements:
                DeviceType.objects.create(
                    title=element["title"],
                    fa_title=element["fa_title"],
                )

        # Create default TimingSettingParametric objects
        if not TimingSetting.objects.exists():
            TimingSetting.objects.create()
