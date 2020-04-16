from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import urllib.request
from datetime import datetime, date, timedelta
from .models import Stock, StockPrice
from .forms import GetDataForm, PredicationForm
from BusinessLogic.dataAnalysis import DataAnalysis


# Create your views here.

def get_company(request, id):
    tmp = StockPrice.objects.filter(id_stock=id).values('id', 'date_time', 'high', 'low', 'open', 'close', 'vol').order_by('date_time')
    for i in range(len(tmp)):
        if i != 0:
            if tmp[i-1]['high'] <= tmp[i]['high']:
                tmp[i]['status_high'] = 1
            else:
                tmp[i]['status_high'] = 2

            if tmp[i-1]['low'] <= tmp[i]['low']:
                tmp[i]['status_low'] = 1
            else:
                tmp[i]['status_low'] = 2

            if tmp[i-1]['open'] <= tmp[i]['open']:
                tmp[i]['status_open'] = 1
            else:
                tmp[i]['status_open'] = 2

            if tmp[i-1]['close'] <= tmp[i]['close']:
                tmp[i]['status_close'] = 1
            else:
                tmp[i]['status_close'] = 2

        else:
            tmp[i]['status_high'] = 0
            tmp[i]['status_low'] = 0
            tmp[i]['status_open'] = 0
            tmp[i]['status_close'] = 0
    stock = Stock.objects.get(id=id)
    return render(request, 'stock/detail.html', {'prices': tmp, 'companyName': stock.company})

def get_grafic(request, id):
    tmp = StockPrice.objects.filter(id_stock=id).values('id', 'date_time', 'high', 'low')
    return JsonResponse(list(tmp), safe=False)

def list_quotes(request):
    stock = Stock.objects.all().values('id', 'company', 'description')
    for st in stock:
        st_p = StockPrice.objects.filter(id_stock=st['id']).values('id',
                                                                   'date_time',
                                                                   'high',
                                                                   'low',
                                                                   'close',
                                                                   'vol',
                                                                   'open')
        #print(st_p)
        st['prices'] = st_p

        now_date = StockPrice.objects.filter(id_stock=st['id']).values('date_time', 'high', 'low').order_by('-date_time').first()
        yesterday = now_date['date_time'] - timedelta(days=1)
        yesterday_st = StockPrice.objects.filter(id_stock=st['id'], date_time=yesterday).values('date_time', 'high', 'low').order_by('-date_time').first()
        if now_date['high'] > yesterday_st['high']:
            st['status_high'] = 1
        else:
            st['status_high'] = 0
        if now_date['low'] > yesterday_st['low']:
            st['status_low'] = 1
        else:
            st['status_low'] = 0
        st['price'] = StockPrice.objects.filter(id_stock=st['id']).order_by('-date_time').first()

    content = {
        'quotes': stock
    }
    return render(request, 'stock/index.html', content)




def refresh_con(request):
    if request.method == 'POST':
        form = GetDataForm(request.POST)
        if form.is_valid():
            name_company = [
                'KMEZ', 'AAPL', 'YHOO'
            ]
            for item in name_company:
                stockId = Stock.objects.get(company=item)
                StockPrice.objects.filter(id_stock = stockId).delete()
                new_quotes(item, form.cleaned_data['year_start'], form.cleaned_data['year_end'], form.cleaned_data['month_start'], form.cleaned_data['month_end'], form.cleaned_data['day_start'], form.cleaned_data['day_end'])
        else:
            return HttpResponse('ERROR!')
    else:
        name_company = [
            'KMEZ', 'AAPL', 'YHOO'
        ]
        for item in name_company:
            stockId = Stock.objects.get(company=item)
            StockPrice.objects.filter(id_stock = stockId).delete()
            new_quotes(item, '2017', '2017','05', '06', '10', '20')
    return HttpResponseRedirect('/stock/')


def new_quotes(code, year_start, year_end, month_start, month_end, day_start, day_end):
    code = code
    market = '1'
    em = '175924'
    e = '.csv'
    p = '8'
    dtf = '1'
    tmf = '1'
    MSOR = '1'
    mstimever = '0'
    sep = '1'
    sep2 = '3'
    datf = '1'
    at = '1'

    quotes(code, year_start, month_start, day_start, year_end, month_end, day_end, e, market, em, day_start, month_start, year_start, day_end,
           month_end, year_end, p, dtf, tmf, MSOR, mstimever, sep, sep2, datf, at)

    in_file = 'company_quotes2.csv'
    with open(in_file, 'r')as read_file:
        tmp_arr = []
        for line in read_file:
            arr_param = line.replace("\n", "").split(',')
            if not arr_param[0] == '<TICKER>':
                tmp_arr.append({
                    'ticker': arr_param[0],
                    'per': arr_param[1],
                    'date': datetime.strptime(arr_param[2] + ' ' + arr_param[3], "%Y%m%d %H%M%S"),
                    'open': arr_param[4],
                    'high': arr_param[5],
                    'low': arr_param[6],
                    'close': arr_param[7],
                    'vol': arr_param[8]
                })

        for item in tmp_arr:
            obj, created = Stock.objects.get_or_create(company=item['ticker'])
            tmp1 = StockPrice.objects.create(
                id_stock=obj,
                date_time=item['date'],
                open=item['open'],
                high=item['high'],
                low=item['low'],
                close=item['close'],
                vol=item['vol']
            )
            tmp1.save()
# http://export.finam.ru/GAZP_200402_200413.txt?market=1&em=16842&code=GAZP&apply=0&df=2&mf=3&yf=2020&from=02.04.2020&dt=13&mt=3&yt=2020&to=13.04.2020&p=7&f=GAZP_200402_200413&e=.txt&cn=GAZP&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1

def quotes(code, year_start, month_start, day_start, year_end, month_end, day_end, e, market, em, df, mf, yf, dt,
           mt, yt, p, dtf, tmf, MSOR, mstimever, sep, sep2, datf, at):
    with urllib.request.urlopen('http://export.finam.ru/' + str(code) + '_' + str(year_start) + str(month_start) + str(
            day_start) + '_' + str(year_end) + str(month_end) + str(day_end) + str(e) + '?market=' + str(
        market) + '&em=' + str(em) + '&code=' + str(code) + '&apply=0&df=' + str(df) + '&mf=' + str(
        mf) + '&yf=' + str(yf) + '&from=' + str(day_start) + '.' + str(month_start) + '.' + str(yf) + '&dt=' + str(
        dt) + '&mt=' + str(mt) + '&yt=' + str(yt) + '&to=' + str(day_end) + '.' + str(month_end) + '.' + str(
        yt) + '&p=' + str(p) + '&f=' + str(code) + '_' + str(year_start) + str(month_start) + str(
        day_start) + '_' + str(year_end) + str(month_end) + str(day_end) + '&e=' + str(e) + '&cn=' + str(
        code) + '&dtf=' + str(dtf) + '&tmf=' + str(tmf) + '&MSOR=' + str(MSOR) + '&mstimever=' + str(
        mstimever) + '&sep=' + str(sep) + '&sep2=' + str(sep2) + '&datf=' + str(datf) + '&at=' + str(at)) as page:
        f = open("company_quotes2.csv", "wb")
        content = page.read()
        f.write(content)
        f.close()

def predictValue(request):
    if request.method == 'POST':
        form = PredicationForm(request.POST)
        if form.is_valid():
            predicator = DataAnalysis(form.cleaned_data['companyName'])
            value = predicator.predictValue(form.cleaned_data['year'], form.cleaned_data['month'], form.cleaned_data['day'])  
            return HttpResponse(value, content_type='application/json')
        else:
            return HttpResponse('false', content_type='application/json')
    else:
        return HttpResponse('false', content_type='application/json')