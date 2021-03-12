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
    # amount = DecimalField(_("Cost"), default=1000.00, null=True)
    # entre = OneToOneField(User, on_delete=SET_NULL, null=True, blank=True)
    first_name = CharField(_("First Name"), max_length=255, null=True, blank=False)
    mid_name = CharField(_("Middle Name"), max_length=255, null=True, blank=False)
    last_name = CharField(_("Last Name"), max_length=255, null=True, blank=False)
    email = EmailField(_("Email"), unique=True, null=True, blank=False)
    phone = CharField(_("Phone Number"), max_length=12, null=True, blank=False)
    state = CharField(_("State of Origin"), max_length=255, null=True, blank=False, default="Bayelsa")
    lga = CharField(_("Local Government Area (LGA)"), max_length=255, null=True, blank=False,)
    bvn = CharField(_("Bank Verification Number (BVN)"), max_length=255, null=True, blank=False,)
    bank_name = CharField(_("Bank Name"), max_length=255, null=True, blank=False,)
    acc_no = CharField(_("Account Number (NUBAN)"), max_length=255, null=True, blank=False,)
    st_o_acc = ImageField(_("Statement of Account"), upload_to=bank_file_path, storage=PrivateRootS3BOTO3Storage(), null=True, blank=False, help_text="upload only clear image file")
    acc_val = ImageField(_("Validate Statement"), upload_to=verify_file_path, storage=PrivateRootS3BOTO3Storage(), null=True, blank=False, help_text="upload only clear image file")
    status = StatusField(default="pending")

    def __str__(self):
        return f"{self.first_name} {self.mid_name}[0:1] {self.last_name}"

    class Meta:
        managed = True
        verbose_name = 'Entrepreneur'
        verbose_name_plural = 'Entrepreneurs'
        ordering = ['-created']

