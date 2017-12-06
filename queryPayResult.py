# -*- coding: utf-8 -*-
"""
<<<<<<< HEAD
Created on Wed Nov 29 13:34:01 2017

@author: xiaokexiao
=======
Created on Wed Nov 29 13:34:01 ****

@author: Gn
>>>>>>> d74b4a917e6f12e5a81196c1ef62a8cd287889fc
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
