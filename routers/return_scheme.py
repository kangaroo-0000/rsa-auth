from lib2to3.pytree import Base
from pydantic import BaseModel
from typing import Optional

from routers.input_scheme import decrypt_data_detail

class BaseResponse(BaseModel):
    status: bool
    detail: Optional[str]

class DecryptResponse(BaseResponse):
    decrypt_message : decrypt_data_detail

class EncryptResponse(BaseResponse):
    encrypt_message : str