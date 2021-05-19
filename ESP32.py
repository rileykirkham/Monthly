def storeCalendarData(storage):
	f = open("CalendarLog.txt","r")
	data = f.readlines()
	for index,line in enumerate(data):
		storage[index] = line


def main():
	storage = {}
	storeCalendarData(storage)
	print(storage)

	
	

if __name__ == '__main__':
	main()