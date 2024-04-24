from flask import Flask, render_template, redirect, request, session
import flask
import mysql.connector
import json
from better_profanity import profanity


app = Flask(__name__)
app.secret_key = "sasank"

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "",
	port = 3307,
	database = "sagss"
)
v_msg = ''
meetingroom_status = ''

# =============================login============================================================================================
@app.route("/login", methods = ['POST', 'GET'])
def login():
	global v_msg
	if request.method == 'GET':
		if "user" in session:
			return redirect("/home")
		else:
			return render_template("login.html",err_msg = '')
	if request.method == 'POST':
		values = request.form.to_dict()
		if values["adid"] == 'FOOD_VENDOR' or values["password"] == 'FOOD_VENDOR':
			session['user'] = 'FOOD_VENDOR'
			session['name'] = 'FOOD_VENDOR'
			return redirect("/food")
		mycursor = mydb.cursor()
		sql = "SELECT user_id,name,role FROM users WHERE adid = %s AND password = %s"
		val = (values["adid"], values["password"])
		mycursor.execute(sql, val)
		result = mycursor.fetchone()
		if result:
			session['user'] = result[0]
			session['name'] = result[1]
			session['role'] = result[2]
			return redirect("/home")
		else:
			v_msg = "invalid credentials"
			return render_template("login.html",err_msg = v_msg)
		
# =============================home============================================================================================
@app.route("/")
@app.route("/home", methods = ['POST', 'GET'])
def home():
	if request.method == 'GET':
		if "user" in session:
			if session.get('user') == 'FOOD_VENDOR':
				return redirect("/food")

			# clear old data
			mycursor = mydb.cursor()
			sql = "delete from `locker_mapping` where to_date < curdate()"
			mycursor.execute(sql)
			mydb.commit()

			mycursor = mydb.cursor()
			sql = "delete from `meetings` where date < curdate()"
			mycursor.execute(sql)
			mydb.commit()

			mycursor = mydb.cursor()
			sql = "delete from `sports_mapping` where date < curdate()"
			mycursor.execute(sql)
			mydb.commit()

			mycursor = mydb.cursor()
			sql = "delete from `food_mapping` where date < curdate()"
			mycursor.execute(sql)
			mydb.commit()

			# load data to dashboard display
			mycursor = mydb.cursor()
			sql = "SELECT * FROM `locker_mapping` where user_id = %s"
			val = (session.get('user'),)
			mycursor.execute(sql,val)
			myresult = mycursor.fetchall()

			mycursor = mydb.cursor()
			sql = "SELECT * FROM `meetings` where user_id = %s"
			val = (session.get('user'),)
			mycursor.execute(sql,val)
			myresult2 = mycursor.fetchall()

			mycursor = mydb.cursor()
			sql = "SELECT * FROM `food_mapping` where user_id = %s"
			val = (session.get('user'),)
			mycursor.execute(sql,val)
			myresult3 = mycursor.fetchall()
			arra = []
			for i in myresult3:
				name2 = json.loads(i[1].replace("'", '"'))
				for key, valu in name2.items():
					if key != 'total':
						if int(valu) == 0:
							continue
						mycursor2 = mydb.cursor()
						sql = "SELECT food FROM `foodmenu` where id = %s"
						val = (int(key),)
						mycursor2.execute(sql,val)
						key = mycursor2.fetchone()[0]
						for j in range(int(valu)):
							arra.append(key)
			arra2 = list(set(arra))
			arra3 = []
			for i in arra2:
				arra3.append((i,arra.count(i),))
			
			mycursor = mydb.cursor()
			sql = "SELECT * FROM `sports_mapping` where user_id = %s"
			val = (session.get('user'),)
			mycursor.execute(sql,val)
			myresult4 = mycursor.fetchall()


			mycursor = mydb.cursor()
			sql = "SELECT * FROM `posts` where date(date) >= curdate()"
			mycursor.execute(sql)
			myresult5 = mycursor.fetchall()
			return render_template("home.html",myresult = myresult,myresult2 = myresult2,myresult3 = arra3, myresult4 = myresult4,myresult5 = myresult5,role = session.get('role'),sessionname = session.get('name'))
		else:
			return redirect("/login")

# =============================locker============================================================================================
from datetime import datetime,date
@app.route("/locker", methods = ['POST', 'GET'])
def locker():
	if request.method == 'GET':
		if "user" not in session:
			return redirect("/login")
		
		return render_template("locker.html",err_msg = "", role = session.get('role'),sessionname = session.get('name'))
	if request.method == 'POST':
		values = request.form.to_dict()

		if datetime.strptime(values["start_date"], '%Y-%m-%d') < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) or datetime.strptime(values["end_date"], '%Y-%m-%d') < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
			return render_template("locker.html",err_msg = "past date not allowed", role = session.get('role'),sessionname = session.get('name'))
		if datetime.strptime(values["start_date"], '%Y-%m-%d') > datetime.strptime(values["end_date"], '%Y-%m-%d'):
			return render_template("locker.html",err_msg = "start date should be less than end date", role = session.get('role'),sessionname = session.get('name'))
		mycursor = mydb.cursor()
		sql = """SELECT l.locker_no, l.floor
		FROM lockers l
		LEFT JOIN (
			SELECT locker_no, floor
			FROM locker_mapping
			WHERE from_date <= %s AND to_date >= %s
			) lm ON l.locker_no = lm.locker_no
			WHERE lm.locker_no IS NULL and l.floor = %s limit 1"""
		val = (values["start_date"],values["start_date"],values["lockerfloor"],)
		mycursor.execute(sql,val)
		myresult = mycursor.fetchall()

		if myresult:
			sql = "Insert into `locker_mapping` (locker_no,user_id,floor,from_date,to_date) values (%s,%s,%s,%s,%s)"
			val = (myresult[0][0],session.get('user'),values["lockerfloor"],values["start_date"],values["end_date"])
			mycursor.execute(sql,val)
			mydb.commit()
			return redirect("/")
		else:
			return "Locker not available"


# =============================locker============================================================================================
@app.route("/food", methods = ['POST', 'GET'])
def food():
	if request.method == 'GET':
		mycursor = mydb.cursor()
		sql = "delete from `food_mapping` where date < curdate() - interval 1 day"
		mycursor.execute(sql)
		mydb.commit()

		if "user" not in session:
			return redirect("/login")
		if session.get('user') == 'FOOD_VENDOR':
			mycursor = mydb.cursor()
			sql = "SELECT U.name,FM.foodlist FROM `food_mapping` FM inner join `users` U on FM.user_id = U.user_id"
			mycursor.execute(sql)
			food_menu = mycursor.fetchall()
			arr,arr2,arr3,arr4,arr5 = [],[],[],[],[]
			for i in food_menu:
				name = i[0]
				name2 = json.loads(i[1].replace("'", '"'))
				for key, valu in name2.items():
					if key != 'total':
						if int(valu) == 0:
							continue
						mycursor2 = mydb.cursor()
						sql = "SELECT food FROM `foodmenu` where id = %s"
						val = (int(key),)
						mycursor2.execute(sql,val)
						key = mycursor2.fetchone()[0]
						arr.append((name,key,int(valu),))
						# distinct keys and count of each key
						arr2.append(key)
						arr4.append(name)
			arr2 = list(set(arr2))
			for i in arr2:
				count = 0
				for j in arr:
					if j[1] == i:count += j[2]
				arr3.append((i,count,))
			arr4 = list(set(arr4))
			for i in arr4:
				for j in arr:
					count = 0
					if j[0] == i:
						f = j[1]
						for k in arr:
							if k[0] == i and k[1] == f:
								count += k[2]
						arr5.append((i,f,count,))
			arr5 = list(set(arr5))
			return render_template("food_vendor.html",food_menu = arr5,food_menu2 = arr3,sessionname = session.get('name'))
		


		mycursor = mydb.cursor()
		sql = "SELECT * FROM `foodmenu` where day = dayofweek(curdate()) and isactive = 1"
		mycursor.execute(sql)
		food_menu = mycursor.fetchall()
		return render_template("food.html",food_menu = food_menu, role = session.get('role'),sessionname = session.get('name'))
	if request.method == 'POST':
		values = request.form.to_dict()
		# {'2': '2', '3': '1', 'total': '280.00'}
		
		mycursor = mydb.cursor()
		sql = "Insert into `food_mapping` (user_id,foodlist,price,date) values (%s,%s,%s,curdate())"
		val = (session.get('user'),str(values),values['total'],)
		mycursor.execute(sql,val)
		mydb.commit()
		return redirect("/")

# =============================meeting============================================================================================
from datetime import datetime, timedelta

# Maximum duration for a booking (in hours)
MAX_DURATION_HOURS = 4

# Maximum booking window (in days) for future bookings
MAX_BOOKING_WINDOW_DAYS = 30

# Minimum duration for a practical booking (in minutes)
MIN_BOOKING_DURATION_MINUTES = 15

@app.route('/meeting_room', methods=['POST','GET'])
def meeting_room():
	global meetingroom_status
	mycursor = mydb.cursor()
	sql = "SELECT * FROM `meeting_room`"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	if request.method == 'GET':
		return render_template("meeting_rooms.html", meetings = myresult, role = session.get('role'),sessionname = session.get('name'))
	if request.method == 'POST':
		floor = request.form['meeting_floor']
		room = request.form['meeting_room']
		date = request.form['meeting_date']
		start_time_str = request.form['meeting_start_time']
		end_time_str = request.form['meeting_end_time']
	
		# Convert string inputs to datetime objects
		start_time = datetime.strptime(start_time_str, '%H:%M')
		start_time = datetime.combine(datetime.strptime(date, '%Y-%m-%d'), start_time.time())
		end_time = datetime.strptime(end_time_str, '%H:%M')
		end_time = datetime.combine(datetime.strptime(date, '%Y-%m-%d'), end_time.time())

		# Check if booking is for a past date or too far in the future
		if start_time < datetime.now():
			meetingroom_status =  "Cannot book for past dates."
			return render_template("meeting_rooms.html", meetings = myresult,meetingroom_status=meetingroom_status, role = session.get('role'),sessionname = session.get('name'))
		
		if start_time > end_time:
			meetingroom_status = "Start time should be before end time."
			return render_template("meeting_rooms.html", meetings = myresult,meetingroom_status=meetingroom_status, role = session.get('role'),sessionname = session.get('name'))
		
		if start_time > (datetime.now() + timedelta(days=MAX_BOOKING_WINDOW_DAYS)):
			meetingroom_status = f"Cannot book for dates more than {MAX_BOOKING_WINDOW_DAYS} days in the future."
			return render_template("meeting_rooms.html", meetings = myresult,meetingroom_status=meetingroom_status, role = session.get('role'),sessionname = session.get('name'))
		

		# Check if room is available for the requested time slot
		if not is_time_slot_available(floor, room, start_time, end_time):
			meetingroom_status = "This room is already booked for the requested time slot. Please choose another time."
			return render_template("meeting_rooms.html", meetings = myresult,meetingroom_status=meetingroom_status, role = session.get('role'),sessionname = session.get('name'))

		if not is_valid_time_range(start_time, end_time):
			meetingroom_status = "Invalid time range. Please select a valid time range."
			return render_template("meeting_rooms.html", meetings = myresult,meetingroom_status=meetingroom_status, role = session.get('role'),sessionname = session.get('name'))

		if not is_within_max_duration(start_time, end_time):
			meetingroom_status = f"Maximum booking duration is {MAX_DURATION_HOURS} hours. Please select a shorter duration."
			return render_template("meeting_rooms.html", meetings = myresult,meetingroom_status=meetingroom_status, role = session.get('role'),sessionname = session.get('name'))

		if not is_practical_duration(start_time, end_time):
			meetingroom_status = f"Minimum practical booking duration is {MIN_BOOKING_DURATION_MINUTES} minutes. Please select a longer duration."
			return render_template("meeting_rooms.html", meetings = myresult,meetingroom_status=meetingroom_status, role = session.get('role'),sessionname = session.get('name'))

		
		# If room is available, book the time slot
		mycursor = mydb.cursor()
		sql = "Insert into `meetings` (floor,meeting_room,date,start_time,end_time,user_id) values (%s,%s,%s,%s,%s,%s)"
		val = (floor,room,date,start_time,end_time,session.get('user'))
		mycursor.execute(sql,val)
		mydb.commit()
		meetingroom_status = "Meeting room booked successfully."
		return render_template("meeting_rooms.html", meetings = myresult,meetingroom_status=meetingroom_status, role = session.get('role'),sessionname = session.get('name'))

# Function to check if the requested time slot is available for the given room
def is_time_slot_available(floor, room, start_time, end_time):
	mycursor = mydb.cursor()
	sql = "SELECT start_time, end_time FROM `meetings` WHERE floor = %s AND meeting_room = %s"
	val = (floor, room)
	mycursor.execute(sql, val)
	myresult = mycursor.fetchall()
	for booked_start, booked_end in myresult:
		if (start_time <= booked_end and end_time >= booked_start) or (start_time == booked_end or end_time == booked_start) or (start_time == booked_end and end_time == booked_start):
			return False
	return True

# Function to check if the selected time range is valid (start time before end time)
def is_valid_time_range(start_time, end_time):
    return start_time < end_time

# Function to check if the duration of the booking is within the maximum allowed duration
def is_within_max_duration(start_time, end_time):
    duration = end_time - start_time
    return duration <= timedelta(hours=MAX_DURATION_HOURS)

# Function to check if the duration of the booking is practical (not too short)
def is_practical_duration(start_time, end_time):
    duration = end_time - start_time
    return duration >= timedelta(minutes=MIN_BOOKING_DURATION_MINUTES)

# =============================recreation============================================================================================
@app.route('/recreation', methods=['POST','GET'])
def recreation():
	global sportbooking_status
	mycursor = mydb.cursor()
	sql = "SELECT * FROM `sports`"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	if request.method == 'GET':
		return render_template("recreation.html", sports = myresult, role = session.get('role'),sessionname = session.get('name'))
	if request.method == 'POST':
		print(request.form.to_dict())
		start_time_str = request.form['sport_start_time']
		sport = request.form['sport']
		slot = int(request.form['slot'])
		date = datetime.now().date()
	
		# Convert string inputs to datetime objects
		start_time = datetime.strptime(start_time_str, '%H:%M')
		start_time = datetime.combine(date, start_time.time())
		end_time = start_time + timedelta(minutes=slot)
 
		if start_time < datetime.now():
			sportbooking_status =  "Cannot book for past time."
			return render_template("recreation.html", sports = myresult, sportbooking_status=sportbooking_status, role = session.get('role'),sessionname = session.get('name'))
				
		if not is_already_booked(session.get('user')):
			sportbooking_status = f"Already booking for today. Please come again tomorrow."
			return render_template("recreation.html", sports = myresult,sportbooking_status=sportbooking_status, role = session.get('role'),sessionname = session.get('name'))
		
		if not is_time_slot_available_recreation(start_time, end_time):
			sportbooking_status = "This slot is already booked for the requested time. Please choose another time."
			return render_template("recreation.html", sports = myresult,sportbooking_status=sportbooking_status, role = session.get('role'),sessionname = session.get('name'))

		mycursor = mydb.cursor()
		sql = "Insert into `sports_mapping` (sport,slot,date,start_time,end_time,user_id) values (%s,%s,%s,%s,%s,%s)"
		val = (sport,slot,date,start_time,end_time,session.get('user'))
		mycursor.execute(sql,val)
		mydb.commit()
		sportbooking_status = "Sport slot booked successfully."
		return render_template("recreation.html", sports = myresult,sportbooking_status=sportbooking_status, role = session.get('role'),sessionname = session.get('name'))

# Function to check if the requested time slot is available for the given slot
def is_time_slot_available_recreation(start_time, end_time):
	mycursor = mydb.cursor()
	sql = "SELECT start_time, end_time FROM `sports_mapping`"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	for booked_start, booked_end in myresult:
		if (start_time <= booked_end and end_time >= booked_start) or (start_time == booked_end or end_time == booked_start) or (start_time == booked_end and end_time == booked_start):
			return False
	return True

# Function to check if the user has already booked a slot for the day
def is_already_booked(user_id):
	mycursor = mydb.cursor()
	sql = "SELECT start_time, end_time FROM `sports_mapping` where user_id = %s"
	val = (user_id,)
	mycursor.execute(sql,val)
	myresult = mycursor.fetchall()
	if myresult:
		return False
	return True


# =============================attendance============================================================================================
def attendence_data(user_id):
	mycursor = mydb.cursor()
	sql = "SELECT login_time FROM `attendance` where user_id = %s"
	val = (user_id,)
	mycursor.execute(sql,val)
	myresult = mycursor.fetchall()
	arr1,arr2 = [],[]
	for i in myresult:
		arr1.append(i[0].strftime("%Y-%m-%d"))
		arr2.append(int(i[0].strftime("%H")) + float(i[0].strftime("%M"))/100)
	return (arr1,arr2)


def get_attendence_data():
	if session.get('role') == 'manager':
		mycursor = mydb.cursor()
		sql = "SELECT adid FROM `users` where user_id = %s union SELECT adid FROM `users` where manager_id = %s"
		val = (session.get('user'),session.get('user'),)
		mycursor.execute(sql,val)
		userids = mycursor.fetchall()
		userids = [i[0] for i in userids]
		arr1,arr2 = attendence_data(session.get('user'))
	else:
		mycursor = mydb.cursor()
		sql = "SELECT adid FROM `users` where user_id = %s"
		val = (session.get('user'),)
		mycursor.execute(sql,val)
		userids = mycursor.fetchall()
		userids = [i[0] for i in userids]
		arr1,arr2 = attendence_data(session.get('user'))
	return (arr1,arr2,userids)

def post_attendence_data(user_name):
	mycursor = mydb.cursor()
	sql = "SELECT user_id,role FROM `users` where adid = %s"
	val = (user_name,)
	mycursor.execute(sql,val)
	user_id = mycursor.fetchone()[0]
	print("user_id==============")
	print(user_id)
	arr1,arr2 = attendence_data(user_id)
	print("arr1==============")
	print(arr1)
	print("arr2==============")
	print(arr2)


	if session.get('role') == 'manager':
		mycursor = mydb.cursor()
		sql = "SELECT adid FROM `users` where user_id = %s union SELECT adid FROM `users` where manager_id = %s"
		val = (session.get('user'),session.get('user'),)
		mycursor.execute(sql,val)
		userids = mycursor.fetchall()
		userids = [i[0] for i in userids]
	else:
		userids = [session.get('user')]
	return (arr1,arr2,userids)

@app.route("/attendance", methods = ['POST', 'GET'])
def attendance():
	if "user" not in session:
		return redirect("/login")
	if request.method == 'GET':
		arr1,arr2,userids = get_attendence_data()
		print(arr1,arr2,userids)
		return render_template("attendance.html",msg = "",arr1 = arr1,arr2 = arr2,userids = userids, role = session.get('role'),sessionname = session.get('name'))
	if request.method == 'POST':
		values = request.form.to_dict()
		print("=============")
		print(values)
		if 'mark_attendence' in values.keys():
			mycursor = mydb.cursor()
			sql = "SELECT * FROM `attendance` where user_id = %s and date(login_time) = curdate()"
			val = (session.get('user'),)
			mycursor.execute(sql,val)
			myresult = mycursor.fetchall()
			if myresult:
				arr1,arr2,userids = get_attendence_data()
				return render_template("attendance.html",msg = "Already marked",arr1 = arr1,arr2 = arr2,userids = userids, role = session.get('role'),sessionname = session.get('name'))
			sql = "Insert into `attendance` (user_id,login_time) values (%s,current_timestamp)"
			val = (session.get('user'),)
			mycursor.execute(sql,val)
			mydb.commit()
			arr1,arr2,userids = get_attendence_data()
			return render_template("attendance.html",msg = "Marked successfully",arr1 = arr1,arr2 = arr2,userids = userids, role = session.get('role'),sessionname = session.get('name'))
		user_name = values['user_name']
		arr1,arr2,userids = post_attendence_data(user_name)
		return render_template("attendance.html",msg = "",arr1 = arr1,arr2 = arr2,userids = userids,user_name = user_name, role = session.get('role'),sessionname = session.get('name'))

# =============================queries============================================================================================
@app.route("/queries", methods = ['POST', 'GET'])
def queries():
	if request.method == 'GET':
		if "user" not in session:
			return redirect("/login")
		mycursor = mydb.cursor()
		
		queries = "select id,(select name from `users` u where u.user_id = q.user_id),query,date from `queries` q order by date desc"
		mycursor.execute(queries)
		queries = mycursor.fetchall()
		query_replies = ''

		query_replies = "select query_id,reply,(select name from `users` u where u.user_id = q.user_id) from `query_replies` q order by date desc"
		mycursor.execute(query_replies)
		query_replies = mycursor.fetchall()

		return render_template("queries.html",queries = queries,query_replies = query_replies,user_id = session.get('user'), role = session.get('role'),sessionname = session.get('name'))
	
	if request.method == 'POST':
		values = request.form.to_dict()
		if 'query_id' in values.keys():
			mycursor = mydb.cursor()
			sql = "insert into `query_replies` (query_id,reply,date,user_id) values (%s,%s,current_timestamp,%s)"
			val = (values['query_id'],values['reply'],session.get('user'),)
			mycursor.execute(sql,val)
			mydb.commit()
			return redirect("/queries")
		
		mycursor = mydb.cursor()
		sql = "Insert into `queries` (user_id,query,date) values (%s,%s,current_timestamp)"
		val = (session.get('user'),values['query'],)
		mycursor.execute(sql,val)
		mydb.commit()
		return redirect("/queries")

# =============================Central repository============================================================================================
from flask import request
from werkzeug.utils import secure_filename
import os

@app.route("/centralrepo", methods = ['POST', 'GET'])
def centralrepo():
	if request.method == 'GET':
		if "user" not in session:
			return redirect("/login")
		sql = "SELECT * FROM `files`"
		mycursor = mydb.cursor()
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		return render_template("centralrepo.html", files = myresult, role = session.get('role'),sessionname = session.get('name'))
		
	if request.method == 'POST':
		title = request.form['title']
		if 'file' not in request.files:
			msg =  'No file part in the request'
		file = request.files['file']
		if file.filename == '':
			msg =  'No file selected for uploading'
		if file:
			filename = secure_filename(file.filename)
			filepath = os.path.join('static/files/', filename)
			file.save(filepath)
			msg =  'File successfully uploaded'
		sql = "Insert into `files` (user_id,file_name,file_path,date) values (%s,%s,%s,current_timestamp)"
		val = (session.get('user'),title,filepath)
		mycursor = mydb.cursor()
		mycursor.execute(sql,val)
		mydb.commit()
		return render_template("centralrepo.html",msg = msg, role = session.get('role'),sessionname = session.get('name'))


# =============================Chatbot============================================================================================
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

@app.route("/chatbot", methods = ['POST', 'GET'])
def chatbot():
	if request.method == 'GET':
		if "user" not in session:
			return redirect("/login")
		return render_template("chatbot.html", role = session.get('role'),sessionname = session.get('name'))
	
	if request.method == 'POST':
		message = request.form['question'] + " explain in formal way."

		client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

		response = client.chat.completions.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": "You have all the knowledge of Bajaj Finserv. You know all the public use cases of projects related to Bajaj Finserv or Bajaj Finance. And you need to explain anything using Bajaj Finserv projects. For every response greet with saying 'Hello Bajajian!"},
			{"role": "user", "content": message}
		]
		)
		return render_template('chatbot.html', response=response.choices[0].message.content.strip(), role = session.get('role'),sessionname = session.get('name'))


# =============================Posts============================================================================================
@app.route("/posts", methods = ['POST', 'GET'])
def posts():
	if request.method == 'GET':
		if "user" not in session:
			return redirect("/login")
		return render_template("posts.html", role = session.get('role'),sessionname = session.get('name'))
	
	if request.method == 'POST':
		values = request.form.to_dict()
		mycursor = mydb.cursor()
		sql = "Insert into `posts` (user_id,Topic,content,date) values (%s,%s,%s,%s)"
		val = (session.get('user'),values['topic'],values['content'],values['todate'])
		mycursor.execute(sql,val)
		mydb.commit()
                        
		return render_template('posts.html', msg="Posted succesfully" ,role = session.get('role'),sessionname = session.get('name'))
# =============================anonymous============================================================================================
@app.route("/anonymous", methods = ['POST', 'GET'])
def anonymous():
	mycursor = mydb.cursor()
	sql = "select user_id,name from `users` where user_id != %s and (role = 'manager' or role = 'HR' or role = 'admin')"
	val = (session.get('user'),)
	mycursor.execute(sql,val)
	users = mycursor.fetchall()

	mycursor = mydb.cursor()
	sql = "SELECT * FROM `anonymous` where adid = %s order by date desc"
	val = (session.get('user'),)
	mycursor.execute(sql,val)
	anonymousmsg = mycursor.fetchall()

	mycursor = mydb.cursor()
	sql = "SELECT (select name from `users` where user_id = a.adid),message,date,(select name from `users` where user_id = a.from_msg) FROM `anonymous` a order by date desc"
	mycursor.execute(sql)
	allmessages = mycursor.fetchall()
	to = [i[0] for i in allmessages]
	to = list(set(to))


	if request.method == 'GET':
		if "user" not in session:
			return redirect("/login")
		
		return render_template("anonymous.html",msg = '', users = users,anonymousmsg = anonymousmsg, role = session.get('role'), allmessages = allmessages, to = to,sessionname = session.get('name'))
	
	if request.method == 'POST':
		values = request.form.to_dict()
		censored = profanity.censor(values['message']) 
		mycursor = mydb.cursor()
		sql = "INSERT into `anonymous` (adid,message,date,from_msg) values (%s,%s,current_timestamp,%s)"
		val = (values['user'],censored,session.get('user'),)
		mycursor.execute(sql,val)
		mydb.commit()
		return render_template('anonymous.html', msg="Sent succesfully", users = users, anonymousmsg = anonymousmsg ,role = session.get('role'), allmessages = allmessages, to = to,sessionname = session.get('name'))



# =============================logout============================================================================================
@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")

if __name__ == '__main__':
	app.run(debug=True,port=7890)