import pandas as pd
import schedule 
import time 
from tvDatafeed import TvDatafeed, Interval

class extracting_view:
    def __init__(self) :
        self.initial_data = pd.DataFrame()
        self.tv = TvDatafeed()
        self.intervals_dataframe = pd.DataFrame()
        self.contador_intervalos = 1
            
    def load_data_initial(self):
        self.initial_data = self.tv.get_hist(symbol='SOLUSDT',exchange='BINANCE',interval=Interval.in_1_minute,n_bars=15)

    def get_intervals(self):
        df_temporal = self.tv.get_hist(symbol='ETHUSDT',exchange='BINANCE',interval=Interval.in_1_minute,n_bars=5)
        self.intervals_dataframe = pd.concat([df_temporal, self.intervals_dataframe])
        if (self.contador_intervalos == 3):
            self.contador_intervalos = 1
            self.initial_data = pd.concat([self.initial_data, self.intervals_dataframe])
            self.intervals_dataframe = pd.DataFrame()
            self.initial_data.to_csv('initial_data.csv')
        self.contador_intervalos = self.contador_intervalos + 1
        print(self.initial_data)

    def run(self):
        schedule.every(1).minutes.do(self.get_intervals)
        while True:
            schedule.run_pending()
            time.sleep(1)


extractor = extracting_view()
extractor.load_data_initial()
extractor.run()