from string import Template

cart_item = Template(
	f"🔹 $name\n"
	f"код: $barcode\n"
	f"кол: $quantity\n"
	f"цена: $price\n"
	f"--\n"
	f"выбрано: $choice"
)

