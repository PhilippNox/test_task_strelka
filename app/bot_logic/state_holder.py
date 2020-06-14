from typing import NamedTuple


class StateHolder(NamedTuple):
	zero: str = 'zero'
	buy: str = 'buy'


state_holder = StateHolder()
