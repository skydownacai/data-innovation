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
def compare_num_parnter_of_diffrent_attribution_under_specific_threhold(attribution,threhold = 8):
    df = pd.read_csv(open("2015年球季学期不同{}不同阀值下的人均友数.csv".format(attribution),encoding='utf-8-sig'))
    for column in df.columns:
        if "Unnamed" in column:
            df.drop(column,axis=1)
    df = df.sort_values(str(threhold),ascending= True)
    df = df.reset_index(drop=True)
    labels = df.loc[:,attribution].values
    sizes =  df.loc[:,str(threhold)].values
    fig = plt.figure(figsize=(8,10))
    plt.bar(x = 0,bottom=list(range(len(labels))),width = sizes,orientation="horizontal",height=0.5)
    plt.title("2015年秋季学期不同{}阀值{}下的人均友数".format(attribution,threhold))
    plt.yticks(list(range(len(labels))),labels,fontsize = 10)
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
def threeD_Histogram_num_property_parnter_of_different_property(attribution):
    # Fixing random state for reproducibility

    fig = plt.figure()
    df = pd.read_csv(open("2015年球季学期不同{}下不同{}馆友数.csv".format(attribution,attribution), encoding='utf-8-sig'))
    df = df.set_index("His|Partner")
    need_drop = list(df[df['num_of_PATRON_DEPT'] < 10].index)
    print(need_drop)
    df = df.drop(columns="num_of_PATRON_DEPT")
    df = df.drop(columns="total_num_of_partner")
    df = df.drop(columns="ratio_diffrent")
    df = df.drop(need_drop)
    df = df.drop(columns=need_drop)

    xlabels = list(df.index)
    x = list(range(len(xlabels)))
    ylabels = list(df.columns)
    y = list(range(len(ylabels)))
    ax = fig.add_subplot(111, projection='3d')
    print(df)
    x,y= np.meshgrid(x,y)
    z = []
    for i in range(len(x)):
        this = []
        for j in range(len(x[0])):
            that  = float(df.loc[xlabels[j],ylabels[i]])
            this.append(that)

        z.append(this)
    z = np.array(z).reshape(df.shape)
    print(z)
    # Plot a basic wireframe.
    ax.plot_wireframe(x, y, z, rstride=10, cstride=10)
    ax.set_xticks(list(range(len(x))))
    ax.set_yticks(list(range(len(x))))
    ax.set_xlabel("dept")
    ax.set_ylabel("dept")
    ax.set_zlabel("人均友数")
    ax.set_zlim(0,np.max(z))
    print(np.max(z))
    plt.show()
def bar_of_ratio_of_diffrent_attribution(attribution):
    fig = plt.figure()
    df = pd.read_csv(open("2015年球季学期不同{}下不同{}馆友数.csv".format(attribution,attribution), encoding='utf-8-sig'))
    df = df.set_index("His|Partner")
    need_drop = list(df[df['ratio_diffrent'] == 0].index) + list(df[df['num_of_PATRON_DEPT'] < 10].index)  + list(df[df['total_num_of_partner'] < 10].index)

    df = df.drop(need_drop)
    df = df.drop(columns=need_drop)
    labels = list(df.index)
    sizes = list(df["ratio_diffrent"].values)
    fig1, ax1 = plt.subplots()
    plt.bar(x = 0,bottom=list(range(len(labels))),width = sizes,orientation="horizontal",height=0.5)
    plt.yticks(list(range(len(labels) )),labels,fontsize = 8)
    plt.legend()
    plt.title("不同{}不同{}馆友数所占比例".format(attribution,attribution))
    plt.show()
bar_of_ratio_of_diffrent_attribution("PATRON_DEPT")