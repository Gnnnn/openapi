# -*- coding: utf-8 -*- 
" Created on Thu Nov 16 10:39:07 2017 @author: pub_Treasurysystem xiaokexiao " 

import config 
import openapi 
import tools 
import time 
import json 


#资产兑付操作
def assetsPlanPay(access_token,requestId,TaskId,conn): 
    #任务开始，维护task表
    TaskStartTime= "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
    tools.taskStartUpdate(TaskStartTime,TaskId,conn)

    sql = 'select ' + config.sql['assetsPlanPay'] + ' from ' + config.sql['assetsPlanPayTable'] + ' where TaskId = ' + TaskId 
    tools.log(sql,'info')
    datas = tools.database(conn,sql); 
    tools.log(datas,'info')
    assetsPlanPayre = [] 
    #此处循环是当一个TaskId查出多条数据时，对每条数据调用该api
    i = 0 
    errortimes = 0   
    successtimes = 0 
    if len(datas) == 0:
        errortimes = errortimes + 1 
        tools.log('there is no data in '+ config.sql['assetsPlanPayTable'] + ' where TaskId = '+TaskId,'error')
        errorInfo = 'there is no data in '+ config.sql['assetsPlanPayTable'] + ' where TaskId = '+TaskId
        tools.noDataUpdate(TaskStartTime,errorInfo,TaskId,conn)
        tools.log(str(successtimes) + "success(es), + str(errortimes) + fail(s)" ,'info')
    while i < len(datas): 
        i = i+1 
        data = datas[i-1] 
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
        #paymentId = paymentId.replace("-",)
        params = {"access_token":access_toke,
                  "requestId":requestId
                  "paymentId":paymentId
                  "trustCode":trustCode
                  "paymentAmount":paymentAmount
                  "payDate":payDate
                  "receiverAccount":receiverAccount
                  "isRegulated":isRegulated
                  "paymentAccount":paymentAccount
                  "sourceSystem":sourceSystem
                  ,productType:productType
                  "updatedBy":updatedBy}
        #re,data = openapi.getAssetsPlanPay(access_token,requestId,paymentId, trustCode,paymentAmount,payDate,receiverAccount,isRegulated,paymentAccount,sourceSystem,productType,updatedBy) 
        re,data = openapi.getAssetsPlanPay(params)
        tools.log(re,'info')
        assetsPlanPayre.append(re) 
        TaskEndTime = "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
        if(re['msg'] == ""): 

            if(data['status'] == '0'): 
                successtimes =successtimes + 1 
                #任务成功，维护task表
                tools.successUpdate(TaskStartTime,TaskEndTime,TaskId,conn)
                #任务成功，维护兑付表
                sql = "update dbo.ABSTrustPaymentOrder set PaymentStatus = N'已执行' where TaskId = " + str(TaskId) 
                tools.databasesql(conn,sql)
                tools.log(data['message'] ,'info')
            elif(data['status']  == '1'): 
                errortimes = errortimes + 1 
                errorInfo = data['message']
                #任务失败，维护task表
                tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId,conn)
                #任务失败，不做兑付表更改处理
                tools.log(errorInfo ,'error')
        else: 
            errortimes = errortimes + 1 
            errorInfo = re['msg']
            #任务失败，维护task表
            tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId,conn)
            #任务失败，不做兑付表更改处理
            tools.log(errorInfo ,'error')
        
        tools.log(str(successtimes) + "success(es), + str(errortimes) + fail(s)" ,'info')
    return assetsPlanPayre



#兑付状态查询，与其他三个不同，不涉及Task表，只更新兑付表PaymentStatus
def queryPayResult(access_token,requestId,conn): 
    tools.querylog("queryPayResult：",'info')
    sql = "select PaymentId from " + config.sql['assetsPlanPayTable'] + " where PaymentStatus = N'已执行'" 
    tools.log(sql,'info')
    datas = tools.database(conn,sql) 
    print datas
    i = 0 
    paymentIds = [] 
    errortimes = 0 
    successtimes = 0 
    re = ''
    data = ''
    #普惠要求没有数据也给他传空值
#    if len(datas) == 0:
#        successtimes = successtimes + 1
#        tools.querylog("there is no data where PaymentStatus = 已执行",'info') 
#        tools.querylog(str(successtimes) + " success(es), + str(errortimes) +  fail(s)",'info') 
#        return re,data
    while i <len(datas): 
        paymentIds.append(datas[i][0]) 
        i = i + 1 
    paymentIds = ','.join(paymentIds)
    tools.querylog("paymentIds:"+paymentIds,'info')
    #print paymentIds
    re,data = openapi.getQueryPayResult(paymentIds,access_token,requestId) 
    tools.querylog(re,'info')
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
                elif(data.values()[j] == 'F'): 
                    sql = "update " + config.sql['assetsPlanPayTable'] +" set PaymentStatus = N'失败' where PaymentId = '" + str(data.keys()[j])+ "'"
                elif(data.values()[j] == 'R'): 
                    sql = "update " + config.sql['assetsPlanPayTable'] +" set PaymentStatus = N'失败' where PaymentId = '" + str(data.keys()[j])+ "'"
                tools.databasesql(conn,sql)
#                tools.querylog(data['message'] ,'info')
    else:
        errortimes = errortimes + 1 
        errorInfo = re['msg'] 
        tools.querylog(errorInfo,'error')     
    tools.querylog(str(successtimes) + " success(es), + str(errortimes) +  fail(s)",'info') 
    return re,data


#资产正式卖出
def assetsSold(access_token,requestId,TaskId,conn): 
    #任务开始，维护task表
    TaskStartTime= "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
    tools.taskStartUpdate(TaskStartTime,TaskId,conn)

    sql = 'select '+ config.sql['assetsSold'] + ' from ' + config.sql['assetsSoldTable'] + ' where TaskId = ' + str(TaskId) 
    datas = tools.database(conn,sql) 
    errortimes = 0 
    successtimes = 0 
    if datas == []: 
        errortimes = errortimes + 1 
        tools.log('there is no data in '+ config.sql['assetsSoldTable'] + ' where TaskId = '+TaskId,'error')
        errorInfo = 'there is no data in '+ config.sql['assetsSoldTable'] + ' where TaskId = '+TaskId
        tools.noDataUpdate(TaskStartTime,errorInfo,TaskId,conn)
        tools.log(str(successtimes) + "success(es), + str(errortimes) + fail(s)" ,'info')
        return  
    #只有一条数据，只取第一条
    data = datas[0] 
    config.assetsSold['ASSETS_BAG_NO'] = data[0] 
    config.assetsSold['PRODUCT_TYPE'] = data[1] 
    if data[2] == 'FA':
        config.assetsSold['DATA_SOURCE'] = '1'
    elif data[2] == 'ACC':
        config.assetsSold['DATA_SOURCE'] = '2'
    config.assetsSold['FINISH_BY'] = data[3] 
    config.assetsSold['FINISH_DATE'] = data[4] 
    config.assetsSold['BAG_SCALE'] = data[5] 
    if config.assetsSold['BAG_SCALE'] == '':
        config.assetsSold['BAG_SCALE'] = 0
    re,data = openapi.getAssetsSold(config.assetsSold['ASSETS_BAG_NO'],config.assetsSold['PRODUCT_TYPE'],config.assetsSold['DATA_SOURCE'],config.assetsSold['FINISH_BY'],config.assetsSold['FINISH_DATE'],config.assetsSold['BAG_SCALE'],access_token,requestId) 
    tools.log(re,'info')
    TaskEndTime = "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
    if(re['msg'] == ""): 
        if(data['status'] == '0'): 
            successtimes =successtimes + 1 
            #任务成功，维护task表
            tools.successUpdate(TaskStartTime,TaskEndTime,TaskId,conn) 
            tools.log(data['message'] ,'info')
        elif(data['status'] == '1'):
            errortimes = errortimes + 1 
            errorInfo = data['message']
            #任务失败，维护task表
            tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId,conn)
            tools.log(errorInfo ,'error')
    else: 
        errortimes = errortimes + 1 
        errorInfo = data['msg']
        #任务失败，维护task表
        tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId,conn)
        tools.log(errorInfo,'error')
    tools.log(str(successtimes) + "success(es), + str(errortimes) + fail(s)" ,'info')
    return re,data
    
    
    
    
#资产卖出前的增删
def assetsAdjust(access_token,requestId,TaskId,conn): 
    TaskId_OPENAPI = TaskId
    sql = "select TaskId from "+ config.DatabaseInfo['DatabaseInterfaceTable'] +" where CreatedTime = (select CreatedTime from "+ config.DatabaseInfo['DatabaseInterfaceTable'] +" where TaskId = " + TaskId + ") and TaskChannel in('Kettle','') and InterfaceType = (select InterfaceType from "+ config.DatabaseInfo['DatabaseInterfaceTable'] +" where TaskId = " + TaskId + ")"
    print sql
    TaskId = tools.database(conn,sql)
    print TaskId
    if TaskId == []:
        tools.log('there is no related TaskId!','error')
        return 
    TaskId = TaskId[0][0]
    print TaskId
    #任务开始，维护task表
    TaskStartTime= "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
    tools.taskStartUpdate(TaskStartTime,TaskId_OPENAPI,conn)
    errortimes = 0
    successtimes = 0
    sql = 'exec ' + config.sql['assetsAdjustSP'] + ' ' + str(TaskId) 
    datas = tools.database(conn,sql) 
    if datas == []: 
        errortimes = errortimes + 1 
        tools.log('there is no data in '+ config.sql['assetsAdjustTable'] + ' where TaskId = '+TaskId,'error')
        errorInfo = 'there is no data in '+ config.sql['assetsAdjustTable'] + ' where TaskId = '+TaskId
        tools.noDataUpdate(TaskStartTime,errorInfo,TaskId,conn)
        tools.log(str(successtimes) + "success(es), + str(errortimes) + fail(s)" ,'info')
        return 
    errortimes = 0 
    successtimes = 0 

    assetsBagNo = datas[0][0] 
    sourceSystem = datas[0][1] 
    if sourceSystem =='ACC': 
        sourceSystem = '2' 
    elif sourceSystem =='FA': 
        sourceSystem = '1'
#    adjustFlag = datas[0][2] 
#    #数据库里adjustFlag 1是增，-1是减。而PH的接口1是增，2是减
#    if adjustFlag =='-1': 
#        adjustFlag = '2' 
    addNumber = datas[0][2] 
    delNumber = datas[0][3] 
    updatedBy = 'system' 
    re,data = openapi.getAssetsAdjust(assetsBagNo,sourceSystem,addNumber,delNumber,updatedBy,access_token,requestId)
    tools.log(re,'info')
    TaskEndTime = "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'" 
    if(re['msg'] == ""): 
        if(data['status'] == '0'): 
            successtimes =successtimes + 1 
            #任务成功，维护task表
            tools.successUpdate(TaskStartTime,TaskEndTime,TaskId_OPENAPI,conn)
            tools.log(data['message'],'info')
        elif(data['status'] == '1'): 
            errortimes = errortimes + 1 
            errorInfo = data['message']
            #任务失败，维护task表
            tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId_OPENAPI,conn)
            tools.log(errorInfo,'error')
    else: 
        errortimes = errortimes + 1 
        errorInfo = re['msg']
        #任务失败，维护task表
        tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId_OPENAPI,conn)
        tools.log(errorInfo,'error')
    tools.log(str(successtimes) + " success(es), + str(errortimes) +  fail(s)",'info') 
    return re,data 
    
 
def passTask(access_token,requestId,TaskId,conn):
    re= ''
    data = ''
    tools.log(re,'info')
    TaskStartTime= "\'" + time.strftime("%Y-%m-%d %X",time.localtime()) + "\'"  
    tools.passUpdate(TaskStartTime,TaskId,conn)
    return re,data
