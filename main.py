from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import smtplib
import requests
import base64
import pandas

my_email="qh182756@gmail.com"
password="uywgriiyqjcaauyg"
API_ID="ff5750d2"
API_KEY="4aa27364c6e82a8cebc7dde64009610e"
SHEET_API_CSE="https://api.sheety.co/9f8b541cea9377651b9327d784fa4fe3/attendenceCse/sheet1"
SHEET_API_ECE="https://api.sheety.co/9f8b541cea9377651b9327d784fa4fe3/attendanceEce/sheet1"
SHEET_LINK_CSE="https://docs.google.com/spreadsheets/d/1FFQK-LG-8H2YNPy11MePS9qzN8gJXRny6GyQY8Os4pU/edit#gid=0"
SHHET_LINK_ECE="https://docs.google.com/spreadsheets/d/1SMYO_1H4Fmrs1lI1gO4C7EKkIZ6mbFsQnHZNMxXTn7c/edit#gid=0"


app = Flask(__name__)

app.config['SECRET_KEY'] = 'rocky'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
FOLDER="D:/python/udemy/68-intinalauthecation/static/files"

login_manager=LoginManager()
login_manager.init_app(app)



##CREATE TABLE IN DB
class Professor(UserMixin, db.Model):
    __tablename___="Professor_Table"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    
    
    
class Student(UserMixin, db.Model):
    __tablename___="Student_Table"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))   
    roll_no= db.Column(db.String(100))   
    days_missed=db.Column(db.Integer)   
    
    
#Line below only required once, when creating DB. 
with app.app_context():
    # db.create_all()
    @login_manager.user_loader
    def load_user(user_id):
        return Professor.query.get(int(user_id))
    
    
    @login_manager.user_loader
    def load_user(user_id):
        return Student.query.get(int(user_id))
    
    
    

    @app.route('/',methods=["GET"])
    def home():     
        logout_user()
        return render_template("main.html")



    @app.route('/facescan',methods=["POST","GET"])
    def face_login():
        if request.method=="POST":
            username=request.form["name"]
            user=Professor.query.filter_by(email=username).first()
            if not user:
                user=Student.query.filter_by(email=username).first()
                if user:
                    flash("This section only teachers can access")
                    return redirect(url_for("face_login"))
                else:
                    flash("This email doesn't exist,Try again later")
                    return redirect(url_for("face_login"))
            password=request.form["password"]
            if user.password==password:
                login_user(user)
                return redirect(url_for("face_scan"))
            else:
                flash("Password doesn't match,try again")
                return redirect(url_for("face_login"))
               
            
        return render_template('login.html')
    
    
    
    
    
    @app.route('/face_scan')
    @login_required
    def face_scan():
         return render_template('face_scan.html')
    
    
    
    
    
    @app.route('/save-photo', methods=['POST'])
    @login_required
    def save_photo():
        image_data = request.form['image'].split(',')[1]
        image_data = base64.b64decode(image_data)

        with open('captured_image.png', 'wb') as f:
            f.write(image_data)
            
        with open('captured_image.png', 'rb') as f:
            image_bytes = f.read()


        image_b64 = base64.b64encode(image_bytes).decode('utf-8')

        payload = {
         'image': image_b64,
         'other_data': '...'
         # add other fields as needed
         }

        #this is for running the face recongition and create csv as output
        # URL="https://6b80-34-87-129-147.ngrok.io/process"
        # response=requests.post(url=URL,json=payload)
        # print(response.json())  
        
        return redirect(url_for('in_sheet'))  
    
    
    
    
    @app.route('/Sheet',methods=["POST","GET"])
    def in_sheet():
        csv="D:/project/vahsist_project/project/static/files/NEW.csv"
        data=pandas.read_csv(csv)
        data=data.to_dict()
        rollno=data["RollNo"][0]
        date=data["Date"][0]
        date=date.replace("-","")
        response=requests.get(url=f"{SHEET_API_CSE}")
        data=response.json()
        data=data["sheet1"]
        c=0            
        for entry in data:
            if entry["rollno"]==rollno:
                id=entry["id"]
                c=1
                
        if c==0:
            response=requests.get(url=f"{SHEET_API_ECE}")
            data=response.json()
            data=data["sheet1"]
            for entry in data:
                 if entry["rollno"]==rollno:
                    id=entry["id"]
                    c=0
            
                    
                        
        sheet_inputs={
                    'sheet1':{

                date:'P'
            
                }
                }

        if c==1:
             response=requests.put(url=f"{SHEET_API_CSE}/{id}",json=sheet_inputs) 
        else:
             response=requests.put(url=f"{SHEET_API_ECE}/{id}",json=sheet_inputs)    
        return jsonify(response={"Success":"Changed in sheet"})     

        
        
    


    @app.route('/teacher_portal_login',methods=["POST","GET"])
    def teacher_portal():
        if request.method=="POST":
            name=request.form["username"]
            
            user=Professor.query.filter_by(email=name).first()
            if not user:
                user=Student.query.filter_by(email=name).first()
                if user:
                    flash("This email corresponds to student login ,Kindly login there")
                    return redirect(url_for("student_portal"))
                else:
                    flash("This email doesn't exist,Try again later")
                    return redirect(url_for("teacher_portal"))
            password=request.form["password"]
            if user.password==password:
                login_user(user)
                return redirect(url_for("t_portal"))
            else:
                flash("Password doesn't match,try again")
                return redirect(url_for("teacher_portal"))
            
            
        return render_template("teacher.html")
    
    
    
    
    @app.route('/student_portal_login',methods=["POST","GET"])
    def student_portal():
        if request.method=="POST":
            name=request.form["username"]
            
            user=Student.query.filter_by(email=name).first()
            if not user:
                user=Professor.query.filter_by(email=name).first()
                if user:
                    flash("This email corresponds to professor login ,Kindly login there")
                    return redirect(url_for("teacher_portal"))
                else:
                    flash("This email doesn't exist,Try again later")
                    return redirect(url_for("student_portal"))
            password=request.form["password"]
            if user.password==password:
                login_user(user)
                return redirect(url_for("s_portal"))
            else:
                flash("Password doesn't match,try again")
                return redirect(url_for("student_portal"))
            
            
            
        return render_template("student.html")
    

    @app.route('/forgot_password',methods=["POST","GET"])
    def forgot_password():
        if request.method=="POST":
            username=request.form["email"]
            user=Professor.query.filter_by(email=username).first()
            if not user:
                user=Student.query.filter_by(email=username).first()
                if user:
                    with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
                        connection.starttls()#to make the message encrypted so that people in between cant read it
                        connection.login(user=my_email,password=password)
                        connection.sendmail(from_addr=my_email,to_addrs=user.email,msg=f"Subject:Retrive Password(PROXY SHIELD)\n\nDear {user.name},\nKindly dont share this email with anybody\n Your password is:{user.password}")
                    flash("The password is sent to your registered email id") 
                    return redirect(url_for('forgot_password'))   
                else:
                    flash("The entered email id doesn't exist,Kindly try again") 
                    return redirect(url_for('forgot_password'))   
            else:
                with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
                        connection.starttls()#to make the message encrypted so that people in between cant read it
                        connection.login(user=my_email,password=password)
                        connection.sendmail(from_addr=my_email,to_addrs=user.email,msg=f"Subject:Retrive Password(PROXY SHIELD)\n\nRespected{user.name},\nKindly dont share this email with anybody\n Your password is:{user.password}")
                flash("The password is sent to your registered email id")        
        
        return render_template('forgot.html')
    
    
    
    

    @app.route('/student_portal',methods=["POST","GET"])
    @login_required
    def s_portal():
        name=current_user.name
        rollno=current_user.roll_no
     
        days=round((22-current_user.days_missed)/22*100)
        return render_template("student1.html",name=name,rollno=rollno,days=days)
    
    @app.route('/teacher_portal',methods=["POST","GET"])
    @login_required
    def t_portal():
        name=current_user.name
        
        return render_template("teacher1.html",name=name,cse=SHEET_LINK_CSE,ece=SHHET_LINK_ECE)


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("home"))


    @app.route('/download')
    @login_required
    def download():
        name="cheat_sheet.pdf"
        return send_from_directory(FOLDER,'cheat_sheet.pdf',download_name='flask_cheatsheet')


    if __name__ == "__main__":
        app.run(debug=True)
