from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from apiclient.discovery import build

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
api_key="AIzaSyBRDH72CIzKXrRLEZHCsqRFGpIHhTS1C6w"
youtube=build('youtube','v3',developerKey=api_key)

def vid_get(vidq):
    req=youtube.search().list(part='snippet',q=vidq,type='video',maxResults=1,videoCategoryId=10)
    res=req.execute()
    vid=res['items'][0]['id']['videoId']
    return vid

class Todo(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    vidid=vid_get(vidq="Kadhaippoma")

    if request.method=='POST':
        vidid=vid_get(vidq=request.form['content'])
    return render_template('index.html', vidid=vidid)



@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

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

@app.route('/test/', methods=['GET', 'POST'])
def test():
    pass
if __name__ == "__main__":
    app.run(debug=True)
