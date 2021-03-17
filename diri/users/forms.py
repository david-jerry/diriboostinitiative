from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, HTML, Field, Fieldset, Layout, Row, Submit
from crispy_forms.bootstrap import InlineField, UneditableField


User = get_user_model()

from diri.users.models import Entrepreneurs
from django import forms
from crispy_forms import layout


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
            "st_o_acc",
            "email",
            "phone",
            "amount",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for field in self.fields.values():
        #     field.widget.attrs["class"] = "sm-form-control col-12 mb-4"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("""
                <ul id="progressbar" class="center">
                    <li class="active">Personal Details</li>
                    <li>Bank Information</li>
                    <li>Verification Fee</li>
                </ul>
            """),
            Fieldset(
                "Personal Information",
                "first_name",
                "mid_name",
                "last_name",
                "state",
                "lga",
                HTML("""<input type="button" name="next" class="next action-button btn-block button button-border button-circle font-weight-medium ml-0 topmargin-sm" value="Next"/>"""),
            ),
            Fieldset(
                "Bank Information",
                HTML("""<small class="text-info bottommargin-lg">Please attach all relevant supporting document</small>"""),
                "bank_name",
                "bvn",
                "acc_no",
                "st_o_acc",
                HTML("""<input type="button" name="next" class="next action-button btn-block button button-border button-circle font-weight-medium ml-0 topmargin-sm" value="Next"/>"""),
                HTML("""<a href="{% url 'home' %}" class="center action-button-previous btn-block button button-border button-circle font-weight-medium ml-0 topmargin-sm">RESET FORM</a>"""),
            ),
            Fieldset(
                "Verify",
                "email",
                "phone",
                UneditableField("amount", css_class='sm-form-control'),
                HTML("""<input onclick="payWithPaystackOrg()" id="pay" type="submit" name="verify" class="submit action-button btn-block button button-border button-circle font-weight-medium ml-0 topmargin-sm" value="Verify"/>"""),
                HTML("""<a href="{% url 'home' %}" class="center action-button-previous btn-block button button-border button-circle font-weight-medium ml-0 topmargin-sm">RESET FORM</a>"""),
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

    def clean_st_o_acc(self):
        sto = self.cleaned_data['st_o_acc']
        if sto is None:
            raise forms.ValidationError("You have to upload a document here")
        return sto

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


