import operator
import numpy as np
import pandas as pd

from typing import Any, List
from typing import Dict
from typing import Union
from typing import Optional
from typing import Tuple

from pyrobot.stock_frame import StockFrame

class Indicators():
# sma ema rsi get definitions
    def __init__(self, price_data_frame: StockFrame) -> None:
        # anything leading with an underscore is private.
        self._stock_frame: StockFrame = price_data_frame
        self._price_groups = self._stock_frame.symbol_goups
        self._current_indicators = {}
        # as we add new rows data we have to recalculate our indicators, loop takes indicators previously entered and assumes you want to keep them the same and uses them and updates columns with latest data.
        self._indicators_signals = {}
        self._frame = self._stock_frame.frame

    def set_indicator_signals(self, indicator: str, buy: float, sell: float, condition_buy: Any, condition_sell: Any) -> None:
        # using indicator it has a signal and the signal is made up of two pieces threshhold and a operator. Thresh hold is a numerical value and the operator is a ><=?
        #VVVVV if there is no signal for that indicator set a template.
        if indicator not in self.set_indicator_signals:
            self._indicators_signals[indicator] = {}

        #Modify the signal
        self._indicators_signals[indicator]['buy'] = buy
        self._indicators_signals[indicator]['sell'] = sell
        self._indicators_signals[indicator]['buy_operator'] = condition_buy
        self._indicators_signals[indicator]['sell_operator'] = condition_sell

    def get_indicator_signals(self, indicator: Optional[str]) -> Dict:

        if indicator and indicator in self._indicators_signals:
            return self._indicator_signals[indicator]
        else:
            return self._indicators_signals

    @property
    def price_data_frame(self) -> pd.DataFrame:

        return self._frame

    @price_data_frame.setter
    def price_data_frame(self, price_data_frame: pd.DataFrame) -> None:

        self._frame = price_data_frame


    def change_in_price(self) -> pd.DataFrame:

        locals_data = locals()
        del locals_data['self']

        column_name = 'change_in_price'
        self._current_indicators[column_name] = {}
        self._current_indicators[column_name]['args'] = locals_data
        self._current_indicators[column_name]['func'] = self.change_in_price

        self._frame[column_name] = self._price_groups['close'].transform(
            lambda x: x.diff()
        )

    def rsi(self, period: int, method: str = 'wilders') -> pd.DataFrame:

        locals_data = locals()
        del locals_data['self']

        column_name = 'change_in_price'
        self._current_indicators[column_name] = {}
        self._current_indicators[column_name]['args'] = locals_data
        self._current_indicators[column_name]['func'] = self.rsi

        if 'change_in_price' not in self._frame.columns:
            self.change_in_price()

        # Define the up days.
        self._frame['up_day'] = self._price_groups['change_in_price'].transform(
            lambda x : np.where(x >= 0, x, 0)
        )

        self._frame['down_day'] = self._price_groups['change_in_price'].transform(
            lambda x : np.where(x < 0, x.abs(), 0)
        )

        self._frame['ewma_day'] = self._price_groups['up_day'].transform(
            lambda x : x.ewm(span=period).mean()
        )

        self._frame['ewma_down'] = self._price_groups['down_day'].transform(
            lambda x : x.ewm(span=period).mean()
        )

        relative_strength = self._frame['ewma_up'] / self._frame['ewma_down']

        relative_strength_index = 100.0 - (100.0 / (1.0 + relative_strength))

        self._frame['rsi'] = np.where(relative_strength_index == 0, 100, 100.0 - (100.0 / (1.0 + relative_strength)))

        self._frame.drop(
            labels=['ewma_up', 'ewma_down', 'down_day', 'up_day', 'change_in_price'],
            axis=1,
            inplace=True
        )
        
        return self._frame

    def sma(self, period: int) -> pd.DataFrame:

        locals_data = locals()
        del locals_data['self']

        column_name = 'sma'
        self._current_indicators[column_name] = {}
        self._current_indicators[column_name]['args'] = locals_data
        self._current_indicators[column_name]['func'] = self.sma

        self._frame[column_name] = self._price_groups['clase'].transform(
            lambda x: x.rolling(window=period).mean()
        )

        return self._frame

    def ema(self, period: int, alpha: float = 0.0) -> pd.DataFrame:

        locals_data = locals()
        del locals_data['self']

        column_name = 'ema'
        self._current_indicators[column_name] = {}
        self._current_indicators[column_name]['args'] = locals_data
        self._current_indicators[column_name]['func'] = self.ema

        self._frame[column_name] = self._price_groups['close'].transform(
            lambda x: x.ewm(span=period).mean()
        )

        return self._frame

    def refresh(self):
        
        #First update the groups
        self._price_groups = self._stock_frame.symbol_goups

        # Loop through all the stored indicators

        for indicator in self._current_indicators:

            indicator_arguments = self._current_indicators[indicator]['args']

            indicator_function = self._current_indicators[indicator]['func']

            # Update the columns
            indicator_function(**indicator_arguments)

    def check_signals(self) -> Union[pd.DataFrame, None]:
        
        signals_df = self._stock_frame._check_signals(indicators=self._indicators_signals)

        return signals_df