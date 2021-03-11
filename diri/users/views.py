from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, ListView
from django.views.generic.edit import CreateView
from diri.users.models import Entrepreneurs
from diri.users.forms import ValidateForm, BioForm, StatementForm
from formtools.wizard.views import SessionWizardView
from django.contrib import messages
from django.shortcuts import render
from django.core.files.storage import DefaultStorage

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class ApplyNow(SessionWizardView, LoginRequiredMixin, SuccessMessageMixin):
    model = Entrepreneurs
    template_name = "pages/home.html"
    form_list = [BioForm, StatementForm, ValidateForm]
    file_storage = DefaultStorage()
    success_url = reverse_lazy("home")
    success_message = _("Your application has been submitted successfully")
    def get(self, request, *args, **kwargs):
        try:
            return self.render(self.get_form())
        except KeyError:
            return super().get(request, *args, **kwargs)

    def done(self, form_list, *args, **kwargs):
        request = self.request
        return render(
            request,
            "pages/home.html",
            {
                "form_data": [form.cleaned_data for form in form_list],
            },
        )


apply_now = ApplyNow.as_view()
