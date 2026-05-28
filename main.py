from database import init_db, add_product, get_all_products, delete_product, save_price
from scraper import get_price
from notifier import send_alert
from datetime import datetime


def check_prices():
    products = get_all_products()

    if not products:
        print("No products being tracked yet.")
        return

    print("\nChecking prices...\n")
    for product in products:
        product_id, url, name, target_price = product
        current_name, current_price = get_price(url)

        if current_price is None:
            print(f"❌ Could not get price for {name} - possibly out of stock")
            continue

        # Save price to history
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_price(product_id, current_price, date)

        print(f"Product: {name}")
        print(f"Current Price: ₹{current_price}")
        print(f"Target Price: ₹{target_price}")

        if current_price <= target_price:
            print(f"🎉 Price dropped! Sending email alert...")
            send_alert(name, current_price, target_price, url)
        else:
            print(f"⏳ Price not yet at target")
        print("-" * 40)


def view_products():
    products = get_all_products()

    if not products:
        print("No products being tracked yet.")
        return

    print("\n--- Tracked Products ---")
    for product in products:
        product_id, url, name, target_price = product
        print(f"{product_id}. {name}")
        print(f"   Target: ₹{target_price}")
        print(f"   URL: {url[:50]}...")
        print()


def main():
    init_db()

    while True:
        print("\n=== Amazon Price Tracker ===")
        print("1. Add product")
        print("2. View tracked products")
        print("3. Check prices now")
        print("4. Remove product")
        print("5. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            url = input("Paste Amazon URL: ")
            target_price = float(input("Enter target price: ₹"))
            print("Fetching product details...")
            name, current_price = get_price(url)
            if name:
                add_product(url, name, target_price)
                print(f"✅ Added: {name}")
                if current_price:
                    print(f"Current price: ₹{current_price}")
            else:
                print("❌ Could not fetch product. Check the URL.")

        elif choice == "2":
            view_products()

        elif choice == "3":
            check_prices()

        elif choice == "4":
            view_products()
            product_id = int(input("Enter product ID to remove: "))
            delete_product(product_id)
            print("✅ Product removed.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()