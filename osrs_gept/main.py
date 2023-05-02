from fastapi import FastAPI

from osrs_gept.bootstrap import init_app


app = FastAPI()
init_app(app)
