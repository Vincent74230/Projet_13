from django.shortcuts import render, redirect
from .models import Category, User
from .forms import CreateUserForm, ModifyUserProfile, ChangePassword
from django.views.generic import View, UpdateView
from application.departements_list import DEPARTEMENTS as departements
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import force_text
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


class Index(View):
    form_class = CreateUserForm
    template_name = 'useraccount/index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form,})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()
            current_site = get_current_site(request)
            msg_html = render_to_string('useraccount/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(
                "Bonjour {}, c'est PeopleSkills".format(user.username),
                "Ceci est un message de PeopleSkills",
                "vincent.nowak@hotmail.fr",
                [user.email],
                html_message=msg_html,
            )
            messages.success(request, ('Activez votre compte en cliquant sur le lien envoyé dans votre boite mail'))

            return redirect(reverse('useraccount:login'))

        return render(request, self.template_name, {'form': form})

def login_page(request):
    """Login page, checks username and password"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request, username=username, password=password
        )  # check if user is in DB
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(
                request, "Votre nom d'utilisateur ou mot de passe est incorrect"
            )

    return render(request, "useraccount/login.html", {})

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Votre compte a été confirmé.'))
            return redirect('/')
        else:
            messages.warning(request, ('Lien de confirmation invalide, peut-être a-t-il déjà été utilisé.'))
            return redirect('/')

@login_required
def log_out(request):
    """Logout function, login required"""
    logout(request)
    return redirect("/")


@login_required
def my_account(request):
    """Manages user profile"""
    choice = request.GET.get("choice")
    form = ModifyUserProfile(instance=request.user)

    if choice == 'mon_profil':
        if request.method == 'POST':
            form = ModifyUserProfile(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, ('Votre profil a bien été modifié'))
                return render(request, 'useraccount/myaccount.html', {'choice':choice, 'form':form})
        return render(request, 'useraccount/myaccount.html', {'choice':choice, 'form':form})

    if choice == 'mes_identifiants':
        if request.method == 'POST':
            form = ChangePassword(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, ('Votre mot de passe a bien été modifié'))
                return render(request, 'useraccount/myaccount.html', {'choice':choice, 'form':form})
        form = ChangePassword(user=request.user)
        return render(request, 'useraccount/myaccount.html', {'choice':choice, 'form':form})
    if choice == 'mes_services':
        return render(request, 'useraccount/myaccount.html', {'choice':choice})
    if choice == 'mes_avis':
        return render(request, 'useraccount/myaccount.html', {'choice':choice})

    return render(request, "useraccount/myaccount.html", {'choice':'mon_profil', 'form':form})
