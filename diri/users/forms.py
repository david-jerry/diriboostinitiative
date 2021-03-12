from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


User = get_user_model()

from diri.users.models import Entrepreneurs
from django import forms


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class BioForm(forms.ModelForm):
    class Meta:
        model = Entrepreneurs
        fields = [
            "first_name",
            "mid_name",
            "last_name",
            "state",
            "lga",
            "bank_name",
            "bvn",
            "acc_no",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "sm-form-control border-form-control"

    def clean_bvn(self):
        bvn = self.cleaned_data['bvn']
        if Entrepreneurs.objects.filter(bvn=bvn).exists():
            raise forms.ValidationError("You have already applied")
        return bvn

    def clean_acc_no(self):
        acc_no = self.cleaned_data['acc_no']
        if Entrepreneurs.objects.filter(acc_no=acc_no).exists():
            raise forms.ValidationError("You have already applied")
        return acc_no

class StatementForm(forms.ModelForm):
    class Meta:
        model = Entrepreneurs
        fields = [
            "st_o_acc",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "sm-form-control border-form-control"

    def clean_st_o_acc(self):
        sto = self.cleaned_data['st_o_acc']
        if sto is None:
            raise forms.ValidationError("You have to upload a document here")
        return sto


class ValidateForm(forms.ModelForm):
    class Meta:
        model = Entrepreneurs
        fields = [
            "email",
            "phone",
            "amount",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs["readonly"] = True
        self.fields['amount'].widget.attrs["disabled"] = True
        for field in self.fields.values():
            field.widget.attrs["class"] = "disabled sm-form-control border-form-control"
            

    def clean_email(self):
        email = self.cleaned_data['email']
        if Entrepreneurs.objects.filter(email=email).exists():
            raise forms.ValidationError("You have already applied")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Entrepreneurs.objects.filter(phone=phone).exists():
            raise forms.ValidationError("You have already applied")
        return phone

    def clean_acc_val(self):
        amount = self.cleaned_data['amount']
        if amount is None:
            raise forms.ValidationError("This is a mandatory one time fee")
        return amount