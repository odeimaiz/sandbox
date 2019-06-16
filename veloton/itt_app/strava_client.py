import os
from six.moves.configparser import ConfigParser

from stravalib.client import Client


def create_client():
	cwd = os.getcwd()
	CFG_FILE = os.path.join(cwd, 'config.ini')

	if not os.path.exists(CFG_FILE):
		raise Exception("Unable to load config.ini. In there an access_token is defined.")

	cfg = ConfigParser()
	with open(CFG_FILE) as fp:
		cfg.readfp(fp, 'config.ini')
		access_token = cfg.get('config_ini', 'access_token')

	client = Client(access_token=access_token)
	return client