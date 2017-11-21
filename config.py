# -*- coding: utf-8 -*- 
""" Created on Thu Nov 16 10:39:22 2017 @author: pub_Treasurysystem xiaokexiao """ 

#普惠测试环境数据库相关信息
DatabaseInfo = {'DatabaseUrl':'' 
                ,'UserName':'' 
                ,'Password':'' 
                ,'Database':'DataInterface' 
                ,'DatabaseInterfaceTable':'dbo.DataInterfaceTask'} 



#涉及到的sql字段和表名
sql = {'assetsPlanPay':'PaymentId,TrustCode,TrustName,PaymentAmount,PayDate,ReceiverAccount,ReceiverBank,ReceiverName,IsRegulated,PaymentOrganization,PaymentAccount,SourceSystem,ProductType ' 
       ,'assetsPlanPayTable':'DataInterface.dbo.ABSTrustPaymentOrder' 
       ,'old_queryPayResult':"select SourceSystem,PaymentId into #re from dbo.ABSTrustPaymentOrder where PaymentStatus = N'???' ;select SourceSystem, PaymentId = (stuff((select '?' + cast(PaymentId as nvarchar(500)) from #re where SourceSystem = a.SourceSystem for xml path('')),1,1,'')) from dbo.ABSTrustPaymentOrder a group by SourceSystem;drop table #re" 
       ,'assetsSold':'ASSETS_BAG_NO,PRODUCT_TYPE,DATA_SOURCE,FINISH_BY,FINISH_DATE' 
       ,'assetsSoldTable':'dbo.ABSAssetBag' 
       ,'assetsAdjustSP':'usp_getAssetAdjustInfo'} 


#普惠Openapi的url
url = {'getToken':'###' 
       ,'getQueryPayResult':'###' 
       ,'getAssetsSold':'###'
       ,'getAssetsPlanPay':'###'
       ,'getAssetsAdjust':'###'} 


#log文件的文件名
logfile = 'msg.log' 


#资产正式卖出接口的字段，此处与sql[assetsSold]必须是一一对应关系
assetsSold = {'ASSETS_BAG_NO':'' ,'PRODUCT_TYPE':'' ,'DATA_SOURCE':'' ,'FINISH_BY':'' ,'FINISH_DATE':''} 
