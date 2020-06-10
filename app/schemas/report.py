from typing import Optional, NamedTuple, Any


class Report(NamedTuple):
	ok:		bool
	code: 	int
	msg:	str
	data: Optional[Any] = None
