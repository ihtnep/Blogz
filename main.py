from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

#@app.route('/newpost', methods=['GET', 'POST'])

@app.route('/', methods=['GET'])
def index():
    #if request.method == 'POST':
        #title = request.form['title']
        #body = request.form['body']
        #new_blog = Blog(blog_name)
        #db.session.add(new_blog)
        #db.session.commit()

    #blogs = Title.query.filter_by(completed=False).all()
    #completed_titles = Task.query.filter_by(completed=True).all()
    #return render_template('blogentry.html',title="Build-A-Blog", 
        #Blogs=blogs)
    if request.args:
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)
        
        #return render_template('blogentry.html', blog=blog)
        return render_template('blogpost.html', blog=blog)

    else:
        blogs = Blog.query.all()

        # return render_template('blogpost.html', title="Build-A-Blog", blogs=blogs)
        return render_template('bloglist.html', title="Build-A-Blog", blogs=blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    if request.method =='GET':
        blogs = Blog.query.all()

        return render_template('blogentry.html', title="Blog Entry", blogs=blogs)
    if request.method =='POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error=""
        body_error=""
        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            query_param_url = "/newpost?id=" + str(new_blog.id)
            blog_id = request.args.get("id")
            #blog = Blog.query.get(blog_id)
            return redirect(query_param_url)
            #return render_template("blogpost.html", blog=blog)
        else:
            return render_template('blogentry.html', title = "Blog Entry", title_error = title_error, body_error = body_error)
    
if __name__ == '__main__':
    app.run()