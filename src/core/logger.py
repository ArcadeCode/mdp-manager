import logging
import colorlog

logger = logging.getLogger('mon_logger') # Créer un logger avec `colorlog`
log_handler = colorlog.StreamHandler() # Créer un handler pour afficher les logs colorés dans la console
# Définir le format des logs avec des couleurs
formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',  # Format du log
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
) 
log_handler.setFormatter(formatter) # Appliquer le format à notre handler
logger.addHandler(log_handler) # Ajouter le handler au logger
logger.setLevel(logging.DEBUG) # Définir le niveau de log
## Tester avec différents niveaux de log
#logger.debug("Ceci est un message de debug")
#logger.info("Ceci est un message d'information")
#logger.warning("Ceci est un message d'avertissement")
#logger.error("Ceci est un message d'erreur")
#logger.critical("Ceci est un message critique")