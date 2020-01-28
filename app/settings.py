import os

PORT = 8888
DOMAIN = 'localhost'
PROTOCOL = 'http'
STATIC_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/templates'
