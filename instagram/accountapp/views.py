from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponsePermanentRedirect
import random
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from .models import UserProfile, SaveSession
import json
from django.views.decorators.csrf import csrf_exempt
from .forms import SearchForm, EditProfile1, EditProfile2, RegistrationForm, ConfirmReg, PasswordEdit
from django.contrib.auth.signals import user_logged_in
# from django.contrib.gis.utils import GeoIp
from rest_framework import viewsets
# Create your views here.


confirm_email = 0
new_user = ''
to_raise = ''
userProfile = False
reset_user = ''

def user_logged_in_handler(sender, request, user, **kwargs):
    try:
        to_save = SaveSession.objects.get(user=user, session_id=request.session.session_key)
        to_save.device_browser = request.user_agent.browser.family #to automatically update the logout date
    except:
        to_save = SaveSession(user=user, session_id=request.session.session_key)
        to_save.device_family = f'{request.user_agent.os.family} {request.user_agent.os.version}'
        to_save.device_browser = request.user_agent.browser.family
        # loc = GeoIp()
        ip = request.META.get('REMOTE_ADDR', None)
        if ip:
            # city = loc.city(ip)['city']
            pass
        else:
            city = 'Ife'
        to_save.save()
user_logged_in.connect(user_logged_in_handler)

@login_required
def homePage(request):
    friends_lists = ['Jerry', 'Obaloluwa', 'Ifeoluwa', 'Abayomi']
    # form = SearchForm()
    return render(request, 'base.html', {'friends_lists': friends_lists, 'v': 10})

@login_required
def myProfile(request, username):
    pass_code = 0
    if username == '__obaloluwa_':
        pass_code = 1
        pass
    else:
        pass
    return render(request, 'accounts/profile/profile.html', {'username': pass_code})

@login_required
def search(request):
    if request.POST and request.is_ajax:
        s_form = SearchForm(request.POST)
        if s_form.is_valid():
            cd = s_form.cleaned_data
            return JsonResponse({'success': True, 'information': cd['search_value']})
    return HttpResponse('your form result')

@login_required
def editProfile(request, val):
    global userProfile
    if val == '1':
        user = User.objects.get(username=request.user.username)
        form1 = EditProfile1(initial={'first_name': user.first_name, 'username': request.user.username, 'email': user.email})
        try:
            user2 = UserProfile.objects.get(user_id=user.id)
            form2 = EditProfile2(initial={'phone': user2.phone, 'gender': user2.gender, 'bio': user2.bio, 'website': user2.website})
            userProfile = True
        except:
            form2 = EditProfile2()
        to_temp = {'form1': form1, 'form2': form2, 'username': '__Obab', 'toActive': val}
        return render(request, 'accounts/profile/settingsEdit.html', to_temp)
    elif val == '2':
        my_id = User.objects.get(username=request.user.username)
        if request.POST and request.is_ajax:
            form1 = EditProfile1(request.POST)
            form2 = EditProfile2(request.POST)
            form1.full_clean()
            form2.full_clean()
            cd1 = form1.cleaned_data
            my_id.first_name = cd1['first_name']
            try:
                my_id.username = cd1['username']
            except: pass
            my_id.email = cd1['email']
            my_id.save()
            if userProfile:
                cd2 = form2.cleaned_data
                my_id.id.userprofile.website = cd2['website']
                my_id.id.userprofile.phone = cd2['phone']
                my_id.id.userprofile.gender = cd2['gender']
                my_id.id.userprofile.bio = cd2['bio']
                my_id.id.userprofile.profile_pics = cd2['profile_pics']
                my_id.id.userprofile.save()
            else:
                cd2 = form2.save(commit=False)
                cd2.user_id = my_id
                cd2.save()
            return JsonResponse({'ll': 'll'})
    elif val == '3':
        my_id = User.objects.get(username=request.user.username)
        my_sessions = SaveSession.objects.filter(user=my_id).values_list()
        print(my_sessions)
        to_temp = {'toActive': val, 'mySessions': my_sessions, }
        return render(request, 'accounts/profile/login_activity.html', to_temp)

def userRegister(request):
    global confirm_email, new_user
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            confirm_email = random.randrange(1000, 9999)
            send_mail(
                'Confirm Password', f'<b>confirmation code: {confirm_email}</b>', 'admin@social.com', [form.cleaned_data['email']],
            )
            return HttpResponsePermanentRedirect(reverse('confirm_reg'))
    else:
        form = RegistrationForm()
    return render(request, 'registration/registerUser.html', {'r_form': form})

def userRegConfirm(request):
    global confirm_email, to_raise
    if request.POST:
        form = ConfirmReg(request.POST)
        if form.is_valid():
            cd = form.cleaned_data['confirm_code']
            if cd == str(confirm_email):
                new_user.save()
                return HttpResponsePermanentRedirect(reverse('login'))
            else:
                request.method = 'GET'
                to_raise = 1
                return HttpResponsePermanentRedirect(reverse('confirm_reg'))
    else:
        form = ConfirmReg()
        to_temp = {'conf_form': form, 'to_raise': to_raise}
        to_raise = 0
    return render(request, 'registration/conf_account.html', to_temp)

def toReset(request):
    if request.POST:
        form = PasswordEdit(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_forgot = User.objects.filter(email=cd['email'], username=cd['username'])
            if user_forgot.exists():
                for user in user_forgot:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Social App',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@social.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return HttpResponsePermanentRedirect(reverse("password_reset_done"))
            else:
                return HttpResponse('user does not exist')
    else:
        form = PasswordEdit()
    return render(request, 'registration/password_reset_form.html', {'form': form})