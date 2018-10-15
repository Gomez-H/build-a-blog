from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_blog = db.Column(db.String(120))
    body_blog = db.Column(db.String(200))
    submitted_blog = db.Column(db.Boolean)
    
    def __init__(self, title_blog):
        self.title_blog = title_blog
        self.submitted_blog = False

blogs = []

@app.route('/')
@app.route('/blog', methods=['GET', 'POST'])
def main_blog_page():
    return render_template('blog.html', blogs=blogs)


@app.route('/newpost', methods=['GET', 'POST'])
def  new_post():
    
    if request.method == 'POST':
        new_title = request.form['blog_title']
        add_title = Blog(new_title)
        new_body = request.form['blog_body']
        add_body = Blog(new_body)
        db.session.add(add_body,add_title)
        db.session.commit()

    
    return render_template('newpost.html')


if __name__ == '__main__':
    app.run()