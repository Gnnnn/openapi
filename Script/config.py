# -*- coding: utf-8 -*- 
""" Created on Thu Nov 16 10:39:22 2017 @author: pub_Treasurysystem xiaokexiao """ 
import time

#普惠测试环境数据库相关信息
DatabaseInfo = {'DatabaseUrl':'215.128.17.106:2433' 
                ,'UserName':'PHabsdbopr' 
                ,'Password':'Hk123456' 
                ,'Database':'DataInterface' 
                ,'DatabaseInterfaceTable':'dbo.DataInterfaceTask'} 



#涉及到的sql字段和表名
sql = {'assetsPlanPay':'paymentId, trustCode,paymentAmount,payDate,receiverAccount,isRegulated,paymentAccount,sourceSystem,productType' 
       ,'assetsPlanPayTable':'DataInterface.dbo.ABSTrustPaymentOrder' 
       ,'old_queryPayResult':"select SourceSystem,PaymentId into #re from dbo.ABSTrustPaymentOrder where PaymentStatus = N'???' ;select SourceSystem, PaymentId = (stuff((select '?' + cast(PaymentId as nvarchar(500)) from #re where SourceSystem = a.SourceSystem for xml path('')),1,1,'')) from dbo.ABSTrustPaymentOrder a group by SourceSystem;drop table #re" 
       ,'assetsSold':'ASSETS_BAG_NO,PRODUCT_TYPE,DATA_SOURCE,FINISH_BY,FINISH_DATE,BAG_SCALE' 
       ,'assetsSoldTable':'DataInterface.dbo.ABSAssetBag'
       ,'assetsAdjustTable':'DataInterface.dbo.ABSPresale'
       ,'assetsAdjustSP':'usp_getAssetAdjustInfo'} 


#普惠Openapi的url
url = {'getToken':'http://esg-oauth-stg.paic.com.cn/oauth/oauth2/access_token?client_id=P_PH_ABS_SERVICE&grant_type=client_credentials&client_secret= hgr563Ai' 
       ,'getQueryPayResult':'http://esg-open-stg.paic.com.cn/open/appsvr/assets/queryPayResult/' 
       ,'getAssetsSold':'http://esg-open-stg.paic.com.cn/open/appsvr/assets/assetsSold/' 
       ,'getAssetsPlanPay':'http://esg-open-stg.paic.com.cn/open/appsvr/assets/assetsPlanPay/' 
       ,'getAssetsAdjust':'http://esg-open-stg.paic.com.cn/open/appsvr/assets/assetsAdjust/'} 


#log文件的文件名
logFileName = str(time.strftime("%Y-%m-%d", time.localtime())) + "-taskMsg.log"
queryFileName = str(time.strftime("%Y-%m-%d", time.localtime())) + "-queryMsg.log"
#logFileName = str(time.strftime("%Y-%m-%d", time.localtime())) + "-Msg.log"


#tasklogfile = 'E:\\openapi\\log\\' + str(taskFileName)
querylogfile = 'E:\\openapi\\log\\' + str(queryFileName)
logfile = 'E:\\openapi\\log\\' + str(logFileName)

#资产正式卖出接口的字段，此处与sql[assetsSold]必须是一一对应关系
assetsSold = {'ASSETS_BAG_NO':'' ,'PRODUCT_TYPE':'' ,'DATA_SOURCE':'' ,'FINISH_BY':'' ,'FINISH_DATE':'','BAG_SCALE':''}