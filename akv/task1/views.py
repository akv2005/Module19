from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import UserRegister
from django.http import HttpResponse
from .models import *

cnt_choice = 5
class main(TemplateView):
    template_name = 'platform.html'

def cart(request):
    global cnt_choice
    cnt = request.GET.get('cnt', cnt_choice)
    if int(cnt) == 0:
        cnt = cnt_choice
    cnt_choice = cnt
    title = 'Ассортимент'
#    games = Game.objects.all()
    games = Game.objects.order_by('cost')
    paginator = Paginator(games, cnt)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    back = 'Вернуться обратно'
    context = {'title': title, 'games': games, 'back': back, 'page_obj': page_obj,}

    return render(request, 'cart.html', context)

def games(request):
    context = {
        'back': '/',
        'cart': '/cart'
    }
    return render(request, template_name='games.html', context=context)


def sign_up_by_html(request):
    i = 0
    info = {'error':[]}
    users = Buyer.objects.all().values_list('name', flat=True)
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeate_password = request.POST.get('repeate_password')
        age = request.POST.get('age')

        print(f'Username: {username}')
        print(f'Password: {password}')
        print(f'Repeate password: {repeate_password}')
        print(f'Age: {age}')
        if username not in users and password == repeate_password and int(age)>=18:
            Buyer.objects.create(name=username, balance=10, age=age)
            return HttpResponse(f'Приветствуем {username}')
        elif username in users:
            i +=1
            info[f'error {i}'] = HttpResponse('Этот логин уже занят', status=400, reason='repeated login')
            return HttpResponse('Этот логин уже занят', status=400, reason='repeated login')
        elif password != repeate_password:
            i +=1
            info[f'error {i}'] = HttpResponse('Пароли не совпадают', status=400, reason='non-identical passwords')
            return HttpResponse('Пароли не совпадают', status=400, reason='non-identical passwords')
        elif int(age) < 18:
            i +=1
            info[f'error {i}'] = HttpResponse(f'Регистрация разрешена с 18ти лет. ', status=400, reason='insufficient age')
            return HttpResponse(f'Регистрация разрешена с 18ти лет.', status=400, reason='insufficient age')
    context = {'info':info}

    return render(request, 'registration_page.html', context)


def sign_up_by_django(request):
    info = {'error': []}
    i = 0
    users = Buyer.objects.all().values_list('name', flat=True)
    if request.method == "POST":
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeate_password = form.cleaned_data['repeate_password']
            age = form.cleaned_data['age']
            if username not in users and password == repeate_password and int(age) >= 18:
                Buyer.objects.create(name=username, balance=10, age=age)
                return HttpResponse(f'Приветствуем {username}')
            elif username in users:
                i += 1
                info[f'error {i}'] = HttpResponse('Этот логин уже занят', status=400, reason='repeated login')
                print(info[f'error {i}'])
                return HttpResponse('Этот логин уже занят', status=400, reason='repeated login')
            elif password != repeate_password:
                i += 1
                info[f'error {i}'] = HttpResponse('Пароли не совпадают', status=400, reason='repeated login')
                print(info[f'error {i}'])
                return HttpResponse('Пароли не совпадают', status=400, reason='non-identical passwords')
            elif int(age) < 18:
                i += 1
                info[f'error {i}'] = HttpResponse(
                    f'Регистрация разрешена с 18ти лет.', status=400,
                    reason='insufficient age')

                return HttpResponse(
                    f'Регистрация разрешена с 18ти лет. ', status=400,
                    reason='insufficient age')

    else:

        form = UserRegister()
        context = {'info': info, 'form': form}
        return render(request, 'registration_page.html', context)



