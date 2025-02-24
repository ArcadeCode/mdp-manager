from core import logger

class EncryptedData :
    """
    A class to represent encrypted data.
    Attributes
    ----------
    iv : bytes
        The initialization vector used for encryption.
    ciphertext : bytes
        The encrypted data.
    tag : bytes
        The authentication tag for the encrypted data.
    Methods
    -------
    get_iv() -> bytes:
        Returns the initialization vector.
    get_ciphertext() -> bytes:
        Returns the encrypted data.
    get_tag() -> bytes:
        Returns the authentication tag.
    __str__() -> str:
        Returns a hexadecimal string representation of the concatenated iv, ciphertext, and tag.
    """
    def __init__(self, iv:bytes, ciphertext:bytes, tag:bytes) -> None :
        self.iv = iv
        self.ciphertext = ciphertext
        self.tag = tag
        logger.debug(f"A new EncryptedData {self} initialized, with iv={iv} ({len(iv)} char), ciphertext={ciphertext} ({len(ciphertext)} char), tag={tag} ({len(tag)} char)")
    def get_iv(self) -> bytes:
        return self.iv
    def get_ciphertext(self) -> bytes:
        return self.ciphertext
    def get_tag(self) -> bytes:
        return self.tag
    def __str__(self) -> str :
        return str(self.iv + self.ciphertext + self.tag)
    def __bytes__(self) -> bytes :
        return self.iv + self.ciphertext + self.tag
    
    def logify(self) -> str :
        # Generate logger.debug pre build string
        return f"EncryptedData {self} with iv={self.iv}, ciphertext={self.ciphertext}, tag={self.tag}"
    
    @classmethod
    def from_bytes(cls, raw_data: str, iv_len: int = 12, tag_len: int = 16) :
        if len(raw_data) < iv_len + tag_len:
            raise ValueError("Invalid input length: not enough data for IV and tag.")

        iv = raw_data[:iv_len]
        tag = raw_data[-tag_len:]
        ciphertext = raw_data[iv_len:-tag_len] if tag_len > 0 else raw_data[iv_len:]

        logger.info(f'''
            called from_bytes from {cls} (it's a @classmethod) parameters are :
            raw_data={raw_data}
            iv={iv}
            tag={tag}
            ciphertext={ciphertext}
            returned : EncryptedData(iv, ciphertext, tag)
            ''')

        return EncryptedData(iv, ciphertext, tag)