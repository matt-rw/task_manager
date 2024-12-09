from ast import literal_eval
from datetime import *
class Book:
	def __init__(
		self, title, author, publisher, date_pub,
		config, location, pages, contents,
		avg_wpp, avg_wpm, avg_mpp, avg_mpc,
		date_start, date_end, events, dates
		):
		self.title      = title
		self.author     = author
		self.publisher  = publisher
		self.date_pub   = date_pub
		# edition
		
		self.config     = config
		self.location   = location
	
		self.pages      = pages
		self.contents   = contents
		
		self.avg_wpp    = avg_wpp
		self.avg_wpm    = avg_wpm
		self.avg_mpp    = avg_mpp
		self.avg_mpc	= avg_mpc

		self.date_start = date_start
		self.date_end   = date_end
		self.events     = events
		self.dates      = dates

	fields = [	
		'title', 'author', 'publisher', 'date_pub',
		'config', 'location', 'pages', 'contents',
		'avg_wpp', 'avg_wpm', 'avg_mpp', 'avg_mpc',
		'date_start', 'date_end', 'events', 'dates'
		]
		
	class Content:
		def __init__(	
			self, title, category, page_start, page_end
			):
			self.title       = title
			self.category    = category
			self.page_start  = page_start
			self.page_end    = page_end

		fields = [
			'title', 'category', 'page_start', 'page_end'
			]

	class Event:
		def __init__(
			self, date, time_start, time_end, time_duration,
			page_start, page_end, page_coverage,
			avg_wpm, avg_mpp
			):
			self.date           = date
			self.time_start     = time_start
			self.time_end       = time_end
			self.time_duration  = time_duration
			
			self.page_start     = page_start
			self.page_end       = page_end
			self.page_coverage  = page_coverage

			self.avg_wpm        = avg_wpm
			self.avg_mpp        = avg_mpp
		
		fields = [	
			'date', 'time_start', 'time_end', 'time_duration',
			'page_start', 'page_end', 'page_coverage',
			'avg_wpm', 'avg_mpp'
			]
	
	def addContent(self, content_args):
		self.contents += Content(content_args)
	
	def addEvent(self, event_args):
		self.events   += Event(event_args)

	def startBook():
		b_args=[None]*len(Book.fields)
		c_args=[None]*len(Book.Content.fields)
		e_args=[]
		for i in range(len(Book.fields)):
			if Book.fields[i] == 'contents':
				print('number of contents')
				c_number = int(input())
				print()
				b_args[i] = [None]*c_number
				for j in range(c_number):
					for k in range(len(Book.Content.fields)):
						print(Book.Content.fields[k])
						c_args[k] = input()
						print()
					b_args[i][j] = Book.Content(
						c_args[0],c_args[1],c_args[2],c_args[3]
						)
					c_args=[None]*len(Book.Content.fields)
			if Book.fields[i] == 'events':
				b_args[i] = []
			if Book.fields[i] == 'avg_wpm' or Book.fields[i] == 'avg_mpp':
				b_args[i] = None
			print(Book.fields[i])
			b_args[i] = input()
			print()
		return Book(
			b_args[0],b_args[1],b_args[2],b_args[3],
			b_args[4],b_args[5],b_args[6],b_args[7],
			b_args[8],b_args[9],b_args[10],
			b_args[11],b_args[12],b_args[13]
			)
	
	def emptyBook():
		empty_book = Book(
			'', '', '', '',
			'', '', '', 
			[],
			'', '', '', '',
			'', '', 
			[], []
			)
		return empty_book
	
	def emptyContent():
		empty_content = Book.Content(
			'', '', '', ''
			)
		return empty_content
	
	def emptyEvent():	
		empty_event = Book.Event(
			'', '', '', '',
			'', '', '',
			'', ''
			)
		return empty_event
	
	def insertEvent(book, event):
		d = Book.dictDate(event.date)
		d = datetime(d['year'], d['month'], d['day'])
		d_list = []
		for i in range(len(book.dates)):
			d_i = Book.dictDate(book.dates[i])
			d_i = datetime(d_i['year'], d_i['month'], d_i['day'])
			# d < d_i
			if d < d_i:
				d_list += [event.date]
				d_list += book.dates[i:]
				break
			# d == d_i
			elif d == d_i: 
				d_list+= book.dates[i:]; break
			# d > d_i and i == len(book.dates)-1
			elif d > d_i:
				d_list += [book.dates[i]]
			if i == (len(book.dates)-1):
				d_list += [event.date]
		if len(book.dates) == 0:
			d_list += [event.date]
		book.dates = d_list
		t_s = Book.dictTime(event.time_start)
		if t_s['code'] == 'PM' and t_s['hour'] > 12:
			t_s['hour']+= 12
		elif t_s['code'] == 'AM' and t_s['hour'] == 12:
			t_s['hour']-= 12
		t_s = time(hour=t_s['hour'], minute=t_s['minute'])
		e_list = []
		for i in range(len(book.events)):
			t_s_i = Book.dictTime(book.events[i].time_start)
			if t_s_i['code'] == 'PM' and t_s_i['hour'] > 12:
				t_s_i['hour']+= 12
			elif t_s_i['code'] == 'AM' and t_s_i['hour'] == 12:
				t_s_i['hour']-= 12
			t_s_i = time(hour=t_s_i['hour'], minute=t_s_i['minute'])
			d_i = Book.dictDate(book.events[i].date)
			d_i = datetime(d_i['year'], d_i['month'], d_i['day'])
			# if d < d_i:
			if d < d_i:
				e_list += [event]
				e_list += book.events[i:]
				break
			elif d == d_i and t_s < t_s_i:
				e_list += [event]
				e_list += book.events[i:]
				break
			elif d > d_i:
				e_list += [book.events[i]]
			elif d == d_i and t_s > t_s_i:
				e_list += [book.events[i]]
			if i == (len(book.events)-1):
				e_list += [event]
		if len(book.events) == 0:
			e_list += [event]
		book.events = e_list
		return book
	
	def readBooks(path=''):
		with open(path+'data/books.txt', 'r') as data:
			books_dict = literal_eval(data.read())
		books = []
		for i in range(len(books_dict)):
			books += [Book.fromDictionary(book=books_dict[i])]
		return books

	def saveBook(book, replace=True, path=''):
		book_dict = Book.toDictionary(book=book)
		with open(path+'data/books.txt','r') as data:
			books_dict = literal_eval(data.read())
		if replace:
			i = -1
			for j in range(len(books_dict)):
				if books_dict[j]['title'] == book_dict['title'] \
					and books_dict[j]['author'] == book_dict['author']:
					i = j
			if i != -1: books_dict[i] = book_dict
			else:       replace = False
		if not replace:
			books_dict[len(books_dict)] = book_dict
		with open(path+'data/books.txt','w') as data:
			data.write(Book.rds(books_dict))
	
	def saveBooks(books:list, path=''):
		books_dict = Book.booksDict(books)
		with open(path+'data/books.txt','w') as data:
			data.write(Book.rds(books_dict))

	def clearData():
		with open('data/books.txt','w') as data:
			data.write('{}')
	
	def saveBackup():
		with open('data/books.txt','r') as data:
			books_dict = literal_eval(data.read())
		file = f'{Book.strDate()[4:]} {Book.strTime()}.txt'
		file = file.replace('/','-').replace(' ','_').replace(':','-')
		path = f'data/backups/'
		with open(path+file, 'w') as data:
			data.write(Book.rds(books_dict))
	
	def booksDict(books:list=None):
		if books is None: books = Book.readBooks()	
		books_dict = {}
		i = 0
		for b_i in books:
			book_dict = Book.toDictionary(book=b_i)
			books_dict[i] = book_dict
			i+= 1
		return books_dict

	def toDictionary(
		book=None, content=None, event=None
		):
		d = {}
		bf = Book.fields
		cf = Book.Content.fields
		ef = Book.Event.fields
		if book:
			c_d = {}
			for i in range(len(book.contents)):
				c_d[i] = Book.toDictionary(content=book.contents[i])
			
			e_d = {}
			for i in range(len(book.events)):
				e_d[i] = Book.toDictionary(event=book.events[i])

			d_d = {}
			for i in range(len(book.dates)):
				d_d[i] = book.dates[i]

			d[bf[0]] = book.title
			d[bf[1]] = book.author
			d[bf[2]] = book.publisher
			d[bf[3]] = book.date_pub
		
			d[bf[4]] = book.config
			d[bf[5]] = book.location
		
			d[bf[6]] = book.pages
			
			d[bf[7]] = c_d
		
			d[bf[8]] = book.avg_wpp
			d[bf[9]] = book.avg_wpm
			d[bf[10]] = book.avg_mpp
			d[bf[11]] = book.avg_mpc

			d[bf[12]] = book.date_start
			d[bf[13]] = book.date_end
			
			d[bf[14]] = e_d
			d[bf[15]] = d_d
		
		if content:
			d[cf[0]] = content.title
			d[cf[1]] = content.category
			d[cf[2]] = content.page_start
			d[cf[3]] = content.page_end
	
		if event:
			d[ef[0]] = event.date
			d[ef[1]] = event.time_start
			d[ef[2]] = event.time_end
			d[ef[3]] = event.time_duration  
			
			d[ef[4]] = event.page_start
			d[ef[5]] = event.page_end
			d[ef[6]] = event.page_coverage

			d[ef[7]] = event.avg_wpm
			d[ef[8]] = event.avg_mpp
			
		return d			
	
	def fromDictionary(
		book=None, content=None, event=None
		):
		o = None
		bf = Book.fields
		cf = Book.Content.fields
		ef = Book.Event.fields
		if book:	
			c_o = []
			for i in range(len(book[bf[7]])):
				c_o   += [Book.fromDictionary(content=book[bf[7]][i])]

			e_o = []
			for i in range(len(book[bf[14]])):
				e_o   += [Book.fromDictionary(event=book[bf[14]][i])]

			dates = []
			for i in range(len(book[bf[15]])):
				dates += [book[bf[15]][i]]
			
			o = Book(
			title      = book[bf[0]],
			author     = book[bf[1]],
			publisher  = book[bf[2]],
			date_pub   = book[bf[3]],
		
			config     = book[bf[4]],
			location   = book[bf[5]],
		
			pages      = book[bf[6]],
			
			contents   = c_o,
		
			avg_wpp    = book[bf[8]],
			avg_wpm    = book[bf[9]],
			avg_mpp    = book[bf[10]],
			avg_mpc    = book[bf[11]],
			date_start = book[bf[12]],
			date_end   = book[bf[13]],
			
			events     = e_o,
			dates      = dates
			)

		if content:
			o = Book.Content(
			title      = content[cf[0]],
			category   = content[cf[1]],
			page_start = content[cf[2]],
			page_end   = content[cf[3]],
			)

		if event:
			o = Book.Event(
			date          = event[ef[0]],
			time_start    = event[ef[1]],
			time_end      = event[ef[2]],
			time_duration = event[ef[3]],
			
			page_start    = event[ef[4]],
			page_end      = event[ef[5]],
			page_coverage = event[ef[6]],

			avg_wpm       = event[ef[7]],
			avg_mpp       = event[ef[8]],
			)

		return o

	def rds(d, t=0):
		s = ('\t'*t)+'{'+'\n'
		i = 0; l = len(d)-1
		for k in d:
			if type(k)==str:
				s += ('\t'*t)+'\''+k+'\''+': '
			elif type(k)==int:
				s += ('\t'*t)+str(k)+': '
			if type(d[k])==dict:
				s += '\n'
				s += Book.rds(d[k], t+1)
			elif type(d[k])==str:
				s += '\''+d[k]+'\''
			if i < l:
				s += ', '+'\n'
				i += 1
			else: s += '\n'
		s += ('\t'*t)+'}'
		return s

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

	def strTime(time:dict=None):
		if time is None:
			t = Book.dictTime()
		else: t = time
		if t['minute'] < 10:
			t['minute'] = '0'+str(t['minute'])
		if 'code' in t:
			return f'{t["hour"]}:{t["minute"]} {t["code"]}'
		else:
			return f'{t["hour"]}:{t["minute"]}'

	def dictTime(time:str=None):
		if time is None:
			t = datetime.now()
			h = t.hour; m = t.minute; #s = t.second
			code = 'AM'
			if h > 12:
				h = h-12
				code = 'PM'
			elif h == 12:
				code = 'PM'
			elif h == 0:
				h = 12
		else:
			t = time[:-3].rsplit(':')
			h = int(t[0])
			m = int(t[1])
			code = time[-2:]
		return {'hour':h, 'minute':m, 'code':code}

	def getDuration(t1, t2):
		# up to seconds and minutes; not hours nor milliseconds
		# t2 > t1
		h1, h2 = t1['hour'], t2['hour']
		m1, m2 = t1['minute'], t2['minute']
		c1, c2 = t1['code'], t2['code']
		if c1 == 'PM' and h1 != 12: h1 += 12
		if c1 == 'AM' and h1 == 12: h1 = 0
		if c2 == 'PM' and h2 != 12: h2 += 12
		if c2 == 'AM' and h2 == 12: h2 = 0
		dt1 = datetime(1,1,1,hour=h1,minute=m1,second=0,microsecond=0)	
		dt2 = datetime(1,1,1,hour=h2,minute=m2,second=0,microsecond=0)
		dtd = dt2 - dt1
		ds = dtd.seconds
		dh = ds // (60**2)
		dm = (ds //  60) % 60
		return {'hour': dh, 'minute':dm}

	def getPageCoverage(p1, p2):
		p1n = p1.isnumeric(); p2n = p2.isnumeric()
		p1e = (p1 == ''); p2e = (p2 == '')
		if p1n and p2n:
			return str(int(p2) - int(p1))
		elif (p1n and p2e) or (p1e and p2n):
			return ''
		elif (p1n and not p2e) or (not p1e and p2n):
			return 'na'
		elif (p1e and not p2e) or (not p1e and p2e):
			return 'na'
		else:
			return ''

if __name__ == '__main__':
	test_book = Book(
		'title', 'author', 'publisher', 'date',
		'config', 'location', 'pages', 
		[Book.Content(
		'title_content', 'category', 'page_start', 'page_end'
		)],
		'avg_wpp', 'avg_wpm', 'avg_mpp', 'avg_mpc',
		'date_start', 'date_end', 
		[Book.Event(
		'date', 'time_start', 'time_end', 'time_duration',
		'page_start', 'page_end', 'page_coverage',
		'avg_wpm', 'avg_mpp'
		)], []
		)
	Book.clearData()
	Book.saveBook(book=test_book)
	#Book.startBook()
	books = Book.readBooks()
	print(books)
	Book.saveBackup()
