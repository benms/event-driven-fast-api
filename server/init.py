from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import config

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=[config.front_url],
  allow_methods=['*'],
  allow_headers=['*']
)