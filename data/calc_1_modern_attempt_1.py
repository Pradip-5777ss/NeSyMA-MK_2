def calculate_total(price: float, tax_rate: float) -> float:
    """Calculates the total price including tax.

    Args:
        price: The base price of the item.
        tax_rate: The tax rate as a decimal (e.g., 0.15 for 15%).

    Returns:
        The total price after tax.
    """
    tax = price * tax_rate
    total = price + tax
    return total

if __name__ == "__main__":
    result = calculate_total(100.0, 0.15)
    print(f"Total: {result}")