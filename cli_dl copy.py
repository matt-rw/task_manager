import os 
import sys
import ast
import random
from time import sleep
from book import *
class CLI:
	"""
	Abbreviations: period (pd), program (pm), practice (pe)
	For period: expressions (ex), operations (os), first lower (fl), first upper (fu)				second lower (sl), second upper (su)
	For program: name (n), number of periods (k), random (r), periods (pds)
	For practice: mode (m), date (de), start (s), finish (f), duration (dn)
	
	Functions:
		__init__(self)
		menu(self)
		practice(self)
		programs(self)
		viewToday(self)    [inc]
		viewProgram(self)  [inc]
		viewAll(self)      [inc]
		options(self)      [inc]
	
	For practice:
		practicePrevious(self)
		practiceProgram(self, page)
		practicePeriod(self, pd)
		practiceStart(self, pd, pm)
		startPeriod(self, pe)
		startProgram(self, pe)

	For program:
		addProgram(self)
		menuProgram(self, n, k, r, d)
		addPeriod(self, k)
		menuPeriods(self, k, pds)
		editProgram(self)   [inc]
		viewPrograms(self)  [inc]
		classPrograms(self) [inc] [del]

	For I/O:
		c(self)
		o(self)
		n(self, c)
		t(self, c)
		i(self)
		readPrograms(self)
		writeProgram(self, pm)
		readPractices(self)
		writePractices(self, pe)
	
	For strings:
		sn(self, c)
		st(self, c)
		rds(self, d, t)
	"""
	def __init__(self, path=''):
		self.path = path
	def menu(self):
		self.c()
		menu = 'Digital Library\n'
		brdr = '_'*10+'\n'
		menu+= '\nRead Commands:\n'
		#menu+= brdr
		menu+= ' 1 | Start\n'
		menu+= ' 2 | End\n'
		#menu+= brdr
		menu+= '\nBook Commands:\n'
		menu+= ' 3 | Add\n'
		menu+= ' 4 | Edit\n'
		menu+= '\nView Commands:\n'
		menu+= ' 5 | Book\n'
		menu+= ' 6 | All\n'
		menu+= '\n'
		#menu+= brdr
		menu+= ' 7 | Options\n'
		menu+= ' 0 | Exit\n'
		menu+= '\n'
		self.o(menu)
		self.o('Enter command:\n')
		option = self.i()
		if option == '1': self.start()
		elif option=='2': self.end()
		elif option=='3': self.add()
		elif option=='4': self.edit()
		elif option=='5': self.viewBook()
		elif option=='6': self.viewAll()
		elif option=='7': self.options()
		elif option=='0': self.c(); sys.exit()
		else:
			self.c(); self.o(menu)
			self.o('Invalid command.\n')
			self.s(2); self.menu()
	def start(self):
		# check for any unended events
		end = self.end(write=False)
		if end == 0:
			self.o('\nEnd all events.\n')
			self.s(2); self.menu()
		# select book
		book = self.bookList()
		# add event
		new_event = self.eventInput()
		if new_event == 0: self.menu()
		else:
			# add new event to file, add to correct loc
			#book.events += [new_event]
			#i = -1
			#for j in range(len(book.dates)):
			#	if book.dates[j] == new_event.date:
			#		i = j
			#if i == -1: book.dates.append(new_event.date)
			book = Book.insertEvent(book, new_event)
			Book.saveBook(book)
			print('\nEvent added.\n'); self.s(2)
			self.menu()

	def end(self, write=True, out=False, time_end=None):
		# find unended event
		books = Book.readBooks(path=self.path)
		event_book = None
		event = None
		ext = None
		if time_end is None:
			ext = True
		if time_end == None:
			time_end = Book.strTime()
		for book in books:
			if len(book.events) != 0:
				for e in book.events:
					if e.time_end == '':
						event_book = book
						event = e
		if event is not None:
			today = Book.strDate()
			if event.date == today:
				if write:
					event.time_end = time_end
					Book.saveBooks(books, path=self.path)
					if out:
						self.o(f'\nEvent for {book.title} ended.\n')
						self.s(2); self.menu()
				else: return 0 # unended event exists
			else:
				# prompt user to enter end time
				# for event in a previous day
				if time_end is None:
					self.o(f'\nEnter ending time for event on {event.date}\n')
					self.s(4)
					event = self.eventInput(event)
					Book.saveBooks(books, path=self.path)
					self.menu()
				elif time_end is not None:
					event.time_end = time_end
					Books.saveBooks(books, path=self.path)
					self.o(f'\nEvent for {book.title} on {event.date} ended.\n')
					self.s(2); self.menu()
		else:
			if write:
				self.o('\nNo event to end.\n')
				self.s(2); self.menu()
			else: return 1
	def add(self):
		pass
		# adjust book fields
		book = self.bookInput(book=None, rm=False)
		if book != 0:
			Book.saveBook(book=book)
		self.menu()
		# save book
	def edit(self):
		# select book
		book = self.bookList()
		if book == 0: self.menu()
		else:
			# remove book from list, save both sides
			books = Book.readBooks()
			books_before = []
			books_after = []
			seen = False
			for b_i in books:
				if (b_i.title == book.title) and (b_i.author == book.author):
					seen = True
				elif not seen:
					books_before.append(b_i)
				elif seen:
					books_after.append(b_i)
			# adjust book fields
			edited_book = self.bookInput(book=book)
			# save book
			if edited_book is not None:
				new_books = books_before + [edited_book] + books_after
			elif edited_book is None:
				new_books = books_before + books_after
			Book.saveBooks(books=new_books)
			self.edit()
	def viewBook(self):
		pass
	def viewAll(self):
		pass
	def viewAll(self):
		pass
	def options(self):
		pass
	""" Functions for Practice """
	def practicePrevious(self):
		pes = self.readPractices()
		pe  = pes[len(pes)-1]
		if pe['m'] == 'pd':
			pd = Period.fromDict(pe['pd'])
			self.startPeriod(Practice(pd=pd))
		elif pe['m']=='pm': 
			pm = Program.fromDict(pe['pm'])
			self.startProgram(Practice(pm=pm))
		else:
			self.c(); self.o('No previous practices')
			self.s(2); self.practice()
	def practiceProgram(self, page=0):
		pm = self.programList()
		if pm: self.practiceStart(pm=pm)
		self.practice()
	def practicePeriod(self, pd):
		os = ''
		for i in range(len(pd.os)):
			os+= pd.os[i].toString()
			if i!=(len(pd.os)-1):
				os+= ','
		fr = f'{pd.fl}-{pd.fu}'
		sr = f'{pd.sl}-{pd.su}'
		if pd.fl == '' and pd.fu == '':
			fr = ''
		if pd.sl == '' and pd.su == '':
			sr = ''
		menu = 'Practice Period\n\n'
		menu+= 'Practice Information\n'
		# progressive menu
		menu+= f'1 | Number of expressions            | {pd.ex}\n'
		menu+= f'2 | Operation(s) (e.g. "+,-,*,/")    | {os}\n'
		menu+= f'3 | First operand range (e.g. "0-9") | {fr}\n'
		menu+= f'4 | Second operand range             | {sr}\n\n' 
		menu+= '5 | Add\n\n'
		menu+= '0 | Cancel\n\n'
		self.c(); self.o(menu)
		self.o('Enter number:\n')
		option = self.i()
		self.c(); self.o(menu)
		if option == '1':
			self.o('Enter expressions:\n')
			ex = self.i()
			pd.ex = int(ex)
			self.practicePeriod(pd)
		elif option=='2':
			self.o('Enter operations:\n')
			os = self.i()
			os = os.rsplit(',')
			for idx in range(len(os)):
				os[idx] = Operation.fromString(os[idx])
			pd.os = os
			self.practicePeriod(pd)
		elif option=='3':
			self.o('Enter first operand range:\n')
			f = self.i()
			fl, fu = f.rsplit('-')
			pd.fl = int(fl); pd.fu = int(fu)
			self.practicePeriod(pd)
		elif option=='4':
			self.o('Enter second operand range:\n')
			s = self.i()
			sl, su = s.rsplit('-')
			pd.sl = int(sl); pd.su = int(su)
			self.practicePeriod(pd)
		elif option=='5':
			# check that period information is complete
			if pd.ex=='' or pd.os==[] or pd.fl=='' or pd.fu=='' or pd.sl=='' or pd.su=='':
				self.o('Incomplete period information.\n')
				time.sleep(2)
				self.practicePeriod(pd)
			else: self.practiceStart(pd)
		elif option=='0': self.practice()
		else:
			self.o('Invalid command.\n')
			self.s(); self.practicePeriod(pd)
	def practiceStart(self, pd=None, pm=None):
		pe = Practice(pd, pm)
		if pe.m == 'pd':
			self.startPeriod(pe)
		elif pe.m=='pm':
			self.startProgram(pe)
	def startPeriod(self, pe):
		fl, fu = pe.pd.fl, pe.pd.fu
		sl, su = pe.pd.sl, pe.pd.su
		os = pe.pd.os
		n_os = len(os)-1
		pe.s = pe.getTime()
		for i in range(pe.pd.ex): # add option for timer between exs
			pe.pdd[i]['first'] = random.randint(fl,fu)
			pe.pdd[i]['second'] = random.randint(sl, su)
			o = os[random.randint(0,n_os)]
			pe.pdd[i]['operation'] = Operation.toString(o)
			# check not div by 0
			pe.pdd[i]['value'] = o.value(pe.pdd[i]['first'],pe.pdd[i]['second'])
			s_e = str(pe.pdd[i]['first'])
			s_e+= ' ' + pe.pdd[i]['operation'] + ' '
			s_e+= str(pe.pdd[i]['second'])
			s_e+= ' = '
			# adjustable time option
			pe.pdd[i]['start'] = pe.getTime()
			self.c()
			self.o(f'Expression {i+1}'); self.n(4)
			self.t(4)
			self.o(s_e)
			pe.pdd[i]['response'] = int(self.i())
			pe.pdd[i]['finish'] = pe.getTime()
			start  = pe.pdd[i]['start']
			finish = pe.pdd[i]['finish']
			pe.pdd[i]['duration'] = pe.getDuration(start, finish)
		pe.f = pe.getTime()
		pe.pdr['expressions'] = pe.pd.ex
		c = 0
		for i in range(pe.pd.ex):
			if pe.pdd[i]['value'] == pe.pdd[i]['response']:
				c+= 1
		pe.pdr['correct'] = c
		pe.pdr['accuracy']= (c/pe.pd.ex)
		pe.pdr['error'] = (1 - (c/pe.pd.ex))
		self.writePractices(pe)
		self.n(2); self.o('Period complete.'); self.n()
		self.s(2)
		# show results page, provide option to exit at any time
		self.practice()
	def startProgram(self, pe):
		pe.s = pe.getTime(millisecond=True)
		for i in range(pe.pm.k):
			pd = pe.pm.pds[i]
			fl, fu = pd.fl, pd.fu
			sl, su = pd.sl, pd.su
			os = pd.os		
			n_os = len(os)-1
			for j in range(pd.ex):
				pe.pmd[i][j]['first'] = random.randint(fl,fu)
				pe.pmd[i][j]['second'] = random.randint(sl, su)
				o = os[random.randint(0,n_os)]
				pe.pmd[i][j]['operation'] = Operation.toString(o)
				# check not div by 0
				pe.pmd[i][j]['value'] = o.value(pe.pmd[i][j]['first'],pe.pmd[i][j]['second'])
				s_e = str(pe.pmd[i][j]['first'])
				s_e+= ' ' + pe.pmd[i][j]['operation'] + ' '
				s_e+= str(pe.pmd[i][j]['second'])
				s_e+= ' = '
				# adjustable time option
				pe.pmd[i][j]['start'] = pe.getTime(millisecond=True)
				s_no = f'Program {pe.pm.n}' + self.sn(1)
				s_no+= f'Period {i+1}' + self.sn(1)
				s_no+= f'Expression {j+1}' + self.sn(4)
				s_no+= self.st(4)
				self.c(); self.o(s_no); self.o(s_e)
				response = ''
				while not response.isnumeric(): 
					response = self.i()
					if response == 'q': self.practiceProgram()
					self.c(); self.o(s_no); self.o(s_e)
				pe.pmd[i][j]['response'] = int(response)
				pe.pmd[i][j]['finish'] = pe.getTime(millisecond=True)
				start  = pe.pmd[i][j]['start']
				finish = pe.pmd[i][j]['finish']
				pe.pmd[i][j]['duration'] = pe.getDuration(start, finish, True)
		pe.f  = pe.getTime(millisecond=True)
		pe.dn = pe.getDuration(pe.s, pe.f, True)
		c_all = 0
		e_all = 0
		for i in range(pe.pm.k):
			pe.pmr[i]['expressions'] = pe.pm.pds[i].ex
			c = 0
			for j in range(pe.pm.pds[i].ex):
				if pe.pmd[i][j]['value'] == pe.pmd[i][j]['response']:
					c+= 1; c_all+= 1
				e_all+= 1
			pe.pmr[i]['correct']  = c
			pe.pmr[i]['accuracy'] = int(c/pe.pm.pds[i].ex*100)
			pe.pmr[i]['error']    = 100 - pe.pmr[i]['accuracy']
		pe.pmr['all']['correct']  = c_all
		pe.pmr['all']['accuracy'] = int(c_all/e_all*100)
		pe.pmr['all']['error']    = 100 - pe.pmr['all']['accuracy']
		self.writePractices(pe)
		self.practiceResults(pe)
	def practiceResults(self, pe):
		s_r = 'Practice Results' + self.sn(2)
		if pe.m == 'pm':	
			at_all = 0
			at_pds = []
			for i in range(len(pe.pm.pds)):
				at_pd = 0
				for j in range(pe.pmr[i]['expressions']):
					m = pe.pmd[i][j]['duration']['minute']
					s = pe.pmd[i][j]['duration']['second']
					ms= pe.pmd[i][j]['duration']['millisecond']
					at_all+= (m*60)+s+(ms/1000)
					at_pd += (m*60)+s+(ms/1000)
				at_pd = at_pd/pe.pmr[i]['expressions']
				dur   = {'minute':(at_pd//60),'second':(at_pd%60)}
				at_pds.append(dur)
			at_all = at_all/pe.pmr['all']['expressions']
			at_all = {'minute':(at_all//60),'second':(at_all%60)}
			s_r+= f'All periods:\n'
			s_r+= f'Correct   | {pe.pmr["all"]["correct"]}'
			s_r+= f' of {pe.pmr["all"]["expressions"]}'
			s_r+= self.sn()
			s_r+= f'Accuracy  | {pe.pmr["all"]["accuracy"]}%'
			s_r+= self.sn()
			s_r+= f'Avg. time | '
			if at_all['minute']>0:
				s_r+= f'{at_all["minute"]} minutes, '
			s_r+= f'{at_all["second"]} seconds'
			s_r+= self.sn(2)
			for i in range(len(pe.pm.pds)):
				s_r+= f'Period {i+1}:\n'
				s_r+= f'Correct  | {pe.pmr[i]["correct"]}'
				s_r+= f' of {pe.pmr[i]["expressions"]}'
				s_r+= self.sn()
				s_r+= f'Accuracy | {pe.pmr[i]["accuracy"]}%'
				s_r+= self.sn()
				s_r+= f'Avg. time | '
				if at_pds[i]['minute']>0:
					s_r+= f'{at_pds[i]["minute"]} minutes, '
				s_r+= f'{round(at_pds[i]["second"], 3)} seconds'
				s_r+= self.sn(2)
		elif pe.m=='pd':
			at_pd = 0
			for i in range(pe.pd.ex):
				m = pe.pdd[i]['duration']['minute']
				s = pe.pdd[i]['duration']['second']
				ts_pd+= (m*60)+s
			at_pd = at_pd/pe.pdr['expressions']
			sec = at_pd%60
			at_pd = {'minute':(at_pd//60),'second':(at_pd%60)}
			s_r+= f'Period results:\n'
			s_r+= f'Correct  | {pe.pdr["correct"]}'
			s_r+= f' of {pe.pdr["expressions"]}' + self.sn()
			s_r+= f'Accuracy | {pe.pdr["accuracy"]}%'
			s_r+= self.sn()
			s_r+= f'Avg. time | '
			if at_pd['minute']>0:
				s_r+= f'{at_pd["minute"]} minutes, '
			s_r+= f'{at_pd["second"]} seconds'
			s_r+= self.sn(2)
		#s_m = self.sn()
		s_m = '1 | Summary of incorrect responses' + self.sn()
		s_m+= '2 | Restart program' + self.sn(2)
		s_m+= '0 | Exit' + self.sn(2)
		self.c(); self.o(s_r); self.o(s_m)
		self.o('Enter number:\n')
		option = self.i()
		if option == '1': self.summaryResponses()
		elif option=='2' and pe.m=='pd': self.practiceStart(pd=pe.pd)
		elif option=='2' and pe.m=='pm': self.practiceStart(pm=pe.pm)
		elif option=='0': self.practice()
		else:
			self.c(); self.o(s_r); self.o(s_m)
			self.o('Invalid command.'); self.s(2)
			self.practiceResults(pe)
	""" Functions for Programs """
	def addProgram(self):
		pm_m = self.programs
		pm_i = self.programInput	
		pm_l = self.programList
		pm_f = self.programFields
		pm_w = self.programWrite
		pd_i = self.periodInput
		pd_f = self.periodFields
		# if 0: pm, if 1: pm_w
		pm   = pm_i(menu=pm_f)
		if pm: pm_w(pm)
		pm_m()
	def editProgram(self):
		pm_m = self.programs
		pm_i = self.programInput
		pm_l = self.programList
		pm_f = self.programFields
		pm_w = self.programWrite
		pd_i = self.periodInput
		pd_f = self.periodFields
		pm   = pm_l()
		if pm: pm = pm_i(menu=pm_f, pm=pm)
		if pm: pm_w(pm=pm)
		pm_m()
	def deleteProgram(self):
		pm = self.programList()
		if pm: self.removeProgram(pm)
		self.programs()
	def bookInput(self, group=1, book=None, rm=True):
		menu = self.bookFields
		#self.c()
		group = 1 # [1,...,4]
		old_book = None
		if book is not None:
			old_book = book
		if book is None:
			book = Book.emptyBook()
		book_dict = Book.toDictionary(book=book)
		date_page = 0
		option = ''
		while True:
			# adaptive scrolling commands (disabled)
			#if option == '4' and (group==3 or group==4): # prev page
			#	group-= 1
			#elif option == '5' and (group==3 or group==4): # next page
				#if group < 4:
				#	group+= 1
				#elif group==4:
				#	self.c()
				#	self.o(menu(args, group))
				#	self.o('Already on last page.')
				#	self.s(2)
			if option == '8': #and (group==1 or group==2): # prev page
				if group > 1:
					group-= 1
				elif group==1:
					self.c()
					self.o(menu(args, group, rm))
					self.o('Already on first page.\n')
					self.s(2)
			elif option == '9': #and (group==1 or group==2): # next page
				if group < 4:
					group+= 1 # group < 4
				elif group==4:
					self.c()
					self.o(menu(args, group, rm))
					self.o('Already on last page.\n')
					self.s(2)
			args = []
			if group == 1:
				args = [
					book_dict['title'], book_dict['author'],
					book_dict['publisher'], book_dict['date_pub']
					]
			elif group==2:
				args = [
					book_dict['config'], book_dict['location'],
					book_dict['pages'], book_dict['contents']
					]
			elif group==3:
				args = [
					book_dict['avg_wpp'], book_dict['avg_mpp'],
					book_dict['avg_mpp'], book_dict['avg_mpc']
					]
			elif group==4:
				args = [
					book.date_start, book.date_end,
					book.events
					]
			self.c()
			self.o(menu(args, group, rm))
			self.o('Enter command:\n')
			option = self.i()
			if option == '1':
				self.c()
				self.o(menu(args, group, rm))
				self.o('Enter field 1:\n')
				s = self.i()
				args[0] = s
				#if self.duplicateProgram(n):
			elif option=='2':
				self.c()
				self.o(menu(args, group, rm))
				self.o('Enter field 2:\n')
				s = self.i()
				args[1] = s
			elif option=='3':
				if group == 4:
					while True:
						dates_dict = book_dict['dates']
						dates = []
						for i in range(len(dates_dict)):
							dates += [dates_dict[i]]
						date, date_page = self.dateList(dates, date_page)
						if date != 0:
							date_events = []
							for i in book_dict['events']:
								if book_dict['events'][i]['date'] == date:
									e = book_dict['events'][i]
									date_events+= [Book.fromDictionary(event=e)]
							events = self.eventList(date_events, book=book, dates=1)
							events_dict = {}
							for i in range(len(events)):
								events_dict[i] = Book.toDictionary(event=events[i])
							s = events_dict
						elif date == 0: s = None; break
				else:
					self.c()
					self.o(menu(args, group, rm))
					self.o('Enter field 3:\n')
					s = self.i()
				args[2] = s
			elif option=='4' and (group==1 or group==2):	
				if group == 2: # contents stage
					contents = book_dict['contents']
					contents = []
					for i in book_dict['contents']:
						c = book_dict['contents'][i]
						contents+= [Book.fromDictionary(content=c)]
					contents = self.contentsList(contents=contents)
					contents_dict = {}
					for i in range(len(contents)):
						contents_dict[i] = Book.toDictionary(content=contents[i])
					s = contents_dict
				else:
					self.c()
					self.o(menu(args, group, rm))
					self.o('Enter field 4:\n')
					s = self.i()
				if s is not None:
					args[3] = s
			#elif (option=='4' or option=='5') and (group==3 or group==4):
			#	pass # change page on next iteration above
			elif (option=='8' or option=='9'): # and (group==1 or group==2):
				pass # change page on next iteration above
			#elif option=='6' and (group==3 or group==4):
			#	self.c()
			#	self.o('Are you sure that you want to remove this book?\n')
			#	self.o(' 1 | Yes\n')
			#	self.o(' 0 | No\n\n')
			#	self.o('Enter command:\n')
			#	option = self.i()
			#	if option == '1':
			#		return None
			#	elif option=='0':
			#		pass
			elif option=='6':
				book = Book.fromDictionary(book=book_dict)
				return book
			elif option=='7' and rm: # and (group==1 or group==2):
				self.c()
				self.o('Are you sure that you want to remove this book?\n')
				self.o(' 1 | Yes\n')
				self.o(' 0 | No\n\n')
				self.o('Enter command:\n')
				option = self.i()
				if option == '1':
					return None
				elif option=='0':
					pass
			elif option=='0':
				if old_book is None:
					return 0
				elif old_book is not None:
					return old_book
			else:
				self.c()
				self.o(menu(args, group, rm))
				self.o('Invalid command.\n')
				self.s(2)	
			if group == 1:
				book_dict['title'] = args[0]
				book_dict['author'] = args[1]
				book_dict['publisher'] = args[2]
				book_dict['date_pub'] = args[3]
			elif group==2:
				book_dict['config'] = args[0]
				book_dict['location'] = args[1]
				book_dict['pages'] = args[2]
				book_dict['contents'] = args[3]
			elif group==3:
				book_dict['avg_wpp'] = args[0]
				book_dict['avg_mpp'] = args[1]
				book_dict['avg_mpp'] = args[2]
				book_dict['avg_mpc'] = args[3]
			elif group==4:
				book_dict['date_start'] = args[0]
				book_dict['date_end'] = args[1]
				book_dict['events'] = args[2]
	def bookList(self, page=0):
		while True:
			menu = f'Select Book\n\n'
			menu+='Books\n'
			books = Book.readBooks(self.path)
			book_l = books[3*page:3*(page+1)] 
			max_l = 0
			for book_i in range(len(book_l)):
				if len(book_l[book_i].title) > max_l:
					max_l = len(book_l[book_i].title)
			for book_i in range(len(book_l)):
				title   = book_l[book_i].title
				n_l = len(title)
				if n_l < max_l:
					title+= ' '*(max_l-n_l)
				author = book_l[book_i].author
				menu+=f' {book_i+1}   | {title} | {author}\n'
			menu+= '\n'
			menu+= ' 8/9 | Previous/Next page\n'
			menu+= ' 0   | Back\n\n'
			self.c(); self.o(menu)
			self.o('Enter number:\n')
			option = self.i()
			if option=='1' or option=='2' or option=='3':
				book = books[(int(option)-1)+(3*page)]
				return book
			elif option=='8':
				if page == 0:
					self.c(); self.o(menu)
					self.o('Already on first page.\n')
					self.s(2)
				else: page -= 1
			elif option=='9':
				nxt_book_l = books[3*(page+1):3*(page+2)]
				if len(nxt_book_l) == 0:
					self.c(); self.o(menu)
					self.o('Already on last page.\n')
					self.s(2)
				else: page += 1
			elif option=='0':
				return 0
			else:
				self.c(); self.o(menu)
				self.o('Invalid command.\n')
				self.s(2)
	def bookFields(self, args:list, group:int, rm:bool):
		menu= 'Book Fields\n\n'
		# group for book = [1, 4]
		if group == 1:
			menu+= f' 1   | Title                          | {args[0]}\n'
			menu+= f' 2   | Author                         | {args[1]}\n'
			menu+= f' 3   | Publisher                      | {args[2]}\n'
			menu+= f' 4   | Date                           | {args[3]}\n'
		elif group == 2:	
			menu+= f' 1   | Configuration                  | {args[0]}\n'
			menu+= f' 2   | Location                       | {args[1]}\n'
			menu+= f' 3   | Pages                          | {args[2]}\n'
			menu+= f' 4   | Contents                       | Open contents\n'#{args[3]}\n'
		elif group == 3:
			menu+= f' 1   | Average words per page         | {args[0]}\n'
			menu+= f' 2   | Average words per minute       | {args[1]}\n'
			menu+= f' 3   | Average minutes per page       | {args[2]}\n'	
		elif group == 4:
			menu+= f' 1   | Date started                   | {args[0]}\n'
			menu+= f' 2   | Date finished                  | {args[1]}\n'
			menu+= f' 3   | Events                         | Open events\n'#{args[2]}\n'		
		menu+= '\n'
		# keep continue as 5 or adjust to group size
		if group == 1 or group == 2 \
			or group == 3 or group == 4: # identical scrolling
			menu+= ' 6   | Save book\n'
			if rm:
				menu+= ' 7   | Remove book\n'
			menu+= ' 8/9 | Previous/Next Page\n'
		# alternate scrolling commands
		#elif group==3 or group == 4:
		#	menu+= ' 4/5 | Previous/Next Page\n'
		#	menu+= ' 6   | Remove book\n\n'
		menu+= ' 0   | Cancel\n\n'
		return menu
	def contentsTableInput(self, contents:list=[]):
		# kd is how many additional Period objects to append to pds
		#for idx in range(int(kd)):
		#	pds.append(Period())
		i = 1
		option = 1
		#progressive = True
		while True:
			#self.c()
			#self.menuProgram()
			#menu(pds)
			menu = self.contentFields(contents)	
			self.c()
			self.o(menu)

			#self.periodFields(pds)
			# manual entry; fix entering fields
			#if not progressive:
			#	self.o('Enter period number:\n')
			#	i = self.i()
			#	self.n()
			#	self.o('Enter option number:\n')
			#	option = self.i()
			#	self.n()
			self.o(f'Arguments for period {i}')
			self.n()
			if option == 1:
				self.o('Enter number of expressions:\n')
				ex = self.i()
				pds[i-1].ex = int(ex)
				if progressive: option+= 1
			elif option==2:
				self.o('Enter operations:\n')
				os = self.i()
				self.n()
				os = os.rsplit(',')
				for idx in range(len(os)):
					os[idx] = Operation.fromString(os[idx])
				pds[i-1].os = os
				if progressive: option+= 1
			elif option==3:
				self.o('Enter first operand range:\n')
				fr = self.i()
				self.n()
				fl, fu = fr.rsplit('-')
				pds[i-1].fl = int(fl)
				pds[i-1].fu = int(fu)
				if progressive: option+= 1
			elif option==4:	
				self.o('Enter second operand range:\n')
				sr = self.i()
				self.n()
				sl, su = sr.rsplit('-')
				pds[i-1].sl = int(sl)
				pds[i-1].su = int(su)
				if progressive and i == int(len(pds)):
					progressive = False
					# update manual entry
					# temp return
					return pds
				elif progressive and i< int(len(pds)):
					i+= 1
					option = 1
	def contentInput(self, content=None):
		menu = self.contentFields
		if content is None:
			content = Book.emptyContent()
		content_dict = Book.toDictionary(content=content)
		args = [
			content_dict['title'], content_dict['category'],
			content_dict['page_start'], content_dict['page_end']
			]
		option = ''
		while True:
			if option == '8':
				return content, 8
			elif option=='9':
				return content, 9
			self.c()
			self.o(menu(args))
			self.o('Enter field number:\n')
			option = self.i()
			if option == '1':
				self.c()
				self.o(menu(args))
				self.o('Enter field 1:\n')
				s = self.i()
				args[0] = s
			elif option=='2':
				self.c()
				self.o(menu(args))
				self.o('Enter field 2:\n')
				s = self.i()
				args[1] = s
			elif option=='3':
				self.c()
				self.o(menu(args))
				self.o('Enter field 3:\n')
				s = self.i()
				args[2] = s
			elif option=='4':
				self.c()
				self.o(menu(args))
				self.o('Enter field 4:\n')
				s = self.i()
				args[3] = s
			elif option=='8' or option=='9':
				# return next iteration
				pass
			elif option=='0':
				return content, 1
			else:
				self.c()
				self.o(menu(args))
				self.o('Invalid command.\n')
				self.s(2)
			content.title = args[0]
			content.category = args[1]
			content.page_start = args[2]
			content.page_end = args[3]

	def contentFields(self, args:list):
		menu= 'Content Fields\n\n'
		menu+= f' 1   | Title                                      | {args[0]}\n'
		menu+= f' 2   | Category (e.g. "Chapter", etc.)            | {args[1]}\n'
		menu+= f' 3   | Starting page                              | {args[2]}\n'
		menu+= f' 4   | Ending page                                | {args[3]}\n'
		menu+= '\n'
		menu+= ' 8/9 | Previous/Next content\n'
		menu+= ' 0   | Back\n\n'
		return menu
	def contentsList(self, contents, page=0):
		while True:
			menu = f'Select Content\n\n'
			menu+='Contents\n'
			length = 5
			content_l = contents[length*page:length*(page+1)]
			max_l = 0
			for content_i in range(len(content_l)):
				if len(content_l[content_i].title) > max_l:
					max_l = len(content_l[content_i].title)
			for content_i in range(len(content_l)):
				title   = content_l[content_i].title
				n_l = len(title)
				if n_l < max_l:
					title+= ' '*(max_l-n_l)
				pages = ''
				if (content_l[content_i].page_start != '') \
					or (content_l[content_i].page_end != ''):
					pages = f'{content_l[content_i].page_start}'
					pages+= f' - {content_l[content_i].page_end}'
				menu+=f' {content_i+1}   | {title} | {pages}\n'
			menu+= '\n'
			menu+= ' 6   | Remove last\n'
			menu+= ' 7   | Add\n\n'
			menu+= ' 8/9 | Previous/Next page\n'
			menu+= ' 0   | Back\n\n'
			self.c(); self.o(menu)
			self.o('Enter command:\n')
			option = self.i()
			c_o = None # next, prev content shortcut
			ll = len(content_l)
			cmd_list = (option=='1' and ll>0)
			cmd_list = cmd_list or (option=='2' and ll>1)
			cmd_list = cmd_list or (option=='3' and ll>2) 
			cmd_list = cmd_list or (option=='4' and ll>3)
			cmd_list = cmd_list or (option=='5' and ll>4)
			if cmd_list:
				c_i = (int(option)-1)+(length*page)
				if c_o is not None:
					c_i = c_o
				content = contents[c_i]
				# open content input and fields to edit
				new_content, code = self.contentInput(content=content)
				contents[c_i] = new_content
				if code == 8: # scroll previous content
					if c_i == 0: pass # do nothing
					else: c_o = c_i - 1
				elif code==9: #scroll next content
					if c_i == len(contents)-1: pass
					else: c_o = c_i + 1
				elif code==1:
					c_o = None
				#return content
			# allow editable cmds depending on list length
			elif option=='6':
				# subtract content
				if len(contents) > 0:
					contents = contents[:len(contents)-1]
					#self.c(); self.o(menu)
					#self.o('Last content removed\n')
					#self.s(2)
				else:
					self.c(); self.o(menu)
					self.o('There are no contents.\n')
					self.s(2)
			elif option=='7':
				# add content
				contents+= [Book.emptyContent()]
				#self.c(); self.o(menu)
				#self.o('Content added\n')
				#self.s(2)
			elif option=='8':
				if page == 0:
					self.c(); self.o(menu)
					self.o('Already on first page.\n')
					self.s(2)
				else: 
					page-= 1
			elif option=='9':
				nxt_content_l = contents[length*(page+1):length*(page+2)]
				if len(nxt_content_l) == 0:
					self.c(); self.o(menu)
					self.o('Already on last page.\n')
					self.s(2); 
					#contents = self.contentsList(contents, page)
				else: 
					#contents = self.contentsList(contents, page+1)
					page+= 1
			elif option=='0':
				# return to book fields
				return contents
			else:
				self.c(); self.o(menu)
				self.o('Invalid command.\n')
				self.s(2)
				#contents = self.contentsList(contents, page)
	def contentsTableFields(self, contents:list): # del function
		cmds = ' 1 | Title\n'
		cmds+= ' 2 | Category (e.g. "Chapter", "Preface", etc.)\n'
		cmds+= ' 3 | Starting page\n'
		cmds+= ' 4 | Ending page\n' 
		cmds+= '\n'
		cmds+= ' 5 | Add content\n'
		menu_pds=menu_exs=menu_os=menu_fr=menu_sr=''
		for idx in range(len(contents)):
			# handle when vars are dif lengths
			content = contents[idx]
			i = str(idx+1)
			t = content['title']
			c = content['category']
			s = content['page_start']
			e = content['page_end']
		
			#e = str(p.ex)
			#f = f'{str(p.fl)}-{str(p.fu)}'
			#s = f'{str(p.sl)}-{str(p.su)}'
			#if p.fl == '':
			#	f = ''
			#if p.sl == '':
			#	s = ''
			#o = '' # check when o==''
			#for j in range(len(p.os)):
			#	o+= p.os[j].toString()
			#	if j < len(p.os)-1:
			#		o+= ', '
			max_len = 0
			for l in [i,t,c,s,e]: #[i,e,f,s,o]:
				if len(l) > max_len:
					max_len = len(l)
			if max_len > len(i): i+= ' '*(max_len-len(i))
			if max_len > len(t): t+= ' '*(max_len-len(t))
			if max_len > len(c): c+= ' '*(max_len-len(c))
			if max_len > len(s): s+= ' '*(max_len-len(s))
			if max_len > len(e): e+= ' '*(max_len-len(e))
			# adjust lengths to be equal
			menu_pds+= f'  {i} '
			bdr      =  '------'
			menu_exs+= f'| {t} '
			menu_os += f'| {c} '
			menu_fr += f'| {s} '
			menu_sr += f'| {e} '
		menu = 'Contents Fields\n\n'
		
		#self.o('Information for periods\n\n')
		#self.o(menu_pds); self.n()
		#self.o(menu_exs); self.n()
		#self.o(menu_os);  self.n()
		#self.o(menu_fr);  self.n()
		#self.o(menu_sr);  self.n()
		#self.n(2)
		#self.o(menu)
		#self.n(2)
		return menu
	def dateList(self, dates, page=0):
		while True:
			menu = f'Select Date\n\n'
			menu+='Dates\n'
			length = 5
			date_l = dates[length*page:length*(page+1)]
			max_l = 0
			for date_i in range(len(date_l)):
				menu+=f' {date_i+1}   | {date_l[date_i]}\n'
			menu+= '\n'
			menu+= ' 8/9 | Previous/Next page\n'
			menu+= ' 0   | Back\n\n'
			self.c(); self.o(menu)
			self.o('Enter command:\n')
			option = self.i()
			ll = len(date_l)
			cmd_list = (option=='1' and ll>0)
			cmd_list = cmd_list or (option=='2' and ll>1)
			cmd_list = cmd_list or (option=='3' and ll>2) 
			cmd_list = cmd_list or (option=='4' and ll>3)
			cmd_list = cmd_list or (option=='5' and ll>4)
			if cmd_list:
				d_i = (int(option)-1)+(length*page)
				date = dates[d_i]
				return date, page
			elif option=='8':
				if page == 0:
					self.c(); self.o(menu)
					self.o('Already on first page.\n')
					self.s(2)
				else: 
					page-= 1
			elif option=='9':
				nxt_date_l = dates[length*(page+1):length*(page+2)]
				if len(nxt_date_l) == 0:
					self.c(); self.o(menu)
					self.o('Already on last page.\n')
					self.s(2); 
				else: 
					page+= 1
			elif option=='0': # exit
				# return to book fields
				return 0, 0
			else:
				self.c(); self.o(menu)
				self.o('Invalid command.\n')
				self.s(2)
	def eventList(self, events, book=None, dates=1, page=0):
		if dates == 1 and len(events) != 0:
			date_1 = events[0].date
		while True:
			menu = f'Select Event\n\n'
			menu+='Events\n'
			length = 5
			event_l = events[length*page:length*(page+1)]
			db_l = 0 # date block length if dates > 1
			b1_l = 0 # block length for start-end times
			b2_l = 0 # block length for duration
			b3_l = 0 # block length for start-end pages
			b4_l = 0 # block length for page coverage
			for event_i in range(len(event_l)):
				e = event_l[event_i]
				if dates > 1:
					if len(e.date) > db_l:
						db_l = len(e.date)
				times = f'{e.time_start}-{e.time_end}'
				if len(times) > b1_l:
					b1_l = len(times)
				if len(e.time_duration) > b2_l:
					b2_l = len(e.time_duration)
				pages = f'pages {e.page_start}-{e.page_end}'
				if len(pages) > b3_l:
					b3_l = len(pages)
				coverage_s = f'{e.page_coverage} pages'
				if len(coverage_s) > b4_l:
					b4_l = len(coverage_s)
			
			for event_i in range(len(event_l)):
				e = event_l[event_i]
				date = e.date
				if dates > 1:
					if len(e.date) < db_l:
						date+= ' '*(db_l-len(date))
				times = f'{e.time_start}-{e.time_end}'
				if len(times) < b1_l:
					times+= ' '*(b1_l-len(times))
				duration = e.time_duration
				if len(duration) > b2_l:
					duration+= ' '*(b2_l-len(duration))
				pages = f'pages {e.page_start}-{e.page_end}'
				if len(pages) < b3_l:
					pages+= ' '*(b3_l-len(pages))
				coverage_s = f'{e.page_coverage} pages'
				if len(coverage_s) < b4_l:
					coverage_s+= ' '*(b4_l-len(coverage_s))
				menu+= f' {event_i+1}   |'
				if dates > 1:
					menu+= f' {e.date} |'
				menu+= f' {times} | {duration} | {pages} | {coverage_s}\n'
			menu+= '\n'
			menu+= ' 7   | Add event\n'
			menu+= ' 8/9 | Previous/Next page\n'
			menu+= ' 0   | Back\n\n'
			self.c(); self.o(menu)
			self.o('Enter number:\n')
			option = self.i()
			ll = len(event_l)
			cmd_list = (option=='1' and ll>0)
			cmd_list = cmd_list or (option=='2' and ll>1)
			cmd_list = cmd_list or (option=='3' and ll>2) 
			cmd_list = cmd_list or (option=='4' and ll>3)
			cmd_list = cmd_list or (option=='5' and ll>4)
			if cmd_list:
				e_i = (int(option)-1)+(length*page)
				event = events[e_i]
				# open event input and fields to edit
				new_event = self.eventInput(event=event, modify_date=False, rm=True)
				if new_event == 7: # remove event
					if e_i == (len(events)-1):
						events = events[:e_i]
					else: events = events[:e_i] + events[e_i+1:]
					self.o('\nEvent removed.\n')
				elif new_event != 0:
					events[e_i] = new_event
			# option for cmd numbers to depend on list length
			#elif option=='6':
				# subtract content
			#	if len(contents) > 0:
			#		contents = contents[:len(contents)-1]
					#self.c(); self.o(menu)
					#self.o('Last content removed\n')
					#self.s(2)
			#	else:
			#		self.c(); self.o(menu)
			#		self.o('There are no contents.\n')
			#		self.s(2)
			#elif option=='7':
			#	# add content
			#	contents+= [Book.emptyContent()]
			#	#self.c(); self.o(menu)
			#	#self.o('Content added\n')
			#	#self.s(2)
			elif option=='7':
				# add event
				event = Book.emptyEvent()
				event.date = date_1
				new_event = self.eventInput(event=event, modify_date=False, rm=False)
				if new_event == 0: pass
				else:
					# add new event to file, add to correct loc
					book.events += [new_event]
					i = -1
					for j in range(len(book.dates)):
						if book.dates[j] == new_event.date:
							i = j
					if i == -1: book.dates.append(new_event.date)
					Book.saveBook(book)
					print('\nEvent added.\n'); self.s(2)
			elif option=='8':
				if page == 0:
					self.c(); self.o(menu)
					self.o('Already on first page.\n')
					self.s(2)
				else: 
					page-= 1
			elif option=='9':
				nxt_event_l = events[length*(page+1):length*(page+2)]
				if len(nxt_event_l) == 0:
					self.c(); self.o(menu)
					self.o('Already on last page.\n')
					self.s(2); 
				else: 
					page+= 1
			elif option=='0':
				# return to date list
				return events
			else:
				self.c(); self.o(menu)
				self.o('Invalid command.\n')
				self.s(2)
				#contents = self.contentsList(contents, page)
	def eventInput(self, event=None, modify_date=True, rm=False):
		if event is None:
			event = Book.emptyEvent()	
			event.date = Book.strDate()
			event.time_start = Book.strTime()
		while True:
			menu = self.eventFields(event, rm)		
			self.c(); self.o(menu)
			self.o('Enter field:\n')
			option = self.i()
			if option == '1':
				if modify_date:
					self.c(); self.o(menu)
					self.o('Enter date:\n')
					date = self.i()
					# assert date formatting
					event.date = Book.strDate(Book.dictDate(date))
				else:
					self.c(); self.o(menu)
					self.o('Date field in Edit is immutable.\n')
					self.o('To create an event with any date, use Start in Main Menu.\n')
					self.s(4)
			elif option=='2':
				self.c(); self.o(menu)
				self.o('Enter start time:\n')
				time_start = self.i()
				# assert start time formatting
				event.time_start = time_start
				if event.time_start == '':
					event.time_duration = ''
			elif option=='3': 
				self.c(); self.o(menu)
				self.o('Enter end time:\n')
				time_end = self.i()
				# assert end time formatting
				event.time_end = time_end
				# assert start and end times not empty for duration
				start_dict = Book.dictTime(event.time_start)
				end_dict = Book.dictTime(event.time_end)
				duration_dict = Book.getDuration(start_dict, end_dict)
				duration_str = Book.strTime(duration_dict)
				event.time_duration = duration_str
			elif option=='4':	
				self.c(); self.o(menu)
				self.o('Enter starting page:\n')
				page_start = self.i()
				# assert starting page formatting
				event.page_start = page_start
				# add conversion for roman numerals
				event.page_coverage = Book.getPageCoverage(event.page_start, event.page_end)
				#if not event.page_start.isnumeric():
				#	event.page_coverage = 'na'
				#elif event.page_start.isnumeric() \
				#	and event.page_end.isnumeric():
				#		event.page_coverage = str(int(event.page_end)-int(event.page_start))
				#elif not event.page_start.isnumeric() \
				#	and event.page_end != '': event.page_coverage = 'na'
				#elif event.page_start == '': event.page_coverage = ''	
			elif option=='5': 
				self.c(); self.o(menu)
				self.o('Enter ending page:\n')
				page_end = self.i()
				# assert ending page formatting
				if event.page_start.isnumeric() \
					and event.page_end.isnumeric() \
					and page_end < event.page_start:
					self.c(); self.o(menu)
					self.o('Invalid ending page number\n')
					self.s(2)
				else:
					event.page_end = page_end
					event.page_coverage = Book.getPageCoverage(event.page_start, event.page_end)
					# assert page start and end not empty for coverage
					# add conversion for roman numerals
					#if event.page_start.isnumeric() and event.page_end.isnumeric():
					#	event.page_coverage = str(int(event.page_end)-int(event.page_start))
					#elif event.page_end == '': event.page_coverage = ''
					#else: event.page_coverage = 'na'
			elif option=='6': 
				# assert date, start time, and page_start not empty
				return event
			elif option=='7' and rm:
				return 7
			elif option=='0': return 0
			else:
				self.c(); self.o(menu)
				self.o('Invalid command.\n')
				self.s(2)
	def eventFields(self, event, rm=False):
		menu = 'Event Fields\n\n'
		menu+= f' 1 | Date                   | {event.date} \n'
		menu+= f' 2 | Start time             | {event.time_start} \n'
		menu+= f' 3 | End time               | {event.time_end} \n'	
		menu+= f' 4 | Starting page          | {event.page_start}\n'
		menu+= f' 5 | Ending page            | {event.page_end}\n\n'
		menu+= f'   Immutable fields\n\n'
		menu+= f'     Duration               | {event.time_duration}\n'
		menu+= f'     Page coverage          | {event.page_coverage}\n'
		menu+= f'     Words per minute       | {event.avg_wpm}\n'
		menu+= f'     Minutes per page       | {event.avg_mpp}\n\n'
		menu+= f' 6 | Continue\n'
		if rm:
			menu+= f' 7 | Remove event\n'
		menu+= f' 0 | Cancel\n\n'
		return menu
		
	def classPrograms(self):
		pms = self.readPrograms()
		c_pms = []
		for i in range(len(pms)):
			pm = pms[i]
			pds = pm['pds']
			c_pds = []
			for j in range(len(pds)):
				pd = pds[j]
				os = pd['os']
				c_os = []
				for o in range(len(os)):
					c_o = Operation.fromString(os[o])
					c_os.append(c_o)
				c_pd = Period(pd['ex'],c_os,pd['fl'],pd['fu'],pd['sl'],pd['su'])
				c_pds.append(c_pd)
			c_pm = Program(pm['n'],pm['k'],pm['r'],c_pds)
			c_pms.append(c_pm)
		return c_pms
	def duplicateProgram(self, name):
		pms = self.readPrograms()
		for pm in pms:
			if pms[pm]['n'] == name:
				return True
		return False
	def replaceProgram(self, pm, pms=None):
		if pms is None: pms = self.readPrograms()
		for pm_i in pms:
			if pms[pm_i]['n'] == pm.n: 
				pms[pm_i] = pm
				self.programWrite(pms=pms)
		return 0
	def removeProgram(self, pm, pms=None):
		if pms is None: pms = self.readPrograms()
		pms_c = pms.copy()
		r = False
		for pm_i in pms:
			if r:
				pms_c[pm_i-1] = pms[pm_i]
				pms_c.pop(pm_i) 
			if pms[pm_i]['n'] == pm.n:
				pms_c.pop(pm_i)
				self.programWrite(pms=pms)
				r = True
		if r: self.programWrite(pms=pms_c)
		return 0
	""" Functions for I/O """
	def c(self):
		os.system('clear')
	def o(self, s):
		sys.stdout.write(s)
		sys.stdout.flush()
	def n(self, c=1):
		sys.stdout.write('\n'*c)
		sys.stdout.flush()
	def t(self, c=1):
		sys.stdout.write('\t'*c)
		sys.stdout.flush()
	def i(self):
		sys.stdout.flush()
		return sys.stdin.readline()[:-1]
	def s(self, sec):
		sleep(sec) #os.system(f'sleep {sec}')
	def readBooks(self):
		with open('data/books.txt','r') as data:
			return ast.literal_eval(data.read())
	def programWrite(self, pm=None, pms=None):
		if pm and pms is None: 
			pms = self.readPrograms()
			n = len(pms)
			pms[n] = pm.dict()
		with open('data/programs.txt','w') as data:
			data.write(self.rds(pms, 0))
	def readPractices(self):
		with open('data/practices.txt','r') as data:
			return ast.literal_eval(data.read())
	def writePractices(self, pe):
		pes = self.readPractices()
		n = len(pes)
		pes[n] = pe.dict()
		with open('data/practices.txt','w') as data:
			data.write(self.rds(pes, 0))
	""" Functions for strings """
	def sn(self, c=1):
		return '\n'*c
	def st(self, c=1):
		return '\t'*c
	def rds(self, d, t): # recursive dictionary string
		s = self.st(t) + '{' + self.sn()
		i = 0
		l = len(d)-1
		for k in d:
			if type(k) == str:
				s+= self.st(t)
				s+= '\'' + str(k) + '\'' +  ': '
			elif type(k)==int:
				s+= self.st(t)
				s+= str(k) + ': '
			if type(d[k]) == dict:
				s+= self.sn()
				s+= self.rds(d[k], t+1)
			elif type(d[k])==str:
				s+= '\'' + d[k] + '\''
			elif type(d[k])==int:
				s+= str(d[k])
			elif type(d[k])==bool:
				s+= str(d[k])
			if i < l:
				s+= ',' + self.sn()
				i+= 1
			else:
				s+= self.sn()
		s+= self.st(t) + '}'
		return s


