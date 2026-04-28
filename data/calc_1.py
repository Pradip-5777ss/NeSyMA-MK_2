def calculate_total(price, tax_rate):
    tax = price * tax_rate
    total = price + tax
    return total

if __name__ == "__main__":
    result = calculate_total(100.0, 0.15)
    print("Total:", result)
