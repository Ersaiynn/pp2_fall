import re
import json

NUM = r"\d[\d\s\u00a0]*,\d{2}"


def to_float(s):
    return float(re.sub(r"[\s\u00a0]", "", s).replace(",", "."))


with open("raw.txt", encoding="utf-8") as f:
    text = f.read()

item_re = re.compile(
    r"^\s*(\d+)\.\s*\n(.+?)\n\s*(\d+,\d{3})\s*x\s*(" + NUM + r")\s*\n\s*(" + NUM + r")\s*\n\s*Стоимость",
    re.MULTILINE | re.DOTALL,
)

items = []
for m in item_re.finditer(text):
    items.append({
        "number": int(m.group(1)),
        "name": re.sub(r"\s+", " ", m.group(2)).strip(),
        "quantity": float(m.group(3).replace(",", ".")),
        "price": to_float(m.group(4)),
        "sum": to_float(m.group(5)),
    })

all_prices = [to_float(p) for p in re.findall(r"x\s*(" + NUM + r")", text)]

calculated_total = round(sum(i["sum"] for i in items), 2)

total_m = re.search(r"ИТОГО:\s*(" + NUM + r")", text)
receipt_total = to_float(total_m.group(1)) if total_m else None

dt_m = re.search(r"Время:\s*(\d{2})\.(\d{2})\.(\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
date = f"{dt_m.group(3)}-{dt_m.group(2)}-{dt_m.group(1)}" if dt_m else None
time = dt_m.group(4) if dt_m else None

pay_m = re.search(r"^(Банковская карта|Наличные|Карта|Безналичные)\s*:", text, re.MULTILINE | re.IGNORECASE)
payment_method = pay_m.group(1) if pay_m else None

check_m = re.search(r"Чек\s*№\s*(\d+)", text)
bin_m = re.search(r"БИН\s*(\d{12})", text)
store_m = re.search(r"^(Филиал.+)$", text, re.MULTILINE)
cashier_m = re.search(r"Кассир\s+(.+)", text)
vat_m = re.search(r"НДС\s*\d+%:\s*(" + NUM + r")", text)

result = {
    "store": store_m.group(1).strip() if store_m else None,
    "bin": bin_m.group(1) if bin_m else None,
    "receipt_number": check_m.group(1) if check_m else None,
    "cashier": cashier_m.group(1).strip() if cashier_m else None,
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "items": items,
    "prices": all_prices,
    "calculated_total": calculated_total,
    "receipt_total": receipt_total,
    "totals_match": calculated_total == receipt_total,
    "vat": to_float(vat_m.group(1)) if vat_m else None,
}

print(json.dumps(result, ensure_ascii=False, indent=2))

print()
print(f"Чек №{result['receipt_number']} | {result['date']} {result['time']} | {result['payment_method']}")
print("-" * 70)
for i in items:
    print(f"{i['number']:>2}. {i['name'][:40]:<40} {i['quantity']:>5.0f} x {i['price']:>9.2f} = {i['sum']:>9.2f}")
print("-" * 70)
print(f"ИТОГО (посчитано): {calculated_total:.2f}")
print(f"ИТОГО (в чеке):    {receipt_total:.2f}")
