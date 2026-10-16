"""Build data/cairnly.db: the shop's help-centre documents and its order table.

Run from anywhere:  python data/create_db.py
The notebook only reads this database (read-only); edit the data here and re-run to change it.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("cairnly.db")

# Help-centre documents (fictional company, written for this project). One document = one retrieval chunk.
KB = [
    {"id": "KB-01", "category": "shipping", "title": "Shipping options and delivery times",
     "text": "Cairnly ships to all EU countries. Standard delivery takes 3–5 business days and costs €4.95; standard delivery is free for orders of €60 or more (after discounts). Express delivery takes 1–2 business days and costs €12.95. Orders placed before 14:00 CET on a business day are dispatched the same day; later orders are dispatched the next business day. We do not deliver on Sundays or public holidays."},
    {"id": "KB-02", "category": "shipping", "title": "International shipping outside the EU",
     "text": "Outside the EU we only ship to the United Kingdom, Switzerland and Norway. Delivery to these countries takes 5–10 business days and costs a flat €19.95, regardless of order value. Import duties and taxes are charged by the destination country and must be paid by the customer on delivery. We currently do not ship to any other country, including the USA, Canada and Australia. Gas canisters cannot be shipped outside the EU."},
    {"id": "KB-03", "category": "orders", "title": "Order tracking",
     "text": "As soon as your order is dispatched you receive an e-mail with a tracking link. You can also follow your order under My Account > Orders. Tracking information can take up to 24 hours to appear after dispatch. The chat assistant can tell you the status of an order once you give the order number and the e-mail address used for the order. If your parcel is more than 3 business days late, contact our support team with your order number so an agent can open an investigation with the carrier."},
    {"id": "KB-04", "category": "orders", "title": "Changing or cancelling an order",
     "text": "You can change or cancel an order yourself under My Account > Orders within 1 hour of placing it. After 1 hour the order is sent to our warehouse and can no longer be changed or cancelled; instead, you can refuse the delivery or return the items free of charge under our returns policy. Click & collect orders can be cancelled until they are ready for pickup."},
    {"id": "KB-05", "category": "returns", "title": "Returns policy",
     "text": "You can return most items within 30 days of delivery for a full refund. Items must be unused, in their original packaging and with all tags attached. Cairnly Club members have an extended return period of 60 days. Returns from EU countries are free; customers in the UK, Switzerland and Norway pay the return shipping. The following items cannot be returned: opened gas canisters, personalised or custom-made items, worn socks and underwear (for hygiene reasons) and gift cards. Refunds are made to the original payment method within 5 business days after we receive and inspect the return."},
    {"id": "KB-06", "category": "returns", "title": "How to return or exchange an item",
     "text": "To start a return, go to My Account > Orders, choose the order and click 'Return item'. Print the prepaid return label and drop the parcel at any partner parcel shop, or bring the item to one of our stores. Guest customers can start a return with their order number and e-mail address on the Returns page. If you need a different size or colour, choose 'Exchange' instead of 'Return' and we ship the new item as soon as the original is scanned by the carrier."},
    {"id": "KB-07", "category": "returns", "title": "Damaged, faulty or wrong items",
     "text": "If an item arrives damaged, faulty or is not what you ordered, report it within 7 days of delivery through the Help form or by e-mail to support@cairnly.example, including your order number and photos of the problem. We will send a free replacement or give a full refund, whichever you prefer. For damaged items worth less than €25 you do not need to send the item back."},
    {"id": "KB-08", "category": "warranty", "title": "Warranty",
     "text": "All products come with the 2-year legal warranty. Cairnly's own-brand tents and backpacks additionally carry a lifetime warranty against manufacturing defects (for example broken seams or faulty zips present from manufacture). The warranty does not cover normal wear and tear, accidental damage, UV degradation or improper use. To make a claim, fill in the warranty form on our website and attach your proof of purchase and photos; our team responds within 5 business days."},
    {"id": "KB-09", "category": "warranty", "title": "Repair service",
     "text": "We repair tents, jackets and backpacks of any brand at our repair workshop. Typical prices: zip replacement €15, patch repair €10, tent pole section replacement €12. Repairs take 2–3 weeks. Items can be dropped off at any store or sent in using the repair form. Repairs of defects covered by the warranty are free of charge."},
    {"id": "KB-10", "category": "payment", "title": "Payment methods",
     "text": "We accept Visa, Mastercard, American Express, PayPal, Apple Pay, Google Pay and bank transfer. Orders paid by bank transfer are reserved for 5 days and dispatched once the payment arrives. With Klarna you can pay within 30 days for orders between €50 and €1,000. We do not offer cash on delivery. Your card is charged when the order is dispatched, not when it is placed."},
    {"id": "KB-11", "category": "pricing", "title": "Price match promise",
     "text": "If you find an identical, in-stock item cheaper at an authorised retailer based in the EU within 14 days of your purchase, we refund the price difference. Send a link to the offer through the Help form. The price match does not apply to marketplace sellers (such as Amazon Marketplace or eBay), clearance or outlet items, flash sales, or prices that require a membership or coupon code."},
    {"id": "KB-12", "category": "pricing", "title": "Discount codes and promotions",
     "text": "Only one discount code can be used per order, and discount codes cannot be applied to items that are already on sale. Subscribing to our newsletter gives you a 10% code for your first order. Codes must be entered at checkout; they cannot be added after an order has been placed. The chat assistant cannot create, send or validate discount codes. We do not announce future sales or Black Friday offers in advance; newsletter subscribers hear about them first."},
    {"id": "KB-13", "category": "loyalty", "title": "Cairnly Club loyalty programme",
     "text": "Cairnly Club is free to join. Members earn 1 point for every €1 spent; 100 points can be exchanged for a €5 voucher. Members get an extended 60-day return period and free express delivery on orders over €150. Points expire if the account has no purchases for 24 months. You can join under My Account > Cairnly Club or in any store."},
    {"id": "KB-14", "category": "payment", "title": "Gift cards",
     "text": "Gift cards are available from €10 to €500 and are valid for 3 years from the date of purchase. Digital gift cards are delivered by e-mail within minutes; physical gift cards can be bought in our stores. A gift card can be used for several orders until its balance is used up, but it cannot be exchanged for cash, refunded or used to buy other gift cards."},
    {"id": "KB-15", "category": "pricing", "title": "Student discount",
     "text": "Students in the EU get 10% off full-price items after verifying their student status through our verification partner on the Student Discount page. The student code can be used once per month and cannot be combined with other discount codes."},
    {"id": "KB-16", "category": "account", "title": "Account and password",
     "text": "To reset your password, click 'Forgot password' on the login page and follow the link in the e-mail (valid for 30 minutes). You can change your e-mail address and delivery addresses under My Account > Settings. To delete your account and personal data, send a request to privacy@cairnly.example; deletion is completed within 30 days in line with the GDPR."},
    {"id": "KB-17", "category": "account", "title": "Payment security and personal data",
     "text": "Cairnly will never ask for your full card number, CVV code or password by chat, e-mail or phone. Never share card details in the chat; payments are only made through our secure checkout. If you think your card details have been exposed, contact your bank. You can request a copy of your personal data at privacy@cairnly.example."},
    {"id": "KB-18", "category": "stores", "title": "Stores and opening hours",
     "text": "Cairnly has two physical stores: the Flagship store at Central Plaza and the Outlet store at Northgate Retail Park. Both are open Monday to Friday 10:00–19:00 and Saturday 10:00–17:00, and closed on Sundays and public holidays. Click & collect is free: orders are usually ready for pickup within 2 hours during opening hours and are kept for 7 days."},
    {"id": "KB-19", "category": "contact", "title": "Contacting customer service",
     "text": "Human agents are available by live chat and phone Monday to Friday 08:00–18:00 CET; the phone number is listed on the Contact page. E-mails to support@cairnly.example are answered within 24 hours on business days. Outside these hours the chat assistant answers general questions and order-status requests; for anything else, please e-mail support@cairnly.example."},
    {"id": "KB-20", "category": "product", "title": "Product: Cairnly Ridge 2 tent",
     "text": "The Cairnly Ridge 2 is a 2-person, 3-season backpacking tent. Weight: 1.9 kg; packed size 45 × 15 cm. Waterproofing: 3,000 mm hydrostatic head on the flysheet and 5,000 mm on the floor. It has two doors and two vestibules and pitches in about 5 minutes. Price: €279. Covered by Cairnly's lifetime warranty against manufacturing defects."},
    {"id": "KB-21", "category": "product", "title": "Product: Cairnly Summit 45 backpack",
     "text": "The Cairnly Summit 45 is a 45-litre trekking backpack weighing 1.3 kg. It comes in two back lengths: S/M (40–48 cm) and M/L (46–54 cm). A rain cover is included and it is compatible with hydration bladders up to 3 litres. Price: €149. Covered by Cairnly's lifetime warranty against manufacturing defects."},
    {"id": "KB-22", "category": "product", "title": "Product: Cairnly Ember stove",
     "text": "The Cairnly Ember is an ultralight gas stove (85 g) with 2.6 kW output that boils 1 litre of water in about 3.5 minutes. It uses EN 417 threaded gas canisters, which are sold separately. Price: €59."},
    {"id": "KB-23", "category": "safety", "title": "Safety: stoves and gas canisters",
     "text": "Never use a stove or any other gas appliance inside a tent, vestibule, car or other enclosed space: this can cause carbon monoxide poisoning, which can be fatal, and fire. Always cook outdoors in a well-ventilated place at least 1 metre away from your tent, on a stable surface. Gas canisters are dangerous goods: they are shipped by standard ground delivery only, never by express delivery or outside the EU."},
    {"id": "KB-24", "category": "product", "title": "Product: Cairnly Drift sleeping bag and temperature ratings",
     "text": "The Cairnly Drift is a synthetic 3-season sleeping bag with a comfort temperature of 2 °C and a limit temperature of −4 °C (ISO 23537). It weighs 1.1 kg and costs €189. The comfort rating is the temperature at which an average person sleeps comfortably; choose a bag whose comfort rating is at or below the coldest night you expect."},
    {"id": "KB-25", "category": "product", "title": "Clothing sizes and fit",
     "text": "Cairnly clothing comes in sizes XS to XXL; a size chart is shown on every product page. If you are between two sizes, we recommend the larger size for jackets and the smaller size for base layers. Exchanges for a different size are free within the return period."},
]

# Simulated orders. E-mail addresses use the reserved example.com domain.
orders = [
    ("A1001", "anna.k@example.com", "Shipped", "SwiftParcel", "SP-552190", "2026-10-08", "2026-10-12", "Cairnly Ridge 2 tent"),
    ("A1002", "marco.r@example.com", "Delivered", "SwiftParcel", "SP-551004", "2026-10-03", "2026-10-03", "Cairnly Summit 45 backpack"),
    ("A1003", "lena.m@example.com", "Delayed: waiting for stock", None, None, "2026-10-07", "2026-10-20", "Cairnly Drift sleeping bag"),
    ("A1004", "tom.b@example.com", "Processing", None, None, "2026-10-09", "2026-10-14", "Cairnly Ember stove, 2 gas canisters"),
    ("A1005", "sara.n@example.com", "Return received, refund in progress", None, None, "2026-10-06", None, "Rain jacket (size M)"),
]


def main():
    DB_PATH.unlink(missing_ok=True)          # always rebuild from the data above
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""CREATE TABLE kb_documents (
            id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            text TEXT NOT NULL)""")
        conn.execute("""CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            status TEXT NOT NULL,
            carrier TEXT,
            tracking_code TEXT,
            last_update TEXT,
            estimated_delivery TEXT,
            items TEXT)""")
        conn.executemany("INSERT INTO kb_documents VALUES (:id, :category, :title, :text)", KB)
        conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)", orders)
    conn.close()                             # the context manager only commits; close so the file is released
    print(f"{DB_PATH}: {len(KB)} help-centre documents, {len(orders)} orders")


if __name__ == "__main__":
    main()
