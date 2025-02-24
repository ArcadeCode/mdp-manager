from core import logger, ServiceKey, EncryptedData

class PasswordEntry :
    def __init__(self, encryptedPassword: EncryptedData, service: str, tags: list = [], description: str|None = None) -> None :
        self.encryptedPassword = encryptedPassword
        self.service = service
        self.tags = tags
        self.description = description
        self.dbID = None # Primary ID from the database

    def __str__(self, password: str = None) -> str :
        response = []
        response += "=== PasswordEntry ===\n"
        response += f"Service : {self.service}\n"
        response += f"Password (encrypted) : {self.encryptedPassword}\n"
        if password != None :
            response += f"Password : {password}\n"
        response += f"Description : {self.description}\n"
    
        response = "".join(response)

        for tag in self.tags : response += str(tag)

        return response
    
    def logify(self) -> str :
        # Generate logger.debug pre build string
        return f"PasswordEntry {self} with EncryptedData : {self.encryptedPassword.logify()}"