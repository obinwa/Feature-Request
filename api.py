import os
from flask import Flask, request, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import *
from flask_heroku import Heroku

PRIORITY_NUM = 10

#Settings
app = Flask(__name__)
heroku = Heroku(app)
app.config["DEBUG"] = False #True

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = 'postgresql://localhost/reqInfo' #"sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
#db.create_all()

class FRequest(db.Model):
    __tablename__  = 'f_request'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    client = db.relationship('Client', back_populates='f_request',lazy = 'joined', uselist='False')#, primaryjoin="client.c.id == f_request.client_id")
    # client_id = db.Column(db.Integer,ForeignKey("client.c.id"))
    client_priority = db.Column(db.Integer)
    target_date = db.Column(db.DateTime)
    product_area = db.Column(db.String)

    def __init__(self,title,desc,clienta,client_priority,tdate,prd_area):
        self.id 
        self.title = title
        self.description = desc
        exists = db.session.query(db.session.query(Client).filter_by(title=clienta).exists()).scalar()

        if exists:
            self.client = db.session.query(Client).filter_by(title=clienta)
            self.client.priority.remove_num(client_priority)
        else :
            priority = Priority([PRIORITY_NUM])
            self.client = [Client(clienta,[priority])]
            self.client[0].priority[0].remove_num(client_priority)

        #self.client =  if exists  else Client(title=client)#client
        #self.client_priority = client_pr
        self.target_date = tdate
        self.product_area = prd_area

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String)
    f_request = db.relationship('FRequest', back_populates='client')
    priority = db.relationship('Priority', back_populates='client',lazy = 'joined', uselist='False')#, primaryjoin="priority.id == client.priority_id")
    req_id = db.Column(db.Integer,ForeignKey("f_request.id"))

    def __init__(self,title,priority):
        self.title = title
        self.priority = priority
    
class Priority(db.Model):
    __tablename__ = 'priority'
    id = db.Column(db.Integer,primary_key=True)
    client_priority = db.Column(postgresql.ARRAY(db.Integer))
    client = db.relationship('Client', back_populates='priority',uselist='False')
    client_id = db.Column(db.Integer,ForeignKey("client.id"))

    def __init__(self,max):
        
        self.client_priority = self.createArr(max)
    
    def createArr(self,max):
        arr = [0] * max[0]
        for i in range(max[0]) :
            arr[i] = i
        return arr


    def array():
        return self.client_priority


    def remove_num(self,num):
        self.client_priority.remove(num)
        
   
@app.route('/priority', methods=['POST'])
def get_priority():
   # console.log(request.form['client'])
    client = request.form['client']
    dexists = db.session.query(db.session.query(Client).filter_by(title=client).exists()).scalar()

    if dexists == True:
        uclient = db.session.query(Client).filter_by(title=client)
        priorityArray = uclient[0].priority[0].client_priority
        return jsonify(priorityArray)
    else :
        priority = Priority([PRIORITY_NUM])
        uclient = Client([client],[priority])
        return jsonify(priority.client_priority)





@app.route('/', methods=['GET'])
def home1():
    return render_template('feature.html')
    #return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/RequestInfo', methods=['POST'])
def home():
    if request.form:
        title = request.form.get("title")
        desc = request.form.get("desc")
        client = request.form.get("client")
        print(client)
        remove_pr = int(request.form.get("client_pr"))
        tdate = request.form.get("tdate")
        prd_area = request.form.get('prd_area')
        message = ""
        
        # exists = db.session.query(db.session.query(Client).filter_by(title=title,desc=desc,client=client,prd_area=prd_area).exists()).scalar()
        # if exists == True :
        #     #indicate that value already exists
        #     message = "Value already exists"
        # else:
            #create feature and save to db
        reqInfo = FRequest(title,desc,client,remove_pr,tdate,prd_area)
        db.session.add(reqInfo)
        db.session.commit()
        message = "Successful submission"



    

        
    #books = Book.query.all()
    return render_template("submit.html", message=message)


def remove_num(num,array):
    array.remove(num)
    return array


app.run()

