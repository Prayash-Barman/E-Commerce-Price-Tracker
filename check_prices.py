import schedule
import time
from database import init_db, get_all_products, save_price
from scraper import get_price
from notifier import send_alert
from datetime import datetime

def check_prices():
    print("\nChecking prices...")
    products = get_all_products()

    if not products:
        print("No products being tracked.")
        return

    for product in products:
        product_id, url, name, target_price = product
        current_name, current_price = get_price(url)

        if current_price is None:
            print(f"❌ Could not get price for {name}")
            continue

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_price(product_id, current_price, date)

        print(f"Product: {name}")
        print(f"Current Price: ₹{current_price}")
        print(f"Target Price: ₹{target_price}")

        if current_price <= target_price:
            print(f"🎉 Price dropped! Sending alert...")
            send_alert(name, current_price, target_price, url)
        else:
            print(f"⏳ Not yet at target price")
        print("-" * 40)

# Run every 24 hours
schedule.every(24).hours.do(check_prices)

# Run once immediately when script starts
check_prices()

print("\n✅ Scheduler running - checking every 24 hours")
print("Keep this window open. Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(1)