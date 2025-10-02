from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)
# database part
app.config['SECRET_KEY'] = "supper_secerete"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///tododata.db" 
db = SQLAlchemy()

# db model
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.Text, nullable = False)
    status = db.Column(db.Boolean, default=False)
    datepost = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


# db initilization and creation part
db.init_app(app)
# with app.app_context():
#     db.create_all()


# core part
@app.route('/')
def index():
    user = User.query.all()
    return render_template('index.html', tasks = user)

@app.route('/completed')
def completed():
    user = User.query.all()
    return render_template('update.html', tasks = user)

@app.route('/', methods=['GET','POST'])
def task_deatils():
    task = request.form.get("task")
    user= User(task=task)
    db.session.add(user)
    db.session.commit()
    return redirect('/')

@app.route('/status/<int:task_id>/update')
def status_update(task_id):
    user = User.query.get_or_404(task_id)
    user.status = bool(True)
    db.session.commit()
    print(user.status)
    return redirect("/")

@app.route("/edit/<int:task_id>/task", methods=["GET", "POST"])
def edit_task(task_id):
    user = User.query.get_or_404(task_id)
    if request.method == "POST":
        user.task = request.form['edit_task']
        db.session.commit()
        return redirect("/")
    return render_template('update.html', tasks = user)



@app.route("/delete/<int:task_id>/task")
def delete_task(task_id):
    user = User.query.get_or_404(task_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")
if __name__ == '__main__':
    app.run(debug=True)