import matplotlib.pyplot as plt
import json
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import axes3d
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
'''
用来绘图出次数
'''
def threhold_vs_num_of_pair():
    with open('count.json') as f:
        data  = json.loads(f.read())
        print(data)

    series = []
    x = []
    for i in range(1,max(map(int,data.keys())) + 1):
        x.append(i)
        if str(i) in data:
            series.append(int(data[str(i)]/2))
        else:
            series.append(0)
    print(series)
    threhold = {
        "阀值":x,
        "人数对":series
    }
    pd.DataFrame(threhold).to_excel("阀值和人数对的关系.xls")
    fig = plt.figure()
    slice = 30
    this_x = x[slice:]
    plt.bar(x=this_x, height=series[slice:], label='', color='indianred', alpha=0.8)
    plt.show()

    fig = plt.figure()
    this_x = x[10:slice]
    plt.bar(x=this_x, height=series[10:slice], label='', color='steelblue', alpha=0.8)
    plt.xticks(this_x,this_x)
    plt.show()

    fig = plt.figure()
    this_x = x[:3]
    plt.bar(x=this_x, height=series[:3], label='', color='orange', alpha=0.8)
    plt.xticks(this_x,this_x)
    plt.show()

    fig = plt.figure()
    this_x = x[3:10]
    plt.bar(x=this_x, height=series[3:10], label='', color='purple', alpha=0.8)
    plt.xticks(this_x,this_x)
    plt.show()
def compare_num_parnter_of_diffrent_dept_under_specific_threhold(threhold = 8):
    df = pd.read_csv(open("2015年球季学期不同学院不同阀值下的人均友数.csv",encoding='utf-8-sig'))
    for column in df.columns:
        if "Unnamed" in column:
            df.drop(column,axis=1)
    df = df.sort_values(str(threhold),ascending= False)
    df = df.reset_index(drop=True)
    print(df.loc[:,['PATRON_DEPT',str(threhold)]])
    labels = df.loc[:,'PATRON_DEPT'].values
    labels = list(labels[:19])
    labels.append('others')
    labels = labels[::-1]
    data =  df.loc[:,str(threhold)].values
    sizes = list(data[:19])
    sizes.append(sum(data[19:])/len(data[19:]))
    sizes = sizes[::-1]
    print(sizes)
    plt.bar(x = 0,bottom=list(range(len(labels))),width = sizes,orientation="horizontal",height=0.5)
    plt.title("2015年秋季学期不同学院阀值{}下的人均友数".format(threhold))
    plt.yti


    cks(list(range(len(labels))),labels,fontsize = 10)
    plt.show()
def compare_num_parnter_of_diffrent_dept():
    fig = plt.figure(figsize=(20,8))
    ax = fig.add_subplot(111, projection='3d')
    valid_depts = ['法学院','会计学院','经济学院','公共经济与管理学院','数学学院','金融学院','财经研究所']
    df = pd.read_csv(open("2015年球季学期不同学院不同阀值下的人均友数.csv", encoding='utf-8-sig'))
    for column in df.columns:
        if "Unnamed" in column:
            df.drop(column, axis=1)
    # Grab some test data.
    labels = df.loc[:,'PATRON_DEPT'].values
    X = np.array(list(range(len(labels))))
    Y = np.array(list(range(len(range(4,16)))))
    X,Y = np.meshgrid(X,Y)

    Z = np.zeros_like(X)
    for i in range(len(X)):
        for j in range(len((X[0]))):
            Z[i][j] = df.loc[j,str(4+i)]

    # Plot a basic wireframe.
    ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
    plt.title("2015年球季学期不同学院不同阀值下的人均友数")
    ax.set_xlabel("学院")
    ax.set_xticks(list(range(len(labels))))
    ax.set_xticklabels(labels,rotation=90,fontdict={'fontsize':5})
    ax.set_ylabel("阀值")
    ax.set_yticks(list(range(len(range(4,16)))))
    ax.set_yticklabels(list(range(4,16)))
    ax.set_zlabel("人均友数")
    plt.show()
compare_num_parnter_of_diffrent_dept_under_specific_threhold()