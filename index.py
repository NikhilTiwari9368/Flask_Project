from flask import Flask, render_template, request, redirect, url_for, session , flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your-secret-key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'DELL12'
app.config['MYSQL_DB'] = 'flask_users'

mysql = MySQL(app)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/blog-single')
def blog_single():
    return render_template('blog-single.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/next')
def next():
    return render_template('next.html')

@app.route('/leadership')
def leadership():
    return render_template('leadership.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            session['username'] = username
            return redirect(url_for('next'))
        else:
            flash("Invalid username or password!", 'error')
    
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        if user:
            return "Username already exists!"
        
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
