import backtrader as bt
import pandas as pd

class MyStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),  # RSI-periode på 14 dager
        ('rsi_overbought', 70),  # Overkjøpt RSI grense
        ('rsi_oversold', 30),  # Oversolgt RSI grense
        ('stop_loss', 0.25),  # Stop-loss satt til 25% under kjøpsprisen
        ('take_profit', 0.20)  # Take-profit på 20% over kjøpsprisen
    )

    def __init__(self):
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)
        self.order = None  # Sporer aktiv ordre
        self.buy_price = None  # Kjøpspris
        self.stop_loss_price = None  # Stop-loss pris
        self.take_profit_price = None  # Take-profit pris
        self.trade_count = 0  # Antall handler

    def next(self):
        if self.order:
            return  # Hvis vi allerede har en aktiv ordre, gjør ingenting

        # Kjøpslogikk - Kjøp når RSI er oversolgt og ingen tidligere ordre
        if self.rsi[0] < self.params.rsi_oversold and self.buy_price is None:
            self.buy_price = self.data.close[0]
            self.stop_loss_price = self.buy_price * (1 - self.params.stop_loss)
            self.take_profit_price = self.buy_price * (1 + self.params.take_profit)
            self.order = self.buy(size=100)  # Juster størrelsen på handelen her
            self.trade_count += 1
            print(f"Kjøper på {self.data.close[0]} den {self.datas[0].datetime.date(0)}")
            print(f"Stop-loss satt til {self.stop_loss_price}, Take-profit satt til {self.take_profit_price}")

        # Salgslogikk - Selg enten på take-profit, stop-loss eller overkjøpt RSI
        elif (self.data.close[0] >= self.take_profit_price or
              self.data.close[0] <= self.stop_loss_price or
              self.rsi[0] > self.params.rsi_overbought):
            if self.order:
                self.order = self.sell(size=100)
                print(f"Selger på {self.data.close[0]} den {self.datas[0].datetime.date(0)}")
                self.buy_price = None  # Tilbakestill kjøpsprisen
                self.stop_loss_price = None  # Tilbakestill stop-loss
                self.take_profit_price = None  # Tilbakestill take-profit

# Legg til CSV-fil for historiske data
data = pd.read_csv('formatted_data.csv', index_col='timestamp', parse_dates=True)

# Konverter data til Backtrader-feed
feed = bt.feeds.PandasData(dataname=data)

# Opprett Cerebro-instans for backtesting
cerebro = bt.Cerebro()

# Legg til data og strategi
cerebro.adddata(feed)
cerebro.addstrategy(MyStrategy)

# Sett startkapital
cerebro.broker.set_cash(10000)

# Kjør backtesting
print(f"Startkapital: {cerebro.broker.getvalue()}")
cerebro.run()
print(f"Sluttsaldo: {cerebro.broker.getvalue()}")
print(f"Antall handler utført: {cerebro.strats[0][0].strategy.trade_count}")

# Plot resultater
cerebro.plot(style='candlestick')
