from core import logger, MasterKey, Session
from pathlib import Path

def load(location: Path = None) -> Session :

    logger.debug(f"load function called to generate session with location={location}")

    if not location:
        location = Path(input("Choose a location : "))

    # TODO: Verify the integrity of the DB

    logger.info("User need to connect")
    while True :
        pwd = input("Enter password : ")
        k_master = MasterKey(master_password=bytes(pwd, encoding="utf8"), db_location=location/Path("database"))
        if k_master.verify_password() == True :
            break
        else :
            logger.error(f"Send {pwd} who is an incorrect password")
            print("Incorrect password")
    logger.info("Password correct, you can now use others commands !")
    return Session(k_master=k_master, location=location)