
from django.shortcuts import render, redirect
from django.http import HttpResponse

from client.models import Client


# Create your views here.
def auth_index(request):
    return render(request, "client/authindex.html", {})


def auth_main(request):
    if request.POST:
        tmp_cl = Client.objects.filter(email=request.POST['email'], password=request.POST['password']).values('id',
                                                                                                              'email').first()
        print(tmp_cl)
        if tmp_cl:
            request.session['client'] = str(tmp_cl['email']) + "---" + str(tmp_cl['id'])
            return redirect('/cabinet')
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
    if request.session.get('client'):
        del request.session['client']
        return redirect('/')
    else:
        return redirect('/cabinet')
