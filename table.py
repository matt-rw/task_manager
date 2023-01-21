from task import *
import datetime
import time
import ast
import copy

class Table:
	def __init__(self):
		self.table = {}
		self.state = 0
	def addNewDay(self, task):
		task = '' + task
		self.table[Table.getToday()] = {task : [('Duration: 0:00', 'Entries: 0')]}
		return self.getTaskToday(task)
	def addTask(self, task, date):
		row = 0
		try:
			tasks = self.getTasks(date)
			# if failed above, add new day
			# search for task, if none then create new
			if task.name in tasks:
				row = tasks[task.name]
			else:
				tasks[task.name] = [('Duration: 0:00', 'Entries: 0')]
				row = tasks[task.name]
		except:
			if date == Table.getToday():
				row = self.addNewDay(task.name)
			else: # add date into dictionary at correct location
				d1 = date
				d = {}
				i = 0
				n = len(self.table) - 1
				inserted = False
				for k in self.table:
					d2 = k
					date_copy = copy.deepcopy(self.table[d2])
					if Table.isDateEarlierThanOrEqual(d1, d2) and not inserted:
						d[d1] = {task.name : [('Duration: 0:00', 'Entries: 0')]}
						d[d2] = date_copy
						inserted = True
					elif i == n and not inserted:
						d[d2] = date_copy
						d[d1] = {task.name : [('Duration: 0:00', 'Entries: 0')]}
					else:
						d[d2] = date_copy
					i+= 1
				print(d)
				self.table = d
				row = self.table[date][task.name]
		if task.end == '...':
			task.end = 0
		# convert start/end time to 24hr format if necessary
		task.start = Table.convertToTwentyFour(task.start)
		task.end = Table.convertToTwentyFour(task.end)
		row.append((task.start,task.end,task.desc))
		entries = int((row[0][1])[9:]) + 1
		row[0] = (row[0][0], 'Entries: ' + str(entries))
		if task.end != 0:
			duration = self.entryDuration(row[-1])
			self.addDuration(row, duration)
	def endTask(self, name=None):
		if name == None:
			# search for ongoing task today
			for nm in self.getTasks(Table.getToday()):
				if self.table[Table.getToday()][nm][-1][1] == 0:
					name = nm
		row = self.getTaskToday(name)
		start = row[-1][0]
		end = Table.getTime()
		desc = row[-1][2]
		if name == 'READ' and desc[-4:-1] == '...':
			page_end = input('End page: \n')
			desc = desc[:-4]+page_end+')'
		row[-1] = (start, end, desc)
		self.addDuration(row, self.entryDuration(row[-1]))
		return Task(name, start, end, desc)
	def editTask(self, date, task_old, task_new):
		tasks = self.getTasks(date)
		duration_prv = tasks[task_old.name][0][0][10:]
		entries_prv = int(tasks[task_old.name][0][1][9:])
		old_tasks = copy.deepcopy(tasks)
		if entries_prv == 1:
			tasks.pop(task_old.name) # remove task from date
			# remove task from table if date is mutable
			#if len(self.table[date]) == 0:
			#	self.table.pop(date)
		else:
			for i in range(len(tasks[task_old.name])):
				entry = tasks[task_old.name][i]
				if entry[0] == task_old.start and entry[1] == task_old.end:
					tasks[task_old.name].pop(i) # remove old task entry
					#old_task_idx = i
					break
			if task_old.end != 0:
				# subtract old_task duration from duration_prv
				task_old_duration = Table.timeDifference(task_old.start, task_old.end)
				duration_temp = Table.timeDifference(task_old_duration, duration_prv)
			else:
				duration_temp = duration_prv
			entries_temp = str(entries_prv - 1)
			# set duration and entries values after removing task_old
			duration_temp = tasks[task_old.name][0][0][:10]+duration_temp
			entries_temp = tasks[task_old.name][0][1][:9]+entries_temp
			tasks[task_old.name][0] = (duration_temp, entries_temp)	
		# convert start/end time to 24hr format if necessary
		task_new.start = Table.convertToTwentyFour(task_new.start)
		task_new.end = Table.convertToTwentyFour(task_new.end)
		row = 0
		# add task_new to date
		if task_new.name in tasks:
			row = tasks[task_new.name]
		else:
			tasks[task_new.name] = [('Duration: 0:00', 'Entries: 1')]
			row = tasks[task_new.name]
			row.append((task_new.start,task_new.end,task_new.desc))
			if task_new.end != 0:
				duration = self.entryDuration(row[-1])
				self.addDuration(row, duration)
			return 1 # successful edit
		if task_new.end == '...':
			task_new.end = 0
		# find position of task in row; if time overlaps, return 0 for invalid
		new_row = [row[0]]
		new_inserted = 0
		# this does not compare other task names, only same task name
		# two tasks can currently overlap, therefore, if names are different
		for e_i in range(len(row[1:])):
			e_i_start = row[e_i+1][0]
			e_i_end = row[e_i+1][1]
			if e_i_end == 0:
				e_i_end = Table.getTime()
			t_n_end = task_new.end
			if t_n_end == 0:
				t_n_end = Table.getTime()
			new_start_later= Table.timeGreaterThan(task_new.start, e_i_start)#row[e_i+1][0])
			new_end_later = Table.timeGreaterThan(t_n_end, e_i_end) #row[e_i+1][1])
			new_end_later_than_start = Table.timeGreaterThan(t_n_end, e_i_start) #row[e_i+1][0])
			new_start_later_than_end = Table.timeGreaterThan(task_new.start, e_i_end) #row[e_i+1][1])
			if new_inserted:
				new_row.append(row[e_i+1])	
			# test if start and end is before new task start
			elif new_start_later and new_end_later:
				new_row.append(row[e_i+1])
				if e_i+2 == len(row):
					new_row.append((task_new.start,task_new.end,task_new.desc))
					new_inserted = e_i+2
			elif new_start_later and not new_end_later:
				# new task falls within another time slot in that task name
				self.table[date] = old_tasks
				return 0 # invalid edit
			elif not new_start_later and new_end_later:
				tasks = copy.deepcopy(old_tasks)
				self.table[date] = old_tasks
				return 0
			elif not new_start_later and new_end_later_than_start \
				and e_i_start != task_new.start:
				tasks = copy.deepcopy(old_tasks)
				self.table[date] = old_tasks
				return 0
			elif new_end_later and not new_start_later_than_end:
				tasks = copy.deepcopy(old_tasks)
				self.table[date] = old_tasks
				return 0
			else:
				new_row.append((task_new.start,task_new.end,task_new.desc))
				new_row.append(row[e_i+1])
				new_inserted = e_i+1
		if new_inserted:
			entries = int((new_row[0][1])[9:]) + 1
			new_row[0] = (new_row[0][0], 'Entries: ' + str(entries))
		if task_new.end != 0:
			duration = self.entryDuration(new_row[new_inserted])
			self.addDuration(new_row, duration)
		# add new row as task row
		tasks[task_new.name] = new_row
		return 1
	def deleteTask(self, date, task_old):
		tasks = self.getTasks(date)
		duration_prv = tasks[task_old.name][0][0][10:]
		entries_prv = int(tasks[task_old.name][0][1][9:])
		old_tasks = copy.deepcopy(tasks)
		if entries_prv == 1:
			tasks.pop(task_old.name) # remove task from date
			# check if there are any other tasks, otherwise remove date
			if len(self.table[date]) == 0:
				self.table.pop(date)
		else:
			for i in range(len(tasks[task_old.name])):
				entry = tasks[task_old.name][i]
				if entry[0] == task_old.start and entry[1] == task_old.end:
					tasks[task_old.name].pop(i) # remove old task entry
					#old_task_idx = i
					break
			# subtract old_task duration from duration_prv
			if task_old.end != 0:
				task_old_duration = Table.timeDifference(task_old.start, task_old.end)
				duration_temp = Table.timeDifference(task_old_duration, duration_prv)
				duration_temp = tasks[task_old.name][0][0][:10]+duration_temp
			else: duration_temp = duration_prv
			entries_temp = str(entries_prv - 1)
			# set duration and entries values after removing task_old
			entries_temp = tasks[task_old.name][0][1][:9]+entries_temp
			tasks[task_old.name][0] = (duration_temp, entries_temp)	
		return 1
	def entryDuration(self, entry):
		return Table.timeDifference(entry[0], entry[1])
	def addDuration(self, row, entry_duration):
		d = (row[0][0])[10:]
		new_d = Table.timeSummation(d, entry_duration)
		row[0] = ('Duration: ' + new_d, row[0][1])
	""" If entry is active, state = 0. Otherwise, state = 1 """
	def getState(self, name=None):
		try:
			row = 0
			if name is None:
				# search for ongoing task
				for nm in self.getTasks(Table.getToday()):
					 if self.table[Table.getToday()][nm][-1][1] == 0:
						 self.state = 0
						 return self.state
			else:
				row = self.getTaskToday(name)
			if name is not None and row[-1][1] == 0:
				self.state = 0
			else:
				self.state = 1
		except:
			self.state = 1
		return self.state	
	def write(self):
		with open('/Users/matthewwear/Desktop/t_manager/data/file.txt','w') as data:
			data.write(str(self.table))
	def read(self):
		with open('/Users/matthewwear/Desktop/t_manager/data/file.txt','r') as data:
			self.table = ast.literal_eval(data.read())
	def delDate(self, date=None):
		if date == None:
			date = Table.getToday()
		self.table.pop(date)
	def delLastEntry(self):
		pass
	def delTask(self, date, task):
		pass
	def getAllBookEvents(self, book):
		book_events = {}
		for date in self.table:
			for task in self.table[date]:
				if task == 'READ':
					for event in self.table[date][task][1:]:
						if ' (pages' in event[2]:
							idx = event[2].index(' (pages')
							event_book = event[2][:idx]
							if event_book == book:
								if date not in book_events:
									book_events[date] = [event]
								else:
									book_events[date]+= [event]
		return book_events
	def getBookDuration(self, book):
		book_duration = '0:00'
		book_events = self.getAllBookEvents(book)
		date_durations = {}
		for date in book_events:
			date_duration = '0:00'
			for event in book_events[date][1:]:	
				event_duration = Table.timeDifference(event[0], event[1])
				book_duration = Table.timeSummation(book_duration, event_duration)
				date_duration = Table.timeSummation(date_duration, event_duration)
			date_durations[date] = date_duration
		return book_duration, date_durations
	""" Helper functions: """
	def getTime():
		t = time.localtime()
		minute = str(t.tm_min)
		if t.tm_min < 10:
			minute = '0' + str(t.tm_min)
		return f'{t.tm_hour}:{minute}'
	def getTasks(self, day):
		return self.table[day]
	def getAllTasks(self):
		tasks = []
		for date in self.table:
			for task in self.table[date]:
				if task not in tasks:
					tasks.append(task)
		return sorted(tasks)
	def getTaskToday(self, task):
		return self.table[Table.getToday()][task]
	def getToday():
		td = datetime.date.today()
		return f'{td.month}/{td.day}/{td.year}'
	def isDateEarlierThanOrEqual(d1, d2):
		m1, d1, y1 = d1.rsplit('/')
		m2, d2, y2 = d2.rsplit('/')
		m1, d1, y1 = int(m1), int(d1), int(y1)
		m2, d2, y2 = int(m2), int(d2), int(y2)
		if y1 < y2:
			return True
		elif y1 == y2 and m1 < m2:
			return True
		elif y1 <= y2 and m1 == m2 and d1 <= d2:
			return True
		else:
			return False
	def isTaskInTable(self, task):
		for date in self.table:
			for t in self.table[date]:
				if task == t:
					return True
		return False
	def getDuration(self, task):
		task_duration = task[0][0][10:]
		if task[-1][1] == 0:
			time = Table.getTime() 
			temp_event_duration = Table.timeDifference(task[-1][0], time)
			temp_task_duration = Table.timeSummation(task_duration, temp_event_duration)
			return temp_task_duration
		return task_duration
	def timeDifference(t1, t2):
		t1 = t1.rsplit(':') # t1 earlier than t2 for positive diff
		t2 = t2.rsplit(':')
		t1 = [int(t1[0]), int(t1[1])]
		t2 = [int(t2[0]), int(t2[1])]
		d_hrs = t2[0] - t1[0]
		d_min = t2[1] - t1[1]
		if t2[1] < t1[1]:
			d_min = t2[1] + (60 - t1[1])
			d_hrs -= 1
		if d_min < 10:
			d_min = '0' + str(d_min)
		return f'{d_hrs}:{d_min}'	
	def timeSummation(t1, t2):
		t1 = t1.rsplit(':')
		t2 = t2.rsplit(':')
		t1 = [int(t1[0]), int(t1[1])]
		t2 = [int(t2[0]), int(t2[1])]
		s_hrs = t1[0] + t2[0]
		s_min = t1[1] + t2[1]
		if s_min > 60:
			s_min = abs(60 - s_min)
			s_hrs += 1
		if s_min < 10:
			s_min = '0' + str(s_min)
		return f'{s_hrs}:{s_min}'
	def timeGreaterThan(t1, t2):
		# used for durations in hh:mm format
		# d1 > d2
		hr1, min1 = t1.rsplit(':')
		hr2, min2 = t2.rsplit(':')
		if int(hr1) > int(hr2):
			return True
		elif int(hr1) == int(hr2) and int(min1) > int(min2):
			return True
		else:
			return False
	def convertToTwelve(t):
		hr, minute = t.rsplit(':')
		code = 'AM'
		if int(hr) >= 12:
			hr = str(int(hr)-12)
			code = 'PM'
		if int(hr) == 0:
			hr = '12'	
		return f'{hr}:{minute} {code}'
	def convertToTwentyFour(t):
		if t == 0:
			return t
		if 'PM' not in t and 'AM' not in t:
			return t
		hr, minute = t.rsplit(':')
		if 'AM' in minute and int(hr) == 12:
			hr = '00'
		if 'PM' in minute and int(hr) < 12:
			hr = str(int(hr)+12)
		minute = minute[:(minute.index('M')-2)]
		return f'{hr}:{minute}'
	def convertMinToTwentyFour(m):
		hrs = str(int(m) // 60)
		mns = int(m) % 60
		if mns < 10:
			mns = '0'+str(mns)
		else:
			mns = str(mns)
		return f'{hrs}:{mns}'
	def addDay(date, repeat=1):
		mo, day, year = date.rsplit('/')
		for i in range(repeat):
			leap = Table.isLeapYear(year)
			if mo in ['1', '3', '5', '7', '8', '10', '12']: # 31
				if int(day) < 31:
					day = str(int(day) + 1)
				elif day == '31':
					if mo == '12':
						mo = '1'
						year = str(int(year)+1)
					elif mo != '12':
						mo = str(int(mo) + 1)
					day = '1'
			elif mo in ['4', '6', '9', '11']: # 30
				if int(day) < 30:
					day = str(int(day) + 1)
				elif day == '30':
					mo = str(int(mo) + 1)
					day = '1' 
			elif mo == '2' and not leap: # 28
				if int(day) < 28:
					day = str(int(day) + 1)
				elif day == '28':
					mo = '3'
					day = '1'
			elif mo == '2' and leap: # 29
				if int(day) < 29:
					day = str(int(day) + 1)
				elif day == '29':
					mo = '3'
					day = '1'
		date = mo+'/'+day+'/'+year
		return date
	def subDay(date, repeat=1):
		mo, day, year = date.rsplit('/')
		for i in range(repeat):
			leap = Table.isLeapYear(year)
			if mo in ['1', '2', '4', '6', '8', '9', '11']: # 31
				if int(day) > 1:
					day = str(int(day) - 1)
				elif day == '1':
					if mo == '1':
						mo = '12'
						year = str(int(year)-1)
					elif mo != '1':
						mo = str(int(mo) - 1)
					day = '31'
			elif mo in ['5', '7', '10', '12']: # 30
				if int(day) > 1:
					day = str(int(day) - 1)
				elif day == '1':
					mo = str(int(mo) - 1)
					day = '30' 
			elif mo == '3' and not leap: # 28
				if int(day) > 1:
					day = str(int(day) - 1)
				elif day == '1':
					mo = '2'
					day = '28'
			elif mo == '3' and leap: # 29
				if int(day) > 1:
					day = str(int(day) - 1)
				elif day == '1':
					mo = '2'
					day = '29'
		date = mo+'/'+day+'/'+year
		return date
	def isLeapYear(year):
		year = int(year)
		if year % 4 == 0:
			if year % 100 == 0:
				if year % 400 == 0:
					return True
				else:
					return False
			else:
				return True
		else:
			return False
	def printTask(self, task):
		s = '\n\n'
		s+='---------\n\n'
		s+= Table.getToday()+'\n\n'
		s+= task+' -> '
		stats = self.table[Table.getToday()][task][0]
		s+=stats[0]+'\n\n'
		s+=stats[1]+'\n'
		task = self.getTaskToday(task)
		for entry in task[1:]:
			t1 = Table.convertToTwelve(entry[0])
			s+=t1+' - '
			if entry[1] != 0:
				t2 = Table.convertToTwelve(entry[1])
				s+=t2+'\n'
		s+='\n'
		print(s)
	def printEntry(self, date, task, entry):
		s = ''
		border = '-'*len(date)
		s+= border+'\n'
		s+= date
		s+= '\n'+border+'\n\n'
		s+= task+' -> '
		t1 = Table.convertToTwelve(entry[0])
		s+=t1+' - '
		if entry[1] != 0:
			t2 = Table.convertToTwelve(entry[1])
			s+=t2+'\n'
		else:
			s+='...'
		s+='\n'
		return s
	def dateTasksToString(self, date):
		if date not in self.table:
			return ''
		border = '-'*len(date)
		s=border + '\n'
		s+=date
		s+='\n'+border+'\n\n'
		for task in self.table[date]:
			s_task=task+' -> '
			stats = self.table[date][task][0]
			s_duration=stats[0][10:]
			s_entries=stats[1]+'\n'
			s_entry_arr = []
			for entry in self.table[date][task][1:]:
				t1 = Table.convertToTwelve(entry[0])
				s_entry=t1+' - '
				if entry[1] != 0:
					t2 = Table.convertToTwelve(entry[1])
					s_entry+=t2
				else:
					s_entry+='...'
					s_temp_e_dur = Table.timeDifference(Table.convertToTwentyFour(t1), Table.getTime())
					s_duration = Table.timeSummation(s_duration, s_temp_e_dur)
				desc = entry[2]
				if desc != '':
					s_entry+=f' -> {desc}'
				s_entry+='\n'
				s_entry_arr.append(s_entry)
			s_duration = f'Duration: {s_duration}\n\n'
			s_task+=s_duration+s_entries
			for s_e in s_entry_arr:
				s_task+=s_e
			s_task+='\n'+border+'\n\n'
			s+=s_task
		return s
	def dateDurationsToString(self, date):
		if date not in self.table:
			return ''
		border = '\n'+'-'*len(date)+'\n'
		s=border
		s+=date
		s+=border+'\n'
		for task in self.table[date]:
			s+=task+' -> '
			stats = self.table[date][task][0]
			s+=stats[0]+'\n'
		s+=border+'\n'
		return s
	def formatOut(self):
		out = self.__repr__()
		with open('/Users/matthewwear/Desktop/t_manager/data/out.txt','w') as data:
			data.write(out)
	def __repr__(self):
		s = '\n\n'
		for day in self.table:
			s+='---------\n\n'
			s+=day+'\n\n'
			for task in self.table[day]:
				s+=task+' -> '
				stats = self.table[day][task][0]
				s+=stats[0]+'\n\n'
				s+=stats[1]+'\n'
				for entry in self.table[day][task][1:]:
					t1 = Table.convertToTwelve(entry[0])
					s+=t1+' - '
					if entry[1] != 0:
						t2 = Table.convertToTwelve(entry[1])
						s+=t2+'\n'
				s+='\n\n'
		return s
