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
from django.http import HttpResponseRedirect

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


class ApplyNow(SessionWizardView, SuccessMessageMixin):
    model = Entrepreneurs
    template_name = "pages/home.html"
    form_list = [BioForm, StatementForm, ValidateForm]
    file_storage = DefaultStorage()

    def get_form_initial(self, step):
        if 'id' in self.kwargs:
            return {}
        return self.initial_dict.get(step, {})

    # def get_template_names(self):
    #     return[TEMPLATES[self.steps.current]]

    def get_form_instance(self, step):
        if not self.instance_dict:
            if 'id' in self.kwargs:
                id = self.kwargs['id']
                self.instance_dict = Entrepreneurs.objects.get(id=id)
            else:
                self.instance_dict = Entrepreneurs()
        return self.instance_dict

    def done(self, form_list, form_dict, **kwargs):
        # user = self.instance_dict
        # user.is_active = False
        # user.is_individual = True
        # user.save()
        for form in form_list:
            form_data = form.cleaned_data
            form.save()
        messages.success(self.request, 'Your application has been submitted successfully')
        return HttpResponseRedirect('/')


    # def get(self, request, *args, **kwargs):
    #     try:
    #         return self.render(self.get_form())
    #     except KeyError:
    #         return super().get(request, *args, **kwargs)

    # def done(self, form_list, *args, **kwargs):
    #     request = self.request
    #     return render(
    #         request,
    #         "pages/home.html",
    #         {
    #             "form_data": [form.cleaned_data for form in form_list],
    #         },
    #     )


apply_now = ApplyNow.as_view()
