# Notes de données
- On utilisera un chiffrement asymétrique (une clé pour le chiffrement sois la clé "de session" et une clé de déchiffrement sois la clé "master")
- Une clé de session est valable pendant 15 minutes maximum.
- La clé Master sera une clé de 512 bits.

### Principe d'ajout d'un mdp
1. On vérifie l'intégrité de la BD.
2. On vérifie l'intégrité de l'objet `PasswordEntry`
3. On chiffre à l'aide de la clé de session.
### Principe de visualisation d'un mdp
1. On vérifie l'intégrité de la BD.
2. On ouvre la BD avec MDP chiffrer
3. L'utilisateur demande l'accès à un MDP dans un `PasswordEntry`
4. DB demande clé Master
5. Déchiffrement avec clé Master

### Fonction nécessaire
- `push_pwd` : Envoyer un objet `PasswordEntry` dans la BD en chiffrant son mdp.
- `pull_pwd` : Retire un objet`PasswordEntry` dans la BD.
- `get_pwd` : Récupérer un objet `PasswordEntry` déchiffrer depuis la BD.
- `generate_strong_pwd` : Génère un mot de passe haute complexité.

- `config_db` : Génère une DB avec un certain niveau de complexité en terme de sécurité. Il demande ces paramètres :
    - `SECURITY_LEVEL` : Niveau de sécurité du système, modifie le niveau de sécurité et augmente drastiquement le temps de calcul pour chiffrer et déchiffrer des entrées de la BD.
        - `LOW` : Préconfigurer pour une sécurité basse, vulnérable aux attaques brutes force mais haute rapidité.
            - `MASTER_PWD_HASH_SIZE` : 128
            - `MASTER_PWD_HASH_ITERATION` : 1000
            - `MASTER_PWD_REGEX_RULES`
            - `MASTER_PWD_SIZE`
            - `SESSION_EXPIRE_TIME` : 15x60
            - `SESSION_PWD_HASH_SIZE`
        - `MEDIUM` : Préconfigurer pour une sécurité standard, pas de vulnérabilité aux attaques brutes forces classiques.
            - `MASTER_PWD_HASH_SIZE` : 256
            - `MASTER_PWD_HASH_ITERATION` : 10000
            - `MASTER_PWD_REGEX_RULES`
            - `MASTER_PWD_SIZE`
            - `SESSION_EXPIRE_TIME` : 15x60
            - `SESSION_PWD_HASH_SIZE`
        - `HIGH` : Préconfigurer pour une sécurité avancée avec protection contre les attaques brutes force à grand hash/s, session courte, prend du temps à exécuter.
            - `MASTER_PWD_HASH_SIZE` : 524
            - `MASTER_PWD_HASH_ITERATION` : 200000
            - `MASTER_PWD_REGEX_RULES`
            - `MASTER_PWD_SIZE`
            - `SESSION_EXPIRE_TIME`
            - `SESSION_PWD_HASH_SIZE`
        - `CUSTOM` : Configuration choisis par l'utilisateur comprenant la personnalisation des paramètres :
            - `MASTER_PWD_HASH_SIZE` : Taille en bits du hash du mot de passe maître.
            - `MASTER_PWD_HASH_ITERATION` : Nombre d'itérations de hachage du mot de passe maître.
            - `MASTER_PWD_REGEX_RULES` : Règles de création du mot de passe maître.
            - `MASTER_PWD_SIZE` : Taille minimal pour le mot de passe maître.
            - `SESSION_EXPIRE_TIME` : Temps en seconde avant que la session sois déconnecter.
            - `SESSION_PWD_HASH_SIZE` : Taille en bits du hash du mdp de session.
    - `USERS_AUTHORIZED` : Tout les utilisateurs autorisé à se connecter à la DB.
    - `MASTER_PWD` : Votre mot de passe maître.
    - `BACKUP_PWD` : Mot de passe de backup souvent générer à partir du phrase : "Quel est le nom de naissance de votre mère ? ...".
    Génère un fichier read only appelé : "config.lock", tout ne peux être modifier dans ce fichier.
- `change_master_pwd` : Change le mot de passe maître.