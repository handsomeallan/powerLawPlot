# coding=utf-8
'''
' 这篇代码主要讲述获取数据库表中数据，再进行简单的统计
' 统计采用SQL语句进行 By：Eastmount CSDN 杨秀璋 Edit By Lxt
'''

import matplotlib.pyplot as plt
import numpy as np
import pymssql

# 根据群内数据绘制幂律分布图
def getPictures(groupName,showName):
    # 1、获取群数据
    try:
        conn = pymssql.connect(host='localhost', user='*', password='*', database='wechat') # 必须打开SQL Server的Tcp/IP协议才可以访问
        cur = conn.cursor()  # 数据库游标

        # groupName = '博士论坛'
        tblName = 't4_'+ groupName +'\n'

        sql = 'select 表情数,人数 from '+ tblName;
        cur.execute(sql)
        result = cur.fetchall()
        # 异常处理
    except pymssql.Error as e:
        print(("SQL Server Error %d: %s") % (e.args[0], e.args[1]))
    finally:
        cur.close()
        conn.commit()
        conn.close()
#'''
    # 2、将表内数据结果赋值给变量
    PLNum = [n[0] for n in result]  # 表情数
    Num = [n[1] for n in result]  # 人数

    # 3、两边起对数log10
    x = np.log(PLNum)
    y = np.log(Num)

    # 4、最小二乘法拟合
    poly = np.polyfit(x, y, deg=1)
    a = np.exp(poly[1]) # 获得系数a
    print(groupName)
    print(a)
    b = poly[0] #获得指数b
    print(b)
    # 5、将结果写入到文本文档：各群数据.txt
    with open('data/各群数据.txt','a',encoding='utf-8') as fs:
        fs.write(groupName+'\n')
        fs.write('x = ' + str(PLNum)+'\n')
        fs.write('y = ' + str(Num)+'\n')
        fs.write('a = ' + str(a) + '\n')
        fs.write('b = ' + str(b) + '\n')


    # 计算拟合值
    # z = np.polyval(poly, x)
    # plt.plot(x, y, 'ro')
    # plt.plot(x, z, 'g-')

    #6、计算幂律分布直线坐标
    # y = a*x^b
    x = PLNum
    y = a*np.power(x,b)

    # 7、绘图

    # 7.1 解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 7.2 设置标题及坐标轴标签
    plt.title(showName,fontsize=20)
    plt.xlabel('表情数')
    plt.ylabel('人数')

    # 7.3 绘图、保存并显示
    plt.loglog(PLNum,Num,'rs',label='人数')
    plt.plot(x,y,'k',label='幂律分布')
    plt.legend()
    plt.savefig(groupName+'.png')
    plt.show()
#'''
if __name__ == '__main__':

    x = ['百科全书','自科重大','教指委','博士17班','信管校友','同学04级','老年群','老连家','滑翔伞','林州滑翔','游戏群','海大摄影']
    y = ['A1','A2','A3','B1','B2','B3','C1','C2','D1','D2','D3','D4']
    i = 0
    for i in range(len(x)):
        getPictures(x[i],y[i])
        i = i+1