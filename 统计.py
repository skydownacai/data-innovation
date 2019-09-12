import os
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from copy import  copy,deepcopy
import json
averages = []
users = {}
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
		print(i,"/",len(files))
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
def compare_num_parnter_of_diffrent_userinfo(init_f,process_f,end_f):
	global users
	user_columns = ['UNIVERSITY_ID', 'PATRON_ID', 'STUDENT_GRADE', 'PATRON_DEPT', 'PATRON_TYPE', 'VISIT_TIME',
					'VISIT_SUBLIBRARY']
	users = pd.read_csv("user.csv")
	dir = "after_data_2/" #这里的数据已经排除了没有1的
	container = {}
	#users.drop_duplicates(subset='PATRON_ID', keep='first', inplace=True)
	init_f(container)
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
			this_count = data[id]
			process_f(his_info,this_count,container,first_enter)
			first_enter = False
	end_f(container)
def init_diffrent_dept_under_differen_threhold(container):
	container['PATRON_DEPT'] =[]
	for value in range(4, 16):
		container[str(value)] = []
	container["num_of_dept"] = []
def diffrent_dept_under_differen_threhold(his_info,count,container,first_enter):
	his_dept = his_info['PATRON_DEPT']
	if his_dept not in container['PATRON_DEPT']:
		container['PATRON_DEPT'].append(his_dept)
		for value in range(4,16):
			container[str(value)].append(0)
		container["num_of_dept"].append(0)
	dept_index = container['PATRON_DEPT'].index(his_dept)
	for value in range(4, 16):
		if count >= value:
			container[str(value)][dept_index] += 1
	if first_enter:
		container['num_of_dept'][dept_index] += 1
def end_diffrent_dept_under_differen_threhold(container):
	container = pd.DataFrame(container)
	pd.DataFrame(container).to_csv("2015年球季学期不同学院不同阀值下的总馆友数.csv",encoding='utf-8-sig')
	for i in range(len(container['PATRON_DEPT'])):
		that = container.iloc[i, -1]
		container.iloc[i, 1:-1] = container.iloc[i, 1:-1] / int(that)
	pd.DataFrame(container).to_csv("2015年球季学期不同学院不同阀值下的人均友数.csv", encoding='utf-8-sig')
compare_num_parnter_of_diffrent_userinfo(init_f=init_diffrent_dept_under_differen_threhold,process_f=diffrent_dept_under_differen_threhold,end_f=end_diffrent_dept_under_differen_threhold)



































































































































































