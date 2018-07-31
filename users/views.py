from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render

from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from .forms import SignUpForm, PhoneVerificationForm
from .models import User

from .models import Alert, Transaction

from .authy_verify import send_sms_verify, check_sms_verify


class IndexView(TemplateView):
    template_name = 'users/index.html'


class SignUpView(SuccessMessageMixin, FormView):
    template_name = 'users/signup_form.html'
    form_class = SignUpForm
    success_url = '/verify'
    success_message = 'The verification code sent to your phone will expire in 4 minutes.'

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        country_code = form.cleaned_data['country_code']
        password = form.cleaned_data['password']
        user = User.objects.create_user(phone_number = phone_number, country_code = country_code, password = password)
        user = authenticate(phone_number=phone_number, password=password)
        user.save()
        self.request.session['phone_number'] = phone_number
        self.request.session['country_code'] = country_code
        
        try:
            # TODO: should probably send this through celery
            response = send_sms_verify(country_code, phone_number)
        except Exception as e:
            messages.add_message(self.request, messages.ERROR,
                                'Verification code not sent. Please sign up again.')
            return redirect('signup')
        
        if response.ok():
            print('user in SignUpView:', user, 'auth?', user.is_authenticated)
            return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.ERROR, response.content['message'])
            return redirect('signup')


class PhoneVerificationView(SuccessMessageMixin, FormView):
    template_name = 'users/phone_verification.html'
    form_class = PhoneVerificationForm

    def form_valid(self, form):
        phone_number = self.request.session['phone_number']
        country_code = self.request.session['country_code']
        verification_code = form.cleaned_data['verification_code']
        try:
            response = check_sms_verify(country_code, phone_number, verification_code)
        except Exception as e:
            messages.add_message(self.request, messages.ERROR,
                                'Verification code error. Please sign up again.')
            return redirect('signup')

        if response.ok():
            user = User.objects.get(phone_number=phone_number)
            login(self.request, user)
            if user.phone_number_verified is False:
                user.phone_number_verified = True
                user.save()
            return redirect('home')
        else:
            messages.add_message(self.request, messages.ERROR, response.content['message'])
            return render(self.request, template_name)


class HomeView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    template_name = 'users/home.html'



'''
class AlertListView(ListView):
    """Shows users a list of alerts"""

    model = Alert


class AlertDetailView(DetailView):
    """Shows users a single alert"""

    model = Alert


class AlertCreateView(SuccessMessageMixin, CreateView):
    """Powers a form to create a new alert"""

    model = Alert
    fields = ['phone_number', 'address']
    success_message = 'Alert successfully created.'
    #success_url = reverse_lazy('list_alert')

class AlertUpdateView(SuccessMessageMixin, UpdateView):
    """Powers a form to edit existing alerts"""

    model = Alert
    fields = ['phone_number', 'address']
    success_message = 'Alert successfully updated.'


class AlertDeleteView(DeleteView):
    """Prompts users to confirm deletion of an alert"""

    model = Alert
    success_url = reverse_lazy('new_alert')



class TransactionListView(ListView):
    """Shows users a list of transactions"""

    model = Transaction


class TransactionDetailView(DetailView):
    """Shows users a single transaction"""

    model = Transaction

'''