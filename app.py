import email
from flask import Flask, render_template, request, redirect, url_for, jsonify,make_response,session
from flask.sessions import NullSession
import flask_login  
from flask_login.utils import logout_user
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import mariadb
from datetime import datetime
import sys


DBuser="root"
DBpassword="12345678"
DBhost="192.168.1.15"
DBport=3306
DBdatabase="admin_myfoster"

#123

app = Flask(__name__)
app.secret_key = '0'
login_manager = flask_login.LoginManager()

login_manager.init_app(app)
users = {}
nameUser = None

class User(flask_login.UserMixin):
    pass

def weeknum_to_dates(weeknum):
    data = [1,2,3,4,5,6,0]
    return [datetime.strptime(str(weeknum) + str('-') + str(x), "%Y-W%W-%w").strftime('%Y-%m-%d') for x in data]


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('Username')
    if email not in users:
        return

    user = User()
    user.id = email
    return user
    
@app.errorhandler(401)
def custom_401(error):
    return redirect(url_for('login_user'))

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)

@app.route("/", methods=['GET', 'POST'])
@app.route("/login_user", methods=['GET', 'POST'])
def login_user():        
    
    return render_template('login.html')

@app.route("/login_CkPass", methods=['GET', 'POST'])
def login_CkPass():
    if request.method == 'POST':
        
        conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin_myfoster.employyees")

        dataUser = request.form['username']
        print(users)
        for data in cur: 
            print(data)
            if dataUser == data[1]:
                if data[2] == None or  data[2] == '':
                    return render_template('login_NoPass.html',username = data[1])        
                else:
                    return render_template('login_Password.html',username = data[1])   
           
            
        return redirect(url_for('login_user'))

@app.route("/login_addPass/<string:username>", methods=['GET', 'POST'])
def login_addPass(username):
    if request.method == 'POST':
        dataPassword = request.form['New_Password']
        NewPassword = generate_password_hash(dataPassword,"sha256")
        print(NewPassword)
        conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
        cur = conn.cursor()
        cur.execute("UPDATE  admin_myfoster.employyees SET Pass = ? WHERE username = ?", (NewPassword,username))
        conn.commit() 
       

    return redirect(url_for('login_user'))

@app.route("/login_Password/<string:username>", methods=['GET', 'POST'])
def login_Password(username):
    if request.method == 'POST':
        dataPassword = request.form['Password']

        conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin_myfoster.employyees WHERE username = ?", (username,))

        conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
        cur1 = conn.cursor()
        cur1.execute("SELECT * FROM admin_myfoster.employyees")

        email = username

        for i in cur1:
            users[i[1]] = {'Password' : i[2]}

        print(users)
        
        
        for data in cur: 
            print(data[2])
           
            print(check_password_hash(data[2], dataPassword))
           
            if check_password_hash(data[2], dataPassword):
                user = User()
                user.id = email
                flask_login.login_user(user)
                    
                global nameUser 
                nameUser = email
                return render_template('login_succeed.html',username = username)   
            else :
                return redirect(url_for('login_user'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_user'))

@app.errorhandler(401)
def custom_401(error):
    return redirect(url_for('login_user'))

@app.errorhandler(404)
def custom_404(error):
    return redirect(url_for('login_user'))


@app.errorhandler(500)
def custom_500(error):
    return redirect(url_for('login_user'))

@app.route("/home/<string:username>", methods=['GET', 'POST'])
@flask_login.login_required
def home(username):
    conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
    cur = conn.cursor()
    cur.execute("SELECT * FROM admin_myfoster.employyees WHERE username = ?", (username,))
   
    for i in cur:
        name = i[3]
        surname = i[4]
        salary = i[5]
        position = i[6]
    return render_template('profile.html',username = username ,name =name ,surname =surname,salary=salary ,position = position )   


@app.route("/Weekly/<string:username>/<string:date>/<string:mode>", methods=['GET', 'POST'])
@flask_login.login_required
def Weekly(username,date,mode):
    conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
    cur = conn.cursor()
    cur.execute("SELECT * FROM admin_myfoster.employyees WHERE username = ?", (username,))

   
    for i in cur:
        name = i[3]
        surname = i[4]
        salary = i[5]
        position = i[6]
    dataOT1 = []
    dataOT2 = []
    dataOT3 = []
    dataOT4 = []
    dataOT5 = []
    dataOT6 = []
    dataOT7 = []
    dataOT8 = []
    dataOT9 = []
    dataOT10 = []
    dataOT11 = []
    dataOT12 = []
    dataOT13 = []
    dataOT14 = []
    dataOT15 = []
    dataOT16 = []
    dataOT17 = []
    dataOT18 = []
    dataOT19 = []
    dataOT20 = []

    conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
    project = conn.cursor()
    project.execute("select projectGenNumber , projectNameEN ,leaderName from admin_myfoster.project where projectOpenDate >= '2020-01-01'")

    projectAll = []
    for k in project:
        projectAll.append(str(k[0]) + str('|') + str(k[1]))


    if request.method == 'POST':
        if mode == '2': 
            Date = request.form['Date']
            Project = request.form['Project']
            ProjectNumber = Project.split("|")[0]
            ProjectName = Project.split("|")[1]
            Activity = request.form['Activity']
            Description = request.form['Description']
            TimeStart_Moning = request.form['TimeStart_Moning']
            TimeEnd_Moning = request.form['TimeEnd_Moning']
            TimeStart_Afternoon = request.form['TimeStart_Afternoon']
            TimeEnd_Afternoon = request.form['TimeEnd_Afternoon']
            TimeStart_OT = request.form['TimeStart_OT']
            TimeEnd_OT = request.form['TimeEnd_OT']

            if TimeStart_Moning :
                TimeStart_Moning = TimeStart_Moning
            else:
                TimeStart_Moning = '00:00'

            if TimeEnd_Moning :
                TimeEnd_Moning = TimeEnd_Moning
            else:
                TimeEnd_Moning = '00:00'

            if TimeStart_Afternoon :
                TimeStart_Afternoon = TimeStart_Afternoon
            else:
                TimeStart_Afternoon = '00:00'

            if TimeEnd_Afternoon :
                TimeEnd_Afternoon = TimeEnd_Afternoon
            else:
                TimeEnd_Afternoon = '00:00'

            if TimeStart_OT :
                TimeStart_OT = TimeStart_OT
            else:
                TimeStart_OT = '00:00'

            if TimeEnd_OT :
                TimeEnd_OT = TimeEnd_OT
            else:
                TimeEnd_OT = '00:00'
         

            print(Date)
            print(ProjectNumber)
            print(ProjectName)
            print(Activity)
            print(Description)
            print(TimeStart_Moning)
            print(TimeEnd_Moning)
            print(TimeStart_Afternoon)
            print(TimeEnd_Afternoon)
            print(TimeStart_OT)
            print(TimeEnd_OT)

            hourStartMoning= int(TimeStart_Moning.split(":")[0])
            minStartMoning = int(TimeStart_Moning.split(":")[1])

            if minStartMoning == 30 :
                minStartMoning = 50

            minStartMoning = minStartMoning * 0.01

            hourEndMoning = int(TimeEnd_Moning.split(":")[0])
            minEndMoning = int(TimeEnd_Moning.split(":")[1])

            if minEndMoning == 30 :
                minEndMoning = 50
            
            minEndMoning = minEndMoning * 0.01    
            allhourMoning = float((hourEndMoning - hourStartMoning) + (minEndMoning - minStartMoning))

            print('allhourMoning' , allhourMoning)

            hourStartAfternoon = int(TimeStart_Afternoon.split(":")[0])
            minStartAfternoon = int(TimeStart_Afternoon.split(":")[1])

            if minStartAfternoon == 30 :
                minStartAfternoon = 50

            minStartAfternoon = minStartAfternoon * 0.01

            hourEndAfternoon = int(TimeEnd_Afternoon.split(":")[0])
            minEndAfternoon = int(TimeEnd_Afternoon.split(":")[1])

            if minEndAfternoon == 30 :
                minEndAfternoon = 50
            
            minEndAfternoon = minEndAfternoon * 0.01    
            allhourAfternoon = float((hourEndAfternoon - hourStartAfternoon) + (minEndAfternoon - minStartAfternoon))

            print('allhourAfternoon' , allhourAfternoon)

            
            hourStartOT= int(TimeStart_OT.split(":")[0])
            minStartOT = int(TimeStart_OT.split(":")[1])

            if minStartOT == 30 :
                minStartOT = 50

            minStartOT = minStartOT * 0.01

            hourEndOT = int(TimeEnd_OT.split(":")[0])
            minEndOT = int(TimeEnd_OT.split(":")[1])

            if minEndOT == 30 :
                minEndOT = 50
            
            minEndOT = minEndOT * 0.01    
            allhourOT = float((hourEndOT - hourStartOT) + (minEndOT - minStartOT))

            print('allhourOT' , allhourOT)
            
            conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
            add = conn.cursor()
            add.execute("SELECT * FROM employyees WHERE username = ?", (username,))

            for i in add:
                id = i[0]
                Name = i[3] + str(' ')+  i[4]

            conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
            leaderNameProject = conn.cursor()
            leaderNameProject.execute("SELECT * FROM project WHERE admin_myfoster.projectGenNumber = ?", (ProjectNumber,))

            for i in leaderNameProject:
                leaderName = i[4]
            
            print(id)
            #print(leaderName)
            date_time_obj = datetime.strptime(Date, '%Y-%m-%d')
            print("------------------------------------")
           
            ListDay = [] 
            rate15 = 0.0
            rate2 = 0.0
            rate3 = 0.0

            if date_time_obj.strftime('%A') == 'Saturday':
                rate15 =  allhourMoning  +  allhourAfternoon 
                rate2 = 0
                rate3 = allhourOT
            elif date_time_obj.strftime('%A') == 'Sunday':
                rate15 = 0
                rate2 = allhourMoning  +  allhourAfternoon 
                rate3 = allhourOT
            else:
                rate15 = allhourOT
                rate2 = 0
                rate3 = 0
            
            print('day ' , date_time_obj.strftime('%A'))
            print('rate1.5 ',rate15)
            print('rate2 ',rate2)
            print('rate3 ',rate3)


            
            conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
            add = conn.cursor()
            add.execute("UPDATE admin_myfoster.overtimev5 SET ProjectName=?,ProjectNumber=?,Activity=?,Description=?,TimeStart_Moning=?,TimeEnd_Moning=?,TimeStart_Afternoon=?,TimeEnd_Afternoon=?,TimeStart_OT=?,TimeEnd_OT=?,Total=?,leaderName=?,Confirm=?  Where ID = ? AND Date = ?", (ProjectName,ProjectNumber,Activity,Description,TimeStart_Moning,TimeEnd_Moning,TimeStart_Afternoon,TimeEnd_Afternoon,TimeStart_OT,TimeEnd_OT,allhourOT,leaderName,"Wait",id,Date))
            conn.commit()

            conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
            rate = conn.cursor()
            rate.execute("UPDATE admin_myfoster.culrate SET ID=?,Name=?,Date=?,rate_15=?,rate_2=?,rate_3=?,Day=?  Where ID = ? AND Date = ? ", (id,Name,Date,rate15,rate2,rate3, date_time_obj.strftime('%A'),id,Date))
            conn.commit()
          


        elif mode == '3':
            Date = request.form['Date']
            Project = request.form['Project']
            ProjectNumber = Project.split("|")[0]
            ProjectName = Project.split("|")[1]
            Activity = request.form['Activity']
            Description = request.form['Description']
            TimeStart_Moning = request.form['TimeStart_Moning']
            TimeEnd_Moning = request.form['TimeEnd_Moning']
            TimeStart_Afternoon = request.form['TimeStart_Afternoon']
            TimeEnd_Afternoon = request.form['TimeEnd_Afternoon']
            TimeStart_OT = request.form['TimeStart_OT']
            TimeEnd_OT = request.form['TimeEnd_OT']
           
            print(Date)
            print(ProjectNumber)
            print(ProjectName)
            print(Activity)
            print(Description)
            print(TimeStart_Moning)
            print(TimeEnd_Moning)
            print(TimeStart_Afternoon)
            print(TimeEnd_Afternoon)
            print(TimeStart_OT)
            print(TimeEnd_OT)

            hourStartMoning= int(TimeStart_Moning.split(":")[0])
            minStartMoning = int(TimeStart_Moning.split(":")[1])

            if minStartMoning == 30 :
                minStartMoning = 50

            minStartMoning = minStartMoning * 0.01

            hourEndMoning = int(TimeEnd_Moning.split(":")[0])
            minEndMoning = int(TimeEnd_Moning.split(":")[1])

            if minEndMoning == 30 :
                minEndMoning = 50
            
            minEndMoning = minEndMoning * 0.01    
            allhourMoning = float((hourEndMoning - hourStartMoning) + (minEndMoning - minStartMoning))

            print('allhourMoning' , allhourMoning)

            hourStartAfternoon = int(TimeStart_Afternoon.split(":")[0])
            minStartAfternoon = int(TimeStart_Afternoon.split(":")[1])

            if minStartAfternoon == 30 :
                minStartAfternoon = 50

            minStartAfternoon = minStartAfternoon * 0.01

            hourEndAfternoon = int(TimeEnd_Afternoon.split(":")[0])
            minEndAfternoon = int(TimeEnd_Afternoon.split(":")[1])

            if minEndAfternoon == 30 :
                minEndAfternoon = 50
            
            minEndAfternoon = minEndAfternoon * 0.01    
            allhourAfternoon = float((hourEndAfternoon - hourStartAfternoon) + (minEndAfternoon - minStartAfternoon))

            print('allhourAfternoon' , allhourAfternoon)

            
            hourStartOT= int(TimeStart_OT.split(":")[0])
            minStartOT = int(TimeStart_OT.split(":")[1])

            if minStartOT == 30 :
                minStartOT = 50

            minStartOT = minStartOT * 0.01

            hourEndOT = int(TimeEnd_OT.split(":")[0])
            minEndOT = int(TimeEnd_OT.split(":")[1])

            if minEndOT == 30 :
                minEndOT = 50
            
            minEndOT = minEndOT * 0.01    
            allhourOT = float((hourEndOT - hourStartOT) + (minEndOT - minStartOT))

            print('allhourOT' , allhourOT)
            
            conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
            add = conn.cursor()
            add.execute("SELECT * FROM admin_myfoster.employyees WHERE username = ?", (username,))

            for i in add:
                id = i[0]
                Name = i[3] + str(' ')+  i[4]

            conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
            leaderNameProject = conn.cursor()
            leaderNameProject.execute("SELECT * FROM admin_myfoster.project WHERE projectGenNumber = ?", (ProjectNumber,))

            for i in leaderNameProject:
                leaderName = i[4]
            
            print(id)
            #print(leaderName)
            date_time_obj = datetime.strptime(Date, '%Y-%m-%d')
            print("------------------------------------")
           
            ListDay = [] 
            rate15 = 0.0
            rate2 = 0.0
            rate3 = 0.0

            if date_time_obj.strftime('%A') == 'Saturday':
                rate15 =  allhourMoning  +  allhourAfternoon 
                rate2 = 0
                rate3 = allhourOT
            elif date_time_obj.strftime('%A') == 'Sunday':
                rate15 = 0
                rate2 = allhourMoning  +  allhourAfternoon 
                rate3 = allhourOT
            else:
                rate15 = allhourOT
                rate2 = 0
                rate3 = 0
            
            print('day ' , date_time_obj.strftime('%A'))
            print('rate1.5 ',rate15)
            print('rate2 ',rate2)
            print('rate3 ',rate3)

            conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
            add = conn.cursor()
            add.execute("INSERT INTO admin_myfoster.overtimev5(ID,Date,Name,ProjectName,ProjectNumber,Activity,Description,TimeStart_Moning,TimeEnd_Moning,TimeStart_Afternoon,TimeEnd_Afternoon,TimeStart_OT,TimeEnd_OT,Total,leaderName,Confirm)  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (id,Date,Name,ProjectName,ProjectNumber,Activity,Description,TimeStart_Moning,TimeEnd_Moning,TimeStart_Afternoon,TimeEnd_Afternoon,TimeStart_OT,TimeEnd_OT,allhourOT,leaderName,"Wait"))
            conn.commit()

            conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
            rate = conn.cursor()
            rate.execute("INSERT INTO admin_myfoster.culrate(ID,Name,Date,rate_15,rate_2,rate_3,Day)  VALUES(?,?,?,?,?,?,?)", (id,Name,Date,rate15,rate2,rate3, date_time_obj.strftime('%A')))
            conn.commit()
            
            

        conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin_myfoster.employyees WHERE username = ?", (username,))

       
    
        for i in cur:
            id = i[0]

        dataweek = request.form['week']
        print(dataweek)
        print(weeknum_to_dates(dataweek))
        print(weeknum_to_dates(dataweek)[0])
        conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
        ot = conn.cursor()
        ot.execute("SELECT * FROM admin_myfoster.overtimev5 WHERE ID = ? AND Date >= ? AND  Date <= ? order by `Date` asc ", (id,weeknum_to_dates(dataweek)[0],weeknum_to_dates(dataweek)[6]))
        
        for i in ot:
            dataOT1.append(i[0])
            dataOT2.append(i[1])
            dataOT3.append(i[2])
            dataOT4.append(i[3])
            dataOT5.append(i[4])
            dataOT6.append(i[5])
            dataOT7.append(i[6])
            dataOT8.append(i[7])
            dataOT9.append(i[8])
            dataOT10.append(i[9])
            dataOT11.append(i[10])
            dataOT12.append(i[11])
            dataOT13.append(i[12])
            dataOT14.append(i[13])
            dataOT15.append(i[14])
            dataOT16.append(i[15])
            dataOT17.append(i[16])
            dataOT18.append(i[17])
            dataOT19.append(i[18])
            dataOT20.append(i[19])
            print(dataOT8)

        return render_template('Weekly.html',username = username ,name =name ,surname =surname,salary=salary ,position = position ,dataweek=weeknum_to_dates(dataweek),dataOT1=dataOT1,dataOT2=dataOT2,dataOT3=dataOT3,dataOT4=dataOT4,dataOT5=dataOT5,dataOT6=dataOT6, \
             dataOT7=dataOT7,dataOT8=dataOT8,dataOT9=dataOT9,dataOT10=dataOT10,dataOT11=dataOT11,dataOT12=dataOT12,dataOT13=dataOT13,dataOT14=dataOT14,dataOT15=dataOT15,dataOT16=dataOT16,dataOT17=dataOT17,dataOT18=dataOT18,dataOT19=dataOT19,dataOT20=dataOT20,project = projectAll,lenproject = len(projectAll),dataweekDE=dataweek) 

    return render_template('Weekly.html',username = username ,name =name ,surname =surname,salary=salary ,position = position ,dataweek=0,dataOT1=dataOT1,dataOT2=dataOT2,dataOT3=dataOT3,dataOT4=dataOT4,dataOT5=dataOT5,dataOT6=dataOT6, \
             dataOT7=dataOT7,dataOT8=dataOT8,dataOT9=dataOT9,dataOT10=dataOT10,dataOT11=dataOT11,dataOT12=dataOT12,dataOT13=dataOT13,dataOT14=dataOT14,dataOT15=dataOT15,dataOT16=dataOT16,dataOT17=dataOT17,dataOT18=dataOT18,dataOT20=dataOT20,project=projectAll,lenproject = len(projectAll),dataweekDE=date)   

@app.route("/listWeekly/<string:username>", methods=['GET', 'POST'])
@flask_login.login_required
def listWeekly(username):
    conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
    cur = conn.cursor()
    cur.execute("SELECT * FROM admin_myfoster.employyees WHERE username = ?", (username,))
   
    for i in cur:
        name = i[3]
        surname = i[4]
        salary = i[5]
        position = i[6]
    
   
    if request.method == 'POST':
        month = request.form['month']
        endMonth =   month +"-15"
        backMonth = int(month.split("-")[1]) 
        backYaer = int(month.split("-")[0]) 

        if backMonth <=  1:
            backMonth = 12
            backYaer = backYaer - 1 
        else:
            backYaer = backYaer
            backMonth = backMonth - 1

        startMonth =  str(backYaer) +'-' + str(backMonth) + "-16" 
        print('startMonth ' , startMonth)
        print('endMonth ' , endMonth)


        conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
        cur = conn.cursor()
        cur.execute("select DISTINCT ID from admin_myfoster.employyees")
        idEmp = []
        count = 0
        Allrate15 = 0
        Allrate2 = 0
        Allrate3 = 0
        F_ALL_DATA = []
        user = ''
        ck = False
        for i in cur:
            count += 1
            idEmp.append(i[0])

            conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
            cat123 = conn.cursor()
            cat123.execute("SELECT c.ID , c.Name , SUM(c.rate_15) as r15 , SUM(c.rate_2) as r2, SUM(c.rate_3) as r3 , ( (((e.Salary / 30) / 8) * 1.5) * SUM(c.rate_15)   )  +  ((((e.Salary / 30) / 8) * 2)*SUM(c.rate_2) )  + ((((e.Salary / 30) / 8) *3)* SUM(c.rate_3) )  + e.Salary  - e.Deduct  as allSalary FROM admin_myfoster.culrate c INNER JOIN admin_myfoster.employyees e ON e.id = c.ID where  Date >= ? and Date <= ? GROUP BY ID",(startMonth,endMonth))
            

        print(month)
        return render_template('listWeekly.html',username = username ,name =name ,surname =surname,salary=salary ,position = position,data = cat123) 


    return render_template('listWeekly.html',username = username ,name =name ,surname =surname,salary=salary ,position = position,data ='-' ) 

@app.route("/detailsWeekly/<string:id>", methods=['GET', 'POST'])
@flask_login.login_required
def detailsWeekly(id):
    conn = mariadb.connect(user=DBuser,password=DBpassword,host=DBhost,port=DBport,database=DBdatabase)
    cur = conn.cursor()
    cur.execute("select DISTINCT ID from admin_myfoster.employyees")
    
    return render_template("",username = id)

@app.route("/po/<string:id>", methods=['GET', 'POST'])
@flask_login.login_required
def po(id):
 
    
    return render_template("po.html",username = id)

if __name__ == "__main__": 
    app.run(host='0.0.0.0', debug=True, port=5000)