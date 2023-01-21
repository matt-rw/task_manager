import table

def main():
	table = Table()
	task = input('Task name: \n')
	table.read()
	if table.getState(task):
		table.startEntry(task)
	else:
		table.endEntry(task)
	table.printTask(task)
	table.write()
	table.formatOut()
main()
