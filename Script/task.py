# -*- coding: utf-8 -*-

"""
Created on Wed Nov 29 13:35:12 2017

@author: PHABSOPRSTG
"""



import openapi 
import time 
import config
import main  
import tools  
import pymssql


def task(access_token,requestId,conn): 

    # Task表交互机制============================================================================= 
    #从Task表里筛选出状态为0或3，方向为1的任务的TaskId和InterfaceType，根据不同的InterfaceType使用checkapi字典映射调用api方法
    sql = 'select TaskId,InterfaceType from ' + config.DatabaseInfo['DatabaseInterfaceTable'] + " where Direction = 1 and ( TaskState = 0 or TaskState = 3 or TaskState = 1) and TaskChannel = 'OPEN_API' " 
    tools.log(sql,'info')
    datas = tools.database(conn,sql) 
    tools.log("TaskIds : " + str(datas),'info')
    #InterfaceType写对应接口的数据库表名，默认值为General,用于调试和特殊任务 
    checkapi = {'ABSAssetBag':main.assetsSold 
                ,'ABSTrustPaymentOrder':main.assetsPlanPay 
                #,'ABSTrust':main.assetsPlanPay 
                ,'ABSPresale':main.assetsAdjust
                ,'':main.passTask} 
#    checkapiJson = {'ABSAssetBag':'assetsSold'
#                ,'ABSTrustPaymentOrder':'assetsPlanPay' 
#                ,'ABSPresale':'assetsAdjust'
#                ,'':''}
    checkapiJson = {'ABSAssetBag':'ABSAssetBag'
                ,'ABSTrustPaymentOrder':'ABSTrustPaymentOrder' 
                ,'ABSPresale':'ABSPresale'
                ,'':''}
    i = 0 
    while i<len(datas): 
        i = i + 1 
        data = datas[i-1] 
        InterfaceType = data[1] 
        TaskId = data[0] 
        tools.log("TaskId : "+TaskId,'info')
        InterfaceTypeJson = checkapiJson.setdefault(InterfaceType,'')
        tools.log("TaskFunc : "+InterfaceType,'info')
        print InterfaceTypeJson
        checkapi[InterfaceTypeJson](access_token,requestId,TaskId,conn)
    return

        

if __name__ == '__main__': 
    tools.log("DataInterfaceTask Start--",'warn')
    global conn
    conn = pymssql.connect(config.DatabaseInfo['DatabaseUrl'],config.DatabaseInfo['UserName'],config.DatabaseInfo['Password'],config.DatabaseInfo['Database'],charset="UTF-8") 
    access_token = openapi.getToken() 
    requestId = str(int(time.time())) 
    task(access_token,requestId,conn)
    conn.close()
    tools.log("DataInterfaceTask End--",'warn')
