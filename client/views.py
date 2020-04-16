from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from client.models import Client
import datetime
from django.conf import settings
from django.template import RequestContext, loader


# Create your views here.
def auth_index(request):
    if hasattr(request.COOKIES, 'customerId'):
        request.session['client'] = str(request.COOKIES['customerId'])
    return render(request, "client/authindex.html", {})


def auth_main(request):
    if request.POST:
        tmp_cl = Client.objects.filter(email=request.POST['email'], password=request.POST['password']).values('id',
                                                                                                              'email').first()
        if tmp_cl:
            request.session['client'] = str(tmp_cl['email']) + "---" + str(tmp_cl['id'])
            response = HttpResponse(render(request, 'client/cabinet.html', {}))
            if request.POST.get('remember-me'):
                response.set_cookie("customerId", tmp_cl['id'])
            return response
        else:
            return redirect('/')
    else:
        return redirect('/')


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
