def calculate_factorial(n):
    if n < 0:
        return None
    result = 1
    i = 1
    while i <= n:
        result = result * i
        i += 1
    return result

if __name__ == "__main__":
    fact = calculate_factorial(5)
    print("Factorial of 5:", fact)
