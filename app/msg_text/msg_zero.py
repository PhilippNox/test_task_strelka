from string import Template

echo = f"Echo:"

menu = f"Бот коммунны Ru-Mos-327."

but_text_level = f"Уровень коммунны."

but_text_goods = f"Доступных товаровы."

but_text_buy = f"Оформить покупку."

curr_level = Template(f"Текущий уровень коммунны 🔸$level")

no_level = f"Уровень коммунны на данный момент не доутупен"

no_goods = f"Список товаров не доступен"

first_line_goods = "Товары:\n"

elem_goods = Template(
	f"🔹 $name\n"
	f"код: $barcode\n"
	f"кол: $quantity\n"
	f"цена: $price\n"
)

