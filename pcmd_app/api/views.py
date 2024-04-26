from flask import Blueprint,request
from flask_restx import Api,Resource,fields
from pcmd_app.utils.flask_utils import try_login
from pcmd_app.utils.psql import get_user_from_db
from pcmd_app import app
import json
api_blueprint = Blueprint('api', __name__)

api = Api(api_blueprint)


validate_user_input = api.model('validate_user_credential',{
    'email':fields.String(required=True,description="Valid Email ID"),
    'password':fields.String(required=True,description="Valid Password")
})

validate_user_output = api.model('validate_credentials_output',{
    'is_feast_user':fields.Boolean(description='True if User has signed up on Feast'),
    'credentials_valid':fields.Boolean(description='True if Provided credentials were valid'),
    'id':fields.Integer(description="A unique ID provided by DB")
})

@api.route('/get_stats')
class Api_get_stats(Resource):
    def get(self):
        with open(app.config["STATISTICS_JSON"],"r") as f:
            data = json.load(f)
        return data

@api.route('/validate_user')
class Api_validate_user(Resource):
    @api.expect(validate_user_input)
    @api.response(200,'Success',validate_user_output)
    def post(self):
        result_data = {}
        json_data = request.get_json(force=True)
        email = json_data['email']
        password = json_data['password']

        user = get_user_from_db('email',email)
        if user is None:
            result_data["is_feast_user"]=False
            result_data['id']=-1
        else:
            result_data["is_feast_user"]=True
            result_data['id']= user[0]
        try:
            try_login(email,password)
            result_data["credentials_valid"] = True
        except:
            result_data["credentials_valid"] = False
        
        return result_data
            
        
        