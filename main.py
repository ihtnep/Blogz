from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:123456@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'
class User(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.before_request
def require_login():
    allowed_routes = ['login', 'sign_up', 'index', 'blog', 'singleuser']
    #print('\n' *10)
    #print(request.endpoint)
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template ("index.html", title="blog users!", users=users)

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method =="GET":
        return render_template ("signup.html", title="signup")
    if request.method =="POST":

        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']


        # username = escape(username)
        # password = escape(password)
        # verify = escape(verify)
        

        username_error = ""
        password_error = ""
        verify_error = ""
        



        if username == "" or " " in username or len(username) < 3 or len(username) > 20: 
            username_error = "Invalid username"
        
        if password == "" or " " in password or len(password) < 3 or len(password) > 20: 
            password_error = "Invalid password"
        
        if verify == "" or verify != password:
            verify_error = "Invalid verification"
        
        if username_error == "" and verify_error == "" and password_error == "":
            existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return render_template ("index.html", username = username)
        else:
            return render_template("signup.html", username_error = username_error
                                            , password_error = password_error    
                                            , verify_error = verify_error
                                            , username = username)
                                
#@app.route('/newpost', methods=['GET', 'POST'])



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/blog', methods=['GET'])
def blog():
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
        blog_id = request.args.get(id)
        blog = Blog.query.get(blog_id)
        
        #return render_template('blogentry.html', blog=blog)
        return render_template('blogpost.html', blog=blog)

    else:
        blogs = Blog.query.all()

        # return render_template('blogpost.html', title="Build-A-Blog", blogs=blogs)
        return render_template('bloglist.html', title="Blogz", blogs=blogs)

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
@app.route('/logout', methods=['GET'])
def logout():
    #session['username']=""
    del session["username"]

    return render_template('index.html', title="Blogz")   
@app.route('/singleuser', methods=['GET'])
def singleuser():
    #id = request.args.get("user")
    #user = request.args.get("id")
    print('hello')
    print('2')
    print(request.args.get("username"))
    if request.args.get("username"):
        username = request.args.get("username")
        user = User.query.filter_by(username=username).first()
       # blogs = Blog.query.filter_by(owner=user.id).all()
        return render_template('singleuser.html', blogs=user.blogs)
    #completed_tasks = Task.query.filter_by(completed=True,owner=owner).all()
    return render_template('singleuser.html', title = "Blog List", id=id)
if __name__ == '__main__':
    app.run()