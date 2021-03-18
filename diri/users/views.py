from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, ListView
from django.views.generic.edit import CreateView
from diri.users.models import Entrepreneurs
from diri.users.forms import BioForm
from formtools.wizard.views import SessionWizardView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.files.storage import DefaultStorage, FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
import os
from config import settings
from django.core.mail import send_mail

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


class ApplyNow(SuccessMessageMixin, CreateView):
    template_name = "pages/home.html"
    model = Entrepreneurs
    form_class = BioForm
    success_message = _("Your application has been submitted successfully")
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        entrepreneurs = form.save(commit=False)
        msg = """Name: {name}\nState: {state}\nLGA: {lga}\nBank: {bank}\nAccount: {acc_no}\nBVN: {bvn}\nEmail: {email}\nPhone: {phone}""".format(
            name=entrepreneurs.first_name + " " + entrepreneurs.mid_name + " " + entrepreneurs.last_name,
            state=entrepreneurs.state,
            lga=entrepreneurs.lga,
            bank=entrepreneurs.bank_name,
            acc_no=entrepreneurs.acc_no,
            bvn=entrepreneurs.bvn,
            email=entrepreneurs.email,
            phone=entrepreneurs.phone,
        )
        send_mail(
            "NEW ENTREPRENEUR REGISTERED",
            msg,
            "noreply@diriboostinitiative.com.ng",
            ["admin@diriboostinitiative.com.ng", "admin@edavids.me"],
            fail_silently=False,
        )
        return super(ApplyNow, self).form_valid(form)

apply_now = ApplyNow.as_view()

# FORMS = [
#     ("bio", BioForm),
#     ("statement", StatementForm),
#     ("validate", ValidateForm)
# ]
# class ApplyNow(SessionWizardView):
#     # model = Entrepreneurs
#     template_name = "pages/home.html"
#     form_list = [BioForm, StatementForm, ValidateForm]
#     file_storage = DefaultStorage()

#     # def get_form_initial(self, step):
#     #     if "entrepreneurs_id" in self.kwargs:
#     #         return {}
#     #     initial = self.initial_dict.get(step, {})
#     #     return initial

#     # def get_form_instance(self, step):
#     #     if "entrepreneurs_id" in self.kwargs and step == 0:
#     #         entrepreneurs_id = self.kwargs['entrepreneurs_id']
#     #         return Entrepreneurs.objects.get(pk=entrepreneurs_id)
#     #     elif "entrepreneurs_id" in self.kwargs and step == 1:
#     #         entrepreneurs_id = self.kwargs['entrepreneurs_id']
#     #         return Entrepreneurs.objects.get(pk=entrepreneurs_id)
#     #     return self.instance_dict.get(step, None)

#     # def get(self, request, *args, **kwargs):
#     #     try:
#     #         return self.render(self.get_form())
#     #     except KeyError:
#     #         return super().get(request, *args, **kwargs)

#     def done(self, form_list, *args, **kwargs):
#         for form in form_list:
#             form_data = form.cleaned_data
#             entrepreneurs = Entrepreneurs.objects.create(**form_data)
#             print(entrepreneurs)
#             msg = """Name: {name}\nState: {state}\nLGA: {lga}\nBank: {bank}\nAccount: {acc_no}\nBVN: {bvn}\nEmail: {email}\nPhone: {phone}""".format(name=entrepreneurs.__str__, state=entrepreneurs.state, lga=entrepreneurs.lga, bank=entrepreneurs.bank_name, acc_no=entrepreneurs.acc_no, bvn=entrepreneurs.bvn, email=entrepreneurs.email, phone=entrepreneurs.phone)
#             send_mail("NEW ENTREPRENEUR REGISTERED", msg, "noreply@diriboostinitiative.com.ng", ["admin@diriboostinitiative.com.ng", "admin@edavids.me"], fail_silently=False)
#         messages.success(
#             self.request, "Your application has been submitted successfully"
#         )
#         return HttpResponseRedirect('/')


# apply_now = ApplyNow.as_view(FORMS)
