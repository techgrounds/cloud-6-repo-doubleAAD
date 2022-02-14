        
# Fix 1  
            '''
        The output should be:
        hello Casper
        hello Floris
        hello Esther
            '''
        foo = 'hello'
        ls = ['Casper', 'Floris', 'Esther']
        for name in ls:
	        print(loo,name)
## The code should be
        foo = 'hello'
        ls = ['Casper', 'Floris', 'Esther']
        for name in ls:
	        print(foo,name)

# Fix 2
        foo = 20
        bar = '80'
        print(foo + bar)
## The code should be
        foo = 20
        bar = 80
        print(foo + bar)

# Fix 3
        foo = 20
        for i in range(10):
	        foo -= 1
        print(foo)

## The code should be
        foo = 20
        for i in range(10):
	        foo += 1

        print(foo)

# Fix 4 

        '''
        The output should be:
        there are 0 kids on the street
        there are 1 kids on the street
        there are 2 kids on the street
        there are 3 kids on the street
        there are 4 kids on the street
        '''

        foo = 0
        while foo <= 5:
	        print('there are', foo, 'kids on the street')
	        foo += 1

## The code should be
        foo = 0
        while foo <= 4:
	        print('there are', foo, 'kids on the street')
	        foo += 1

# Fix 5

- The out put should be: Start Wars

        ls = ['Lord of the rings', 'Star Trek', 'Iron Man', 'Star Wars']
                 ↓
        print(ls[4])
                 ↑

## The code should be
        ls = ['Lord of the rings', 'Star Trek', 'Iron Man', 'Star Wars']
        print(ls[3])

# Fix 6

- The out put should be: 80

        foo = 80
        if foo < 30:
	        print(foo)
        else:
	        print('big number wow')
        elif foo < 100:
	        print(foo)
## The code should be
        foo = 80
        if foo < 30:
	        print(foo)
        elif foo < 100:
	        print(foo)    
        else:
	        print('big number wow')

# Fix 7
            '''
        The output should be:
        ['Dog', 'Cat', 'Fly']
            '''

        ln = ['Dog', 'Cat', 'Elephant', 'Fly', 'Horse']
        short_names = []

        for animal in ln:
	        if len(animal) == 3:
		        short_names.append(animal)
	        short_names = []

        print(short_names)
## The code should be

        ln = ['Dog', 'Cat', 'Elephant', 'Fly', 'Horse']
        short_names = []
        for animal in ln:
            if len(animal) == 3:
                short_names.append(animal)
        print(short_names)

# Fix 8
            '''
        The output should be:
        20
            '''
        foo = 10
        bar = 2
        print(foo**bar)

## The code should be

        foo = 10
        bar = 2
        print(foo * bar)

# Fix 9


            '''
        The output should be:
        0
        1
        2
        3
        4
        8
        9
            '''

        for i in range(10):
	        if i < 5:
		        print(i)
	        elif i < 8:
		        break
	        else:
		        print(i)
        
## The code should be

        for i in range(10):
	        if i < 10:
		        print(i)
	        elif i < 8:
		        break
	        else:
		        print(i)

# Fix 10
            '''
        The output should be:
        the number is 20
            '''
        print('the number is' + 20)


## The code should be

        print('the number is ' + '20')


# Fix 11
                '''
        The output should be:
        IT LIVES!
                '''

        dev monster():
	print('IT LIVES!')
        monster()


## The code should be

        
        def monster():
	        print('IT LIVES!')
        monster()

# Fix 12
                '''
        The output should be:
                4
                16129
                '''

        def square(x):
	        return x**2

        nr = square(2)
        print(nr)

        big = square(foo)
        print(big)

        foo = 127


## The code should be

        def square(x):
	        return x**2

        nr = square(2)
        print(nr)

        foo = 127

        big = square(foo)
        print(big)

# Fix 13
                '''
        The output should be:
        Your random number is: <insert random number here>
                '''
        import random

        random.randint(1,100)
        print("Your random number is:")


## The code should be

        import random

        a = random.randint(1,100)
        print(f'{"Your random number is:"}{a}')
        

# Fix 14
                '''
        The output should be:
                True
                '''
        def rtn(x):
	        return(x)

        foo = rtn(3)

        if foo > rtn(4):
	        print(True)
        else:
	        print(False)


## The code should be

        def rtn(x):
	        return(x)

        foo = rtn(7)

        if foo > rtn(4):
	        print(True)
        else:
	        print(False)



# Fix 15
                '''
        The output should be:
        a5|||5|||5|||a5|||5|||5|||a5|||5|||5|||
                '''

        foo = ''
        for i in range(3):
	        foo += 'a'
	        for j in range(3):
		foo += '5'
	        for k in range(3):
		foo += '|'

        print(foo)


## The code should be

        foo = ''
        for i in range(3):
	        foo += 'a'
	        for j in range(3):
		        foo += '5'
	                for k in range(3):
		                foo += '|'

        print(foo)




# Fix 16
                '''
        The output should be:

                '''
        import random

        # generate random int
        goal = random.randint(1,100)

        win = False
        tries = 0

        while win == False and tries < 7:
	try:
		# ask for input
		inpt = int(input("Please input a number between 1 and 100: "))
		# count attempt as a try
		tries += 1

		# check for match
		if inpt == goal:
			win = True
			print("Congrats, you guessed the number!")
			print("It took you", tries, "tries")
		# give hints
		elif inpt < goal:
			print("The number should be higher")
		else:
			print("The number should be lower")

	except:
		print("Please type an integer")

        # 
        if win == False:
	print("Game over! You took more than seven tries")


## The code should be

        import random

        # generate random int
        goal = random.randint(1,100)

        win = False
        tries = 0

        while win == False and tries < 7:
	try:
		# ask for input
		inpt = int(input("Please input a number between 1 and 100: "))
		# count attempt as a try
		tries += 1

		# check for match
		if inpt == goal:
			win = True
			print("Congrats, you guessed the number!")
			print("It took you", tries, "tries")
		# give hints
		elif inpt < goal:
			print("The number should be higher")
		else:
			print("The number should be lower")

	except:
		print("Please type an integer")

        # 
        if win == False:
	print("Game over! You took more than seven tries")




