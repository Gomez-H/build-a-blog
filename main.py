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
    
    def __init__(self, title_blog, body_blog):
        self.title_blog = title_blog
        self.body_blog = body_blog
        self.submitted_blog = False


@app.route('/')
@app.route('/blog', methods=['GET', 'POST'])
def main_blog_page():
    blog_id = request.args.get('id')
    blogs = Blog.query.all()
    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template('display_blog.html', blog=blog) 
    return render_template('blog.html', blogs=blogs)
    
@app.route('/add_to_homepage', methods=['GET','POST']) 
def add_to_homepage():
    new_title = request.form['title_blog']
    new_body = request.form['body_blog']
    
    if new_title == "" or new_body == "":
        error_title = "Please fill in the title"
        error_body = "Please fill in the body"
        return redirect("/newpost?error_title=" + error_title + '&error_body=' + error_body )
    
    
    if request.method == 'POST':
        new_title = request.form['title_blog']
        new_body = request.form['body_blog']
        add_content = Blog(new_title, new_body)
        db.session.add(add_content)
        db.session.commit()

        current_id = add_content.id
        return redirect('/blog?id={0}'.format(current_id))
        
        #blog = Blog.query.all()
        #return render_template('/display_blog.html', blog=blog)

@app.route('/newpost', methods=['GET','POST'])
def new_post():
    encoded_error = request.args.get("error_title")
    encoded_error1 = request.args.get("error_body")
    print('****************')
    print(encoded_error1)
    return render_template('/newpost.html', error_title=encoded_error, error_body=encoded_error1)

if __name__ == '__main__':
    app.run()