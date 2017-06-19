try:
    while True:
		person = raw_input('Enter your name: ')
		print 'Hello ' + person
except KeyboardInterrupt:
    print('interrupted!')