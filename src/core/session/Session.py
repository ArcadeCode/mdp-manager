from core import logger
from core.password.MasterKey import MasterKey

from pathlib import Path

class Session :
    def __init__(self, k_master: MasterKey, location: Path) -> None :
        self.k_master = k_master
        self.location = location

        from core.db.database import Database
        self.db = Database(session=self)

    def get_master_key(self) -> MasterKey :
        return self.k_master
    
    def verify_master_key(self) -> bool :
        result = self.k_master.verify_password()
        if result == False :
            logger.error(f"{self.k_master} invalid password")
            raise Exception("invalid k_master")
        else :
            logger.debug(f"Verifying {self.k_master} validated ")
        return result 