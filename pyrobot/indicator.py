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
