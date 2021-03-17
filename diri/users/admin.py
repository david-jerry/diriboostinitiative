import csv
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Entrepreneurs
from diri.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected models as CSV format"


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(Entrepreneurs)
class EntrepreneursAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = [
        "amount",
        "first_name",
        "mid_name",
        "last_name",
        "email",
        "phone",
        "state",
        "lga",
        "bvn",
        "bank_name",
        "acc_no",
        "st_o_acc",
    ]
    list_editable = [
        "first_name",
        "mid_name",
        "last_name",
        "email",
        "phone",
        "state",
        "lga",
        "bvn",
        "bank_name",
        "acc_no",
        "st_o_acc",
    ]
    actions = ["export_as_csv"]
