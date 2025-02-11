from .profile import ProfileAdmin
from .contact_number import UserContactNumberAdmin
from .registry_request import UserRegistryRequestAdmin
from .skill import TechnicianSkillAdmin
from .service_card import TechnicianServiceCardAdmin
from .technician_rating import TechnicianRatingAdmin
from .technician_status import TechnicianStatusAdmin


__all__ = [
    'ProfileAdmin',
    'UserContactNumberAdmin',
    'UserRegistryRequestAdmin',
    'TechnicianSkillAdmin',
    'TechnicianServiceCardAdmin',
    'TechnicianRatingAdmin',
    'TechnicianStatusAdmin',
]