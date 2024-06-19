from fastapi import APIRouter, Request, File, UploadFile
from pinterest.pin_publisher import PinterestPublisher 

from typing import Annotated
import shutil 
import os 


router = APIRouter(prefix="/pinterest", tags=["Publish - Pinterest 🅿️"])


@router.post("/")
async def render_main(request: Request, file_data: Annotated[UploadFile, File], name: str | None = None, description: str | None = None, link: str | None = None): 
    email = request.cookies.get("pinterest_email")
    password = request.cookies.get("pinterest_psw")

    with open(file_data.filename, "wb") as buffer: 
        shutil.copyfileobj(file_data.file, buffer) 

    try: 
        pp = PinterestPublisher()
        try:
            pp.login(email, password)
        except: 
            return {"message": "Неверный ник или пароль пользователя. Или попробуйте очистить куки."}
        pp.upload(name=name, description=description, link=link, video=os.path.abspath(file_data.filename))
        pp.close_browser()
    except Exception as ex: 
        return {"message": f"[ERROR] {ex}"} 
    finally: 
        os.remove(file_data.filename) 

    return {"message": "Пин опубликовано!"}


@router.delete("/cookies/")
async def delete_cookies(request: Request): 
    email = request.cookies.get("pinterest_email")

    try: 
        os.remove(f"pinterest/cookies/{email}_cookies")
    except: 
        return {"message": "Кук нету"} 
    
    return {"message": "Куки были удаленны"}


