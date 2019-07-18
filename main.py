from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['DEBUG'] = True

project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, "flicklist.db"))
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body
@app.route('/')
def get_something():
    return redirect('/addnew')

@app.route('/addnew', methods = ['GET', 'POST'])
def new_post():
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title == '':
            return render_template('add-new.html', error1="Please add a title")
        if body == '':
            return render_template('add-new.html', error2="Please add an entry")
        new_entry = Blog(title, body)
        db.session.add(new_entry)
        db.session.commit()
        return redirect('/blog')
        
        
    return render_template('add-new.html')

@app.route('/blog-entry')
def display_entry():
    id_value = request.args.get('id')
    blog = Blog.query.filter_by(id=id_value).first() 
    return render_template('blog-entry.html', title=blog.title, body=blog.body)

@app.route('/blog')
def blog():
    entries = Blog.query.all()
    return render_template('full-blog.html', title="My Blog", entries=entries)

if __name__ == '__main__':
    app.run()




