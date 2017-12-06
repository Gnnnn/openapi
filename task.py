# -*- coding: utf-8 -*-
"""
<<<<<<< HEAD
Created on Wed Nov 29 13:35:12 2017

@author: xiaokexiao
=======
Created on Wed Nov 29 13:35:12 ****

@author: Gn
>>>>>>> d74b4a917e6f12e5a81196c1ef62a8cd287889fc
"""

import openapi 
import time 
import tools
import config
import main    
        
def task(access_token,requestId): 
<<<<<<< HEAD
    # Task?????============================================================================= 
    #?Task????????0?3????1????TaskId?InterfaceType??????InterfaceType??checkapi??????api??
    sql = 'select TaskId,InterfaceType from ' + config.DatabaseInfo['DatabaseInterfaceTable'] + ' where Direction = 1 and ( TaskState = 0 or TaskState = 3 )' 
    datas = tools.database(sql) 
    tools.log("TaskIds : " + str(datas),'info')
    #InterfaceType????????????????General,????????? 
=======
    # Task表交互机制============================================================================= 
    #从Task表里筛选出状态为0或3，方向为1的任务的TaskId和InterfaceType，根据不同的InterfaceType使用checkapi字典映射调用api方法
    sql = 'select TaskId,InterfaceType from ' + config.DatabaseInfo['DatabaseInterfaceTable'] + ' where Direction = 1 and ( TaskState = 0 or TaskState = 3 )' 
    datas = tools.database(sql) 
    tools.log("TaskIds : " + str(datas),'info')
    #InterfaceType写对应接口的数据库表名，默认值为General,用于调试和特殊任务 
>>>>>>> d74b4a917e6f12e5a81196c1ef62a8cd287889fc
    checkapi = {'ABSAssetBag':main.assetsSold 
                ,'ABSTrustPaymentOrder':main.assetsPlanPay 
                ,'ABSPresale':main.assetsAdjust
                ,'':main.passTask} 
    checkapiJson = {'ABSAssetBag':'assetsSold'
                ,'ABSTrustPaymentOrder':'assetsPlanPay' 
                ,'ABSPresale':'assetsAdjust'
                ,'':'no TaskName'}
    i = 0 
    while i<len(datas): 
        i = i + 1 
        data = datas[i-1] 
        InterfaceType = data[1] 
        TaskId = data[0] 
        tools.log("TaskId : "+TaskId,'info')
        tools.log("TaskFunc : "+checkapiJson[InterfaceType],'info')
        checkapi[InterfaceType](access_token,requestId,TaskId)
    return
        
        
if __name__ == '__main__': 
    tools.log("DataInterfaceTask Start--",'warn')
    access_token = openapi.getToken() 
    requestId = str(int(time.time())) 
    
    task(access_token,requestId)
    tools.log("DataInterfaceTask End--",'warn')
