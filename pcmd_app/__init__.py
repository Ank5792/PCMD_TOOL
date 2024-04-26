from flask import Flask
from flask_login import LoginManager

app = Flask(__name__,instance_relative_config=True)
app.config.from_pyfile("app_configs.py")
#app.config['SQLALCHEMY_database_URI'] = 'postgresql://postgres:sonalnirmal@localhost/feast_db'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = "Please Log-in with your Intel Credentials before using the service."
login_manager.login_message_category = "danger"

from pcmd_app.auth.views import auth
app.register_blueprint(auth)
from pcmd_app.web.views import web
app.register_blueprint(web)
from pcmd_app.api.views import api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')