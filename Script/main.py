# -*- coding: utf-8 -*- 
<<<<<<< HEAD:Script/main.py
"""
Created on Thu Nov 30 14:11:38 ****

@author: Gn
"""
=======
""" Created on Thu Nov 16 10:39:07 2017 @author: *** **** """ 
>>>>>>> 6d016066d07e0a58c7a778636273b2e278395dab:main.py

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

    sql = 'select ' + config.sql['assetsPlanPay'] + ' from ' + config.sql['assetsPlanPayTable'] + ' where TaskId = ' + TaskId 
    print sql
    datas = tools.database(sql); 
    print datas
    assetsPlanPayre = [] 
    #此处循环是当一个TaskId查出多条数据时，对每条数据调用该api
    i = 0 
    while i < len(datas): 
        i = i+1 
        data = datas[i-1] 
        errortimes = 0   
        successtimes = 0 
        paymentId=data[0] 
        trustCode=data[1]
        paymentAmount=data[2] 
        payDate=data[3] 
        receiverAccount=data[4] 
        isRegulated=data[5] 
        if isRegulated== "True":
            isRegulated = 'Y'
        elif isRegulated== "False":
            isRegulated = 'N'
        paymentAccount=data[6] 
        sourceSystem=data[7]
        if sourceSystem== "ACC":
            sourceSystem = '2'
        elif sourceSystem== "FA":
            sourceSystem = '1'
        productType=data[8] 
        if productType == 'None':
            productType = ""
        updatedBy='system' 
        paymentId = paymentId.replace("-","")
        params = {"access_token":access_token,"requestId":requestId,"paymentId":paymentId, "trustCode":trustCode,"paymentAmount":paymentAmount,"payDate":payDate,"receiverAccount":receiverAccount,"isRegulated":isRegulated,"paymentAccount":paymentAccount,"sourceSystem":sourceSystem,"productType":productType,"updatedBy":updatedBy}
        #re,data = openapi.getAssetsPlanPay(access_token,requestId,paymentId, trustCode,paymentAmount,payDate,receiverAccount,isRegulated,paymentAccount,sourceSystem,productType,updatedBy) 
        re,data = openapi.getAssetsPlanPay(params)
        tools.log(re,'info')
        assetsPlanPayre.append(re) 
        TaskEndTime = "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
        if(re['msg'] == ""): 
            #此处返回的status不确定，普惠还没定下来
# =============================================================================
#             #任务成功，维护task表
#             tools.successUpdate(TaskStartTime,TaskEndTime,TaskId)
#             #任务成功，维护兑付表
#             sql = 'update dbo.ABSTrustPaymentOrder set PaymentStatus = N"' + data['status'] +'" where TaskId = ' + str(TaskId)
#             tools.databasesql(sql)
# =============================================================================

            if(data['status'] == '0'): 
                successtimes =successtimes + 1 
                #任务成功，维护task表
                tools.successUpdate(TaskStartTime,TaskEndTime,TaskId)
                #任务成功，维护兑付表
                sql = "update dbo.ABSTrustPaymentOrder set PaymentStatus = N'成功' where TaskId = " + str(TaskId) 
                tools.databasesql(sql)
                tools.log(data['message'] ,'info')
            elif(data['status']  == '1'): 
                errortimes = errortimes + 1 
                errorInfo = data['message']
                #任务失败，维护task表
                tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId)
                #任务失败，维护兑付表
                sql = "update dbo.ABSTrustPaymentOrder set PaymentStatus = N'失败' where TaskId = " + str(TaskId) 
                tools.databasesql(sql)
                tools.log(errorInfo ,'error')
        else: 
            errortimes = errortimes + 1 
            errorInfo = re['msg']
            #任务失败，维护task表
            tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId)
            #任务失败，维护兑付表
            sql = "update dbo.ABSTrustPaymentOrder set PaymentStatus = N'失败' where TaskId = " + str(TaskId) 
            tools.databasesql(sql)
            tools.log(errorInfo ,'error')
        
        tools.log(str(successtimes) + "success(es)," + str(errortimes) + "fail(s)" ,'info')
    return re,data



#兑付状态查询，与其他三个不同，不涉及Task表，只更新兑付表PaymentStatus
def queryPayResult(access_token,requestId): 
    tools.querylog("queryPayResult：",'info')
    sql = "select PaymentId from " + config.sql['assetsPlanPayTable'] + " where PaymentStatus = N'已执行'" 
    #print sql
    datas = tools.database(sql) 
    i = 0 
    paymentIds = [] 
    errortimes = 0 
    successtimes = 0 
    while i <len(datas): 
        paymentIds.append(datas[i][0]) 
        i = i + 1 
    paymentIds = ','.join(paymentIds)
    tools.querylog("paymentIds:"+paymentIds,'info')
    #print paymentIds
    re,data = openapi.getQueryPayResult(paymentIds,access_token,requestId) 
    tools.log(re,'info')
    #测试用例1
    #re = {u'msg': u'', u'data': u"{'status':'1','9E416A55-4221-40CE-BE8E-F988167F8367':'N'}", u'requestId': u'1511848724', u'ret': u'0'}
    #data = {u'status': u'1',u'9E416A55-4221-40CE-BE8E-F988167F8367':u'N'}
    #测试用例2
    #re = {u"ret":u"13008(示例)",u"msg":u"access_token为空(示例)",u"data":u""}
    #data = {u'status':u'',u'message':u''}
    #测试用例3
    #re = {u'msg': u'', u'data': u"{'status':'0'}", u'requestId': u'1511849902', u'ret': u'0'}
    #data = {u'status': u'0'}
    if(re["msg"] == ""): 
        if(data['status'] == '0'): 
            #未完成
            errortimes = errortimes + 1 
            errorInfo = '未完成'
            tools.querylog(errorInfo,'error') 
        elif(data['status'] == '1'): 
            successtimes =successtimes + 1 
            j = 0 
            #已完成，返回多条数据形如{status:'1','id1':'Y(成功)','id2':'F(失败)','id3':'R(退票)'}
            while j < len(data)-1:
                j = j + 1 
                if(data.values()[j] == 'Y'): 
                    sql = "update " + config.sql['assetsPlanPayTable'] +" set PaymentStatus = N'成功' where PaymentId = '" + str(data.keys()[j]) + "'"
                elif(data.values()[j] == 'N'): 
                    sql = "update " + config.sql['assetsPlanPayTable'] +" set PaymentStatus = N'失败' where PaymentId = '" + str(data.keys()[j])+ "'"
                elif(data.values()[j] == 'R'): 
                    sql = "update " + config.sql['assetsPlanPayTable'] +" set PaymentStatus = N'失败' where PaymentId = '" + str(data.keys()[j])+ "'"
                tools.databasesql(sql)
                tools.querylog(data['message'] ,'info')
    else:
        errortimes = errortimes + 1 
        errorInfo = re['msg'] 
        tools.querylog(errorInfo,'error')     
    tools.querylog(str(successtimes) + " success(es)," + str(errortimes) + " fail(s)",'info') 
    return re,data


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

    re,data = openapi.getAssetsSold(config.assetsSold['ASSETS_BAG_NO'],config.assetsSold['PRODUCT_TYPE'],config.assetsSold['DATA_SOURCE'],config.assetsSold['FINISH_BY'],config.assetsSold['FINISH_DATE'],access_token,requestId) 
    tools.log(re,'info')
    TaskEndTime = "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
    if(re['msg'] == ""): 
        if(data['status'] == '0'): 
            successtimes =successtimes + 1 
            #任务成功，维护task表
            tools.successUpdate(TaskStartTime,TaskEndTime,TaskId) 
            tools.log(data['message'] ,'info')
        elif(data['status'] == '1'):
            errortimes = errortimes + 1 
            errorInfo = data['message']
            #任务失败，维护task表
            tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId)
            tools.log(errorInfo ,'error')
    else: 
        errortimes = errortimes + 1 
        errorInfo = data['msg']
        #任务失败，维护task表
        tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId)
        tools.log(errorInfo,'error')
    tools.log(str(successtimes) + "success(es)," + str(errortimes) + "fail(s)" ,'info')
    return re,data
    
    
    
    
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
    if sourceSystem =='ACC': 
        sourceSystem = '2' 
    elif sourceSystem =='FA': 
        sourceSystem = '1'
    adjustFlag = datas[0][2] 
    #数据库里adjustFlag 1是增，-1是减。而PH的接口1是增，2是减
    if adjustFlag =='-1': 
        adjustFlag = '2' 
    adjustNumber = datas[0][3] 
    updatedBy = 'system' 

    re,data = openapi.getAssetsAdjust(assetsBagNo,sourceSystem,adjustFlag,adjustNumber,updatedBy,access_token,requestId) 
    tools.log(re,'info')
    TaskEndTime = "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
    if(re['msg'] == ""): 
        if(data['status'] == '0'): 
            successtimes =successtimes + 1 
            #任务成功，维护task表
            tools.successUpdate(TaskStartTime,TaskEndTime,TaskId)
            tools.log(data['message'],'info')
        elif(data['status'] == '1'): 
            errortimes = errortimes + 1 
            errorInfo = data['message']
            #任务失败，维护task表
            tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId)
            tools.log(errorInfo,'error')
    else: 
        errortimes = errortimes + 1 
        errorInfo = re['msg']
        #任务失败，维护task表
        tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId)
        tools.log(errorInfo,'error')
    tools.log(str(successtimes) + " success(es)," + str(errortimes) + " fail(s)",'info') 
    return re,data 
    
 
def passTask(access_token,requestId,TaskId):
    re= ''
    data = ''
    tools.log(re,'info')
    return re,data
# =============================================================================
# def main(access_token,requestId): 
#     # Task表交互机制============================================================================= 
#     #从Task表里筛选出状态为0或3，方向为1的任务的TaskId和InterfaceType，根据不同的InterfaceType使用checkapi字典映射调用api方法
#     sql = 'select TaskId,InterfaceType from ' + config.DatabaseInfo['DatabaseInterfaceTable'] + ' where Direction = 1 and ( TaskState = 0 or TaskState = 3 )' 
#     datas = tools.database(sql) 
#     #InterfaceType写对应接口的数据库表名，默认值为General,用于调试和特殊任务 
#     checkapi = {'ABSAssetBag':assetsSold 
#                 ,'ABSTrustPaymentOrder':assetsPlanPay 
#                 ,'ABSPresale':assetsAdjust} 
#     i = 0 
#     while i<len(datas): 
#         i = i + 1 
#         data = datas[i-1] 
#         InterfaceType = data[1] 
#         TaskId = data[0] 
#         print "TaskId : "+TaskId
#         re,data = checkapi[InterfaceType](access_token,requestId,TaskId) 
#         print re,data
#         
# 
# 
#     return
#         
#         
# if __name__ == '__main__': 
#     access_token = openapi.getToken() 
#     requestId = str(int(time.time())) 
#     
#     queryPayResult(access_token,requestId) 
#     main(access_token,requestId)
# 
# 
#     # 每隔30分钟轮循机制============================================================================= 
#     # 每隔30分钟运行一次queryPayResult函数
#     sleeptime = tools.sleeptime(0,30,0)
#     while 1 == 1:
#         time.sleep(sleeptime)
#         queryPayResult(access_token,requestId)
