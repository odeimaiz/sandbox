import pandas as pd


COLUMNS = ['Pos', 'Name', 'Time']

def learboard_to_csv(client, segment_id, timeframe=None, gender=None, club_id=None, nResults=None):
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


def sum_learboards(segment_ids, outfilename):
	dfs = []
	for segment_id in segment_ids:
		df = pd.read_csv('leaderboards/'+str(segment_id)+'.csv')
		dfs.append(df)

	df_overall = pd.DataFrame(columns=COLUMNS)
	if len(dfs) > 0:
		for _index_ref, row_ref in dfs[0].iterrows():
			pos = '1'
			name = row_ref['Name']
			times = [row_ref['Time']]
			for dfs_b in dfs[1:]:
				for _index_b, row_b in dfs_b.iterrows():
					if row_ref['Name'] == row_b['Name']:
						times.append(row_b['Time'])
				if len(times) == len(segment_ids):
					df_overall = df_overall.append({
						'Pos': pos,
						'Name': name,
						'Time': sum(times)
					}, ignore_index=True)

	df_overall = df_overall.sort_values(by=['Time'], ascending=[True])
	pos = 1
	for index, _row in df_overall.iterrows():
		df_overall.loc[index, 'Pos'] = pos
		pos = pos + 1
	df_overall.to_csv('leaderboards/'+outfilename, sep=',', encoding='utf-8', index=False)
