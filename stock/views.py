from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from datetime import datetime, date, timedelta
from .models import Stock, StockPrice
from .forms import GetDataForm, PredicationForm
from BusinessLogic.prediction import IPrediction, PandasPrediction
from BusinessLogic.exchange import IExchange, FinamExchange


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

    #getExchangeIntegration().get_data(code, year_start, month_start, day_start, year_end, month_end, day_end, e, market, em, day_start, month_start, year_start, day_end,
     #      month_end, year_end, p, dtf, tmf, MSOR, mstimever, sep, sep2, datf, at)

    in_file = 'company_quotes2.csv'
    with open(in_file, 'r') as read_file:
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

def predictValue(request):
    if request.method == 'POST':
        form = PredicationForm(request.POST)
        if form.is_valid():
            predicator = getPredictionEngine(form.cleaned_data['companyName'])
            value = predicator.predict(form.cleaned_data['year'], form.cleaned_data['month'], form.cleaned_data['day'])  
            return HttpResponse(value, content_type='application/json')
        else:
            return HttpResponse('false', content_type='application/json')
    else:
        return HttpResponse('false', content_type='application/json')

def getExchangeIntegration() -> IExchange:
    return FinamExchange()

def getPredictionEngine(companyName) -> IPrediction:
    return PandasPrediction(companyName)
