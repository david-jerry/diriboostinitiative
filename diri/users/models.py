import random
import os
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models import (
    BooleanField,
    CharField,
    TextField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    FileField,
    ForeignKey,
    ManyToManyField,
    ImageField,
    IntegerField,
    OneToOneField,
    Q,
    SlugField,
    CASCADE,
    SET_NULL,
    URLField,
)

from model_utils.models import TimeStampedModel
from model_utils.fields import StatusField
from model_utils import Choices
from .validators import validate_file_extension
from diri.utils.storages import PrivateRootS3BOTO3Storage

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def bank_file_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "documents/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

def verify_file_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "verify/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class User(AbstractUser):
    """Default user for diri."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Entrepreneurs(TimeStampedModel):
    STATUS = Choices("pending", "approved", "rejected")
    BANKS = (
       ('', _('SELECT BANK')),
       ('ACCESS BANK PLC', _('ACCESS BANK PLC')),
       ('CITIBANK NIG. PLC', _('CITIBANK NIG. PLC')),
       ('ECOBANK NIG. PLC', _('ECOBANK NIG. PLC')),
       ('FIDELITY BANK PLC', _('FIDELITY BANK PLC')),
       ('FIRST BANK NIG. LTD', _('FIRST BANK NIG. LTD')),
       ('FIRST CITY MONUMENT BANK PLC', _('FIRST CITY MONUMENT BANK PLC')),
       ('GLOBUS BANK LTD', _('GLOBUS BANK LTD')),
       ('GUARANTY TRUST BANK PLC', _('GUARANTY TRUST BANK PLC')),
       ('HERITAGE BANKING COMPANY LTD', _('HERITAGE BANKING COMPANY LTD')),
       ('KEYSTONE BANK', _('KEYSTONE BANK')),
       ('POLARIS BANK', _('POLARIS BANK')),
       ('PROVIDUS BANK', _('PROVIDUS BANK')),
       ('STANBIC IBTC BANK LTD', _('STANBIC IBTC BANK LTD')),
       ('STANDARD CHARTERED BANK NIG. LTD', _('STANDARD CHARTERED BANK NIG. LTD')),
       ('STERLING BANK PLC', _('STERLING BANK PLC')),
       ('SUNTRUST BANK NIG. PLC', _('SUNTRUST BANK NIG. PLC')),
       ('TITAN TRUST BANK LTD', _('TITAN TRUST BANK LTD')),
       ('UNION BANK OF NIG. PLC', _('UNION BANK OF NIG. PLC')),
       ('UNITED BANK FOR AFRICA PLC', _('UNITED BANK FOR AFRICA PLC')),
       ('UNITY BANK PLC', _('UNITY BANK PLC')),
       ('WEMA BANK PLC', _('WEMA BANK PLC')),
       ('ZENITH BANK PLC', _('ZENITH BANK PLC')),
    )
    STATES = (
            ("Abia", "Abia"),
            ("Adamawa","Adamawa"),
            ("Akwa Ibom","Akwa Ibom"),
            ("Anambra","Anambra"),
            ("Bauchi","Bauchi"),
            ("Bayelsa","Bayelsa"),
            ("Benue",    "Benue"),
            ("Borno",    "Borno"),
            ("Cross River",    "Cross River"),
            ("Delta",    "Delta"),
            ("Ebonyi",    "Ebonyi"),
            ("Edo",    "Edo"),
            ("Ekiti",    "Ekiti"),
            ("Enugu",    "Enugu"),
            ("FCT - Abuja",    "FCT - Abuja"),
            ("Gombe",    "Gombe"),
            ("Imo",    "Imo"),
            ("Jigawa",    "Jigawa"),
            ("Kaduna",    "Kaduna"),
            ("Kano",    "Kano"),
            ("Katsina",    "Katsina"),
            ("Kebbi",    "Kebbi"),
            ("Kogi",    "Kogi"),
            ("Kwara",    "Kwara"),
            ("Lagos",    "Lagos"),
            ("Nasarawa",    "Nasarawa"),
            ("Niger",    "Niger"),
            ("Ogun",    "Ogun"),
            ("Ondo",    "Ondo"),
            ("Osun",    "Osun"),
            ("Oyo",    "Oyo"),
            ("Plateau",    "Plateau"),
            ("Rivers",    "Rivers"),
            ("Sokoto",    "Sokoto"),
            ("Taraba",    "Taraba"),
            ("Yobe",    "Yobe"),
            ("Zamfara",    "Zamfara"),
    )
    amount = CharField(_("Statement Validation Fee"), default="1000.00", max_length=7, null=True, blank=True, help_text="This is a compulsory one time payment from all applicants, charged for their bank statement verification.")
    first_name = CharField(_("First Name"), max_length=255, null=True, blank=False)
    mid_name = CharField(_("Middle Name"), max_length=255, null=True, blank=False)
    last_name = CharField(_("Last Name"), max_length=255, null=True, blank=False)
    email = EmailField(_("Email Address"), unique=True, null=True, blank=False)
    phone = CharField(_("Phone Number"), max_length=12, null=True, blank=False)
    state = CharField(_("State of Origin"), choices=STATES, default="Bayelsa", max_length=255, null=True, blank=False)
    lga = CharField(_("Local Government Area (LGA)"), max_length=255, null=True, blank=True,)
    bvn = CharField(_("Bank Verification Number (BVN)"), max_length=255, null=True, blank=True,)
    bank_name = CharField(_("Bank Name"), max_length=255, choices=BANKS, null=True, blank=True,)
    acc_no = CharField(_("Account Number (NUBAN)"), max_length=255, null=True, blank=True,)
    st_o_acc = FileField(_("Statement of Account"), upload_to=bank_file_path, null=True, blank=True, validators=[validate_file_extension], help_text="upload your account statement for verification")
    status = StatusField(default="pending")

    def __str__(self):
        return f"{self.first_name} {self.mid_name} {self.last_name}"

    class Meta:
        managed = True
        verbose_name = 'Entrepreneur'
        verbose_name_plural = 'Entrepreneurs'
        ordering = ['-created']

