        
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


