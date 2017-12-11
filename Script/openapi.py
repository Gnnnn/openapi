# -*- coding: utf-8 -*- 
"""
Created on Thu Nov 30 14:11:38 ****

@author: Gn
"""

import config 
import tools 
import requests 
import json 


#获取access_token值
def getToken(): 
    url = config.url['getToken'] 
    html = requests.get(url) 
    data = json.dumps(html.json()) 
    access_token = json.loads(str(data)).get('data').get('access_token') 
    #tools.log(access_token,'info'); 
    return access_token 


#获取资管计划兑付状态查询api的结果
def getQueryPayResult(paymentIdList,access_token,requestId): 
    url = config.url['getQueryPayResult'] + '?access_token='+access_token+'&request_id='+requestId+'&paymentIdList='+paymentIdList
    #print url
    tools.querylog(url,'info') 
    headers = {'content-type': 'application/json','charset':'UTF-8'}
    r = requests.get(url,headers=headers)
    re,data = tools.strtojson(r.text)
    tools.querylog(re,'info') 
    return re,data 

#获取资产正式卖出api结果
def getAssetsSold(assetsBagNo,productType,sourceSystem,finishBy,finishDate,access_token,requestId): 
    url = config.url['getAssetsSold'] + '?access_token='+access_token+'&request_id='+requestId+'&assetsBagNo='+assetsBagNo+'&sourceSystem='+sourceSystem+'&productType='+productType+'&finishBy='+finishBy+'&finishDate='+finishDate 
    #data = json.dumps({"assetsBagNo":"资产包编号","productType":"产品大类","sourceSystem":"来源系统("1"：FA "2": ACC)","finishBy":"已完成操作人","finishDate":"已完成日期(格式 yyyy-MM-dd )"}) 
    #print url 
    headers = {'content-type': 'application/json','charset':'UTF-8'}
    r = requests.get(url,headers=headers)
    re,data = tools.strtojson(r.text)
    return re,data


#获取资产对付操作api结果
def getAssetsPlanPay(params): 
#def getAssetsPlanPay(access_token,requestId,paymentId, trustCode,paymentAmount,payDate,receiverAccount,isRegulated,paymentAccount,sourceSystem,productType,updatedBy): 
    #url = config.url['getAssetsPlanPay'] + '?access_token='+access_token+'&request_id='+requestId+'&paymentId='+paymentId+'&trustCode='+trustCode+'&trustName='+trustName+'&paymentAmount='+paymentAmount+'&payDate='+payDate+'&receiverAccount='+receiverAccount+'&receiverBank='+receiverBank+'&receiverName='+receiverName+'&isRegulated='+isRegulated+'&paymentOrganization='+paymentOrganization+'&paymentAccount='+paymentAccount+'&sourceSystem='+sourceSystem+'&productType='+productType+'&updatedBy='+updatedBy 
    url = config.url['getAssetsPlanPay']
    #data = json.dumps({"paymentId":"兑付id","trustCode":"资管计划标识","trustName":"资管计划名称","paymentAmount":"兑付金额","payDate":"兑付日期(格式：yyyy-MM-dd)","receiverAccount":"收款账户","receiverBank":"收款账户开户行","receiverName":"收款人","isRegulated":"是否监管账户","paymentOrganization":"法人主体","paymentAccount":"付款账户","sourceSystem":"来源系统","productType":"产品代码","updatedBy" : "操作人"}) 
    headers = {'content-type': 'application/json','charset':'UTF-8'}
    r = requests.get(url,headers=headers,params=params)
    re,data = tools.strtojson(r.text)
    tools.log(re,'info') 
    return re,data 


#获取资产增删api结果
def getAssetsAdjust(assetsBagNo,sourceSystem,adjustFlag,adjustNumber,updatedBy,access_token,requestId): 
    url = config.url['getAssetsAdjust'] + '?access_token='+access_token+'&request_id='+requestId+'&assetsBagNo='+assetsBagNo+'&sourceSystem='+sourceSystem+'&adjustFlag='+adjustFlag+'&adjustNumber='+adjustNumber+'&updatedBy='+updatedBy 
    #data = json.dumps({"assetsBagNo":"资产包编号","sourceSystem":"来源系统("1"：FA "2": ACC)","adjustFlag":"资产调整标记("1"表示增加 "2"表示删除"),"adjustNumber":"资产调成数目","updatedBy" : "操作人"}) 
    tools.log(url,'info')
    headers = {'content-type': 'application/json','charset':'UTF-8'}
    r = requests.get(url,headers=headers)
    re,data = tools.strtojson(r.text)
    tools.log(re,'info') 
    return re,data