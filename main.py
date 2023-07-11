from fastapi import FastAPI
from database  import models
from database.database import engine
from routers import user,vehicle, booking, photo
from auth  import authentication
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles




app = FastAPI()


app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vehicle.router)
app.include_router(photo.router)
app.include_router(booking.router)


app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],      
    )

app.mount('/images', StaticFiles(directory='images'), name='images')

models.Base.metadata.create_all(engine)