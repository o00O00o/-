from user.models import User
from user.forms import UserForm, RegisterForm, ChangeForm
from django.shortcuts import render, redirect, reverse


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect(reverse('index'))
                else:
                    message = "Your password is wrong！"
            except:
                message = "The user does not exist！"
        return render(request, 'user/login.html', locals())

    login_form = UserForm()
    return render(request, 'user/login.html', locals())


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:
                message = "You need to enter the same password twice!"
                return render(request, 'user/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:
                    message = 'The same user name exists, please change you username！'
                    return render(request, 'user/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = 'The email account has been used, please change another one!'
                    return render(request, 'user/register.html', locals())

                new_user = User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.save()
                return redirect(reverse('index'))
    register_form = RegisterForm()
    return render(request, 'user/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('index'))
    request.session.flush()
    return redirect(reverse('index'))


def account(request):
    username = request.session['user_name']
    user = User.objects.get(name=username)
    password = user.password
    email = user.email
    user_info = {}
    user_info['password'] = password
    user_info['email'] = email
    return render(request, 'user/account.html', user_info)


def change(request):
    if request.method == "POST":
        change_form = ChangeForm(request.POST)
        if change_form.is_valid():
            password1 = change_form.cleaned_data['password1']
            password2 = change_form.cleaned_data['password2']
            email = change_form.cleaned_data['email']
            if password1 != password2:
                message = "You need to enter the same password twice!"
                return render(request, 'user/change.html', locals())

            same_email_user = User.objects.filter(email=email)
            if same_email_user:
                message = 'The email account has been used, please change another one!'
                return render(request, 'user/change.html', locals())

            username = request.session['user_name']
            user = User.objects.get(name=username)
            user.password = password1
            user.email = email
            user.save()
            return redirect('/user/account/')

    change_form = ChangeForm()
    return render(request, 'user/change.html', locals())

