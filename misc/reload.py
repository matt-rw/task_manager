from table import *

def main():
	table = Table()
	table.read()
	table.write()
	table.formatOut()
	with open('out.txt', 'r') as data:
		print(data.read())
main()
