from flask_wtf import Form
from wtforms import StringField,PasswordField,EmailField
from wtforms import validators,ValidationError

class User():    
    def __init__(self, user):
        self.nick_name   = user[2]
        self.email       = user[1] 
        self.id          = user[0]
        self.is_admin    = user[5]
        self.profile_img = user[4]

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return self.id
    
class LoginForm(Form):
    email = EmailField('email',[validators.DataRequired()])
    password = PasswordField('Password',[validators.DataRequired()])  
    def validate_email(form,field):
        domain = field.data.split("@")
        if not len(domain)==2:
            raise ValidationError('Not a valid Email')
        if not domain[1].lower() == "intel.com":
            raise ValidationError('Only intel Emails are allowed')

class SignupForm(LoginForm):
    nickname = StringField('Nickname',[validators.DataRequired(),validators.Length(min=5,max=15,message="Nickname should be 5-15 character long.")])