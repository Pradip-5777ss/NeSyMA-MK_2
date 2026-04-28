def apply_discount(price, is_member):
    if is_member:
        discount = price * 0.20
    else:
        discount = price * 0.05
    return price - discount

if __name__ == "__main__":
    final_price = apply_discount(200.0, True)
    print("Final price:", final_price)
