import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from .jwt_class import UserInDB , User, TokenData
# jwt 過期時間相關設定
from datetime import datetime, timedelta
# 密碼的 Hash 驗證
from passlib.context import CryptContext
# jwt 加解密
from jose import jwt, JWTError

# username: admin
# password: admin123!
user_db = {
    "admin": {
        "username":"admin",
        "hashed_password":"$2b$12$MnsQ2qob7Jqt2r7yT7WLWuRIjdSc94JU7duDcLIRWNfHYBcMcN6Oa",
        "email":"admin@gmail.com"
    }
}

load_dotenv(".env")

# 加密密鑰
SECRET_KEY = os.getenv("SECRET_KEY")
# jwt加密演算法
ALGORITHM = os.getenv("ALGORITHM")
# 過期時間
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# 指定 API 使用的 OAuth 認證方式 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 指定加密方式
pwd_handler = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash_password(password: str)-> str:
    return pwd_handler.hash(password)

def verify_password(oringin_password,hashed_password):
    return pwd_handler.verify(oringin_password,hashed_password)

def get_user(db, username:str):
    # 檢查使用者存在與否
    if username in db:
        # 使用 key 找尋對應資料
        user_dict = db[username]
        # 回傳帶有密碼的 使用者資料
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
    # 1.在資料庫尋找用戶
    user = get_user(db, username)
    if(not user):
        # 2.用戶不存在
        return False
    if(not verify_password(password, user.hashed_password)):
        # 3.密碼錯誤
        return False
    return user

# 用戶通過驗證，生成 token
def create_access_token(data:dict,
                        expires_delta: Optional[timedelta] = None):
    # 另產生一個 dict data
    to_encode = data.copy()
    if expires_delta:
        # 有指定則使用指定時間
        expire = datetime.utcnow() + expires_delta
    else:
        # 無指定則延長 15 分鐘
        expire = datetime.utcnow() + timedelta(minutes=15)
    # 新增過期相關資訊
    to_encode.update({"exp":expire})
    # 加密 jwt 資訊
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if(not username):
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(user_db, username=token_data.username)
    if(not user):
        raise credentials_exception
    return user

# 可以在 User 新增值（user.disabled）來判斷是否屬於活躍用戶
def get_current_active_user(user: User = Depends(get_current_user)):
    return user

