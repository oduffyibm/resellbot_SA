# Custom extension for IBM Watson Assistant which provides a
# REST API around a single database table (coverages).
#
# The code demonstrates how a simple REST API can be developed and
# then deployed as serverless app to IBM Cloud Code Engine.
#
# See the README and related tutorial for details.
#
# Written by Henrik Loeser (data-henrik), hloeser@de.ibm.com
# (C) 2022 by IBM

import os
import ast
import urllib.parse
from dotenv import load_dotenv
from apiflask import APIFlask, Schema, HTTPTokenAuth, PaginationSchema, pagination_builder, abort
from apiflask.fields import Integer, String, Boolean, Date, List, Nested
from apiflask.validators import Length, Range
# Database access using SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Set how this API should be titled and the current version
API_TITLE='coverages API for Watson Assistant'
API_VERSION='1.0.0'

# create the app
app = APIFlask(__name__, title=API_TITLE, version=API_VERSION)

# load .env if present
load_dotenv()

# the secret API key, plus we need a username in that record
API_TOKEN="{{'{0}':'appuser'}}".format(os.getenv('API_TOKEN'))
#convert to dict:
tokens=ast.literal_eval(API_TOKEN)

# database URI
DB2_URI=os.getenv('DB2_URI')
# optional table arguments, e.g., to set another table schema
ENV_TABLE_ARGS=os.getenv('TABLE_ARGS')
TABLE_ARGS=None
if ENV_TABLE_ARGS:
    TABLE_ARGS=ast.literal_eval(ENV_TABLE_ARGS)


# specify a generic SERVERS scheme for OpenAPI to allow both local testing
# and deployment on Code Engine with configuration within Watson Assistant
app.config['SERVERS'] = [
    {
        'description': 'Code Engine deployment',
        'url': 'https://{appname}.{projectid}.{region}.codeengine.appdomain.cloud',
        'variables':
        {
            "appname":
            {
                "default": "myapp",
                "description": "application name"
            },
            "projectid":
            {
                "default": "projectid",
                "description": "the Code Engine project ID"
            },
            "region":
            {
                "default": "us-south",
                "description": "the deployment region, e.g., us-south"
            }
        }
    },
    {
        'description': 'local test',
        'url': 'http://127.0.0.1:{port}',
        'variables':
        {
            'port':
            {
                'default': "5000",
                'description': 'local port to use'
            }
        }
    }
]


# set how we want the authentication API key to be passed
auth=HTTPTokenAuth(scheme='ApiKey', header='API_TOKEN')

# configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI']=DB2_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize SQLAlchemy for our database
db = SQLAlchemy(app)


# sample records to be inserted after table recreation
sample_coverages=[
    {
	"country":"Sample",
	"shortname":"Sample",
        "ceid":"Sample",
        "bpsstor":"Sample",
        "bpspow":"Sample",
	"crossbpssof":"Sample",
    	"crossbpsdaa":"Sample",
	"bpsdaa":"Sample",
        "bpsauto":"Sample",
        "bpssus":"Sample",
        "bpssec":"Sample",
	"bpscloud":"Sample",
    	"ptsstor":"Sample",
	"ptspow":"Sample",
	"crosspts":"Sample",
        "crossptsdaa":"Sample",
        "ptsdaa":"Sample",
        "ptsauto":"Sample",
	"ptssus":"Sample",
	"ptssec":"Sample",
        "ptscloud":"Sample",
        "covered":"Sample"
    },
    {
	"country":"Demonstration",
	"shortname":"Demonstration",
        "ceid":"Demonstration",
        "bpsstor":"Demonstration",
        "bpspow":"Demonstration",
	"crossbpssof":"Demonstration",
    	"crossbpsdaa":"Demonstration",
	"bpsdaa":"Demonstration",
        "bpsauto":"Demonstration",
        "bpssus":"Demonstration",
        "bpssec":"Demonstration",
	"bpscloud":"Demonstration",
    	"ptsstor":"Demonstration",
	"ptspow":"Demonstration",
	"crosspts":"Demonstration",
        "crossptsdaa":"Demonstration",
        "ptsdaa":"Demonstration",
        "ptsauto":"Demonstration",
	"ptssus":"Demonstration",
	"ptssec":"Demonstration",
        "ptscloud":"Demonstration",
        "covered":"Demonstration"
    },

]


# Schema for table “coverages"
# Set default schema to "coverages"
class CoverageModel(db.Model):
    __tablename__ = 'coverages'
    __table_args__ = TABLE_ARGS
    index = db.Column('INDEX',db.Integer, primary_key=True)
    country = db.Column('COUNTRY',db.String(255))
    shortname = db.Column('SHORTNAME',db.String(255))
    ceid = db.Column('CEID',db.String(255))
    bpsstor = db.Column('BPSSTOR',db.String(255))
    bpspow = db.Column('BPSPOW',db.String(255))
    crossbpssof = db.Column('CROSSBPSSOF',db.String(255))
    crossbpsdaa = db.Column('CROSSBPSDAA',db.String(255))
    bpsdaa = db.Column('BPSDAA',db.String(255))
    bpsauto = db.Column('BPSAUTO',db.String(255))
    bpssus = db.Column('BPSSUS',db.String(255))
    bpssec = db.Column('BPSSEC',db.String(255))
    bpscloud = db.Column('BPSCLOUD',db.String(255))
    ptsstor = db.Column('PTSSTOR',db.String(255))
    ptspow = db.Column('PTSPOW',db.String(255))
    crosspts = db.Column('CROSSPTS',db.String(255))
    crossptsdaa = db.Column('CROSSPTSDAA',db.String(255))
    ptsdaa = db.Column('PTSDAA',db.String(255))
    ptsauto = db.Column('PTSAUTO',db.String(255))
    ptssus = db.Column('PTSSUS',db.String(255))
    ptssec = db.Column('PTSSEC',db.String(255))
    ptscloud = db.Column('PTSCLOUD',db.String(255))
    covered = db.Column('COVERED',db.String(255))
    
    


# the Python output for Coverages
class CoverageOutSchema(Schema):
    index = Integer()
    country = String()
    shortname = String()
    ceid = String()
    bpsstor = String()
    bpspow = String()
    crossbpssof = String()
    crossbpsdaa = String()
    bpsdaa = String()
    bpsauto = String()
    bpssus = String()
    bpssec = String()
    bpscloud = String()
    ptsstor = String()
    ptspow = String()
    crosspts = String()
    crossptsdaa = String()
    ptsdaa = String()
    ptsauto = String()
    ptssus = String()
    ptssec = String()
    ptscloud = String()
    covered = String()


# the Python input for coverages
class CoverageInSchema(Schema):
    country = String(required=True, validate=Length(0, 255))
    shortname = String(required=True, validate=Length(0, 255))
    ceid = String(required=True, validate=Length(0, 255))
    bpsstor = String(required=True, validate=Length(0, 255))
    bpspow = String(required=True, validate=Length(0, 255))
    crossbpssof = String(required=True, validate=Length(0, 255))
    crossbpsdaa = String(required=True, validate=Length(0, 255))
    bpsdaa = String(required=True, validate=Length(0, 255))
    bpsauto = String(required=True, validate=Length(0, 255))
    bpssus = String(required=True, validate=Length(0, 255))
    bpssec = String(required=True, validate=Length(0, 255))
    bpscloud = String(required=True, validate=Length(0, 255))
    ptsstor = String(required=True, validate=Length(0, 255))
    ptspow = String(required=True, validate=Length(0, 255))
    crosspts = String(required=True, validate=Length(0, 255))
    crossptsdaa = String(required=True, validate=Length(0, 255))
    ptsdaa = String(required=True, validate=Length(0, 255))
    ptsauto = String(required=True, validate=Length(0, 255))
    ptssus = String(required=True, validate=Length(0, 255))
    ptssec = String(required=True, validate=Length(0, 255))
    ptscloud = String(required=True, validate=Length(0, 255))
    covered = String(required=True, validate=Length(0, 255))
    

# use with pagination
class CoverageQuerySchema(Schema):
    page = Integer(load_default=1)
    per_page = Integer(load_default=20, validate=Range(max=255))

class CoveragesOutSchema(Schema):
    coverages = List(Nested(CoverageOutSchema))
    pagination = Nested(PaginationSchema)

# register a callback to verify the token
@auth.verify_token  
def verify_token(token):
    if token in tokens:
        return tokens[token]
    else:
        return None

# retrieve a single coverage record by CEID
@app.get('/coverages/ceid/<string:ceid>')
@app.output(CoverageOutSchema)
@app.auth_required(auth)
def get_coverage_ceid(ceid):
    """Coverage record by CEID
    Retrieve a single coverage record by its CEID
    """
    search="%{}%".format(ceid)
    return CoverageModel.query.filter(CoverageModel.ceid.ilike(search)).first()

# retrieve a single coverage record by name
@app.get('/coverages/name/<string:short_name>')
@app.output(CoverageOutSchema)
@app.auth_required(auth)
def get_coverage_name(short_name):
    """Coverage record by name
    Retrieve a single coverage record by its short name
    """
    search="%{}%".format(short_name.replace("+","_"))
#    new_search=search.replace("+","%20")
#    fnew_search=new_search.format(short_name)
#    encoded_search=urllib.parse.quote(search).format(short_name)
    return CoverageModel.query.filter(CoverageModel.shortname.ilike(search)).first()


# get all coverages
@app.get('/coverages')
@app.input(CoverageQuerySchema, 'query')
#@app.input(CoverageInSchema(partial=True), location='query')
@app.output(CoveragesOutSchema)
@app.auth_required(auth)
def get_coverages(query):
    """all coverages
    Retrieve all coverage records
    """
    pagination = CoverageModel.query.paginate(
        page=query['page'],
        per_page=query['per_page']
    )
    return {
        'coverages': pagination.items,
        'pagination': pagination_builder(pagination)
    }

# create a coverage record
@app.post('/coverages')
@app.input(CoverageInSchema, location='json')
@app.output(CoverageOutSchema, 201)
@app.auth_required(auth)
def create_coverage(data):
    """Insert a new coverage record
    Insert a new coverage record with the given attributes. Its new CEID is returned.
    """
    coverage = CoverageModel(**data)
    db.session.add(coverage)
    db.session.commit()
    return coverage


# delete a coverage record
@app.delete('/coverages/ceid/<int:ceid>')
@app.output({}, 204)
@app.auth_required(auth)
def delete_coverage(ceid):
    """Delete a coverage record by ceid
    Delete a single coverage record identified by its ceid.
    """
    coverage = CoverageModel.query.get_or_404(ceid)
    db.session.delete(coverage)
    db.session.commit()
    return ''

# (re-)create the coverage table with sample records
@app.post('/database/recreate')
@app.input({'confirmation': Boolean(load_default=False)}, location='query')
#@app.output({}, 201)
@app.auth_required(auth)
def create_database(query):
    """Recreate the database schema
    Recreate the database schema and insert sample data.
    Request must be confirmed by passing query parameter.
    """
    if query['confirmation'] is True:
        db.drop_all()
        db.create_all()
        for e in sample_coverages:
            coverage = CoverageModel(**e)
            db.session.add(coverage)
        db.session.commit()
    else:
        abort(400, message='confirmation is missing',
            detail={"error":"check the API for how to confirm"})
        return {"message": "error: confirmation is missing"}
    return {"message":"database recreated"}


# default "homepage", also needed for health check by Code Engine
@app.get('/')
def print_default():
    """ Greeting
    health check
    """
    # returning a dict equals to use jsonify()
    return {'message': 'This is the South America Coverage API server'}


# Start the actual app
# Get the PORT from environment or use the default
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=int(port))
