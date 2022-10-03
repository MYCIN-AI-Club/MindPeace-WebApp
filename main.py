from flask import Flask,render_template,redirect,url_for,request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
import matplotlib.pyplot as plt



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///trackdb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db= SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    password = db.Column(db.String(10), nullable=False)
    trackers= db.relationship('Tracker',backref='owner')
    def __init__(self,username,password):
        self.username=username
        self.password=password
class Tracker(db.Model): 
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(30),nullable=False)
    type=db.Column(db.String(30),nullable=False)
    description=db.Column(db.String(100))
    last_update=db.Column(db.DateTime,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    logs=db.relationship('Logs',backref='tracker')
    def __init__(self,name,type,description,user_id,last_update=datetime.now()):
        self.name=name
        self.type=type
        self.description=description
        self.last_update=last_update
        self.user_id=user_id
#Logs class to be made


db.create_all()
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/dashboard<username>")
def dashboard(username):
    user=User.query.filter_by(username=username).first()
    t=Tracker.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', title='Dashboard',username=username,trackers=t,user_id=user.id)
    
    

@app.route('/login', methods=['GET'])
def login():
    if request.method =='POST':
        username=request.form['username']  
        password=request.form['password']
        u=User(username,password)
        user=User.query.filter_by(username=username).all()
        if(len(user)==0):
            db.session.add(u)
            db.session.commit()
            db.session.close()
        return redirect(url_for('dashboard',username=username))
           
 
@app.route('/addtracker<user_id>',methods=['GET','POST']) 

def addtracker(user_id):
    U=User.query.filter_by(id=user_id).first()
    username=U.username
    
    if request.method =='POST':
        name=request.form['name']
        description=request.form['description']
        type=request.form['type']
        dt=datetime.now()
        t=Tracker(name,type,description,user_id,dt)
        
        db.session.add(t)
        db.session.commit()
        db.session.close()
        
             
        return redirect(url_for('dashboard',username=username))
         

    return render_template('addtracker.html',username=username) 
@app.route('/delete<id>')    

def delete(id):
    t=Tracker.query.filter_by(id=id).first()
    u=User.query.filter_by(id=t.user_id).first()
    Tracker.query.filter_by(id=id).delete()

    db.session.commit()

    return redirect(url_for('dashboard',username=u.username))
@app.route('/edit<id>',methods=['GET','POST'])    
def edit(id):
    t=Tracker.query.filter_by(id=id).first()
    u=User.query.filter_by(id=t.user_id).first()
    l=Logs.query.filter_by(tracker_id=id).all()
    
    for i in range(len(l)):
        print(l[i],l[i].tracker_id)
    if(request.method=='POST'):
        db.session.delete(t)
        db.session.commit()
        if t:
            name=request.form['name']
            description=request.form['description']
            type=request.form['type']
            dt=datetime.now()
            t=Tracker(name,type,description,u.id,dt)
            db.session.add(t)
            db.session.commit()
            tc=Tracker.query.filter_by(id=id).first()
            for i in range(len(l)):
                l[i].tracker_id=tc.id
                db.session.commit()
            
        return redirect(url_for('dashboard',username=u.username))

    return render_template('edit.html',id=id,username=u.username,t=t)

@app.route('/addlog<id>',methods=['GET','POST']) 
def addlog(id):
    t=Tracker.query.filter_by(id=id).first()
    u=User.query.filter_by(id=t.user_id).first()

    if request.method=='POST':
        date=request.form['when']
        value=request.form['value']
        notes=request.form['notes']
        when=datetime.strptime(date,'%Y-%m-%d').date()
        l=Logs(value,notes,id,when)
        dt=datetime.now()
        t.last_update=dt
        db.session.add(l)
        db.session.commit()
        return redirect(url_for('dashboard',username=u.username))
    return render_template('addlog.html',id=id,username=u.username,name=t.name)
@app.route('/tracker<id>') 
def tracker(id):
    t=Tracker.query.filter_by(id=id).first()
    u=User.query.filter_by(id=t.user_id).first()  
    l=Logs.query.filter_by(tracker_id=t.id).all()
    time=[]
    v=[]S
    for i in l:
        time.append(i.when)
        v.append(i.value)

    plt.bar(time,v,width=0.5,color='blue')
    plt.xlabel("X Axis") 
    plt.ylabel("Y Axis")
    plt.savefig('static/myplot.png')
    # plt.show()

    return render_template('tracker.html',t=t,username=u.username,logs=l)

   

if __name__=='__main__' :
    app.run(debug=True)
