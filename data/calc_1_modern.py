def calculate_total(price, tax_rate):
    return price + (price * tax_rate)

if __name__ == "__main__":
    result = calculate_total(100.0, 0.15)
    print("Total:", result)
