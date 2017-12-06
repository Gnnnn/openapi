# -*- coding: utf-8 -*-
"""

Created on Wed Nov 29 13:34:01 ****

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
