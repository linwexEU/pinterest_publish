from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.pinterest import router as router_pp 
from bot.pinterest import router as router_bot_pp

import uvicorn 


app = FastAPI(title="Multi Bot Publisher")

app.include_router(router_bot_pp)
app.include_router(router_pp)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == "__main__": 
    uvicorn.run(app)






