from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import current_app, g
import sqlite3
import click


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WS2.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), default='')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' % self.id

class Venues(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   Ven_Name=db.Column(db.String(200))
   Artist_Name=db.Column(db.String(200))
   Ven_descrip=db.Column(db.String(10000))
   Ven_Date=db.Column(db.String)
   Seats_Avail=db.Column(db.Integer, default=50)
   
   def _repr_(self):
        return '<Task %r>' % self.id
    
with app.app_context():
    db.create_all()
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
    
@app.route('/Post_ven', methods=['POST', 'GET'])
def Post_ven():
    if request.method == 'POST':
        Name=request.form['Ven_Name']
        Artist_Name=request.form['Artist_Name']
        Ven_descrip=request.form['Ven_descrip']
        Ven_Date=request.form['Ven_Date']
        Seats_Avail=request.form['Seats_Avail']
        new_Ven=Venues(Ven_Name=Name,Artist_Name=Artist_Name,Ven_descrip=Ven_descrip,Ven_Date=Ven_Date)
        try:
            db.session.add(new_Ven)
            db.session.commit()
            return redirect('/')
        except:
             return 'There was an issue adding your task. You may have left an field empty'

    else:
        
        V_ID = Venues.query.order_by(Venues.id).all()
        return render_template('index.html', V_ID=V_ID)       
       
       
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/Ven_update', methods=['POST', 'GET'])
def Ven_update():
    if request.method == 'POST':
        return render_template('Ven_update.html')
    else:
        return render_template('index.html')
      
   
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
