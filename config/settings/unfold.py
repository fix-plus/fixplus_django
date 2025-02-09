from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_SYMBOL": "build_circle",
    "SHOW_LANGUAGES": True,
    "BORDER_RADIUS": "8px",
    "COLORS": {
        "base": {
            "50": "245 247 250",
            "100": "230 232 235",
            "200": "210 213 218",
            "300": "185 188 192",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18"
        },
        "primary": {
            "50": "240 248 255",
            "100": "224 242 254",
            "200": "186 230 253",
            "300": "125 211 252",
            "400": "56 189 248",
            "500": "14 165 233",
            "600": "2 132 199",
            "700": "3 105 161",
            "800": "4 70 107",
            "900": "2 49 73",
            "950": "0 30 60"
        }
    },
    "SIDEBAR": {
            "show_search": False,  # Search in applications and models names
            "show_all_applications": True,  # Dropdown with all applications and models
            "navigation": [
                {
                    "title": _("Users"),
                    "separator": True,  # Top border
                    "collapsible": True,  # Collapsible group of links
                    "items": [
                        {
                            "title": _("Groups"),
                            "icon": "diversity_2",
                            "link": reverse_lazy("admin:auth_group_changelist"),
                        },
                        {
                            "title": _("Users"),
                            "icon": "people",
                            "link": reverse_lazy("admin:authentication_user_changelist"),
                        },
                        {
                            "title": _("Profiles"),
                            "icon": "badge",
                            "link": reverse_lazy("admin:account_profile_changelist"),
                        },
                        {
                            "title": _("Contact Numbers"),
                            "icon": "phone_in_talk",
                            "link": reverse_lazy("admin:account_usercontactnumber_changelist"),
                        },
                        {
                            "title": _("Registration Requests"),
                            "icon": "how_to_reg",
                            "link": reverse_lazy("admin:account_userregistryrequest_changelist"),
                        },
                        {
                            "title": _("Technician Skills"),
                            "icon": "lightbulb",
                            "link": reverse_lazy("admin:account_technicianskill_changelist"),
                        },
                        {
                            "title": _("Technician Service Cards"),
                            "icon": "style",
                            "link": reverse_lazy("admin:account_technicianservicecard_changelist"),
                        },
                    ],
                },
                {
                    "title": _("Medias"),
                    "separator": True,  # Top border
                    "collapsible": True,  # Collapsible group of links
                    "items": [
                        {
                            "title": _("Services Card"),
                            "icon": "image",
                            "link": reverse_lazy("admin:media_uploadservicecardmedia_changelist"),
                        },
                    ],
                },
            ],
        },
}