from fastapi import APIRouter, Response 


router = APIRouter(prefix="/auth/pinterest", tags=["Auth - Pinterest 🅿️"])


@router.post("/", summary="Авторизоваться 📲")
async def render_auth(response: Response, email: str, password: str): 
    response.set_cookie("pinterest_email", email, httponly=True) 
    response.set_cookie("pinterest_psw", password, httponly=True) 
    return {"message": "Данные про аккаунт сохранены!"}


@router.post("/exit/", summary="Выйти с аккаунта 📴")
async def render_exit(response: Response): 
    response.delete_cookie("pinterest_email") 
    response.delete_cookie("pinterest_psw") 
    return {"message": "Данные о аккаунте были удалены!"}