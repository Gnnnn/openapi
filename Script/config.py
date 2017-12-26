# -*- coding: utf-8 -*- 
""" Created on Thu Nov 16 10:39:22 * @author: * * """ 
import time

#测试环境数据库相关信息
DatabaseInfo = {'DatabaseUrl':'**' 
                ,'UserName':'*' 
                ,'Password':'*' 
                ,'Database':'*' 
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
url = {'getToken':'*' 
       ,'getQueryPayResult':'*' 
       ,'getAssetsSold':'*' 
       ,'getAssetsPlanPay':'*' 
       ,'getAssetsAdjust':'*'} 


#log文件的文件名
logFileName = str(time.strftime("%Y-%m-%d", time.localtime())) + "-taskMsg.log"
queryFileName = str(time.strftime("%Y-%m-%d", time.localtime())) + "-queryMsg.log"
#logFileName = str(time.strftime("%Y-%m-%d", time.localtime())) + "-Msg.log"


#tasklogfile = 'E:\\openapi\\log\\' + str(taskFileName)
querylogfile = 'E:\\openapi\\log\\' + str(queryFileName)
logfile = 'E:\\openapi\\log\\' + str(logFileName)

#资产正式卖出接口的字段，此处与sql[assetsSold]必须是一一对应关系
assetsSold = {'ASSETS_BAG_NO':'' ,'PRODUCT_TYPE':'' ,'DATA_SOURCE':'' ,'FINISH_BY':'' ,'FINISH_DATE':'','BAG_SCALE':''}