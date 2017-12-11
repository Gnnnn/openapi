# -*- coding: utf-8 -*-
"""
<<<<<<< HEAD:Script/queryPayResult.py
Created on Thu Nov 30 14:11:38 ****
=======

Created on Wed Nov 29 13:34:01 ****
>>>>>>> 6d016066d07e0a58c7a778636273b2e278395dab:queryPayResult.py

@author: Gn
"""

import openapi 
import time 
import main    
import tools
        
        
if __name__ == '__main__': 
    tools.querylog("queryPayResult Start--",'warn')
    access_token = openapi.getToken() 
    tools.querylog("access_token : " + access_token,'info') 
    requestId = str(int(time.time())) 
    
    main.queryPayResult(access_token,requestId)
    tools.querylog("queryPayResult End--",'warn')
