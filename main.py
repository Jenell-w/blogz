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
# I need to find the id of the entry in the table (blog) and pull it out and 
#display the associated title and body.  how do i get the individual blog id
#and find the associated table information?  
    title = request.args.get('title')    
    body = request.args.get('body')
    blogid = Blog.query.filter_by(id=1).first() 
    return render_template('blog-entry.html', title=title, body=body, blogid=blogid)

# my blogid query below does not seem to be extracting just the id number from the table
# Perhaps these two routes ('/blog-entry') and ('/blog) need to be reconfigured?
@app.route('/blog')
def blog():
    entries = Blog.query.all()
    blogid = Blog.query.filter_by(id=1).first()
    return render_template('full-blog.html', title="My Blog", entries=entries, blogid=blogid)

if __name__ == '__main__':
    app.run()




