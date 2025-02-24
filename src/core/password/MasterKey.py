import argon2.low_level as argon2
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import HKDF

import os
from time import time
from pathlib import Path

from core import logger
from core.password.ServiceKey import ServiceKey

currentDir = Path(__file__).resolve().parent

class MasterKey :
    def __init__(self, master_password: bytes, db_location: Path = currentDir):
        logger.debug("New MasterKey called")
        self.debug_time_derivation = None
        self.__master_password = master_password        # master password in clear
        #self.__dbLocation = db_location
        self.__saltLocation = db_location/Path("salt.bytes") # Store in .bytes because the salt in manipulate has bytes all along.
        self.__verifierLocation = db_location/Path("verifier.bytes")
        self.__salt = self.load_salt()                  # Salt used to generate master key
        self.K_master = self.derive_master_key()        # The master key

        del self.__master_password # We not need it anymore and it's risked to save it on memory

    def derive_master_key(self) -> bytes:
        """Dérive la clé principale K_master (32 bytes pour AES-256) avec Argon2."""
        logger.debug("Deriving the master key...")
        t = time()

        derived_K_master = argon2.hash_secret_raw(
            secret=self.__master_password,
            salt=self.__salt,
            time_cost=24,      # Nombre d'itérations
            memory_cost=65536*4,    # Mémoire utilisée en KB (64x4 MiB)
            parallelism=os.cpu_count(),  # Nombre de threads utilisés
            hash_len=32,          # Longueur de la clé en bytes
            type=argon2.Type.ID   # Mode Argon2id recommandé
        )

        self.debug_time_derivation = time() - t
        return derived_K_master
    
    def derive_service_key(self, service_name: str) -> ServiceKey:
        """Dérive une clé unique pour un service donné."""
        k_service = HKDF(
            master=self.K_master,  # Clé maître
            key_len=32,  # 256 bits (adapté pour AES-256)
            salt=None,  # Optionnel, peut être spécifique au service
            hashmod=SHA256,
            context=service_name.encode()  # Différent pour chaque service
        )
    
        return ServiceKey(k_service=k_service, service=service_name)

    def load_salt(self) -> bytes :
        '''Charge le sel depuis le fichier adéquats'''
        logger.debug("Trying to load MasterKey salt")
        if not self.__saltLocation.is_file() :
            logger.debug("There is no salt, generating one...")
            # Génération d'un sel unique
            salt_master: bytes = os.urandom(512)
            logger.debug(f"Random salt generate : {salt_master}")
            # Stockage dans un endroit sécurisé
            with open(self.__saltLocation, "wb") as f :
                logger.debug(f"Writing new salt in {self.__saltLocation.absolute()}")
                f.write(salt_master)
        else :
            logger.debug("There is one salt already generated, loading...")
            # Sel déjà généré, chargement du sel
            with open(self.__saltLocation, "rb") as f :
                salt_master = f.read()
            logger.debug(f"Master key salt loaded : {str(salt_master)[:30]+" [...]"}")

        return salt_master
        
    def save_password_verifier(self, word: str = "Nikita") : # Nikita is the name of one of my cats ^^
        derived_key = self.derive_service_key(word)
        logger.debug(f"Verifier word : {word} derived has : {derived_key}")
        with open(self.__verifierLocation, "wb") as f :
            logger.debug(f"Writing new verifier in {self.__verifierLocation.absolute()}")
            f.write(derived_key.k_service)
        logger.debug("Verifier derived word was saved")

    def load_password_verifier(self) -> bytes:
        """Charge le mot de passe vérificateur à partir du fichier spécifié."""
        logger.debug(f"Loading verifier from {self.__verifierLocation.absolute()}")
        
        if not Path(self.__verifierLocation).is_file():
            logger.error("Verifier file not found!")
            raise FileNotFoundError(f"Verifier file not found at location: {self.__verifierLocation.absolute()}")
        
        with open(self.__verifierLocation, "rb") as f:
            verifier_word = f.read()
            logger.debug(f"Verifier loaded: {verifier_word.hex()}")
        
        return verifier_word
    def verify_password(self, word: str = "Nikita") -> bool:
        """Vérifie si le mot de passe correspond au mot de passe maître dérivé."""
        logger.debug("Verifying password...")

        # Charger le mot de passe vérificateur
        saved_verifier = self.load_password_verifier() # 1. Loading the good derived word verifier
        derived_word= self.derive_service_key(word).k_service   # 2. Derived with the current K_master the word verifier
        is_verified = saved_verifier == derived_word   # 3. Compare the good derived word verifier with the current one
        
        if is_verified:
            logger.debug("Password is correct.")
        else:
            logger.warning("Password is incorrect.")
        
        return is_verified


    def get_k_master(self) -> bytes :
        return self.K_master
    
    def haveStoredSalt(self) -> bool :
        return self.__saltLocation.is_file()
    
    def get_debug_time_derivation(self) -> float :
        return self.debug_time_derivation