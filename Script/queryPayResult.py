# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 13:34:01 *

@author: *
"""

import openapi 
import time 
import main    
import tools
import config
import pymssql
        
        
if __name__ == '__main__': 
    tools.querylog("queryPayResult Start--",'warn')
    global conn
    conn = pymssql.connect(config.DatabaseInfo['DatabaseUrl'],config.DatabaseInfo['UserName'],config.DatabaseInfo['Password'],config.DatabaseInfo['Database'],charset="UTF-8") 
    access_token = openapi.getToken() 
    tools.querylog("access_token : " + access_token,'info') 
    requestId = str(int(time.time())) 
    
    main.queryPayResult(access_token,requestId,conn)
    conn.close()
    tools.querylog("queryPayResult End--",'warn')