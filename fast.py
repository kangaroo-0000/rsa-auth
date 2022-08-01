# load_dotenv一定要在最前
from utils.fast_verify.jwt_method import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, user_db, get_current_active_user, oauth2_scheme
from fast_swagger import *
from routers.router import authorize_app
from utils.fast_verify.jwt_class import Token, User
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status
from datetime import timedelta
import uvicorn
from dotenv import load_dotenv
load_dotenv(".env")
# jwt 驗證
# swagger


app = FastAPI(openapi_tags=tags_metadata)

# jwt verify
# ------------------------------------------ #


@app.post('/token', response_model=Token, tags=["OAuth2 - JWT"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    user = authenticate_user(user_db, username, password)
    if(not user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/user', tags=["OAuth2 - JWT"])
async def read_user(user: User = Depends(get_current_active_user)):
    return user


@app.get('/user/token', tags=["OAuth2 - JWT"])
async def read_token(token: str = Depends(oauth2_scheme)):
    return {"token": token}
# ------------------------------------------ #

app.include_router(authorize_app, dependencies=[
                   Depends(get_current_active_user)])


# if "__main__" == __name__:
#     uvicorn.run(app, host="0.0.0.0", port=8081)
