from django.shortcuts import render, redirect
from .models import Category, User, Services, Rating
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
from .services import SERVICES_DICT as services_dict
from .score_extend import ScoreRegistration


class Index(View):
    form_class = CreateUserForm
    template_name = "useraccount/index.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()
            current_site = get_current_site(request)
            msg_html = render_to_string(
                "useraccount/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            send_mail(
                "Bonjour {}, c'est PeopleSkills".format(user.username),
                "Ceci est un message de PeopleSkills",
                "vincent.nowak@hotmail.fr",
                [user.email],
                html_message=msg_html,
            )
            messages.success(
                request,
                (
                    "Activez votre compte en cliquant sur le lien envoyé dans votre boite mail"
                ),
            )

            return redirect(reverse("useraccount:login"))

        return render(request, self.template_name, {"form": form})


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
            messages.success(request, ("Votre compte a été confirmé."))
            return redirect("/")
        else:
            messages.warning(
                request,
                ("Lien de confirmation invalide, peut-être a-t-il déjà été utilisé."),
            )
            return redirect("/")


@login_required
def log_out(request):
    """Logout function, login required"""
    logout(request)
    return redirect("/")


@login_required
def my_account(request):
    """Manages user profile : profile, my identifiers, my scores, """
    choice = request.GET.get("choice")
    form = ModifyUserProfile(instance=request.user)

    if choice == "mon_profil":
        if request.method == "POST":
            form = ModifyUserProfile(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, ("Votre profil a bien été modifié"))
                return render(
                    request,
                    "useraccount/myaccount.html",
                    {"choice": choice, "form": form},
                )
        return render(
            request, "useraccount/myaccount.html", {"choice": choice, "form": form}
        )

    if choice == "mes_identifiants":
        if request.method == "POST":
            form = ChangePassword(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, ("Votre mot de passe a bien été modifié"))
                return render(
                    request,
                    "useraccount/myaccount.html",
                    {"choice": choice, "form": form},
                )
        form = ChangePassword(user=request.user)
        return render(
            request, "useraccount/myaccount.html", {"choice": choice, "form": form}
        )
    if choice == "mes_services":
        user = User.objects.get(username=request.user.username)

        # Making simple list of all services
        services_list = []
        for category, services in services_dict.items():
            for service in services:
                services_list.append(service)

        # Making list of all users required services
        user_required_services_name = []
        for element in user.required_services.all():
            user_required_services_name.append(element.name)

        # Making list of all proposed services
        user_proposed_services_name = []
        for element in user.proposed_services.all():
            user_proposed_services_name.append(element.name)

        if request.method == "POST":
            # Grabing required services checked by user
            checkboxes_required_services = request.POST.getlist("required")
            if checkboxes_required_services:
                for service in services_list:
                    if service in checkboxes_required_services:
                        service_query = Services.objects.get(name=service)
                        user.required_services.add(service_query)
                    else:
                        service_query = Services.objects.get(name=service)
                        user.required_services.remove(service_query)
            else:
                user_required_services = user.required_services.all()
                if user_required_services:
                    for required_service in user_required_services:
                        service_query = Services.objects.get(name=required_service)
                        user.required_services.remove(service_query)
                else:
                    pass

            # Grabing proposed services checked by user from frontend
            checkboxes_proposed_services = request.POST.getlist("proposed")
            if checkboxes_proposed_services:
                for service in services_list:
                    if service in checkboxes_proposed_services:
                        service_query = Services.objects.get(name=service)
                        user.proposed_services.add(service_query)
                    else:
                        service_query = Services.objects.get(name=service)
                        user.proposed_services.remove(service_query)
            else:
                user_proposed_services = user.proposed_services.all()
                if user_proposed_services:
                    for proposed_service in user_proposed_services:
                        service_query = Services.objects.get(name=proposed_service)
                        user.proposed_services.remove(service_query)
                else:
                    pass

            user_required_services_name = []
            for element in user.required_services.all():
                user_required_services_name.append(element.name)

            user_proposed_services_name = []
            for element in user.proposed_services.all():
                user_proposed_services_name.append(element.name)

        context = {
            "choice": choice,
            "user_required_services_name": user_required_services_name,
            "user_proposed_services_name": user_proposed_services_name,
            "services_dict": services_dict,
        }
        return render(request, "useraccount/myaccount.html", context)
    if choice == "mes_avis":
        # Fetching score received by current user
        score_received = Rating.objects.filter(receiver_id=request.user.pk)

        # Fetching score sent by current user
        score_sent = Rating.objects.filter(sender_id=request.user.pk)

        scores_dict_list = []
        if score_received:
            for notation in score_received:
                dico = {}
                if notation.score_pending:
                    dico["score_status"] = "pending"
                    dico["role"] = "receiver"
                    dico["sender"] = User.objects.get(id=notation.sender_id).username
                    scores_dict_list.append(dico)
                else:
                    dico["score_status"] = "completed"
                    dico["role"] = "receiver"
                    dico["sender"] = User.objects.get(id=notation.sender_id).username
                    dico["score_sent"] = notation.score_sent
                    dico["score_received"] = notation.score_received
                    scores_dict_list.append(dico)

        if score_sent:
            for notation in score_sent:
                dico = {}
                if notation.score_pending:
                    dico["score_status"] = "pending"
                    dico["role"] = "sender"
                    dico["receiver"] = User.objects.get(
                        id=notation.receiver_id
                    ).username
                    scores_dict_list.append(dico)
                else:
                    dico["score_status"] = "completed"
                    dico["role"] = "sender"
                    dico["receiver"] = User.objects.get(
                        id=notation.receiver_id
                    ).username
                    dico["score_sent"] = notation.score_sent
                    dico["score_received"] = notation.score_received
                    scores_dict_list.append(dico)

        context = {"choice": choice, "scores_dict_list": scores_dict_list}

        return render(request, "useraccount/myaccount.html", context)

    return render(
        request, "useraccount/myaccount.html", {"choice": "mon_profil", "form": form}
    )


@login_required
def score(request):
    """Manages score system between two registered members"""
    receiver_username = request.GET.get("receiver")
    receiver = User.objects.get(username=receiver_username)
    if request.method == "POST":
        sender_rating_choice = request.POST.get("rating_value")
        registration = ScoreRegistration(
            receiver_username, sender_rating_choice, request.user
        )
        registration.score_status_verification()
        if (
            registration.score_status
            == "Vous avez déjà noté cette personne, elle doit maintenant vous noter en retour"
        ):
            messages.info(
                request,
                (
                    "Vous avez déjà noté cette personne, elle doit maintenant vous noter en retour"
                ),
            )
        if (
            registration.score_status
            == "Vous avez noté cette personne, elle a répondu, notation complète"
        ):
            messages.info(
                request,
                ("Vous avez noté cette personne, elle a répondu, notation complète"),
            )
        if (
            registration.score_status
            == "Cette personne vous a déjà noté, nous enregistrons votre note envers elle"
        ):
            messages.info(
                request,
                (
                    "Cette personne vous a déjà noté, nous enregistrons votre note envers elle"
                ),
            )
            note = Rating.objects.filter(sender_id=receiver)
            note = note[0]
            note.score_received = int(sender_rating_choice)
            note.score_pending = False
            note.save()
        if (
            registration.score_status
            == "Cette personne vous a noté, vous avez déjà répondu, notation complète"
        ):
            messages.info(
                request,
                (
                    "Cette personne vous a noté, vous avez déjà répondu, notation complète"
                ),
            )
        if (
            registration.score_status
            == "Vous êtes le premier à noter cette personne, nous enregistrons votre note"
        ):
            messages.info(
                request,
                (
                    "Vous êtes le premier à noter cette personne, nous enregistrons votre note et la prévenons par mail"
                ),
            )
            note = Rating(
                sender_id=request.user.pk,
                receiver_id=(User.objects.get(username=receiver_username)).pk,
                score_sent=int(sender_rating_choice),
            )
            note.save()
            send_mail(
                "Bonjour {}, c'est PeopleSkills".format(receiver.username),
                "L'utilisateur {} souhaite vous attribuer une note, notez-le en retour.\nRendez-vous sur votre page 'mon compte', onglet 'mes avis'".format(
                    request.user.username
                ),
                "vincent.nowak@hotmail.fr",
                [receiver.email],
            )

    return render(request, "useraccount/score.html", {"receiver": receiver_username})
