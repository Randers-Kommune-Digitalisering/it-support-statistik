import os
from dotenv import load_dotenv


# loads .env file, will not overide already set enviroment variables (will do nothing when testing, building and deploying)
load_dotenv()


DEBUG = os.getenv('DEBUG', 'False') in ['True', 'true']
PORT = os.getenv('PORT', '8080')
POD_NAME = os.getenv('POD_NAME', 'pod_name_not_set')

QUEUES = ['IT_Digitalisering_1818']

ZYLINC_URL = os.environ["ZYLINC_URL"].strip()
ZYLINC_REALM = os.environ["ZYLINC_REALM"].strip()
ZYLINC_CLIENT = os.environ["ZYLINC_CLIENT"].strip()
ZYLINC_SECRET = os.environ["ZYLINC_SECRET"].strip()

KEYCLOAK_URL = os.environ["KEYCLOAK_URL"].strip()
KEYCLOAK_REALM = os.environ["KEYCLOAK_REALM"].strip()
KEYCLOAK_CLIENT = os.environ["KEYCLOAK_CLIENT"].strip()
KEYCLOAK_ROLES = ['admin', 'view']
