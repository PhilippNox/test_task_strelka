from string import Template

echo = f"Echo:"

menu = f"Бот коммуны Ru-Mos-327."

but_text_level = f"Уровень коммуны."

but_text_goods = f"Доступные товары."

but_text_buy = f"Оформить покупку."

curr_level = Template(f"Текущий уровень коммуны 🔸$level")

no_level = f"Уровень коммуны на данный момент не доступен"

no_goods = f"Список товаров не доступен"

first_line_goods = "Товары:\n"

elem_goods = Template(
	f"🔹 $name\n"
	f"код: $barcode\n"
	f"кол: $quantity\n"
	f"цена: $price\n"
)

