
numbers = []
total = 0

while True:
    try:
        num = float(input("Enter a number (or type 'done' to finish): "))
        numbers.append(num)
        total += num
        avg = total / len(numbers)
        print(f"Running average: {avg}")
    except ValueError:
        break

print("Final list of numbers:", numbers)
print("Final average:", total / len(numbers) if numbers else 0)