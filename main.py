# -*- coding: utf-8 -*- 
""" Created on Thu Nov 16 10:39:07 2017 @author: pub_Treasurysystem xiaokexiao """ 

import config 
import openapi 
import tools 
import time 
import json 


#资产兑付操作
def assetsPlanPay(access_token,requestId,TaskId): 
    #任务开始，维护task表
    TaskStartTime= "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
    tools.taskStartUpdate(TaskStartTime,TaskId)

    sql = 'select ' + config.sql['assetsPlanPay'] + 'from' + config.sql['assetsPlanPayTable'] + 'where TaskId = ' + TaskId 
    datas = tools.database(sql); 
    assetsPlanPayre = [] 
    #此处循环是当一个TaskId查出多条数据时，对每条数据调用该api
    i = 0 
    while i < len(datas): 
        i = i+1 
        data = datas[i-1] 
        errortimes = 0 
        successtimes = 0 
        TrustCode=data[1] 
        TrustName=data[2] 
        PaymentAmount=data[3] 
        PayDate=data[4] 
        ReceiverAccount=data[5] 
        ReceiverBank=data[6] 
        ReceiverName=data[7] 
        IsRegulated=data[8] 
        PaymentOrganization=data[9] 
        PaymentAccount=data[10] 
        SourceSystem=data[11] 
        ProductType=data[12] 
        PaymentId=data[0] 
        updatedBy='system' 
        
        re = openapi.getAssetsPlanPay(PaymentId,TrustCode,TrustName,PaymentAmount,PayDate,ReceiverAccount,ReceiverBank,ReceiverName,IsRegulated,PaymentOrganization,PaymentAccount,SourceSystem,ProductType,access_token,requestId,updatedBy) 
        assetsPlanPayre.append(re) 

        TaskEndTime = "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
        if(json.loads(str(re)).get('msg') is None): 
            #任务成功，维护task表
            tools.successUpdate(TaskStartTime,TaskEndTime,TaskId)
            #任务成功，维护兑付表
            sql = 'update dbo.ABSTrustPaymentOrder set PaymentStatus = N"' + json.loads(str(re)).get('data').get('status') +'" where TaskId = ' + str(TaskId)
            tools.databasesql(sql)

            #if(json.loads(str(re)).get('data').get('status') == 0): 
            #    successtimes =successtimes + 1 
            #    #任务成功，维护task表
            #    tools.successUpdate(TaskStartTime,TaskEndTime,TaskId)
            #    #任务成功，维护兑付表
            #    sql = 'update dbo.ABSTrustPaymentOrder set PaymentStatus = N"成功" where TaskId = ' + str(TaskId) 
            #    tools.databasesql(sql)

            #elif(json.loads(str(re)).get('data').get('status') == 1): 
            #    errortimes = errortimes + 1 
            #    errorInfo = json.loads(str(re)).get('data').get('message') 
            #    #任务失败，维护task表
            #    tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId)
            #    #任务失败，维护兑付表
            #    sql = 'update dbo.ABSTrustPaymentOrder set PaymentStatus = N"失败" where TaskId = ' + str(TaskId) 
            #    tools.databasesql(sql)
        else: 
            errortimes = errortimes + 1 
            errorInfo = json.loads(str(re)).get('msg') 
            #任务失败，维护task表
            tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId)
            #任务失败，维护兑付表
            sql = 'update dbo.ABSTrustPaymentOrder set PaymentStatus = N"失败" where TaskId = ' + str(TaskId) 
            tools.databasesql(sql)

        tools.log(str(successtimes) + "success(es)," + str(errortimes) + "fail(s)" ,'info')
    return assetsPlanPayre 



#兑付状态查询，与其他三个不同，不涉及Task表，只更新兑付表PaymentStatus
def queryPayResult(access_token,requestId): 
    sql = "select PaymentId from " + config.sql['assetsPlanPayTable'] + " where PaymentStatus = N'已执行'" 
    datas = tools.database(sql) 
    i = 0 
    paymentIds = [] 
    errortimes = 0 
    successtimes = 0 
    while i <len(datas): 
        paymentIds.append(datas[i][0]) 
        i = i + 1 
    
    re = openapi.getQueryPayResult(paymentIds,access_token,requestId) 
    if(json.loads(str(re)).get('msg') == ""): 
        if(json.loads(str(re)).get('data').get('status') == '0'): 
            #未完成
            errortimes = errortimes + 1 
            errorInfo = json.loads(str(re)).get('data').get('message') 
            tools.log(errorInfo,'error') 
        elif(json.loads(str(re)).get('data').get('status') == '1'): 
            successtimes =successtimes + 1 
            j = 0 
            #已完成，返回多条数据形如{status:'1','id1':'Y(成功)','id2':'F(失败)','id3':'R(退票)'}
            while j < len(json.loads(str(re)).get('data'))-1:
                j = j + 1 
                if(json.loads(str(re)).get('data').values()[j] == 'Y'): 
                    sql = "update " + config.sql['assetsPlanPayTable'] +" set PaymentStatus = N'成功' where PaymentId = " + json.loads(str(re)).get('data').keys()[j] 
                elif(json.loads(str(re)).get('data').values()[j] == 'N'): 
                    sql = "update " + config.sql['assetsPlanPayTable'] +" set PaymentStatus = N'失败' where PaymentId = " + json.loads(str(re)).get('data').keys()[j] 
                elif(json.loads(str(re)).get('data').values()[j] == 'R'): 
                    sql = "update " + config.sql['assetsPlanPayTable'] +" set PaymentStatus = N'失败' where PaymentId = " + json.loads(str(re)).get('data').keys()[j] 
    else:
        errortimes = errortimes + 1 
        errorInfo = json.loads(str(re)).get('msg') 
        tools.log(errorInfo,'error') 
    tools.log(str(successtimes) + "success(es)," + str(errortimes) + "fail(s)",'info') 
    return re 


#资产正式卖出
def assetsSold(access_token,requestId,TaskId): 
    #任务开始，维护task表
    TaskStartTime= "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
    tools.taskStartUpdate(TaskStartTime,TaskId)

    sql = 'select '+ config.sql['assetsSold'] + ' from ' + config.sql['assetsSoldTable'] + ' where TaskId = ' + str(TaskId) 
    datas = tools.database(sql) 
    errortimes = 0 
    successtimes = 0 
    if datas == []: 
        tools.log('there is no data in ABSAssetBag!','error') 
        return 
    #只有一条数据，只取第一条
    data = datas[0] 
    config.assetsSold['ASSETS_BAG_NO'] = data[0] 
    config.assetsSold['PRODUCT_TYPE'] = data[1] 
    config.assetsSold['DATA_SOURCE'] = data[2] 
    config.assetsSold['FINISH_BY'] = data[3] 
    config.assetsSold['FINISH_DATE'] = data[4] 

    re = openapi.getAssetsSold(config.assetsSold['ASSETS_BAG_NO'],config.assetsSold['PRODUCT_TYPE'],config.assetsSold['DATA_SOURCE'],config.assetsSold['FINISH_BY'],config.assetsSold['FINISH_DATE'],access_token,requestId) 

    TaskEndTime = "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
    if(json.loads(str(re)).get('msg') is None): 
        if(json.loads(str(re)).get('data').get('status') == 0): 
            successtimes =successtimes + 1 
            #任务成功，维护task表
            tools.successUpdate(TaskStartTime,TaskEndTime,TaskId) 
        elif(json.loads(str(re)).get('data').get('status') == 1): 
            errortimes = errortimes + 1 
            errorInfo = json.loads(str(re)).get('data').get('message') 
            #任务失败，维护task表
            tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId)
    else: 
        errortimes = errortimes + 1 
        errorInfo = json.loads(str(re)).get('msg') 
        #任务失败，维护task表
        tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId)
    print str(successtimes) + "success(es)," + str(errortimes) + "fail(s)" 
    return re 
    
    
    
    
#资产卖出前的增删
def assetsAdjust(access_token,requestId,TaskId): 
    #任务开始，维护task表
    TaskStartTime= "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
    tools.taskStartUpdate(TaskStartTime,TaskId)

    sql = 'exec ' + config.sql['assetsAdjustSP'] + ' ' + str(TaskId) 
    datas = tools.database(sql) 
    if datas == []: 
        tools.log('there is no data in ABSPresale!','error') 
        return 
    errortimes = 0 
    successtimes = 0 

    assetsBagNo = datas[0][0] 
    sourceSystem = datas[0][1] 
    adjustFlag = datas[0][2] 
    #数据库里adjustFlag 1是增，-1是减。而PH的接口1是增，2是减
    if adjustFlag == -1: 
        adjustFlag = 2 
    adjustNumber = datas[0][3] 
    updatedBy = 'system' 

    assetsAdjustRe = openapi.getAssetsAdjust(assetsBagNo,sourceSystem,adjustFlag,adjustNumber,updatedBy,access_token,requestId) 

    TaskEndTime = "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
    if(json.loads(str(assetsAdjustRe)).get('msg') is None): 
        tools.log(json.loads(str(assetsAdjustRe)).get('data'),'info') 
        if(json.loads(str(assetsAdjustRe)).get('data').get('status') == 0): 
            successtimes =successtimes + 1 
            #任务成功，维护task表
            tools.successUpdate(TaskStartTime,TaskEndTime,TaskId) 
        elif(json.loads(str(assetsAdjustRe)).get('data').get('status') == 1): 
            errortimes = errortimes + 1 
            errorInfo = json.loads(str(assetsAdjustRe)).get('data').get('message') 
            #任务失败，维护task表
            tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId)
    else: 
        errortimes = errortimes + 1 
        errorInfo = json.loads(str(assetsAdjustRe)).get('msg') 
        #任务失败，维护task表
        tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId)
    tools.log(str(successtimes) + " success(es)," + str(errortimes) + " fail(s)",'info') 
    return assetsAdjustRe 
    
    
def main(access_token,requestId): 
    # Task表交互机制============================================================================= 
    #从Task表里筛选出状态为0或3，方向为1的任务的TaskId和InterfaceType，根据不同的InterfaceType使用checkapi字典映射调用api方法
    sql = 'select TaskId,InterfaceType from ' + config.DatabaseInfo['DatabaseInterfaceTable'] + ' where Direction = 1 and ( TaskState = 0 or TaskState = 3 )' 
    datas = tools.database(sql) 

    #InterfaceType写对应接口的数据库表名，默认值为General,用于调试和特殊任务 
    checkapi = {'ABSAssetBag':assetsSold 
                ,'ABSTrustPaymentOrder':assetsPlanPay 
                ,'ABSPresale':assetsAdjust} 
    i = 0 
    while i<len(datas): 
        i = i + 1 
        data = datas[i-1] 
        InterfaceType = data[1] 
        TaskId = data[0] 
        checkapi[InterfaceType](access_token,requestId,TaskId) 
    
    # 每隔5分钟轮循机制============================================================================= 
    # 每隔30分钟运行一次queryPayResult函数
    sleeptime = tools.sleeptime(0,30,0)
    while 1 == 1:
        time.sleep(sleeptime)
        queryPayResult(access_token,requestId)

    return
        
        
if __name__ == '__main__': 
    access_token = openapi.getToken() 
    requestId = str(int(time.time())) 
    queryPayResult(access_token,requestId) 
    main(access_token,requestId)

