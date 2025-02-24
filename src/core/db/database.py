from core import logger, PasswordEntry, EncryptedData
from typing import List
import sqlite3

class Database:
    def __init__(self, session):
        self.session = session

        # Register adapters and converters for sqlite3 to handle bytes data has BLOB
        sqlite3.register_adapter(bytes, sqlite3.Binary)
        sqlite3.register_converter("BLOB", bytes)

        db_path = session.location / "database/passwords.db"

        # Connexion persistante à la base de données
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # Création de la table si elle n'existe pas
        self._create_table()

    def _create_table(self):
        with self.conn :
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    primary_key INTEGER PRIMARY KEY AUTOINCREMENT,
                    password BLOB NOT NULL,
                    service TEXT NOT NULL,
                    tags TEXT DEFAULT '',
                    description TEXT DEFAULT ''
                );
            ''')

    def serialize_password(self, entry: PasswordEntry):
        """Stocke un PasswordEntry dans la base de données."""
        logger.info(f"Attempt to serialize a password on the DB {self} with session {self.session}, password = {str(entry)}")
        with self.conn:
            self.cursor.execute('''
                INSERT INTO passwords (password, service, tags, description) 
                VALUES (?, ?, ?, ?);
            ''', (bytes(entry.encryptedPassword), entry.service, str(entry.tags), entry.description))
        logger.debug("New PasswordEntry pushed in the database")
        logger.info(f"Password {entry.encryptedPassword} for service {entry.service} added to the database with tags: {entry.tags} and description: {entry.description}")

    def deserialize_password(self, index: int) -> PasswordEntry:
        """Récupère un PasswordEntry par son index dans la base de données."""
        with self.conn:
            self.cursor.execute('''
                SELECT password, service, tags, description FROM passwords
                LIMIT 1 OFFSET ?;
            ''', (index,))
            row = self.cursor.fetchone()

        if row is None:
            raise IndexError("No password found at the given index.")

        encrypted_password = EncryptedData.from_bytes(raw_data=row[0])

        return PasswordEntry(
            encryptedPassword=encrypted_password,
            service=row[1],
            tags=row[2],
            description=row[3]
        )

    def deserialize_all_passwords(self) -> List[PasswordEntry]:
        """Récupère tous les PasswordEntry de la base de données."""
        with self.conn:
            self.cursor.execute("SELECT password, service, tags, description FROM passwords")
            rows = self.cursor.fetchall()

        passwords = []
        for row in rows:
            encrypted_password = EncryptedData.from_bytes(raw_data=row[0])
            passwords.append(PasswordEntry(
                encryptedPassword=encrypted_password,
                service=row[1],
                tags=row[2],
                description=row[3]
            ))

        return passwords


    def show_password(self) -> str :
        pass
    def show_all_passwords(self) -> str :
        pass

    def close(self):
        """Ferme proprement la connexion à la base de données"""
        if self.conn:
            self.conn.close()
            logger.debug("Database connection ended")

    def __del__(self):
        """Destructeur : Ferme la connexion lorsque l'objet est supprimé"""
        self.close()
        logger.debug(f"Destructor of {self} called")