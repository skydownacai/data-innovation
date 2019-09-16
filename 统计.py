import os
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from copy import  copy,deepcopy
import json
averages = []
users = {}
user_columns = ['UNIVERSITY_ID', 'PATRON_ID', 'STUDENT_GRADE', 'PATRON_DEPT', 'PATRON_TYPE', 'VISIT_TIME',
				'VISIT_SUBLIBRARY']
container  = {}
def file_drop_encounter_only_one_and_records():
	for file in os.listdir("data_2/"):
		with open("data_2/" + file) as f:
			data = json.load(f)
		after = {
		}
		for id in data:
			if id == "record":
				continue
			this_count = data[id]
			if this_count > 1:
				after[id] = this_count
		with open("after_data_2/"+file,'w') as f:
			f.write(json.dumps(after))
def average_partner(threhold:int):
	dir = "after_data_2/"
	total_user = {
		"PATRON_ID":[]
	}
	for i in range(4, 16):
		total_user[str(i)] = []
	files = os.listdir(dir)
	for i in range(len(files)):
		print(i,"/",100)
		file = files[i]
		with open(dir+ file) as f:
			data = json.load(f)
		this_partner = 0
		total_user["PATRON_ID"].append(file.replace(".json",""))
		for value in range(4, 16):
				total_user[str(value)].append(0)
		for id in data:
			if id == "record":
				continue
			this_count = data[id]
			for value in range(4, 16):
				if this_count >= value:
					total_user[str(value)][i] = total_user[str(value)][i] + 1
			if this_count >= threhold:
				this_partner = this_partner + 1
		averages.append(this_partner)
	pd.DataFrame(total_user).to_csv("每个学生对应的不同阀值下的馆友数表.csv",encoding="utf-8-sig")
	print('over')
	return  np.average(averages)
def threhold_vs_pair():
	COUNT = {}
	dir = "after_data_2/"
	for file in os.listdir(dir):
		with open(dir + file) as f:
			data = json.load(f)
		for id in data:
			this_count = data[id]
			if this_count not in COUNT:
				COUNT[this_count] = 1
			else:
				COUNT[this_count] = COUNT[this_count] + 1
	for key in COUNT:
		COUNT[key] = int(COUNT[key]/2)
	return COUNT
def compare_num_parnter_of_diffrent_userinfo(init_f,process_f,end_f,attribution):
	global users
	users = pd.read_csv("user.csv")
	dir = "after_data_2/" #这里的数据已经排除了没有1的
	container = {}
	attribution_box = []
	users.set_index("PATRON_ID", drop=True, inplace=True, verify_integrity=False)
	for column in users.columns:
		if "Unnamed" in column:
			users = users.drop(column, axis=1)
	init_f(attribution)
	files = os.listdir(dir)
	for i in range(len(files)):
		file = files[i]
		print(i,"/",len(files))
		with open(dir + file) as f:
			data = json.load(f)
		his_id = file.replace(".json","")
		his_info = users.loc[his_id]
		first_enter = True
		for id in data:
			parterinfo = users.loc[id]
			this_count = data[id]
			process_f(his_info,this_count,first_enter,attribution,parterinfo)
			first_enter = False
	end_f(attribution)
def init(attribution):
	global container
	container[attribution] =[]
	for value in range(4, 16):
		container[str(value)] = []
	container["num_of_" + attribution] = []
def process(his_info,count,first_enter,attribution,parterinfo):
	global container
	his_attribution = his_info[attribution]
	if str(his_attribution) == "nan":
		return 0
	if his_attribution not in container[attribution]:
		container[attribution].append(his_attribution)
		for value in range(4,16):
			container[str(value)].append(0)
		container["num_of_"+attribution].append(0)
	attribution_index = container[attribution].index(his_attribution)
	for value in range(4, 16):
		if count >= value:
			container[str(value)][attribution_index] += 1
		else:
			break
	if first_enter:
		container['num_of_'+attribution][attribution_index] += 1
def end(attribution):
	global container
	container = pd.DataFrame(container)
	container.to_csv("2015年球季学期不同{}不同阀值下的总馆友数.csv".format(attribution),encoding='utf-8-sig')
	container = container.drop(container[container['num_of_' + attribution] <= 7].index)
	for i in range(len(container[attribution])):
		that = container.iloc[i, -1]
		exists = container.iloc[i, 1:-1]
		container.iloc[i, 1:-1] = exists / int(that)
	container.to_csv("2015年球季学期不同{}不同阀值下的人均友数.csv".format(attribution), encoding='utf-8-sig')
def init_2(attribution):
	global container
	container['His|Partner'] = []
	container['num_of_'+attribution] = []
	container['8']   = []
	container = pd.DataFrame(container)
def process_2(his_info,count,first_enter,attribution,parterinfo):
	global container
	his_attribution = his_info[attribution]
	partner_attribution = parterinfo[attribution]
	if str(his_attribution) == "nan" :
		return 0
	if his_attribution not in list(container['His|Partner'].values):
		new = {'His|Partner':str(his_attribution),'num_of_'+attribution:0}
		for column in container.columns:
			if column not in ['His|Partner','num_of_'+attribution]:
				new[column] = 0

		container = container.append(new,ignore_index=True)
	if his_attribution not in list(container.columns):
		container[his_attribution] = 0
	attribution_index = list(container['His|Partner'].values).index(his_attribution)
	if first_enter:
		container.loc[attribution_index,'num_of_'+attribution] += 1
	if count >= 8 :
		if partner_attribution not in list(container.columns):
			container[partner_attribution] = 0
		container.loc[attribution_index,partner_attribution] += 1
def end_2(attribution):
	global container
	container.to_csv("row.csv",encoding='utf-8-sig')
	container['total_num_of_partner'] = 0
	container['ratio_diffrent'] = 0
	container = container.set_index("His|Partner",drop = True)
	container = container.applymap(lambda x:0 if np.isnan(x) else x)
	i = -1
	for index in container.index:
		i += 1
		all = sum(container.iloc[i,1:-2])
		container.iloc[i,-2] = all
		itself = container.loc[index,index]
		if all != 0:
			container.loc[index,'ratio_diffrent'] =  1 - float(itself/all)
	container.to_csv("2015年球季学期不同{}下不同{}馆友数.csv".format(attribution,attribution),encoding='utf-8-sig')
	for i in range(len(container)):
		all = container.iloc[i,0]
		exits = container.iloc[i, 1:-2]
		if all != 0:
			container.iloc[i, 1:-2] = exits / int(all)
	container.to_csv("2015年球季学期不同{}下人均不同{}馆友数.csv".format(attribution,attribution), encoding='utf-8-sig')
compare_num_parnter_of_diffrent_userinfo(init_f=init_2,process_f=process_2,end_f=end_2,attribution="PATRON_DEPT")



































































































































































