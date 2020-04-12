from stock.models import Stock, StockPrice
import pandas as pd
from fbprophet import Prophet
import datetime

class DataAnalysis:

    _companyName = ""
    _tempFileName = "tempAnalisFile.csv"

    def __init__(self, companyName):
        self._companyName = companyName

    def predictValue(self):
        # СОздание временного Csv файла
        self.createTempCsv()

        df = pd.read_csv(self._tempFileName)

        # СОздание и заполнения данными Предсказателя
        m = Prophet()
        m.fit(df)

        # Определение даты для прогноза (может быть множество )
        dataFrame = pd.DataFrame({ 'ds': [datetime.date(2017, 5, 4)] })
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
