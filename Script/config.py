# -*- coding: utf-8 -*- 
<<<<<<< HEAD:Script/config.py
"""
Created on Thu Nov 30 14:11:38 ****

@author: Gn
"""
=======
""" Created on Thu Nov 16 10:39:22 2017 @author: **** *** """ 
>>>>>>> 6d016066d07e0a58c7a778636273b2e278395dab:config.py
import time

#普惠测试环境数据库相关信息
DatabaseInfo = {'DatabaseUrl':'****' 
<<<<<<< HEAD:Script/config.py
                ,'UserName':'**' 
                ,'Password':'**' 
                ,'Database':'**' 
                ,'DatabaseInterfaceTable':'*.**'} 
>>>>>>> 6d016066d07e0a58c7a778636273b2e278395dab:config.py



#涉及到的sql字段和表名
sql = {'assetsPlanPay':'paymentId, trustCode,paymentAmount,payDate,receiverAccount,isRegulated,paymentAccount,sourceSystem,productType' 
       ,'assetsPlanPayTable':'DataInterface.dbo.ABSTrustPaymentOrder' 
       ,'old_queryPayResult':"select SourceSystem,PaymentId into #re from dbo.ABSTrustPaymentOrder where PaymentStatus = N'???' ;select SourceSystem, PaymentId = (stuff((select '?' + cast(PaymentId as nvarchar(500)) from #re where SourceSystem = a.SourceSystem for xml path('')),1,1,'')) from dbo.ABSTrustPaymentOrder a group by SourceSystem;drop table #re" 
       ,'assetsSold':'ASSETS_BAG_NO,PRODUCT_TYPE,DATA_SOURCE,FINISH_BY,FINISH_DATE' 
       ,'assetsSoldTable':'dbo.ABSAssetBag' 
       ,'assetsAdjustSP':'usp_getAssetAdjustInfo'} 


#普惠Openapi的url
url = {'getToken':'http://esg-oauth-stg.paic.com.cn/oauth/oauth2/access_token?client_id=P_PH_ABS_SERVICE&grant_type=client_credentials&client_secret= hgr563Ai' 
       ,'getQueryPayResult':'http://****/open/appsvr/assets/queryPayResult/' 
       ,'getAssetsSold':'http://****/open/appsvr/assets/assetsSold/' 
       ,'getAssetsPlanPay':'http://****/open/appsvr/assets/assetsPlanPay/' 
       ,'getAssetsAdjust':'http://****/open/appsvr/assets/assetsAdjust/'} 


#log文件的文件名
logFileName = str(time.strftime("%Y-%m-%d", time.localtime())) + "-taskMsg.log"
queryFileName = str(time.strftime("%Y-%m-%d", time.localtime())) + "-queryMsg.log"
#logFileName = str(time.strftime("%Y-%m-%d", time.localtime())) + "-Msg.log"


#tasklogfile = 'E:\\openapi\\log\\' + str(taskFileName)
querylogfile = 'E:\\openapi\\log\\' + str(queryFileName)
logfile = 'E:\\openapi\\log\\' + str(logFileName)

#资产正式卖出接口的字段，此处与sql[assetsSold]必须是一一对应关系
