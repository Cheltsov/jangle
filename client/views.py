from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from client.models import Client
import datetime
from django.conf import settings
from django.template import RequestContext, loader
from .forms import RegistrationForm
from BusinessLogic.encoder import IEncoder, SHA256Encoder


# Create your views here.
def auth_index(request):
    if hasattr(request.COOKIES, 'customerId'):
        request.session['client'] = str(request.COOKIES['customerId'])
    return render(request, "client/authindex.html", {})


def auth_main(request):
    if request.POST:
        tmp_cl = Client.objects.filter(email=request.POST['email'], password=getEncoder().encode(request.POST['password'])).values('id', 'email').first()
        if tmp_cl:
            request.session['client'] = str(tmp_cl['email']) + "---" + str(tmp_cl['id'])
            response = HttpResponseRedirect('/cabinet')
            if request.POST.get('remember-me'):
                response.set_cookie("customerId", tmp_cl['id'])
            return response
        else:
             return HttpResponse('ERROR!')
    else:
        return redirect('/')

def registration(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirmationPassword']: 
                Client.objects.create(
                    email = form.cleaned_data['email'],
                    password = getEncoder().encode(form.cleaned_data['password']),
                    phone = '0123456789',
                    country = 'Ukraine',
                    city = 'Odessa',
                    birthday = '1999-01-01',
                    fio = 'Johann van der Test',
                    money = 100000
                )
                return redirect('/')
            else:
                return HttpResponse('ERROR!')
    else:
        return render(request, "client/registration.html")

def cabinet(request):
    if request.session.get('client'):
        return render(request, 'client/cabinet.html', {})
    else:
        return redirect('/')


def logout(request):
    response = HttpResponseRedirect("/")
    if request.COOKIES.get('customerId'):
        response.delete_cookie('customerId')
        
    if request.session.get('client'):
        del request.session['client']
    return response

def getEncoder() -> IEncoder:
    return SHA256Encoder()