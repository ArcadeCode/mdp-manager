from core import logger, MasterKey
from pathlib import Path
import os

def init(location: Path = None, force: bool = False):
    logger.info(f"command 'init' with location={location}, force={force}")

    if not location:
        location = Path(input("Choose a location : "))

    if force:
        # If force==true, reinitializing the database
        logger.warning(f"Forcing new initialization of the DB at location {location}")
        salt_file = Path(location / "database/salt.bytes")
        verifier_file = Path(location / "database/verifier.bytes")
        if salt_file.exists():
            os.remove(salt_file)
        else:
            logger.warning(f"{salt_file} does not exist, nothing to remove.")
        if verifier_file.exists():
            os.remove(verifier_file)
        else:
            logger.warning(f"{verifier_file} does not exist, nothing to remove.")
    else:
        if Path(location / "database").exists():
            # If the database already exists
            logger.fatal("Fatal error, attempt to initializing without forcing new initialization on an existing DB.")
            raise FileExistsError(f"Database already exists at location: {location}. Please use another location or use -f=true to force reinitializing.")
        else:
            logger.debug("Initializing new DB")
    
    os.makedirs(location / "database", exist_ok=True)
    
    while True:
        pwd1 = input("Enter password: ")
        pwd2 = input("Confirm password: ")
        if pwd1 == pwd2:
            print("Password confirmed.")
            break
        else:
            print("Passwords do not match. Try again.")

    logger.info("Generating the master key... This can take time, please wait...")
    master_password = bytes(pwd1, encoding="utf8")
    k_master = MasterKey(master_password=master_password, db_location=location/Path("database"))
    logger.debug(f"k_master: {k_master} generated, in {k_master.get_debug_time_derivation()}s")
    k_master.save_password_verifier()
    logger.info("Your master key has been generated!")
    # TODO: Generate TABLEs in SQL
    logger.info(f"Your database has being generated, now load it via this commande : \n$python ./src/main.py -l={location}")