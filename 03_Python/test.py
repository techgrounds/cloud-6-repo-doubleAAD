x = 100
while x:
    guess = int(input("Guess a number: "))
    if guess < x:
        print(guess, "is pretty low")
    if guess > x:
        print(guess, "is pretty high")
    if guess == x:
        print(guess, "is the right number!")
        break

