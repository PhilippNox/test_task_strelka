from app.core.config import settings
import app.schemas_db as sch_db
from app.db import crud_deal


async def get_level():
	if settings.HUMAN_NUM < 1:
		return sch_db.ReportLevel(ok=False, code=1, msg="Number of humans less than 1")
	balance = await crud_deal.get_balance()
	if not balance.ok:
		return sch_db.ReportLevel(ok=False, code=2, msg="Balance are not available")
	out_data = round(balance.data / settings.HUMAN_NUM * abs(settings.FLOORS_NUM) * 0.01, 3)
	return sch_db.ReportLevel(ok=True, code=0, msg="Current level", data=out_data)
