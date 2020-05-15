import mysql.connector
from flask import Flask, render_template, url_for, redirect, request, make_response, jsonify
import simplejson as json
from json import JSONEncoder
import datetime
import math
from datetime import timedelta
from decimal import Decimal
from flask_cors import CORS
#from sqlalchemy import create_engine

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

connection_config_dict = {'host': 'localhost','user' : 'cian','database' :'modulerdatabase','auth_plugin' :'mysql_native_password'}
#connection_config_dict = {'host': 'mvroso.mysql.pythonanywhere-services.com','user' : 'mvroso','password' : '1234abcd', 'database' :'mvroso$ModulerDatabase','auth_plugin' :'mysql_native_password'}
#engine = create_engine('mysql+mysqlconnector://mvroso:1234abcd@mvroso.mysql.pythonanywhere-services.com[:3306]/mvroso$ModulerDatabase', pool_recycle=280)

colours = [["#A3B824","#00BF63","#00A2B1","#00C4D0","#0F86DC","#FF4894","#D639BD","#DD0F83","#A54BDD","#FF6A6A","#C07F32","#FFB400","#F28F00","#FF7448","#FF3D3D"],
          ["#A3B824","#00BF63","#00A2B1","#00C4D0","#0F86DC","#FF4894","#D639BD","#DD0F83","#A54BDD","#FF6A6A","#C07F32","#FFB400","#F28F00","#FF7448","#FF3D3D"],
          ["#131803","#002E0A","#001D25","#002128","#010D52","#51050B","#450439","#4F0111","#1E055B","#4E0808","#3A0904","#440D00","#480A00","#4E0805","#570404"],
          ["#2A3108","#004E1E","#002730","#003A42","#032067","#6C1020","#5C0C4E","#660323","#331070","#6A1717","#4E1B0B","#612600","#621E00","#69180F","#710D0D"],
          ["#181E04","#002E0A","#00232C","#00282F","#02155A","#5D0712","#500644","#5B021E","#250864","#570B0B","#400D05","#4D1200","#510E00","#570C07","#630606"],
          ["#37400B","#004E1E","#003F49","#004B53","#052E77","#81162F","#6E115F","#780535","#42177F","#7C2020","#5D260F","#743600","#752B00","#7C2316","#861212"],
          ["#566312","#006F32","#005C67","#006E77","#084794","#A5244C","#8C1D7A","#95084B","#5E269A","#A23535","#794019","#9C5A00","#994800","#A23A24","#A91F1F"],
          ["#758519","#008F45","#007885","#00909A","#0B60B1","#C93269","#A92895","#B20B61","#7A35B5","#C74A4A","#955923","#C47E00","#BC6400","#C75132","#CB2B2B"],
          ["#94A720","#00AF59","#0094A2","#00B3BE","#0E79CE","#ED4186","#C733B0","#CF0E78","#9744D0","#EC5F5F","#B2722D","#EBA200","#E08100","#EC6841","#EE3737"],
          ["#ACBF2D","#0EC56C","#10ABB9","#0ECAD5","#2092E0","#FF549F","#DA47C4","#E0218F","#AE59E0","#FF7474","#C68A3D","#FFBA09","#F3980B","#FF7E51","#FF4A48"],
          ["#BDCD3E","#2AD27D","#2FBEC8","#29D6DE","#43AAE7","#FF6CB4","#E264D1","#E744A8","#C075E7","#FF8987","#D3A152","#FFC61A","#F6A921","#FF9163","#FF6660"],
          ["#CEDC4F","#46DF8E","#4FD1D8","#44E2E8","#65C3EE","#FF85CA","#EB80DE","#EE67C1","#D291EE","#FF9E9A","#E0B868","#FFD22C","#F9BB37","#FFA575","#FF7F74"],
          ["#DFEA60","#61EC9F","#6FE3E8","#5FEDF1","#87DBF5","#FF9DDF","#F39CEB","#F58ADA","#E4ADF5","#FFB2AD","#ECCE7E","#FFDE3E","#FBCC4C","#FFB987","#FF9989"],
          ["#F0F871","#7DF9B0","#8EF6F7","#7AF9FA","#AAF3FC","#FFB5F4","#FBB9F8","#FCADF3","#F6C9FC","#FFC7C0","#F9E593","#FFEA4F","#FEDD62","#FFCC99","#FFB39F"],

          ["#131803","#002E0A","#001D25","#002128","#010D52","#51050B","#450439","#4F0111","#1E055B","#4E0808","#3A0904","#440D00","#480A00","#4E0805","#570404"],
          ["#2A3108","#004E1E","#002730","#003A42","#032067","#6C1020","#5C0C4E","#660323","#331070","#6A1717","#4E1B0B","#612600","#621E00","#69180F","#710D0D"], 
          ["#F1F4DE","#D9F5E8","#D9F1F3","#D9F6F8","#DBEDFA","#FFE4EF","#F9E1F5","#FADBEC","#F1E4FA","#FFE9E9","#F6ECE0","#FFF4D9","#FDEED9","#FFEAE4","#FFE2E2"]]


class DateTimeEncoder(json.JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            if isinstance(obj, datetime.timedelta) or isinstance(obj, Decimal):
                return str(obj)
            return super(DateTimeEncoder, self).default(obj)

##################################################### FUNCTIONS ##################################################
def round_up(n, decimals=1):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def timelineData(values, classes):
  json = []
  for item in values:
    time = item[2] - item[1]
    intTime = int(time.days + 1)
    hours = round_up(item[3]/intTime, 2)
    name = item[0]
    date = item[1]
    while (date <= item[2]):
      entry = []
      entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%b-%d'))
      entry.append(name)
      entry.append(hours)
      json.append(entry)
      date = date + timedelta(days=1)
  final = parseTimelineClasses(classes, json)
  return final

def parseTimelineClasses(classes, json):
  start1 = "2018-09-09"
  end1 = "2018-11-25"
  start2 = "2019-01-20"
  end2 = "2019-04-07"
  noclass = ["2018-10-21", "2019-03-03"]
  for item in classes:
    time = item[4] - item[3]
    hours = int(time.seconds/3600)
    if (item[2] == 1):
      sunday =  datetime.datetime.strptime(start1, '%Y-%m-%d')
      while(sunday <= datetime.datetime.strptime(end1, '%Y-%m-%d')):
        if sunday not in noclass:
          entry = []
          date = sunday + timedelta(days=item[1])
          entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%b-%d'))
          entry.append(item[0])
          entry.append(hours)
          json.append(entry)
        sunday = sunday + timedelta(days=7)
    elif (item[2] == 2):
      sunday =  datetime.datetime.strptime(start2, '%Y-%m-%d')
      while(sunday <= datetime.datetime.strptime(end2, '%Y-%m-%d')):
        if sunday not in noclass:
          entry = []
          date = sunday + timedelta(days=item[1])
          entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%b-%d'))
          entry.append(item[0])
          entry.append(hours)
          json.append(entry)
        sunday = sunday + timedelta(days=7)
  return json

def makePieBarJSON(values):
  data_keys = ["label","value"]
  data = []
  for result in values:
    entry = []
    entry.append(str(result[0]))
    entry.append(result[1])
    data.append(dict(zip(data_keys,entry)))
  return data

def modulePopulator(moduleIDs, studentID):
  activity_keys = ["activity_ID", "activityType", "title", "start_date", "due_date", "grade_percentage", "grading_description", "description", "estimated_time","lecture","activity_type_ID","colour","class_time_spent","submitted","feedback", "notes"]
  module_keys = ["module_ID", "module_code" , "module_name", "module_lecturer", "module_lecturer_ID","module_lecturer_email","colour","courses", "activities", "classes", "feedback"]
  course_keys = ["course_ID", "course_name", "coordinator_name","coordinator_email"]
  total_json = []
  note_keys = ["text"]
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered=True)
  for item in moduleIDs:
    module=[]
    activities=[]
    classes=[]
    courses=[]
    feedback=[]
    cur.execute("SELECT m.module_ID, m.module_code, m.module_name, s.staff_name, s.staff_ID, s.staff_email FROM Modules as m LEFT JOIN Staff as s ON (s.staff_ID = m.staff_ID) WHERE m.module_ID = %s", (str(item[0]),))
    detailslist = cur.fetchall()
    module.append(detailslist[0][0])
    module.append(detailslist[0][1])
    module.append(detailslist[0][2])
    module.append(detailslist[0][3])
    module.append(detailslist[0][4])
    module.append(detailslist[0][5])
    module.append(colours[0][int(item[0])])
    cur.execute("SELECT mc.course_ID, c.course_name, s.staff_name, s.staff_email FROM Module_Course as mc LEFT JOIN Courses AS c ON (mc.course_ID = c.course_ID) LEFT JOIN Staff as s ON (s.staff_ID = c.staff_ID) WHERE mc.module_ID = %s",(str(detailslist[0][0]),))
    courselist = cur.fetchall()
    for k in courselist:
      courses.append(dict(zip(course_keys, k)))
    module.append(courses)

    if(studentID):
      cur.execute("SELECT a.activity_ID, at.activity_type, a.activity_name, a.start_date, a.end_date, a.module_value, a.grading, a.activity_description, a.hours, u.hours, cd.class_name, u.submitted, a.activity_type_ID FROM Activities AS a LEFT JOIN Class_Details as cd ON (a.lecture_ID = cd.class_details_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = a.activity_type_ID) LEFT JOIN Student_Progress as u ON (u.student_ID = %s AND u.activity_ID = a.activity_ID) WHERE a.module_ID = %s", (studentID,str(item[0])))
      activity_keys = ["activity_ID", "activityType", "title", "start_date", "due_date", "grade_percentage", "grading_description", "description", "estimated_time", "time_spent","lecture","submitted","activity_type_ID", "colour", "class_time_spent","feedback"]
    else: cur.execute ("SELECT a.activity_ID, at.activity_type, a.activity_name, a.start_date, a.end_date, a.module_value, a.grading, a.activity_description, a.hours, cd.class_name, a.activity_type_ID FROM Activities AS a LEFT JOIN Class_Details as cd ON (a.lecture_ID = cd.class_details_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = a.activity_type_ID) WHERE a.module_ID = %s", (str(item[0]),))
    activitylist = cur.fetchall()

    for activity in activitylist:
      feedback_keys = ["feedback_ID","feedback_title", "feedback_description"]
      cur.execute("SELECT f.feedback_set_ID, fd.feedback_name, fd.feedback_description FROM Feedback_Set as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_activity_ID = %s AND f.feedback_type_ID = 2)",(activity[0],))
      feedbacklist = cur.fetchall()
      feedback = []
      actent = []
      for subact in activity:
        actent.append(subact)

      if(studentID):
        actent.append(colours[int(activity[12])][int(item[0])])
      else: actent.append(colours[int(activity[10])][int(item[0])])


      cur.execute("SELECT AVG(hours) hours FROM Student_Progress WHERE activity_ID = %s",(activity[0],))
      x = cur.fetchall()
      actent.append(x[0][0])


      if(studentID == 0):
        cur.execute("SELECT SUM(submitted) submitted FROM Student_Progress WHERE activity_ID = %s",(activity[0],))
        sub = cur.fetchall()
        if sub[0][0] is None: actent.append(0)
        else: actent.append(int(sub[0][0]))

      for subfeed in feedbacklist:
        feedback.append(dict(zip(feedback_keys, subfeed)))
      actent.append(feedback)
      cur.execute("SELECT n.note_text from Activity_Notes as n WHERE n.note_activity_ID = %s", (str(activity[0]),))
      notelist = cur.fetchall()
      notes = []
      for note in notelist:
        notes.append(dict(zip(note_keys,note)))
      actent.append(notes)
      activities.append(dict(zip(activity_keys, actent)))

    module.append(activities)
    cur.execute("SELECT c.class_ID, at.activity_type, c.class_location, c.start_time, c.end_time, c.class_day, c.class_semester, c.activity_type_ID FROM Classes AS c LEFT JOIN Days as d ON (c.class_day = d.day_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = c.activity_type_ID) WHERE c.module_ID = %s", (str(item[0]),))
    classlist = cur.fetchall()
    cur.execute("SELECT class_date, class_name, class_description, class_ID, class_details_ID from Class_Details WHERE module_ID = %s", (str(item[0]),))
    classdetails = cur.fetchall()
    feedback_keys = ["name", "description"]
    cur.execute("SELECT f.feedback_set_ID, fd.feedback_name, fd.feedback_description FROM Feedback_Set as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_activity_ID = %s AND f.feedback_type_ID = 1)",(str(detailslist[0][0]),))
    feedbacklist = cur.fetchall()
    start1 = "2018-09-09"
    end1 = "2018-11-25"
    start2 = "2019-01-20"
    end2 = "2019-04-07"
    noclass = ["2018-10-21", "2019-03-03"]
    class_keys = ["class_ID", "activityType", "location", "start_time", "end_time","date","notes","title", "description", "linked_activities", "feedback", "colour"]
    feedback_keys = ["feedback_ID","feedback_title", "feedback_description"]
    note_keys = ["text"]
    act_keys = ["activity_ID","activity_name", "start", "end"]

    for classitem in classlist:
      colour = colours[int(classitem[7])][int(item[0])]
      if (classitem[6] == 1):
        sunday =  datetime.datetime.strptime(start1, '%Y-%m-%d')
        while(sunday <= datetime.datetime.strptime(end1, '%Y-%m-%d')):
          if sunday not in noclass:
            entry = []
            date = sunday + timedelta(days=classitem[5])
            entry.append(classitem[0])
            entry.append(classitem[1])
            entry.append(classitem[2])
            entry.append(datetime.datetime.strptime(str(classitem[3]),'%H:%M:%S').strftime('%H:%M:%S'))
            entry.append(datetime.datetime.strptime(str(classitem[4]),'%H:%M:%S').strftime('%H:%M:%S'))
            entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
            sort = 1
            print(classitem[0],entry[5])
            cur.execute("SELECT n.note_text from Lecture_Notes as n WHERE n.note_lecture_ID = %s AND n.note_lecture_date = %s", (classitem[0],entry[5]))
            notelist = cur.fetchall()
            notes = []
            for note in notelist:
              notes.append(dict(zip(note_keys,note)))
            entry.append(notes)            
            for thing in classdetails:
              if datetime.datetime.strptime(str(thing[0]),'%Y-%m-%d').strftime('%Y-%m-%d') == entry[5]:
                entry.append(thing[1])
                entry.append(thing[2])
                cur.execute("SELECT a.activity_ID, a.activity_name, a.start_date, a.end_date from Activities as a WHERE a.lecture_ID = %s", (thing[4],))
                actlist = cur.fetchall()
                acts = []
                for act in actlist:
                  acts.append(dict(zip(act_keys,act)))
                entry.append(acts)
                sort = 0
            if(sort):
              entry.append(classitem[1])
              entry.append("None")
              entry.append([])
            cur.execute("SELECT f.feedback_set_ID, fd.feedback_name, fd.feedback_description FROM Feedback_Set as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_activity_ID = %s AND f.feedback_type_ID = 3)",(str(classitem[0]),))
            feedbacklist = cur.fetchall()
            feedback = []
            for subfeed in feedbacklist:
              feedback.append(dict(zip(feedback_keys, subfeed)))
            entry.append(feedback)
            entry.append(colour)
            classes.append(dict(zip(class_keys,entry)))
          sunday = sunday + timedelta(days=7)

      elif (classitem[6] == 2):
        sunday =  datetime.datetime.strptime(start2, '%Y-%m-%d')
        while(sunday <= datetime.datetime.strptime(end2, '%Y-%m-%d')):
          if sunday not in noclass:
            entry = []
            date = sunday + timedelta(days=classitem[5])
            entry.append(classitem[0])
            entry.append(classitem[1])
            entry.append(classitem[2])
            entry.append(datetime.datetime.strptime(str(classitem[3]),'%H:%M:%S').strftime('%H:%M:%S'))
            entry.append(datetime.datetime.strptime(str(classitem[4]),'%H:%M:%S').strftime('%H:%M:%S'))
            entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
            sort = 1
            for thing in classdetails:
              if datetime.datetime.strptime(str(thing[0]),'%Y-%m-%d').strftime('%Y-%m-%d') == entry[5]:
                entry.append(thing[1])
                entry.append(thing[2])
                cur.execute("SELECT n.note_text from Lecture_Notes as n WHERE n.note_lecture_ID = %s", (thing[4],))
                notelist = cur.fetchall()
                notes = []
                for note in notelist:
                  notes.append(dict(zip(note_keys,note)))
                entry.append(notes)
                cur.execute("SELECT a.activity_ID, a.activity_name, a.start_date, a.end_date from Activities as a WHERE a.lecture_ID = %s", (thing[4],))
                actlist = cur.fetchall()
                acts = []
                for act in actlist:
                  acts.append(dict(zip(act_keys,act)))
                entry.append(acts)
                sort = 0
            if(sort):
              entry.append(classitem[1])
              entry.append("None")
              entry.append([])
              entry.append([])
            cur.execute("SELECT f.feedback_set_ID, fd.feedback_name, fd.feedback_description FROM Feedback_Set as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_activity_ID = %s AND f.feedback_type_ID = 3)",(str(classitem[0]),))
            feedbacklist = cur.fetchall()
            feedback = []
            for subfeed in feedbacklist:
              feedback.append(dict(zip(feedback_keys, subfeed)))
            entry.append(feedback)
            entry.append(colour)
            classes.append(dict(zip(class_keys,entry)))
          sunday = sunday + timedelta(days=7)
    module.append(classes)
    for j in feedbacklist:
      feedback.append(dict(zip(feedback_keys, j)))
    total_json.append(dict(zip(module_keys, module)))
  cur.close()
  mydb.close()
  return total_json

def parseFeedbackHistogram(modulelist):
  subkeys = ["question", "dialvalue", "bardata"]
  modules = []
  question = []
  data = []
  datalist = []
  count = 0
  total = 0
  current = modulelist[0][0]
  for entry in modulelist:
    data = []
    data.append(entry[1])
    data.append(entry[2])
    if (entry[0] != current):
      question.append(current)
      question.append(round_up(total/count))
      count = 0
      total = 0
      question.append(makePieBarJSON(datalist))
      modules.append(dict(zip(subkeys,question)))
      datalist = []
      question = []
      current = entry[0]
    datalist.append(data)
    count = count + entry[2]
    total = total + entry[1]*entry[2]


  question.append(current)
  question.append(round_up(total/count))
  question.append(makePieBarJSON(datalist))
  modules.append(dict(zip(subkeys,question)))
  datalist = []
  question = []
  return modules

def nestedCategoryStack(module_name,activities,classes,colour,hours):
  TOTAL_WEEKS = 12
  keys = ["label","color","value","category"]
  subkeys = ["label","color","value"]
  stack = []
  module = []
  module.append(module_name)
  module.append(colour)
  module.append(hours)

  for item in activities:
    entry = []
    entry.append(item[1])
    entry.append(colour)
    entry.append(item[2])
    stack.append(dict(zip(subkeys,entry)))

  for classitem in classes:
    entry = []
    entry.append(classitem[0])
    entry.append(colour)
    entry.append(int(classitem[1].seconds/3600*TOTAL_WEEKS))
    stack.append(dict(zip(subkeys,entry)))

  module.append(stack)
  return dict(zip(keys,module))

##################################################### OUTPUTS ##################################################

@app.route("/modulesByStudent<string:studentID>")
def modulesByStudent(studentID):
  mydb = mysql.connector.connect(**connection_config_dict)
  json_data = []
  cur = mydb.cursor(buffered=True)
  cur.execute("SELECT course_ID FROM Students WHERE student_ID = %s ", (studentID,))
  courseID = cur.fetchall()
  courseID = str(courseID[0][0])

  cur.execute("SELECT s.student_ID,s.student_name, s.student_number, s.student_email, s.course_ID, c.course_name FROM Students as s LEFT JOIN Courses as c ON (c.course_ID = s.course_ID) WHERE s.student_ID = %s",(studentID,))
  student=cur.fetchall()
  studentkeys = ["student_ID","student_name","student_number","student_email","course_ID","course_name"]
  details = dict(zip(studentkeys,student[0]))
  json_data.append(details)
  cur.execute("Select m.module_ID FROM Modules as m LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) WHERE mc.course_ID = %s", (courseID,))
  module_list = cur.fetchall()
  cur.close()
  mydb.close()
  json_data.append(modulePopulator(module_list,studentID))
  keys=["student","modules"]
  final = dict(zip(keys, json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/modulesByStaff<string:staffID>")
def modulesByStaff(staffID):
  mydb = mysql.connector.connect(**connection_config_dict)
  json_data = []
  cur = mydb.cursor(buffered=True)
  cur.execute("Select module_ID FROM Modules WHERE staff_ID = %s", (staffID,))
  module_list = cur.fetchall()
  cur.close()
  mydb.close()
  json_data = modulePopulator(module_list,0)

  response = app.response_class(
        response=json.dumps(json_data, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/moduleByModule<string:moduleID>")
def moduleByModule(moduleID):
  json_data = []
  module_list = []
  module_list.append(moduleID)
  json_data = modulePopulator(module_list,0)
  response = app.response_class(
        response=json.dumps(json_data, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/modulesByCourse<string:courseID>")
def modulesByCourse(courseID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered=True)
  json_data = []
  cur.execute("Select m.module_ID FROM Modules as m LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) WHERE mc.course_ID = %s", (courseID,))
  module_list = cur.fetchall()
  cur.close()
  mydb.close()
  json_data = modulePopulator(module_list,0)
  response = app.response_class(
        response=json.dumps(json_data, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/studentsByModule<string:moduleID>")
def studentsByModule(moduleID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered = True)
  json_data = []
  student = []
  json_keys = ["pie","Students"]
  cur.execute("SELECT s.course_ID, c.course_name, s.student_name, s.student_ID, s.student_number FROM Students as s LEFT JOIN Courses as c ON (s.course_ID = c.course_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = %s AND mc.course_ID = s.course_ID)", (moduleID,))
  student_list = cur.fetchall()
  cur.execute("SELECT c.course_name, COUNT(c.course_name) Students FROM Students as s LEFT JOIN Courses as c ON (s.course_ID = c.course_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = %s AND mc.course_ID = s.course_ID)", (moduleID,))
  pie_list = cur.fetchall()
  json_data.append(makePieBarJSON(pie_list))
  cur.close()
  mydb.close()
  student_keys = ["course_ID", "course_name", "student_name", "student_ID", "student_number"]
  for item in student_list:
    student.append(dict(zip(student_keys, item)))
  json_data.append(student)
  final = dict(zip(json_keys, json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

############################################## GRAPHS ###############################################################
@app.route("/activityTypePieChartsByModule<string:moduleID>")
def activityTypePieChartsByModule(moduleID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor()
  json_data = []
  byHours = []
  keys = ["ByHours","ByGrade"]

  cur.execute("SELECT at.activity_type, SUM(a.hours) Hours FROM Activities as a LEFT JOIN Activity_Type as at ON (a.activity_type_ID = at.activity_type_ID) WHERE module_ID = %s  GROUP BY at.activity_type", (moduleID,))
  byHoursActivity = cur.fetchall()
  cur.execute("SELECT at.activity_type, CAST(SUM(timediff(c.end_time, c.start_time)) as time) as weeklyhours FROM Classes as c LEFT JOIN Activity_Type as at ON (c.activity_type_ID = at.activity_type_ID) WHERE c.module_ID = %s GROUP BY at.activity_type", (moduleID,))
  byHoursClass = cur.fetchall()
  for classtype in byHoursClass:
    entry = []
    hours = int(classtype[1].seconds/3600*30)
    entry.append(classtype[0])
    entry.append(hours)
    byHours.append(entry)
  for activity in byHoursActivity:
    byHours.append(activity)
  json_data.append(makePieBarJSON(byHours))

  cur.execute("SELECT at.activity_type, SUM(a.module_value) Grade FROM Activities as a LEFT JOIN Activity_Type as at ON (a.activity_type_ID = at.activity_type_ID) WHERE module_ID = %s  GROUP BY at.activity_type", (moduleID,))
  byGrade = cur.fetchall()
  json_data.append(makePieBarJSON(byGrade))

  final = dict(zip(keys,json_data))
  response = app.response_class(
      response=json.dumps(final, indent=4, cls=DateTimeEncoder),
      status=200,
      mimetype='application/json'
  )
  cur.close()
  mydb.close()
  return response

@app.route("/activityTypePieChartsByCourse<string:courseID>")
def activityTypePieChartsByCourse(courseID):
  TOTAL_WEEKS = 12
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor()
  json_data = []
  byHours =[]
  byModuleHours = []
  keys = ["ByModule","ByGradeAvg","ByActivity"]
  cur.execute("SELECT m.module_name, SUM(a.hours) hours FROM Activities as a LEFT JOIN Modules as m ON (m.module_ID = a.module_ID) WHERE a.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s AND mc.module_ID = a.module_ID) GROUP BY a.module_ID", (courseID,))
  byModuleHoursActivity = cur.fetchall()

  cur.execute("SELECT m.module_name, CAST(SUM(timediff(c.end_time, c.start_time)) as time) as weeklyhours FROM Classes as c LEFT JOIN Modules as m ON (m.module_ID = c.module_ID) WHERE c.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s AND mc.module_ID = c.module_ID) GROUP BY c.module_ID", (courseID,))
  byModuleHoursClass = cur.fetchall()
  for moduleclasstype in byModuleHoursClass:
    entry = []
    hours = int(moduleclasstype[1].seconds/3600*TOTAL_WEEKS)
    entry.append(moduleclasstype[0])
    entry.append(hours)
    byModuleHours.append(entry)
  for moduleactivity in byModuleHoursActivity:
    byModuleHours.append(moduleactivity)
  json_data.append(makePieBarJSON(byModuleHours))

  cur.execute("SELECT at.activity_type, AVG(a.module_value) grade FROM Activities as a LEFT JOIN Activity_Type as at ON (a.activity_type_ID = at.activity_type_ID) WHERE a.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s AND mc.module_ID = a.module_ID) GROUP BY at.activity_type", (courseID,))
  byGrade = cur.fetchall()
  json_data.append(makePieBarJSON(byGrade))

  cur.execute("SELECT at.activity_type, SUM(a.hours) hours FROM Activities as a LEFT JOIN Activity_Type as at ON (a.activity_type_ID = at.activity_type_ID) WHERE a.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s AND mc.module_ID = a.module_ID) GROUP BY at.activity_type", (courseID,))
  byHoursActivity = cur.fetchall()
  cur.execute("SELECT at.activity_type, CAST(SUM(timediff(c.end_time, c.start_time)) as time) as weeklyhours FROM Classes as c LEFT JOIN Activity_Type as at ON (c.activity_type_ID = at.activity_type_ID) WHERE c.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s AND mc.module_ID = c.module_ID) GROUP BY at.activity_type", (courseID,))
  byHoursClass = cur.fetchall()

  for classtype in byHoursClass:
    entry = []
    hours = int(classtype[1].seconds/3600*30)
    entry.append(classtype[0])
    entry.append(hours)
    byHours.append(entry)
  for activity in byHoursActivity:
    byHours.append(activity)

  json_data.append(makePieBarJSON(byHours))
  final = dict(zip(keys,json_data))
  response = app.response_class(
      response=json.dumps(final, indent=4, cls=DateTimeEncoder),
      status=200,
      mimetype='application/json'
  )
  mydb.close()
  return response

@app.route("/feedbackBarChartsByModule<string:moduleID>")
def feedbackBarChartByModule(moduleID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered = True)
  json_data = []
  keys = ["byModule","byActivity", "byClass"]

  cur.execute("SELECT fd.feedback_name, f.feedback_score, COUNT(f.feedback_score) Entries FROM Feedback as f LEFT JOIN Feedback_Set as fs ON (fs.feedback_set_ID = f.feedback_set_ID) LEFT JOIN Feedback_Details as fd ON (fs.feedback_details_ID = fd.feedback_ID) WHERE (fs.feedback_activity_ID = %s AND fs.feedback_type_ID = 1) GROUP BY f.feedback_score,fd.feedback_name ORDER BY fd.feedback_name", (moduleID,))
  modulelist = cur.fetchall()
  if(cur.rowcount > 0):json_data.append(parseFeedbackHistogram(modulelist))
  else: json_data.append([])

  cur.execute("SELECT fd.feedback_name, f.feedback_score, COUNT(f.feedback_score) Entries FROM Feedback as f LEFT JOIN Feedback_Set as fs ON (fs.feedback_set_ID = f.feedback_set_ID) LEFT JOIN Feedback_Details as fd ON (fs.feedback_details_ID = fd.feedback_ID) WHERE (fs.feedback_activity_ID in (SELECT a.activity_ID FROM Activities as a WHERE a.module_ID = %s) AND fs.feedback_type_ID = 2) GROUP BY f.feedback_score,fd.feedback_name ORDER BY fd.feedback_name", (moduleID,))
  activitylist = cur.fetchall()
  if(cur.rowcount > 0):json_data.append(parseFeedbackHistogram(activitylist))
  else: json_data.append([])

  cur.execute("SELECT fd.feedback_name, f.feedback_score, COUNT(f.feedback_score) Entries FROM Feedback as f LEFT JOIN Feedback_Set as fs ON (fs.feedback_set_ID = f.feedback_set_ID) LEFT JOIN Feedback_Details as fd ON (fs.feedback_details_ID = fd.feedback_ID) WHERE (fs.feedback_activity_ID in (SELECT c.class_ID FROM Classes as c WHERE c.module_ID = %s) AND fs.feedback_type_ID = 3) GROUP BY f.feedback_score,fd.feedback_name ORDER BY fd.feedback_name", (moduleID,))
  classlist = cur.fetchall()

  if(cur.rowcount > 0):json_data.append(parseFeedbackHistogram(classlist))
  else: json_data.append([])
  cur.close()
  mydb.close()
  final = dict(zip(keys,json_data))
  response = app.response_class(
      response=json.dumps(final, indent=4, cls=DateTimeEncoder),
      status=200,
      mimetype='application/json'
  )
  return response
@app.route("/feedbackByActivity<string:activityID>")
def feedbackByActivity(activityID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered = True)
  json_data = []
  keys = ["Questions"]
  cur.execute("SELECT fd.feedback_name, f.feedback_score, COUNT(f.feedback_score) Entries FROM Feedback as f LEFT JOIN Feedback_Set as fs ON (fs.feedback_set_ID = f.feedback_set_ID) LEFT JOIN Feedback_Details as fd ON (fs.feedback_details_ID = fd.feedback_ID) WHERE (fs.feedback_activity_ID = %s AND fs.feedback_type_ID = 2) GROUP BY f.feedback_score,fd.feedback_name ORDER BY fd.feedback_name", (activityID,))
  activitylist = cur.fetchall()
  print(activitylist)
  if(cur.rowcount > 0):json_data.append(parseFeedbackHistogram(activitylist))
  else: json_data.append([])
  cur.close()
  mydb.close()
  final = dict(zip(keys,json_data))
  response = app.response_class(
      response=json.dumps(final, indent=4, cls=DateTimeEncoder),
      status=200,
      mimetype='application/json'
  )
  return response

@app.route("/feedbackByClass<string:classID>")
def feedbackByClass(classID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered = True)
  json_data = []
  keys = ["Questions"]

  cur.execute("SELECT fd.feedback_name, f.feedback_score, COUNT(f.feedback_score) Entries FROM Feedback as f LEFT JOIN Feedback_Set as fs ON (fs.feedback_set_ID = f.feedback_set_ID) LEFT JOIN Feedback_Details as fd ON (fs.feedback_details_ID = fd.feedback_ID) WHERE (fs.feedback_activity_ID  = %s AND fs.feedback_type_ID = 3) GROUP BY f.feedback_score,fd.feedback_name ORDER BY fd.feedback_name", (classID,))
  classlist = cur.fetchall()

  if(cur.rowcount > 0):json_data.append(parseFeedbackHistogram(classlist))
  else: json_data.append([])
  cur.close()
  mydb.close()
  final = dict(zip(keys,json_data))
  response = app.response_class(
      response=json.dumps(final, indent=4, cls=DateTimeEncoder),
      status=200,
      mimetype='application/json'
  )
  return response

@app.route("/nestedPieByCourse<string:courseID>")
def nestedPieByCourse(courseID):
  TOTAL_WEEKS = 12
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered = True)
  keys = ["label","color","value","category"]
  colours = ["#f8bd19","#f8bd18","#f8fd19","#f8ad19","#f8cd19","#f82d19","#f83d19","#f86d19","#f8b119","#f1bd19","#d8bd19","#c8bd19","#a8bd19","#f81d19"]
  modules = []
  json_data = []
  cur = mydb.cursor(buffered = True)
  cur.execute("SELECT c.course_name, SUM(a.hours) FROM Courses as c LEFT JOIN Activities as a ON (a.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s))",(courseID,))
  activityhours = cur.fetchall()

  cur.execute("SELECT co.course_name, CAST(SUM(timediff(c.end_time, c.start_time)) as time) as weeklyhours FROM Classes as c LEFT JOIN Courses as co ON (co.course_ID = %s) WHERE (c.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s)) GROUP BY co.course_name", (courseID,courseID))
  classhours = cur.fetchall()

  if activityhours[0][1] is None: activitytotal = 0
  else : activitytotal = activityhours[0][1]

  if classhours[0][1] is None: classtotal = 0
  else: classtotal = int(classhours[0][1].seconds/3600*TOTAL_WEEKS)
  coursehours = classtotal + activitytotal

  cur.execute("SELECT module_ID FROM Module_Course WHERE course_ID = %s",(courseID,))
  moduleIDs = cur.fetchall()
  count = 0
  for moduleID in moduleIDs:
    colour = colours[count]
    count = count + 1
    cur.execute("SELECT m.module_name, at.activity_type, SUM(a.hours) FROM Activities as a LEFT JOIN Activity_Type as at ON (a.activity_type_ID = at.activity_type_ID) LEFT JOIN Modules as m ON (m.module_ID = a.module_ID) WHERE a.module_ID = %s GROUP BY at.activity_type", (moduleID[0],))
    activities = cur.fetchall()

    cur.execute("SELECT at.activity_type, CAST(SUM(timediff(c.end_time, c.start_time)) as time) as weeklyhours FROM Classes as c LEFT JOIN Activity_Type as at ON (at.activity_type_ID = c.activity_type_ID) WHERE c.module_ID = %s GROUP BY c.module_ID,c.activity_type_ID", (courseID,))
    classes = cur.fetchall()

    cur.execute("SELECT SUM(hours) FROM Activities WHERE module_ID = %s",(moduleID[0],))
    activity_total = cur.fetchall()
    cur.execute("SELECT CAST(SUM(timediff(end_time, start_time)) as time) as weeklyhours FROM Classes WHERE module_ID = %s", (moduleID[0],))
    class_total = cur.fetchall()
    if activity_total[0][0] is None: activitytotal = 0
    else: activitytotal = activity_total[0][0]

    if class_total[0][0] is None: classtotal = 0
    else: classtotal = int(class_total[0][0].seconds/3600*TOTAL_WEEKS)

    hours = classtotal + activitytotal
    cur.execute("SELECT module_name FROM Modules WHERE module_ID = %s",(moduleID[0],))
    module_name = cur.fetchall()
    modules.append(nestedCategoryStack(module_name[0][0],activities,classes,colour,hours))

  json_data.append(activityhours[0][0])
  json_data.append("#ffffff")
  json_data.append(coursehours)
  json_data.append(modules)
  cur.close()
  mydb.close()

  final = []
  final.append(dict(zip(keys,json_data)))
  response = app.response_class(
      response=json.dumps(final, indent=4, cls=DateTimeEncoder),
      status=200,
      mimetype='application/json'
  )
  return response


@app.route("/timelineByCourse<string:courseID>")
def timelineByCourse(courseID):
  mydb = mysql.connector.connect(**connection_config_dict)
  json_data = []
  values = []
  classes = []
  try:
    cur = mydb.cursor(buffered=True)
    cur.execute("SELECT m.module_name, a.start_date, a.end_date, a.hours FROM Activities AS a LEFT JOIN Modules as m ON (m.module_ID = a.module_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) WHERE mc.course_ID = %s", (courseID,))
    values = cur.fetchall()
    cur.execute("SELECT  m.module_name, c.class_day, c.class_semester, c.start_time, c.end_time FROM Classes AS c LEFT JOIN Modules as m ON (m.module_ID = c.module_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) WHERE mc.course_ID = %s", (courseID,))
    classes = cur.fetchall()
    json_data.append(timelineData(values, classes))

    values = []
    classes = []
    cur.execute("SELECT at.activity_type, a.start_date, a.end_date, a.hours FROM Activities AS a LEFT JOIN Activity_Type as at ON (at.activity_type_ID = a.activity_type_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = a.module_ID) WHERE mc.course_ID = %s", (courseID,))
    values = cur.fetchall()
    cur.execute("SELECT at.activity_type, c.class_day, c.class_semester, c.start_time, c.end_time FROM Classes AS c LEFT JOIN Activity_Type as at ON (at.activity_type_ID = c.activity_type_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = c.module_ID) WHERE mc.course_ID = %s", (courseID,))
    classes = cur.fetchall()
    json_data.append(timelineData(values, classes))
  except Exception: # Catch exception which will be raise in connection loss
    mydb = mysql.connector.connect(**connection_config_dict)
    cur = mydb.cursor(buffered=True)
  finally:
    cur.close()
    mydb.close()

  schema_data = [{
      "name": "Date",
      "type": "date",
      "format": "%Y-%b-%d"
    },
    {
      "name": "Module",
      "type": "string"
    },
    {
      "name": "Hours",
      "type": "number"
    }
  ]

  binning = {
        "month": [1],
        "day": [6]
      }

  json_data.append(schema_data)
  json_data.append(binning)
  keys = ["byModule","byActivity","schema","bin"]
  final = dict(zip(keys,json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/timelineByModule<string:moduleID>")
def timelineByModule(moduleID):
  mydb = mysql.connector.connect(**connection_config_dict)
  json_data = []
  values = []
  classes = []
  values = []
  classes = []
  json_data.append([])
  try:
    cur = mydb.cursor(buffered=True)
    cur.execute("SELECT at.activity_type, a.start_date, a.end_date, a.hours FROM Activities AS a LEFT JOIN Activity_Type as at ON (at.activity_type_ID = a.activity_type_ID) WHERE a.module_ID = %s", (moduleID,))
    values = cur.fetchall()
    cur.execute("SELECT at.activity_type, c.class_day, c.class_semester, c.start_time, c.end_time FROM Classes AS c LEFT JOIN Activity_Type as at ON (at.activity_type_ID = c.activity_type_ID) WHERE c.module_ID = %s", (moduleID,))
    classes = cur.fetchall()
  except Exception: # Catch exception which will be raise in connection loss
    mydb = mysql.connector.connect(**connection_config_dict)
    cur = mydb.cursor(buffered=True)
  finally:
    mydb.close()
  json_data.append(timelineData(values, classes))

  schema_data = [{
      "name": "Date",
      "type": "date",
      "format": "%Y-%b-%d"
    },
    {
      "name": "Module",
      "type": "string"
    },
    {
      "name": "Hours",
      "type": "number"
    }
  ]

  binning = {
        "month": [1],
        "day": [6]
      }

  json_data.append(schema_data)
  json_data.append(binning)
  keys = ["byModule", "byActivity","schema","bin"]
  final = dict(zip(keys,json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

############################################ INPUT #############################################################

@app.route("/updateStudentProgress", methods=['POST'])
def updateStudentProgress():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)
  activityID = str(req['activityID'])
  studentID =  str(req['studentID'])
  hours = int(req['hours'])
  submitted = int(req['submitted'])
  mydb = mysql.connector.connect(**connection_config_dict)
  try:
    cur = mydb.cursor(buffered=True)
    cur.execute("SELECT hours FROM Student_Progress WHERE activity_ID = %s AND student_ID = %s",(activityID,studentID))
    if(cur.rowcount == 0):
      cur.execute("INSERT INTO Student_Progress (student_ID, activity_ID, hours, submitted) VALUES (%s,%s,%s,%s)",(studentID, activityID, hours,submitted))
      mydb.commit()

    elif(cur.rowcount > 0):
      response = cur.fetchall()
      hours = hours + response[0][0]
      cur.execute("UPDATE Student_Progress SET hours = %s WHERE activity_ID = %s AND student_ID = %s",(str(hours),activityID,studentID))
      mydb.commit()

    cur.execute("SELECT AVG(hours) hours FROM Student_Progress WHERE activity_ID = %s",(activityID,))
    hours = cur.fetchall()
    avg = round_up(hours[0][0])
    cur.execute("UPDATE Activities SET student_hours = %s WHERE activity_ID = %s",(str(avg),activityID,))
  except Exception: # Catch exception which will be raise in connection loss
    mydb = mysql.connector.connect(**connection_config_dict)
    cur = mydb.cursor(buffered=True)
  finally:
    mydb.commit()
    mydb.close()
  return res

@app.route("/updateFeedback", methods=['POST'])
def updateFeedback():
  req = request.get_json()
  scoreArray = req['answers']
  questionsArray = req['questions']
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered=True)
  i = 0

  while (i<len(questionsArray)):
    print(questionsArray[i],scoreArray[i])
    try:
      cur = mydb.cursor(buffered=True)
      cur.execute("INSERT INTO Feedback (feedback_set_ID, feedback_score) VALUES (%s,%s)",(str(questionsArray[i]), str(scoreArray[i])))
      i=i+1
    except Exception: # Catch exception which will be raise in connection loss
      mydb = mysql.connector.connect(**connection_config_dict)
      cur = mydb.cursor(buffered=True)
    finally:
      cur.close()
      mydb.commit()
  mydb.close()
  res = make_response(jsonify({"message": "OK"}), 200)
  return res

@app.route("/updateActivity", methods=['POST'])
def updateActivity():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)

  mydb = mysql.connector.connect(**connection_config_dict)

  activityID = int(req['activityID'])
  moduleID =  str(req['moduleID'])
  start = str(req['start'])
  end = str(req['end'])
  hours = str(req['hours'])
  grade = str(req['grade'])
  activity_type = str(req['type'])
  title = str(req['title'])
  description = str(req['description'])
  if title == "0":
    title = None
  lecture = None
  if description == "0":
    description = None

  cur = mydb.cursor(buffered=True)
  cur.execute("SELECT activity_type_ID FROM Activity_Type WHERE activity_type = %s",(activity_type,))
  activity_type_ID = cur.fetchall()
  if activityID > 0: 
    cur.execute("UPDATE Activities SET activity_type_ID = %s, start_date = %s, end_date = %s, hours = %s, module_value = %s, activity_name = %s, activity_description = %s WHERE activity_ID = %s",(activity_type_ID[0][0], start, end, hours, grade, title, description, activityID))
  else: 
    cur.execute("INSERT INTO Activities (module_ID, activity_type_ID, start_date, end_date, hours, module_value, lecture_ID, activity_name, activity_description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(moduleID, activity_type_ID[0][0], start, end, hours, grade, lecture, title, description))
  cur.close()
  mydb.commit()
  mydb.close()
  return res

@app.route("/updateClass", methods = ['POST'])
def updateClass():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)

  mydb = mysql.connector.connect(**connection_config_dict)


  classID = str(req['classID'])
  moduleID =  str(req['moduleID'])
  name = str(req['name'])
  description = str(req['description'])
  date = str(req['date'])
  activities = req['activities']

  i = 0
  if name == "0":
    name = None
  if description == "0":
    description = None

  cur = mydb.cursor(buffered=True)
  cur.execute("SELECT class_details_ID FROM Class_Details WHERE class_ID = %s AND class_date = %s", (classID, date))
  lectureinit = cur.fetchall()

  if (cur.rowcount >0): cur.execute("UPDATE Activities SET lecture_ID = %s WHERE lecture_ID = %s",(None, lectureinit[0][0]))
  cur.execute("DELETE FROM Class_Details WHERE class_ID = %s AND class_date = %s", (classID, date))
  cur.execute("INSERT INTO Class_Details (class_ID, module_ID, class_date, class_name, class_description) VALUES (%s,%s,%s,%s,%s)",(classID, moduleID, date, name, description))
  cur.execute("SELECT class_details_ID FROM Class_Details WHERE class_ID = %s AND class_date = %s", (classID, date))
  lecture = cur.fetchall()
  cur.execute("UPDATE Activities SET lecture_ID = %s WHERE lecture_ID = %s",(None, lecture[0][0]))
  try:
    while (i<len(activities)):
      cur.execute("UPDATE Activities SET lecture_ID = %s WHERE activity_ID = %s",(lecture[0][0], str(activities[i])))
      i=i+1
  except Exception: # Catch exception which will be raise in connection loss
    mydb = mysql.connector.connect(**connection_config_dict)
    cur = mydb.cursor(buffered=True)
  finally:
    cur.close()
    mydb.commit()
    mydb.close()
  return res

@app.route("/updateClassNotes", methods = ['POST'])
def updateClassNotes():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)

  mydb = mysql.connector.connect(**connection_config_dict)
  classID = str(req['classID'])
  date = str(req['date'])
  note =  str(req['note'])

  cur = mydb.cursor(buffered=True)  
  cur.execute("DELETE FROM Lecture_Notes WHERE note_lecture_ID = %s AND note_lecture_date = %s)", (classID, date))
  cur.execute("INSERT INTO Lecture_Notes (note_lecture_ID, note_lecture_date, note_text) VALUES (%s,%s,%s)", (classID, date, note))

  cur.close()
  mydb.commit()
  mydb.close()    
  return res
@app.route("/")
def test():
    return render_template("test.html")

if __name__ == '__main__':
    app.run(debug=True)