import os
import pandas as pd
from six.moves.configparser import ConfigParser

from stravalib import model
from stravalib.client import Client


COLUMNS = ["Pos", "Name", "Time"]

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

def learboard_to_csv(client, segment_id, timeframe=None, gender=None, club_id=None, nResults=None):
	# get_segment_leaderboard(segment_id, gender=None, age_group=None, weight_class=None, following=None,
	# 	club_id=None, timeframe=None, top_results_limit=None, page=None, context_entries=None)
	leaderboard = client.get_segment_leaderboard(segment_id, timeframe=timeframe, gender=gender, club_id=club_id, top_results_limit=nResults)

	df = pd.DataFrame(columns=COLUMNS)
	for entry in leaderboard:
		df = df.append({
			COLUMNS[0]: entry.rank,
			COLUMNS[1]: entry.athlete_name,
			COLUMNS[2]: entry.elapsed_time.seconds
			}, ignore_index=True)

	file_name = str(segment_id) + "_leaderboard.csv"
	df.to_csv(file_name, sep=',', encoding='utf-8', index=False)