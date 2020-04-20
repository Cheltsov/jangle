from stock.models import Stock, StockPrice
import pandas as pd
from fbprophet import Prophet
import datetime
from abc import abstractmethod

class IPrediction():
    @abstractmethod
    def predict(self,  year, month, day) -> float:
        pass

class PandasPrediction(IPrediction):

    _companyName = ""
    _tempFileName = "tempAnalisFile.csv"

    def __init__(self, companyName):
        self._companyName = companyName

    def predict(self, year, month, day)  -> float:
        # СОздание временного Csv файла
        self.createTempCsv()

        df = pd.read_csv(self._tempFileName)

        # СОздание и заполнения данными Предсказателя
        m = Prophet()
        m.fit(df)

        # Определение даты для прогноза (может быть множество )
        dataFrame = pd.DataFrame({ 'ds': [datetime.date(int(year), int(month), int(day))] })
        forecast = m.predict(dataFrame)
        return forecast["yhat"][0]

    def createTempCsv(self):
        stockId = Stock.objects.filter(company = self._companyName).values('id')
        stockPrices = StockPrice.objects.filter(id_stock = stockId[0]['id']).values('date_time', 'high')

        f = open(self._tempFileName, "w")
        f.write("ds,y")
        for stockPrice in stockPrices:
            date_time = stockPrice['date_time'].strftime("%Y-%m-%d")
            f.write("\n" + date_time +"," + str(stockPrice['high']))
        f.close()
