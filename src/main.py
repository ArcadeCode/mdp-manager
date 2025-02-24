from core import logger
from cli import init, load, add, show
import argparse
from pathlib import Path

def index_type(value):
    if value == "all":
        return value
    try:
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid index: {value}. Must be an integer or 'all'.")

def make_debug_db(location: Path|None):
    """Creates a debug database with predefined entries."""
    from uuid import uuid4
    from os import getcwd
    from random import randint

    import secrets
    import string
    def generate_secure_password(length=64):
        """Génère un mot de passe sécurisé avec une longueur donnée."""
        alphabet = string.ascii_letters + string.digits + string.punctuation + " "  # Lettres, chiffres, symboles et espace
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password

    if location == None :
        location = Path(getcwd()+"/debug/"+str(uuid4()))

    logger.info(f"Creating debug database at {location}")
    init(location, force=True)
    session = load(location)
    for i in range(40):
        add(session, 
            password=generate_secure_password(16), 
            service_name=f"test_service_{i}", 
            description="",
            no_tags=bool(randint(0, 1))
        )
    logger.info("Debug database created successfully.")
    logger.info(f"Path to DB : {location}")

def main():
    parser = argparse.ArgumentParser(description="Script accepting various password manager commands.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Command load with location option
    load_parser = subparsers.add_parser("load", help="Load data")
    load_parser.add_argument("-l", "--location", help="Specify the location to load data from")
    
    # Command init with location option
    init_parser = subparsers.add_parser("init", help="Create a new password manager DB")
    init_parser.add_argument("-l", "--location", help="Specify the location for the new entry")
    init_parser.add_argument("-f", "--force", help="Force the reinitialization of the DB")

    # Command add
    add_parser = subparsers.add_parser("add", help="Add a new password to the database")
    add_parser.add_argument("password", help="Password to store")
    add_parser.add_argument("-s", "--service", type=str, required=True, help="Service name")
    add_parser.add_argument("--description", type=str, default="", help="Description (optional)")
    add_parser.add_argument("--no-tags", action="store_true", help="Disable tags for this entry")
    add_parser.add_argument("-l", "--location", help="Specify the location of the database")
    
    # Command show
    show_parser = subparsers.add_parser("show", help="Show one or more passwords from the DB")
    show_parser.add_argument("-l", "--location", help="Specify the location of the database")
    show_parser.add_argument("-i", "--index", type=index_type, default="all", help="Show one or more passwords")
    
    # Command make-debug-db
    debug_parser = subparsers.add_parser("make-debug-db", help="Create a debug database with predefined entries")
    debug_parser.add_argument("-l", "--location", required=False, default=None, help="Specify the location for the debug database")
    
    args = parser.parse_args()
    
    if args.command == "load":
        logger.info(f"command 'load' with location={args.location}")
        load(Path(args.location) if args.location else None)
    elif args.command == "init":
        logger.info(f"command 'init' with location={args.location}, force={args.force}")
        init(Path(args.location) if args.location else None, force=args.force)
    elif args.command == "add":
        logger.info(f"command 'add' with location={args.location}, password={'*' * len(args.password)}, service_name={args.service}, description={args.description}, no_tags={args.no_tags}")
        session = load(Path(args.location) if args.location else None)
        add(session=session, password=args.password, service_name=args.service, description=args.description, no_tags=args.no_tags)
    elif args.command == "show":
        logger.info(f"command 'show' with location={args.location}, password_index={args.index}")
        session = load(Path(args.location) if args.location else None)
        show(session=session, password_index=args.index)
    elif args.command == "make-debug-db":
        logger.info(f"command 'make-debug-db' with location={args.location}")
        make_debug_db(Path(args.location) if args.location else None)

if __name__ == "__main__":
    main()
