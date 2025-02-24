from core import logger, Session
from typing import Literal

def show(session: Session, password_index: int|Literal["all"]) -> None:
    if type(password_index) == int :
        result = [session.db.deserialize_password(password_index)]

    elif type(password_index) == str and password_index == "all" :
        result = session.db.deserialize_all_passwords()
    else :
        logger.fatal("password_index invalid type")
        raise ValueError("password_index invalid type")
    
    for password in result :
        k_service = session.k_master.derive_service_key(password.service)
        password_in_clear = k_service.decrypt_password(password.encryptedPassword)
        logger.info(f"{password.__str__(password_in_clear)}\n")

    if len(result) == 0 :
        logger.warning("0 passwords in the DB")
        