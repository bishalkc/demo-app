from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from os import environ

#### IMPORTS: DB ####
# import app.config.db as db_config
# import databases
# import sqlalchemy
#### IMPORTS: DB ####


#### IMPORTS: Logging ####
# import logging
# from logging.config import dictConfig
# from app.config.log import logging_config
#### IMPORTS: Logging ####


# Initialize API
api = FastAPI()

class Item(BaseModel):
    text: str

# Load & Intialize Logging
# dictConfig(logging_config)
# logger = logging.getLogger('api')
# logger.info("Started Application. Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)")

# DATABASE #
# database = databases.Database(db_config.DB_URL)
# db_engine = sqlalchemy.create_engine(db_config.DB_URL)
# metadata = sqlalchemy.MetaData()
# DATABASE #


# TEMPLATING #
templates = Jinja2Templates(directory="app/html")
# TEMPLATING #



# @api.on_event("startup")
# async def startup():
#     if not database.is_connected:
#         print("INFO:\t  Connecting to Database")
#         await database.connect()
#         print("INFO:\t  Connected to Database")


# @api.on_event("shutdown")
# async def shutdown():
#     if database.is_connected:
#         await database.disconnect()
#         print("INFO:\t  Disconnected from Database")

## VARS ##
ENV_HOSTNAME = environ.get('HOSTNAME')
SECRET_USER = environ.get('SECRET_USER')
SECRET_PASSWORD = environ.get('SECRET_PASSWORD')
SECRET_HOST = environ.get('SECRET_HOST')
SECRET_DBNAME = environ.get('SECRET_DBNAME')
SSM_NAME = environ.get('SSM_NAME')
SSM_ENVIRONMENT = environ.get('SSM_ENVIRONMENT')
SSM_FRAMEWORK = environ.get('SSM_FRAMEWORK')
SSM_API_KEY = environ.get('SSM_API_KEY')
SSM_HASH_KEY = environ.get('SSM_HASH_KEY')
IMAGE_ID = environ.get('IMAGE_ID')

CUSTOM_HEADERS = {"X-App-Header": "demo-app", "Content-Language": "en-US", "Content-Type": "application/json"}
## VARS ##

# @api.api_route("/", methods=["GET", "HEAD"])
# def root():
#     # logger.debug("Addressing request for: /")
#     content = {"app-name": "demo-app"}
#     # logger.info("Sending response for: /")
#     return JSONResponse(content=content, headers=CUSTOM_HEADERS)



@api.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@api.api_route("/private/hostname", methods=["GET", "HEAD"])
def hostname():
    content = {"hostname": ENV_HOSTNAME}
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)


@api.get("/health/liveness")
def liveness():
    content = {"state": "ALIVE"}
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)


@api.get("/health/readiness")
def readiness():
    content = {"state": "READY"}
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)


@api.get("/secrets")
def readiness():
    content = {"SECRET_USER": SECRET_USER, "SECRET_PASSWORD": SECRET_PASSWORD, "SECRET_HOST": SECRET_HOST, "SECRET_DBNAME": SECRET_DBNAME}
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)

@api.get("/ssm")
def readiness():
    content = {"SSM_NAME": SSM_NAME, "SSM_ENVIRONMENT": SSM_ENVIRONMENT, "SSM_FRAMEWORK": SSM_FRAMEWORK, "SSM_API_KEY": SSM_API_KEY, "SSM_HASH_KEY": SSM_HASH_KEY}
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)

@api.get("/id")
def readiness():
    content = {"IMAGE_ID": IMAGE_ID}
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)

@api.post("/publisher")
async def publisher(data: Item):
    content = {"message": f"{data.text}"}
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)
