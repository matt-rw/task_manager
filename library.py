import os
import sys
from time import sleep
from ast import literal_eval
from datetime import datetime
import editor
from table import Table
PATH = '/Users/matthewwear/Desktop/'
class Books:
	def __init__(self):
		self.books = self.readBooks()
	def readBooks(self):
		files = os.popen(f'ls {PATH+"d_library/library"}').read()
		files = files.rsplit('\n')[:-1]
		return files
	def writeBooks(self):
		books = self.booksToDictionary()
		with open('data/books.txt', 'w') as data:
			data.write(books)
		return
	def bookList(self, page=0, length=7):
		while True:
			tcols = int(os.popen('tput cols').read())
			tlines = int(os.popen('tput lines').read())
			menu = f'Select Book\n\n'
			menu+='Books\n'
			books = self.books
			book_l = books[length*page:length*(page+1)] 
			for i in range(len(book_l)):
				book = book_l[i]
				if len(book) > tcols-5:
					filetype = ''
					if '.pdf' in book or '.txt' in book:
						filetype = book[-3:]
					book = book[:tcols-11] + '...' + filetype
				menu+= f' {i+1} | {book}\n'
			#max_l = 0
			#for book_i in range(len(book_l)):
			#	if len(book_l[book_i].title) > max_l:
			#		max_l = len(book_l[book_i].title)
			#for book_i in range(len(book_l)):
			#	title   = book_l[book_i].title
			#	n_l = len(title)
			#	if n_l < max_l:
			#		title+= ' '*(max_l-n_l)
			#	author = book_l[book_i].author
			#	menu+=f' {book_i+1}   | {title} | {author}\n'
			menu+= '\n'
			menu+= ' 8/9 | Previous/Next page\n'
			menu+= ' 0   | Back\n\n'
			self.c(); self.o(menu)
			self.o('Enter number:\n')
			option = self.i()
			if option.isnumeric():
				if 1 <= int(option) <= length:
					book = self.books[(int(option)-1)+(length*page)]
					return book
				elif option=='8':
					if page == 0:
						self.c(); self.o(menu)
						self.o('Already on first page.\n')
						self.s(2)
					else: page -= 1
				elif option=='9':
					nxt_book_l = books[length*(page+1):length*(page+2)]
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
	def viewBook(book, args:list):
		# args
		book_events = args[0]
		book_duration = args[1]
		date_durations = args[2]
		print(book_events)
		# initialize general stats
		book_stats = Books.computeBookStats(book_events, pages=120, words_per_page=200)
		print(book_stats)	
		hours_today = '0:00'
		hours_this_week = '0:00'
		hours_last_week = '0:00'
		hours_this_month = '0:00'
		hours_total = '0:00'
		days_since_start = 0
		days_read = 0
		avg_words_per_min = 0
		avg_mins_per_page = 0
		# get dates menu
		dates = []
		for date in book_events:
			dates.append(date)
		page = 0
		page_dates = Books.dateMenu(dates, page)
	def dateMenu(dates, page=0):
		length = 5
		header = ''
		page_dates = dates[length*page:length*(page+1)]
		page_range = range(len(page_dates))
		s_list = []
		if header: s_list+= [header+'\n']	
		for i in page_range:
			s_list+= [f' {i+1} | {page_dates[i]}']
		return s_list
	def computeBookStats(events, pages, words_per_page):
		hours_today = '0:00'
		hours_this_week = '0:00'
		hours_last_week = '0:00'
		hours_this_month = '0:00'
		hours_total = '0:00'
		days_read = 0
		days_since_start = 0
		date_started = ''
		date_finished = ''
		pages_read = 0
		pages_today = 0	
		words_per_min_avg = 0
		words_per_min_today = 0
		mins_per_page_avg = 0
		mins_per_page_today = 0
		# hours today
		today = Table.getToday()
		if today in events:
			for event in events[today]:
				event_duration = Table.timeDifference(event[0], event[1])
				hours_today = Table.timeSummation(hours_today, event_duration)
		# hours this week
		weekday = datetime.weekday(datetime.today())
		date_i = today
		for i in range(weekday):
			if date_i in events:
				for event in events[date_i]:
					event_duration = Table.timeDifference(event[0], event[1])
					hours_this_week = Table.timeSummation(hours_this_week, event_duration)
			date_i = Table.subDay(date_i)
		# hours last week
		last_sun = Table.subDay(today, repeat=weekday+1)
		date_i = last_sun
		for i in range(6):
			if date_i in events:
				for event in events[date_i]:
					event_duration = Table.timeDifference(event[0], event[1])
					hours_last_week = Table.timeSummation(hours_last_week, event_duration)
			date_i = Table.subDay(date_i)
		# hours this month
		_, day, _ = today.rsplit('/')
		date_i = today
		for i in range(int(day)):
			if date_i in events:
				for event in events[date_i]:
					event_duration = Table.timeDifference(event[0], event[1])
					hours_this_month = Table.timeSummation(hours_this_month, event_duration)
			date_i = Table.subDay(date_i)
		# hours total and days read
		for date in events:
			for event in events[date]:
				event_duration = Table.timeDifference(event[0], event[1])
				hours_total = Table.timeSummation(hours_total, event_duration)
			days_read+= 1
		# day started and day finished
		i = 0
		for date in events:
			if i == 0: 
				date_started = date
			elif i == len(events):
				idx = event[2].index('(pages')
				pages = event[2][idx:]
				idx = pages.index('-')
				page_end = pages[idx+1:-1]
				if page_end == pages:
					date_finished = date
			i+= 1
		# pages read and pages today
		for date in events:
			for event in events[date]:
				idx = event[2].index('(pages')
				pages = event[2][idx:]
				idx = pages.index('-')
				page_start = pages[7:idx]
				page_end = pages[idx+1:-1]
				if page_start.isnumeric() and page_end.isnumeric():
					coverage = int(page_end) - int(page_start)
					pages_read += coverage
					if date == today:
						pages_today += coverage
		# words per min avg
		hours, mins = hours_total.rsplit(':')
		mins = (int(hours) * 60) + int(mins)
		if mins == 0:
			words_per_min_avg = None
		else:
			words_per_min_avg = (pages_read * words_per_page) / mins	
		# words per min today
		hours, mins = hours_today.rsplit(':')
		mins = (int(hours) * 60) + int(mins)
		if mins == 0:
			words_per_min_today = None
		else:
			words_per_min_today = (pages_today * words_per_page) / mins	
		# mins per page avg
		hours, mins = hours_total.rsplit(':')
		mins = (int(hours) * 60) + int(mins)
		if pages_read == 0:
			mins_per_page_avg = None
		else:
			mins_per_page_avg = mins / pages_read
		# mins per page today
		hours, mins = hours_today.rsplit(':')
		mins = (int(hours) * 60) + int(mins)
		if pages_today == 0:
			mins_per_page_today = None
		else:
			mins_per_page_today = mins / pages_today
		# format output
		stats = [hours_today, hours_this_week, hours_last_week, hours_this_month, hours_total, days_read, days_since_start, date_started, date_finished, pages_read, pages_today, words_per_min_avg, words_per_min_today, mins_per_page_avg, mins_per_page_today]
		return stats
	def c(self):
		os.system('clear')
	def o(self, s):
		sys.stdout.write(s)
		sys.stdout.flush()
	def i(self):
		sys.stdout.flush()
		return sys.stdin.readline()[:-1]
	def s(self, sec):
		sleep(sec)
	def strDate(date:dict=None):
		if date is None:
			d = Book.dictDate()
		else: d = date
		return f'{d["weekday"]} {d["month"]}/{d["day"]}/{d["year"]}'
	def dictDate(date:str=None):
		weekdays = [
			'Mon', 'Tue', 'Wed', 'Thu', 
			'Fri', 'Sat', 'Sun'
			]
		if date is None:
			d = datetime.today()
			weekday = datetime.weekday(d)
			weekday = weekdays[weekday]
		else: 
			if not date[0].isnumeric():
				weekday = date[:3]
				d = date[4:].rsplit('/')
				d = [int(d[0]), int(d[1]), int(d[2])]
				d = datetime(month=d[0], day=d[1], year=d[2])
			elif date[0].isnumeric():
				d = date.rsplit('/')
				d = [int(d[0]), int(d[1]), int(d[2])]
				d = datetime(month=d[0], day=d[1], year=d[2])
				weekday = datetime.weekday(d)
				weekday = weekdays[weekday]
		return {'weekday':weekday, 'month':d.month, 'day':d.day, 'year':d.year}	
if __name__ == '__main__':
	books = Books()
	books.bookList()
