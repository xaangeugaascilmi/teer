import db
from order import Cart

def print_header(title: str) -> None:
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

def show_menu() -> None:
    print_header("MENU")
    menu = db.get_menu()
    for cat, items in menu.items():
        print(f"\n-- {cat} --")
        for it in items:
            print(f"  [{it['id']}] {it['name']} - RM {it['price']:.2f}")

def show_cart(cart: Cart) -> None:
    print_header("YOUR CART")
    if cart.is_empty():
        print("Cart is empty.")
        return
    rows = cart.as_rows()
    print(f"{'ID':<6}{'Item':<28}{'Qty':<6}{'Unit':<12}{'Line Total'}")
    print("-" * 60)
    for r in rows:
        print(f"{r[0]:<6}{r[1]:<28}{r[2]:<6}{r[3]:<12}{r[4]}")
    print("-" * 60)
    print(f"Subtotal:     RM {cart.subtotal():.2f}")
    print(f"Service 6%:   RM {cart.service_charge():.2f}")
    print(f"TOTAL:        RM {cart.total():.2f}")

def get_int(prompt: str):
    try:
        return int(input(prompt).strip())
    except Exception:
        return None

def add_flow(cart: Cart) -> None:
    item_id = get_int("Enter ITEM ID to add: ")
    if item_id is None:
        print("Invalid input.")
        return
    item = db.find_item_by_id(item_id)
    if not item:
        print("No item with that ID.")
        return
    qty = get_int("Enter quantity: ")
    if qty is None or qty <= 0:
        print("Quantity must be positive.")
        return
    cart.add_item(item, qty)
    print(f"Added {qty} x {item['name']}.")

def remove_flow(cart: Cart) -> None:
    if cart.is_empty():
        print("Cart is empty.")
        return
    item_id = get_int("Enter ITEM ID to remove: ")
    if item_id is None:
        print("Invalid input.")
        return
    ok = cart.remove_item(item_id)
    if ok:
        print("Item removed.")
    else:
        print("Item ID not found in cart.")

def checkout_flow(cart: Cart) -> None:
    if cart.is_empty():
        print("Cart is empty.")
        return
    path = cart.write_receipt()
    db.append_order_history({
        "total": cart.total(),
        "items": [{"id": c.item_id, "name": c.name, "qty": c.qty, "unit_price": c.unit_price} for c in cart.items]
    })
    print_header("CHECKOUT")
    print(f"Receipt saved: {path}")

def main_loop() -> None:
    cart = Cart()
    while True:
        print_header("ONLINE FOOD ORDERING SYSTEM")
        print("1) View Menu")
        print("2) Add Item")
        print("3) View Cart")
        print("4) Remove Item")
        print("5) Checkout")
        print("0) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            show_menu()
        elif choice == "2":
            show_menu()
            add_flow(cart)
        elif choice == "3":
            show_cart(cart)
        elif choice == "4":
            show_cart(cart)
            remove_flow(cart)
        elif choice == "5":
            show_cart(cart)
            checkout_flow(cart)
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid choice.")
        input("\nPress ENTER to continue...")

if __name__ == "__main__":
    main_loop()