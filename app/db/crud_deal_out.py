from fastapi.logger import logger
from app.db.core_db import database
import app.schemas_income as sch_in
import app.schemas_db as sch_db
import app.db.crud_user as crud_us
import app.db.crud_deal as crud_dl
import uuid


async def deal_out(income: sch_in.DealRequest):
	transaction = await database.transaction()
	try:
		rlts = await crud_dl.update_goods(income.items, deal_is_out=True)
		if None in rlts:
			await transaction.rollback()
			return sch_db.Report(ok=False, code=2, msg="Barcode error",
								 data=crud_dl.get_unknow_barcode(income.items, rlts))
		quant = [e['quantity'] for e in rlts]
		if any(elem < 0 for elem in quant):
			await transaction.rollback()
			return sch_db.Report(ok=False, code=3, msg="Not enough quantity",
								 data=crud_dl.get_negavite_quant(income.items, quant))

		deal_uuid = uuid.uuid4()
		deal_id, _ = await crud_dl.create_deal(
			deal_uuid,
			await crud_us.get_or_create_user(income.id),
			crud_dl.get_amount(income.items, rlts)
		)
		await crud_dl.update_countbook(income.items, rlts, deal_id, deal_is_out=True)
	except Exception as e:
		await transaction.rollback()
		logger.warning(f"deal_out: Exception: {e}")
		return sch_db.Report(ok=False, code=1, msg="Unknown error")
	else:
		await transaction.commit()
	return sch_db.Report(ok=True, code=0, msg="Buy deal done", data=deal_uuid)


