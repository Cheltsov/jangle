from abc import abstractmethod
import urllib.request

class IExchange():
    @abstractmethod
    def get_data(self, code, year_start, month_start, day_start, year_end, month_end, day_end, e, market, em, df, mf, yf, dt, mt, yt, p, dtf, tmf, MSOR, mstimever, sep, sep2, datf, at):
        pass

# http://export.finam.ru/GAZP_200402_200413.txt?market=1&em=16842&code=GAZP&apply=0&df=2&mf=3&yf=2020&from=02.04.2020&dt=13&mt=3&yt=2020&to=13.04.2020&p=7&f=GAZP_200402_200413&e=.txt&cn=GAZP&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1
class FinamExchange(IExchange):
    def get_data(self, code, year_start, month_start, day_start, year_end, month_end, day_end, e, market, em, df, mf, yf, dt, mt, yt, p, dtf, tmf, MSOR, mstimever, sep, sep2, datf, at):
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
