from table import *
from task import *
import library
import sys
import os
import time
import math
dl_path = './library'
sys.path.insert(0, dl_path)

class Editor():
	def __init__(self, table):
		self.t = table
		self.menu()

	def menu(self):
		os.system('clear')
		options = f'Task Manager\n\nTask Commands: \n 1 | Add \n 2 | End \n 3 | Edit \n\nView Commands: \n 4 | Today \n 5 | Task \n 6 | Book \n 7 | All \n\nGroup Commands: \n 8 | Edit \n 9 | View \n\n 0 | Exit \n'
		print(options)
		option = input('Enter number: \n')
		if option == '1':
			self.addTask()
		elif option == '2':
			self.endTask()
		elif option == '3':
			self.editTask()
		#elif option == '4':
		#	self.viewLast()
		elif option == '4':
			self.viewToday()
		elif option == '5':
			self.viewByType()
		elif option == '6':
			self.viewBook()
		elif option == '7':
			self.viewAll()
		elif option == '8':
			self.editGroup()
		elif option == '9':
			self.viewGroups()
		elif option == '0':
			os.system('clear')
			sys.exit()
		else:
			os.system('clear')
			print(options)
			print(f'Invalid command: \n{option}')
			time.sleep(2)
			self.menu()

	def addTask(self):
		os.system('clear')
		task = Task()
		if self.t.getState() == 0:
			os.system('clear')
			print(f'Error: End current task.')
			time.sleep(2)
			self.menu()		
		task.start = Table.convertToTwelve(Table.getTime())
		task.end = '...'
		date = Table.getToday()
		options = f'Add Task \n\nTask Information \n 1 | Name        | {task.name} \n 2 | Date        | {date} \n 3 | Start time  | {task.start} \n 4 | End time    | {task.end} \n 5 | Description | {task.desc} \n\n 8 | Add task \n\n 0 | Cancel \n'
		print(options)
		book = ''
		page_start = ''
		page_end = ''
		while True:
			option = input('Enter number: \n')
			if option == '1':
				os.system('clear')
				print(options)
				task.name = input('Name: \n')
				""" Digital Library integration """
				if task.name == 'READ': # adjust code in options
				#	event = book.Book.emptyEvent()
				#	dl = cli_dl.CLI(path)
				#	book_o = dl.bookList()
				#	title = book_o.title
					books = library.Books()
					book = books.bookList()
					#options = f'Add Task \n\nTask Information \n 1 | Name        | {task.name} \n 2 | Start time  | {task.start} \n 3 | End time    | {task.end}\n'
					options = f'Add Task \n\nTask Information \n 1 | Name        | {task.name} \n 2 | Date        | {date} \n 3 | Start time  | {task.start} \n 4 | End time    | {task.end} \n 5 | Description | {task.desc} \n'
					options+= f' 5 | Book        | {book} \n'
					options+= f' 6 | Start page  | {page_start} \n 7 | End page    | {page_end} \n\n'
					options+= f' 8 | Add task \n\n 0 | Cancel \n'
					# pull up book list
					# select book
					# enter fields for new event
					# save and write to file
					#books = book.
				else:
					book = ''
					page_start = ''
					page_end = ''
					#options = f'Add Task \n\nTask Information \n 1 | Name        | {task.name} \n 2 | Start time  | {task.start} \n 3 | End time    | {task.end} \n 4 | Description | {task.desc} \n\n'
					#options = f'Add Task \n\nTask Information \n 1 | Name        | {task.name} \n 2 | Date        | {date} \n 4 | Start time  | {task.start} \n 3 | End time    | {task.end} \n 4 | Description | {task.desc} \n\n 7 | Add task \n\n 0 | Cancel \n'
					options = f'Add Task \n\nTask Information \n 1 | Name        | {task.name} \n 2 | Date        | {date} \n 3 | Start time  | {task.start} \n 4 | End time    | {task.end} \n 5 | Description | {task.desc} \n\n 8 | Add task \n\n 0 | Cancel \n'
					#options+= f' 7 | Add task \n\n 0 | Cancel \n'
			elif option == '2':
				os.system('clear')
				print(options)
				date = input('Date (M/D/Y): \n')
			elif option == '3':
				os.system('clear')
				print(options)
				task.start = input('Start time (hh:mm AM/PM): \n')
			elif option == '4':
				os.system('clear')
				print(options)
				task.end = input('End time (hh:mm AM/PM): \n')
			elif option == '5':
				os.system('clear')
				print(options)
				if task.name == 'READ':
					book = library.Books().bookList()
				else:
					task.desc = input('Description: \n')
			elif option == '6' and book != '':
				os.system('clear')
				print(options)
				page_start = input('Start page: \n')
			elif option == '7' and book != '':
				os.system('clear')
				print(options)
				page_end = input('End page: \n')
			elif option == '8':
				if task.name == '':
					os.system('clear')
					print(options)
					print(f'Invalid name.')#: \n{task.name}')
					time.sleep(2)
				else:
					if task.name == 'READ':
						if page_end == '':
							page_end = '...'
						task.desc = f'{book} (pages {page_start}-{page_end})'
							# DL: add new event
						#	event.date = book.Book.strDate()
						#	event.time_start = task.start
						#	if task.end != '...' and task.end != 0:
						#		event.time_end = task.end
						#	book_o = book.Book.insertEvent(book_o, event)
						#	book.Book.saveBook(book_o, path=path)
							
					self.t.addTask(task, date)
					self.t.write()
					os.system('clear')
					print(options)
					print('Task added.')
					time.sleep(2)
					self.menu()
			elif option == '0':
				self.menu()
			else:
				os.system('clear')
				print(options)
				print(f'Invalid command: \n{option}')
				time.sleep(2)
			os.system('clear')
			if task.name == 'READ':
				#options = f'Add Task \n\nTask Information \n 1 | Name        | {task.name} \n 2 | Start time  | {task.start} \n 3 | End time    | {task.end}\n'
				#options = f'Add Task \n\nTask Information \n 1 | Name        | {task.name} \n 2 | Date        | {date} \n 4 | Start time  | {task.start} \n 3 | End time    | {task.end} \n 4 | Description | {task.desc} \n\n 7 | Add task \n\n 0 | Cancel \n'
				options = f'Add Task \n\nTask Information \n 1 | Name        | {task.name} \n 2 | Date        | {date} \n 3 | Start time  | {task.start} \n 4 | End time    | {task.end} \n 5 | Description | {task.desc} \n'
				options+= f' 5 | Book        | {book} \n'
				options+= f' 6 | Start page  | {page_start} \n 7 | End page    | {page_end} \n\n'
				options+= f' 8 | Add task \n\n 0 | Cancel \n'
			else: 
				#options = f'Add Task \n\nTask Information \n 1 | Name        | {task.name} \n 2 | Start time  | {task.start} \n 3 | End time    | {task.end} \n 4 | Description | {task.desc} \n\n'
				#options = f'Add Task \n\nTask Information \n 1 | Name        | {task.name} \n 2 | Date        | {date} \n 4 | Start time  | {task.start} \n 3 | End time    | {task.end} \n 4 | Description | {task.desc} \n\n 7 | Add task \n\n 0 | Cancel \n'
				options = f'Add Task \n\nTask Information \n 1 | Name        | {task.name} \n 2 | Date        | {date} \n 3 | Start time  | {task.start} \n 4 | End time    | {task.end} \n 5 | Description | {task.desc} \n\n 8 | Add task \n\n 0 | Cancel \n'
			print(options)

	def endTask(self):
		if self.t.getState() == 0:
			# task.name == 'READ':
				#if task.desc[-3:] == '...':
				#	page_end = input('End page:\n')
				#	task.desc[-3:] = page_end
			task = self.t.endTask()
				#path = './library/'
				#dl = cli_dl.CLI(path)
				#dl.end(write=True, out=False, time_end=book.Book.strTime())
			duration = Table.timeDifference(task.start, task.end)
			os.system('clear')
			print(f'End Task \n\n')
			print(f'\nTask {task.name}: {Table.convertToTwelve(task.start)}-{Table.convertToTwelve(task.end)}')
			print(f'Duration: {duration}')
			if task.name == 'READ':
				print(task.desc)
			time.sleep(3)
			self.t.write()
			self.t.formatOut()
		else:
			os.system('clear')
			print(f'End Task \n\n')
			print(f'No task available to end.')
			time.sleep(2)
		self.menu()

	def editTask(self, date=None, date_page=0, task_page=0):
		# Date list
		if not date:
			dates = []
			for date in self.t.table:
				dates.append(date)
			date, date_page = self.listItemsOut(dates, date_page, length=5, header='Select date')
			if date==0: self.menu()	
			date = date.strip()
		# Task list
		tasks = []
		for task in self.t.table[date]:
			for i in range(len(self.t.table[date][task])):
				if i > 0:
					name = task
					start, end = self.t.table[date][task][i][:2]
					start = Table.convertToTwelve(start)
					if end == 0: end = '...'
					else: end = Table.convertToTwelve(end)
					tasks+= [f'{name}: {start} - {end}']
		task_old, task_page = self.listItemsOut(tasks, task_page, length=5, header='Select task')
		if task_old==0: self.editTask(date=None, date_page=date_page)
		task_obj = Task()
		task_name = task_old[:task_old.index(':')]
		start_time = task_old[task_old.index(':')+2:task_old.index('-')-1]
		start_time = Table.convertToTwentyFour(start_time)
		for i in range(len(self.t.table[date][task_name])):
			if start_time == self.t.table[date][task_name][i][0]:
				task_obj.name = task_name
				task_obj.start = self.t.table[date][task_name][i][0]
				task_obj.start = Table.convertToTwelve(task_obj.start)
				task_obj.end = self.t.table[date][task_name][i][1]
				task_old = Task()
				task_old.name = task_name
				task_old.start = self.t.table[date][task_name][i][0]
				task_old.end = self.t.table[date][task_name][i][1]
				task_old.desc = self.t.table[date][task_name][i][2]
				if task_obj.end == 0: task_obj.end = '...'
				else: task_obj.end = Table.convertToTwelve(task_obj.end)
				task_obj.desc = self.t.table[date][task_name][i][2]
		task_new = self.taskFields('Edit Task', 'Edit task', 'Delete task', task_obj)
		if task_new == 0: self.editTask(date, date_page, task_page)
		elif task_new==2: 
			self.t.deleteTask(date, task_old)
			self.t.write()
			print('\nTask deleted.\n')
			time.sleep(4); self.editTask(date_page=date_page)
		else:
			if task_new.end == '...': task_new.end = 0
			val = self.t.editTask(date, task_old, task_new)
			if val == 0:
				#os.system('clear')
				print('\nInvalid edit.\n')
			elif val==1:
				self.t.write()
				#os.system('clear')
				print('\nTask edited.\n')
			time.sleep(4); self.editTask(date_page=date_page)

	def taskFields(self, header, cmd_name, cmd_name2=None, task=None):
		os.system('clear')
		if not task:
			task = Task()
			task.start = Table.convertToTwelve(Table.getTime())
			task.end = '...'
		s_list = [header+'\n']
		s_list+= ['Task Information']
		s_list+= [f' 1 | Name        | {task.name} ']
		#s_list+= [f' 2 | Date        | {} ']
		s_list+= [f' 2 | Start time  | {task.start}']
		s_list+= [f' 3 | End time    | {task.end} ']
		book = ''
		page_start = ''
		page_end = ''
		if task.name == 'READ':
			idx = task.desc.index(' (pages')
			book = task.desc[:idx]
			hyphen = idx + task.desc[idx:].index('-')
			page_start = task.desc[idx+len(' (pages '):hyphen]
			page_end = task.desc[hyphen+1:-1]
			s_list+= [f' 4 | Book        | {book}']
			s_list+= [f' 5 | Start page  | {page_start}']
			s_list+= [f' 6 | Start end   | {page_end}']
		else:
			s_list+= [f' 4 | Description | {task.desc} ']
		s_list+= [f'\n 7 | {cmd_name} ']
		if cmd_name2: s_list+= [f' 8 | {cmd_name2} ']
		s_list+= ['\n 0 | Cancel \n']
		for i in s_list: print(i)
		while True:
			option = input('Enter number: \n')
			if option == '1':
				name_prv = task.name
				os.system('clear')
				for i in s_list: print(i)
				task.name = input('Name: \n')
				if name_prv == 'READ' and task.name != 'READ':
					s_list = s_list[:5]
					task.desc = ''
					s_list+= [f' 4 | Description | {task.desc} ']
					s_list+= [f'\n 7 | {cmd_name} ']
					if cmd_name2: s_list+= [f' 8 | {cmd_name2} ']
					s_list+= ['\n 0 | Cancel \n']
				elif name_prv != 'READ' and task.name == 'READ':
					s_list = s_list[:5]
					s_list+= [f' 4 | Book        | {book}']
					s_list+= [f' 5 | Start page  | {page_start}']
					s_list+= [f' 6 | Start end   | {page_end}']
					s_list+= [f'\n 7 | {cmd_name} ']
					if cmd_name2: s_list+= [f' 8 | {cmd_name2} ']
					s_list+= ['\n 0 | Cancel \n']
					book = library.Books().bookList()
					page_start = ''
					page_end = ''
					task.desc = ''
			elif option == '2':
				os.system('clear')
				for i in s_list: print(i)
				task.start = input('Start time (hh:mm AM/PM): \n')
			elif option == '3':
				os.system('clear')
				for i in s_list: print(i)
				task.end = input('End time (hh:mm AM/PM): \n')
			elif option == '4' and task.name != 'READ':
				os.system('clear')
				for i in s_list: print(i)
				task.desc = input('Description: \n')
			elif option == '4' and task.name == 'READ':
				os.system('clear')
				for i in s_list: print(i)
				book = library.Books().bookList()
			elif option == '5' and task.name == 'READ':
				os.system('clear')
				for i in s_list: print(i)
				page_start = input('Start page: \n')
			elif option == '6' and task.name == 'READ':
				os.system('clear')
				for i in s_list: print(i)
				page_end = input('End page: \n')
			elif option == '7':
				if task.name == '':
					os.system('clear')
					for i in s_list: print(i)
					print(f'Invalid name.')#: \n{task.name}')
					time.sleep(2)
				else:
					if task.name == 'READ':
						task.desc = f'{book} (pages {page_start}-{page_end})'
					return task
			elif cmd_name2 and option == '8':
				return 2
			elif option == '0':
				return 0
			else:
				os.system('clear')
				for i in s_list: print(i)
				print(f'Invalid command: \n{option}')
				time.sleep(2)
			s_list[2] = f' 1 | Name        | {task.name} '
			s_list[3] = f' 2 | Start time  | {task.start}'
			s_list[4] = f' 3 | End time    | {task.end} '
			if task.name == 'READ':	
				s_list[5] = f' 4 | Book        | {book}'
				s_list[6] = f' 5 | Start page  | {page_start}' 
				s_list[7] = f' 6 | End page    | {page_end}'
			else:
				s_list[5] = f' 4 | Description | {task.desc} '
			os.system('clear')			
			for i in s_list: print(i)
	def taskList(self):
		tasks = self.t.getAllTasks()
		task, page = self.listItemsOut(tasks, page=0, length=5, header='Select task')
		return task, page
	def listItems(items, page=0, length=5, cmd=1, header='', scroll=True, request=True):
		page_items = items[length*page:length*(page+1)]
		#if len(page_items) == 0:
		#	return None
		max_l = 0
		page_range = range(len(page_items))
		for i in page_range:
			if len(page_items[i]) > max_l: max_l = len(page_items[i])
		for i in page_range:
			if len(page_items[i]) < max_l: page_items[i] += ' '*(max_l - len(page_items[i]))
		s_list = []
		if header: s_list+= [header+'\n']
		for i in page_range:
			s_list += [f' {cmd} | {page_items[i]}']
			cmd += 1
		if scroll:
			cmd = length+1
			s_list += [f'\n 8 | Previous page']; cmd += 1
			s_list += [f' 9 | Next page']
		return s_list
	def listItemsOut(self, items, page, length, header):
		s_list = Editor.listItems(items, page, length, header=header)
		s_list+= ['\n 0 | Back\n']
		os.system('clear')
		for item in s_list: print(item)
		option = input('Enter number:\n')
		cmd = 1
		if not option.isnumeric():
			os.system('clear')
			for i in s_list: print(i)
			print('Invalid command.')
			time.sleep(2)
			return self.listItemsOut(items, page, length, header)
		if 1<=int(option)<=5:
			item = items[(length*page)+(int(option)-cmd)]
			return item, page
		elif int(option) == 8:
			if page == 0:
				os.system('clear')
				for i in s_list: print(i)
				print('Already on first page.')
				time.sleep(2)
				return self.listItemsOut(items, page, length, header)
			else: 
				return self.listItemsOut(items, page-1, length, header)
		elif int(option) == 9:
			if len(items[5*(page+1):5*(page+1)*2]) == 0:
				os.system('clear')
				for i in s_list: print(i)
				print('Already on last page.')
				time.sleep(2) 
				return self.listItemsOut(items, page, length, header)
			else: 
				return self.listItemsOut(items, page+1, length, header)
		elif int(option) == 0:
			return 0, page
		else:
			os.system('clear')
			for i in s_list: print(i)
			print('Invalid command.')
			time.sleep(2); 
			return self.listItemsOut(items, page, length, header)
	def viewLast(self):
		if len(self.t.table) == 0:
			os.system('clear')
			print('No tasks available.')
			time.sleep(2); self.menu()
		else:
			last_date = 0
			for date in self.t.table:
				last_date = date
			last_task = 0
			last_entry = 0
			last_entry_start = '00:00'
			for task in self.t.table[last_date]:
				for entry in self.t.table[last_date][task][1:]:
					if Table.timeGreaterThan(entry[0], last_entry_start):
						last_task = task
						last_entry = entry
						last_entry_start = entry[0]
			s = self.t.printEntry(last_date, last_task, last_entry)
			s+= '\n'
			os.system('clear')
			print(s)
			print('0 | Back \n')
			option = input('Enter number: \n')
			if option == '0':
				self.menu()
			else:
				os.system('clear')
				print(s)
				print('0 | Back\n')
				print('Invalid command. ')
				time.sleep(2)
				self.viewLast()
	def viewToday(self):
		s = self.t.dateTasksToString(Table.getToday())
		os.system('clear')
		if s == '':
			print('No tasks available. \n')
		else:
			print(s)
		print('0 | Back \n')
		option = input('Enter number: \n')
		if option == '0':
			self.menu()
		else:
			os.system('clear')
			print(s)
			print('0 | Back\n')
			print('Invalid command. ')
			time.sleep(2)
			self.viewToday()
	def getTypeChart(self, durations, max_dur, args:dict):
		rows=args['rows']+1 # with axis labels
		cols=args['cols']+1 
		col_size=args['col_size']
		marker=args['marker']
		empty=args['empty']
		start_date=args['start']
		# 20 x 19 graph of duratiIons
		# rows down from 16 with scroll # original: 21 with 20 including 0 and lowest axis
		# cols including y-axis labels, cols = 8 for one week
		# max cols for regular sized terminal window = 15
		# col size 6 min col size with today marked
		marker = marker + ' '*(col_size-1)
		empty = empty + ' '*(col_size-1)
		if max_dur == '0:00':
			if rows-2 < 10:
				max_dur = '0:0'+str(rows-2)
			elif rows-2 >= 10:
				max_dur = '0:'+str(rows-2)
		max_hr, max_min = max_dur.rsplit(':')
		max_dur_min = (int(max_hr) * 60) + int(max_min)
		step = max_dur_min / (rows-2)
		chart = [['']*cols]*rows
		start = False
		x_labels = []
		d_i = start_date
		x_labels.append(d_i)
		for j in range(cols-2):
			d_i = Table.addDay(d_i)
			x_labels.append(d_i)
		y_labels = []
		for i in range(rows-1):
			y_labels.append(math.ceil(step*(rows-2-i)))
		s = ''
		duration_gt_zero = []
		for i in range(rows):
			for j in range(cols):
				if i == rows - 1: # x-axis
					if j == 0:
						s+=' '*col_size
					else:
						mo_x, day_x, yr_x = x_labels[j-1].rsplit('/')
						abrv = ''
						if x_labels[j-1] == Table.getToday():
							abrv+='*' # today marker
						abrv+= mo_x+'/'+day_x
						if len(abrv) < col_size:
							dif = col_size - len(abrv)
							abrv += ' '*dif
						s += abrv
				elif j == 0: # y-axis
					y_label = str(y_labels[i])
					y_label = Table.convertMinToTwentyFour(y_label)
					dur_y_len = len(y_label)
					if dur_y_len < col_size:
						dif = col_size - dur_y_len
						y_label += ' '*dif
					elif dur_s_len > col_size:
						print('Error: max duration exceeded.')
						time.sleep(2)
						return
					s+=y_label
				elif j > 0:
					date = x_labels[j-1]
					if date in durations:
						dur = durations[date]
						d_hr, d_min = dur.rsplit(':')
						dur_min = (int(d_hr) * 60) + int(d_min)
						# options: choose closest row, or first row gt next
						# change: choose next row that is gt, ie floor
						if dur_min >= y_labels[i]:
							s+=marker
							durations.pop(date)
							duration_gt_zero.append(date)
						else:
							s+=empty
					else: # date either has 0 duration or has not occurred
						# 0 duration
						# check if date is before today's date
						date_ete = Table.isDateEarlierThanOrEqual(date, Table.getToday())
						if date_ete and (date not in duration_gt_zero):
							if i == rows-2: # duration 0
								s+=marker
							else:
								s+=empty
						else:
							s+=empty
			if i < rows-1:
				s+='\n'
		return s
	def chartOptions(self, chart_options):
		co = chart_options
		options = 'Chart Options\n\n'
		options+= f' 1 | First date  | {co["start"]}\n'
		options+= f' 2 | Rows        | {co["rows"]}\n'
		options+= f' 3 | Columns     | {co["cols"]}\n'
		options+= f' 4 | Column size | {co["col_size"]}\n'
		options+= f' 5 | Item mark   | {co["marker"]}\n'
		options+= f' 6 | Empty mark  | {co["empty"]}\n\n'
		options+= ' 0 | Back \n'
		while True:
			os.system('clear')
			print(options)
			cmd = input('Enter command: \n')
			if cmd == '1':
				os.system('clear')
				print(options)
				co['start'] = input('Enter first date: \n')
			elif cmd == '2':
				os.system('clear')
				print(options)
				co['rows'] = int(input('Enter rows: \n'))
			elif cmd=='3':
				os.system('clear')
				print(options)
				co['cols'] = int(input('Enter rows: \n'))
			elif cmd=='4':
				os.system('clear')
				print(options)
				co['col_size'] = int(input('Enter column size: \n'))
			elif cmd=='5':
				os.system('clear')
				print(options)
				co['marker'] = input('Enter item mark: \n')
			elif cmd=='6':
				os.system('clear')
				print(options)
				co['empty'] = input('Enter empty mark: \n')
			elif cmd=='0':
				return co
			else:
				os.system('clear')
				print(options)
				print('Invalid command.')
				time.sleep(2)	 
			options = 'Chart Options\n\n'
			options+= f' 1 | First date  | {co["start"]}\n'
			options+= f' 2 | Rows        | {co["rows"]}\n'
			options+= f' 3 | Columns     | {co["cols"]}\n'
			options+= f' 4 | Column size | {co["col_size"]}\n'
			options+= f' 5 | Item mark   | {co["marker"]}\n'
			options+= f' 6 | Empty mark  | {co["empty"]}\n\n'
			options+= ' 0 | Back \n'
	def viewByType(self, task=None, chart_options=None, book=None):
		os.system('clear')
		if task is None:
			#task = input('Task name: \n')
			task_i, page_task = self.taskList()
			if task_i != 0:
				task = task_i
			else:
				self.menu()
		if not self.t.isTaskInTable(task):
			print(f'No tasks available for {task}.')
			time.sleep(2)
			self.viewByType()
		title = f'Chart of durations: {task}'
		min_dur = '0:00'
		max_dur = '0:00'
		if chart_options is None:
			chart_options = {'start':None, 'rows':12, 'cols':12, 'col_size':6, 'marker':'o', 'empty':'.'}
		if chart_options['start'] is None:
			chart_options['start'] = Table.subDay(Table.getToday(), repeat=chart_options['cols']//2)
		# make start date approx. 5 days before today's date if available
		today = Table.getToday()
		durations = {}
		if book is None:
			for date in self.t.table:
				if task in self.t.table[date]:
					if chart_options['start'] == '':
						chart_options['start'] = date
					duration = self.t.getDuration(self.t.table[date][task])
					durations[date] = duration
					if Table.timeGreaterThan(min_dur, duration):
						min_dur = duration
					if Table.timeGreaterThan(duration, max_dur):
						max_dur = duration
		else:
			book_duration, durations = self.t.getBookDuration(book)
		chart = self.getTypeChart(durations, max_dur, chart_options)
		os.system('clear')
		if book is not None:
			book_s = book
			if len(book) > 40:
				book_s = book[:37]+'...'
			title+= f' {book_s} ({book_duration})'
		#	title+= f' (total duration for {book}: {book_duration})'
		print(title+'\n')
		print(chart+'\n')
		options = ' 1   | Change task \n'
		options+= ' 2   | Options \n'
		if task == 'READ':
			options+= ' 3   | Select Book \n'
		options+= ' 8/9 | Previous/Next page\n'
		options+= ' 0   | Back\n'
		print(options)
		option = input('Enter command: \n')
		if option == '1':
			os.system('clear')
			print(title+'\n')
			print(chart+'\n')
			print(options)
			#new_task = input('Enter task: \n')
			new_task, page_task = self.taskList()
			if new_task == 0:
				new_task = task
			if not self.t.isTaskInTable(new_task):
				os.system('clear')
				print(title+'\n')
				print(chart+'\n')
				print(options)
				sys.stdout.write(f'No tasks available for: \n{new_task}')
				sys.stdout.flush()
				time.sleep(2)
				self.viewByType(task, chart_options, book)
			else:
				self.viewByType(new_task, chart_options, book=None)
		elif option == '2':
			chart_options = self.chartOptions(chart_options)
			self.viewByType(task, chart_options, book)
		elif option == '3' and task == 'READ':
			new_book = library.Books().bookList()
			if new_book == 0:
				self.viewByType(task, chart_options, book)
			else:
				book = new_book
				book_duration, durations = self.t.getBookDuration(book)
				self.viewByType(task, chart_options, book)
		elif option == '8': # prev page
			cols = chart_options['cols']
			chart_options['start'] = Table.subDay(chart_options['start'], repeat=cols)
			self.viewByType(task, chart_options, book)
		elif option == '9':# next page
			cols = chart_options['cols']
			chart_options['start'] = Table.addDay(chart_options['start'], repeat=cols)
			self.viewByType(task, chart_options, book)
		elif option == '0':
			self.menu()
		else:
			os.system('clear')
			print(title+'\n')
			print(chart+'\n')
			print(options)
			print('Invalid command.')
			# method to write w/o adding newline:
			#sys.stdout.write(f'Invalid command: \n{option}') # no newline
			#sys.stdout.flush()
			time.sleep(2)
			self.viewByType(task, chart_options, book)
	def viewBook(self):
		book = library.Books().bookList()
		if book == 0: 
			self.menu()
		else:
			book_events = self.t.getAllBookEvents(book)
			book_duration, date_durations = self.t.getBookDuration(book)
			# pass to view page in library module
			args = [book_events, book_duration, date_durations]
			library.Books.viewBook(book, args)

	def viewAll(self):
		# potentially write a scroll and only show tasks over a single date
		s = ''
		for date in self.t.table:
			s += self.t.dateDurationsToString(date)
		os.system('clear')
		if s == '':
			print('No tasks available. \n')
		else:
			print(s)
		print('0 | Back \n')
		option = input('Enter number: ')
		if option == '0':
			self.menu()
		else:
			os.system('clear')
			print(s)
			print('0 | Back\n')
			print('Invalid command.')
			time.sleep(2)
			self.viewAll()
