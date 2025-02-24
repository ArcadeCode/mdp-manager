from core import logger, Session, PasswordEntry

def add(session: Session, service_name: str, password: str, no_tags: bool = False, tags: list = [], description: str = "") :
    session.verify_master_key()

    # TODO: Propose à l'utilisateur d'ajouter des tags

    k_service = session.k_master.derive_service_key(service_name)
    encrypted_data = k_service.encrypt_password(password)
    pwd = PasswordEntry(encryptedPassword=encrypted_data, service=service_name, tags=tags, description=description)

    session.db.serialize_password(pwd)

    logger.info(f"Password saved :\n{str(pwd)}")