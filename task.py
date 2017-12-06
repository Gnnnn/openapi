# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 13:35:12 2017

@author: xiaokexiao
"""

import openapi 
import time 
import tools
import config
import main    
        
def task(access_token,requestId): 
    # Task?????============================================================================= 
    #?Task????????0?3????1????TaskId?InterfaceType??????InterfaceType??checkapi??????api??
    sql = 'select TaskId,InterfaceType from ' + config.DatabaseInfo['DatabaseInterfaceTable'] + ' where Direction = 1 and ( TaskState = 0 or TaskState = 3 )' 
    datas = tools.database(sql) 
    tools.log("TaskIds : " + str(datas),'info')
    #InterfaceType????????????????General,????????? 
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
