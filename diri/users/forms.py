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
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="col-md-12 mb-4"),
                Column("mid_name", css_class="col-md-12 mb-4"),
                Column("last_name", css_class="col-md-12 mb-4"),
                Column("state", css_class="col-md-6 mb-4"),
                Column("lga", css_class="col-md-6 mb-4"),
                Column("bank_name", css_class="col-md-12 mb-4"),
                Column("bvn", css_class="col-md-6 mb-4"),
                Column("acc_no", css_class="col-md-6 mb-4"),
                css_class="row form-section mb-4",
            ),
            Submit(
                "submit",
                "Submit ",
                css_class="button button-border button-circle font-weight-medium ml-0 topmargin-sm",
            ),
        )

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
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("st_o_acc", css_class="col-md-12 mb-4"),
                css_class="row form-section mb-4",
            ),
            Submit(
                "submit",
                "Submit ",
                css_class="button button-border button-circle font-weight-medium ml-0 topmargin-sm",
            ),
        )

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
            
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("email", css_class="col-md-6 mb-4"),
                Column("phone", css_class="col-md-6 mb-4"),
                Column("amount", css_class="col-md-12 mb-4"),
                css_class="row form-section mb-4",
            ),
            # Submit(
            #     "submit",
            #     "Submit ",
            #     css_class="button button-border button-circle font-weight-medium ml-0 topmargin-sm",
            # ),
        )

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