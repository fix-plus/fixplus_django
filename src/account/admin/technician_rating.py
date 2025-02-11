from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin, TabularInline

from src.account.models import TechnicianRating, TechnicianRatingValue


class TechnicianRatingValueInline(TabularInline):
    model = TechnicianRatingValue
    extra = 1


@admin.register(TechnicianRating)
class TechnicianRatingAdmin(ModelAdmin):
    list_display = [
        "mobile",
        "full_name",
        "created_at",
    ]
    list_select_related = ["user"]
    list_filter_submit = True
    list_filter = [
        ("user__mobile", FieldTextFilter),
        ("user__profile__national_code", FieldTextFilter),
        ("user__profile__full_name", FieldTextFilter),
    ]
    inlines = [TechnicianRatingValueInline]

    def mobile(self, obj):
        return obj.user.mobile

    def full_name(self, obj):
        return obj.user.profile.full_name