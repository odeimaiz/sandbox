import pandas as pd


COLUMNS = ['Pos', 'Name', 'Time']

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

	file_name = 'leaderboards/' + str(segment_id) + '.csv'
	df.to_csv(file_name, sep=',', encoding='utf-8', index=False)


def sum_learboards(segment_id_1, segment_id_2):
	df_1 = pd.read_csv('leaderboards/'+str(segment_id_1)+'.csv')
	df_2 = pd.read_csv('leaderboards/'+str(segment_id_2)+'.csv')
	df_overall = pd.DataFrame(columns=COLUMNS)
	for _index1, row1 in df_1.iterrows():
		for _index2, row2 in df_2.iterrows():
			if row1['Name'] == row2['Name']:
				df_overall = df_overall.append({
					'Pos': 1,
					'Name': row1['Name'],
					'Time': row1['Time'] + row2['Time']
				}, ignore_index=True)
	df_overall = df_overall.sort_values(by=['Time'], ascending=[True])
	pos = 1
	for index, _row in df_overall.iterrows():
		df_overall.loc[index, 'Pos'] = pos
		pos = pos + 1
	df_overall.to_csv('leaderboards/overall.csv', sep=',', encoding='utf-8', index=False)
