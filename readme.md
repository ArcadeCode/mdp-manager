# 🔒 MDP Manager - Encrypted SQLite Database for Passwords
MDP Manager is a secure password manager that stores passwords in an encrypted SQLite database. It is written in Python and leverages **Argon2ID**, **AES-256**, and **HKDF** for encryption and key derivation.  
Currently, the database is accessible only via a **CLI application**, but a **GUI version is planned for the future**.

## 📌 Features
- 🔐 **AES-256 encrypted SQLite database**
- 📂 **Local password storage**, without reliance on third-party services
- 🛠 **Password management via a Python CLI app**


## How are the files stored ? 
- A `database/` folder is created in the chosen location on your system. Inside this folder, you will find several files:  
- `passwords.db`: The file containing all encrypted passwords, stored within the database itself, which is encrypted using the master password.  
- `salt.bytes`: The file storing the salt for the master password. **NEVER DELETE THIS FILE, OR YOU WILL LOSE YOUR MASTER PASSWORD AND ALL STORED PASSWORDS IN THE DATABASE.**  
- `verifier.bytes`: The file storing the result of a derivation with the master password. If the derivation fails, it means the password is incorrect.

## 🚀 Installation
### Copie depuis github
Cloner le repo :
```sh
git clone https://github.com/ArcadeCode/mdp-manager.git
cd ./mdp-manager/
```
### Install Dependencies
To install the required dependencies, simply run:
```sh
pip install requirement.txt
```

### Build a database
To initialize a database run :
```sh
python ./src/main.py init --location="insert the location" 
```
You will be invited to create a master password.

### Add a password
To add a password run :
```sh
python ./src/main.py add "password"  --location="insert the location" --service="service linked to the password has string"
# Exemple :
python ./src/main.py add "SuperPassword" --location="C://myDatabase/" --service="chess.com"
```

### Show one or all your passwords :
```sh
# Get the 45 registered password
python ./src/main.py show -l="insert the location" -i=45
# Get all password in the database
python ./src/main.py show -l="insert the location" -i="all"
```

## 📝 To-do
### 🔧 Need to be implemented
- [ ] Adding `del` function to delete password entry in the database.
- [ ] Finish the development of the tagging system for password entries.
- [ ] Add `run.sh` and `run.bat` files to make accessing code more simple.
- [ ] Add unit-tests to test commands and Class.

### ✨ To enhance experience
- [ ] Adding GUI system
- [ ] Upgrade CLI experience using rich print
- [ ] Adapt this project to poetry manager

## Licence :
- [Under GPL-3 licence](./licence.md)