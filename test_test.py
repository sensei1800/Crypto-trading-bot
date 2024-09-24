import unittest
import backtrader as bt
import pandas as pd

class TestBacktestBot(unittest.TestCase):

    def test_backtrader_setup(self):
        # Test for å sjekke om backtrader settes opp riktig
        cerebro = bt.Cerebro()
        self.assertIsInstance(cerebro, bt.Cerebro)

    def test_data_loading(self):
        # Test for å sikre at CSV-filen lastes riktig
        try:
            data = pd.read_csv('formatted_data.csv', index_col='timestamp', parse_dates=True)
            self.assertIsNotNone(data)
        except Exception as e:
            self.fail(f"Data loading failed with exception: {e}")

if __name__ == "__main__":
    unittest.main()
