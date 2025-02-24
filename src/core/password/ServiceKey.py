from core import logger
from core.password.EncryptedData import EncryptedData

from Crypto.Cipher import AES
import os

class ServiceKey :
    def __init__(self, k_service: bytes, service: str|None = None) -> None :
        self.k_service = k_service

        if service == None :
            logger.debug(f"ServiceKey {self} established with no service associate, k_service = {k_service}")
        else :
            logger.debug(f"ServiceKey {self} established with service associate = '{service}', k_service = {k_service}")

    def encrypt_password(self, password: str) -> EncryptedData :
        """Chiffre un mot de passe avec AES-GCM."""
        iv = os.urandom(12)  # IV aléatoire pour AES-GCM
        cipher = AES.new(self.k_service, AES.MODE_GCM, nonce=iv)
        ciphertext, tag = cipher.encrypt_and_digest(password.encode())
        return EncryptedData(iv, ciphertext, tag)  # Concaténation du IV, du texte chiffré et du tag

    def decrypt_password(self, encrypted_data: EncryptedData) -> str:
        """Déchiffre un mot de passe avec AES-GCM."""
        iv = encrypted_data.get_iv()
        ciphertext =encrypted_data.get_ciphertext()
        tag = encrypted_data.get_tag()

        cipher = AES.new(self.k_service, AES.MODE_GCM, nonce=iv)  # Création du déchiffreur
        decrypted_password = cipher.decrypt_and_verify(ciphertext, tag)  # Vérification + déchiffrement

        return decrypted_password.decode()  # Conversion en texte