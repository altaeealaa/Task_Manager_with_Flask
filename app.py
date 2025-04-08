from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__) #referencing the file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class ToDo(db.Model):
   id= db.Column(db.Integer, primary_key=True)
   content = db.Column(db.String(200), nullable=False)
   data_created = db.Column(db.DateTime, default=datetime.utcnow)

   def __repr__(self):#will return a string everytime a new item is created
      return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET']) #so when we browse to url, 404 error doesn't appear. In it we pass url of your route.


def index():#fct of this route
   if request.method == 'POST':
      task = request.form['content']
      new_task = ToDo(content= task)

      try:
         db.session.add(new_task)
         db.session.commit()
         return redirect('/')
      except:
         return('There was an error adding the task')
    
   else:
      query_tasks=ToDo.query.order_by(ToDo.data_created).all()
      return render_template('index.html', tasks=query_tasks) #it knows it should look in folder "templates". It's that name for a reason 

@app.route('/delete/<int:id>')
def delete(id):
   task_to_delete = ToDo.query.get_or_404(id)

   try:
      db.session.delete(task_to_delete)
      db.session.commit()
      return redirect('/')
   except:
      return 'Error while deleting the task'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
   task=ToDo.query.get_or_404(id)

   if request.method=='POST':
      task.content=request.form['content']

      try:
         db.session.commit()
         return redirect('/')
      except:
         return 'An issue occured while updating the task'
      
   else:
      return render_template('update.html', task=task)
   

if __name__ == "__main__":
   app.run(debug=True) #debug=True, so if we have any errors it will pop up on screen
