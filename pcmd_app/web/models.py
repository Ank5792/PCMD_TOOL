from flask_wtf import Form
from wtforms import StringField,SelectField,EmailField,TextAreaField
from wtforms import validators,ValidationError

class NewProject(Form):
    owner = EmailField('email',[validators.DataRequired()])
    short_description = StringField('short_description',[validators.DataRequired()])  
    description = TextAreaField('description',[validators.DataRequired()])  
    tool_name = StringField('tool_name',[validators.DataRequired()]) 
    current_status  = SelectField('current_status',choices=[('','Please Select an option'),('web_dev','Web-Based, no link'),('web_prod','Web-Based with link'),('off_dev','Offline tool (no download link availble)'),('off_prod','Offline tool (link to download)')],validators=[validators.DataRequired()]) 
    working_links = StringField('working_links') 
    banner_img = StringField('banner_img') 
    jira_link = StringField('jira_link') 
    ags_link = StringField('ags_link') 
    wiki_link = StringField('wiki_link') 
    current_devs = StringField('current_devs',[validators.DataRequired()]) 
    
    def validate_owner(form,field):
        domain = field.data.split("@")
        if not len(domain)==2:
            raise ValidationError('Not a valid Email')
        if not domain[1].lower() == "intel.com":
            raise ValidationError('Only intel Emails are allowed')
    
