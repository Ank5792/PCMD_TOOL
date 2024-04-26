from flask import (request,render_template,flash, redirect, url_for,Blueprint,g)
from flask_login import (current_user,login_user,logout_user,login_required)
from pcmd_app import login_manager
from pcmd_app.auth.models import User,LoginForm,SignupForm
from pcmd_app.utils.psql import insert_new_user,get_user_from_db
from pcmd_app.utils.flask_utils import try_login,rsa_decrypt


auth = Blueprint('auth', __name__)
@login_manager.user_loader
def load_user(id):
    user = get_user_from_db('id',id)
    return User(user)

@auth.before_request
def get_current_user():
    g.user = current_user

@auth.route('/signup', methods = ['GET','POST'])
def signup():
    if current_user.is_authenticated:
        flash('You are already logged in.','info')
        return redirect(url_for('web.home'))
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        email = request.form['email'].lower()
        password = request.form['password']
        password=rsa_decrypt(password)
        nickname = request.form['nickname']
        try:
            try_login(email,password)
        except:
            flash('Invalid email or password. Please try again.','danger')
            return redirect(url_for("auth.signup"))
        
        if get_user_from_db('email',email) is not None:
            flash("You have already signed-up. Please log-in here","danger")
            return redirect(url_for("auth.login"))
        else:
            insert_suc = insert_new_user(email,nickname)
            if insert_suc:
                flash("Successfully signed-up. Please Login here...","success")
                return redirect(url_for("auth.login"))

    return render_template('signup.html',form=form)



@auth.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.','info')
        return redirect(url_for('web.home'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = str(request.form['email']).lower()
        password = request.form['password']
        password=rsa_decrypt(password)
        user = get_user_from_db('email',email)
        if user is None:
            #insert_suc = insert_new_user(email,"New User")
            insert_suc = insert_new_user(email, str(email.split(".")[0]))
            if insert_suc:
                flash("Welcome to FEAST!!!","success")
                user = get_user_from_db('email',email)
        try:
            try_login(email,password)
        except:
            flash('Invalid email or password. Please try again.','danger')
            return render_template('login.html', form=form)        
        login_user(User(user))
        return redirect(url_for('web.home'))
    return render_template('login.html', form=form)
        
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))