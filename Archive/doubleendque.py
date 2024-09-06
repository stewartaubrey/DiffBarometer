from ucollections import deque

#def collect_recent_numbers():
maxlen=3
recent_numbers = deque([],maxlen)

while True:
    user_input = input("Enter a number (or type 'done' to finish): ")
    if user_input.lower() == 'done':
        break
    try:
        number = float(user_input)
        recent_numbers.append(number)
        #print(f"Recent numbers: {list(recent_numbers)}")
        print(recent_numbers)
    except ValueError:
        print("Please enter a valid number.")

print("Final list of recent numbers:", list(recent_numbers))
print(sum(recent_numbers))
    
#collect_recent_numbers()