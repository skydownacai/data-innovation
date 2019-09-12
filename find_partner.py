import pandas as pd
import os
import json
import  time
import threading
dir  = "data_3/"
file = "data_3.csv"
threhold = 30
df = pd.read_csv(file)
len_df = len(df)
enter_time = time.time()
try:
	os.mkdir(dir)
except:
	pass
for i in range(len_df):
	if i% 100 == 0:
		print(i)
	item = df.iloc[i]
	this_id = item['PATRON_ID']
	this_file = dir+ str(this_id) + ".json"
	j = i - 1
	if (os.path.exists(this_file) == False):
		f = open(this_file,'w')
		this_data = {"record":[]}
	else:
		f = open(this_file,'r')
		this_data = json.loads(f.read())
		f.close()
		f = open(this_file,'w')
	#把自己的文件打开
	j = i - 1
	while True:
		if(j < 0):
			break
		#print(j,end=":")
		item_before = df.iloc[j]
		that_id = int(item_before['PATRON_ID'])
		if item['VISIT_TIME'] - item_before['VISIT_TIME'] > threhold:
			break
		if str(that_id) not in this_data:
			this_data[str(that_id)] = 1
		else:
			this_data[str(that_id)] = this_data[str(that_id)] + 1
		this_data['record'].append((i,j))
		j = j - 1

	j = i + 1
	#print("backward")
	while True:
		if(j >= len_df):
			break
		#print(j,end=":")
		item_after = df.iloc[j]
		that_id = int(item_after['PATRON_ID'])
		if item_after['VISIT_TIME'] - item['VISIT_TIME']  > threhold:
			break
		if str(that_id) not in this_data:
			this_data[str(that_id)] = 1
		else:
			this_data[str(that_id)] = this_data[str(that_id)] + 1
		this_data['record'].append((i,j))
		j = j + 1
	f.write(json.dumps(this_data))
	f.close()
print(time.time() - enter_time)