# -*- coding: utf-8 -*-
"""
<<<<<<< HEAD
Created on Thu Nov 30 14:11:38 2017

@author: xiaokexiao
>>>>>>> d74b4a917e6f12e5a81196c1ef62a8cd287889fc
"""

import threading 
import task
import openapi
import tools
import time


<<<<<<< HEAD
#loops ????????????????????5????????1?30?????????2
loops = [300,1800 ] 
  
def runTask(nloop, nsec): 
    tools.log("DataInterfaceTask Start--",'warn')
    access_token = openapi.getToken() 
    requestId = str(int(time.time())) 
    
    task.task(access_token,requestId)
    tools.log("DataInterfaceTask End--",'warn')
    time.sleep(nsec)
 
    
def runQuery(nloop, nsec): 
    tools.log("queryPayResult Start--",'warn')
    access_token = openapi.getToken() 
    requestId = str(int(time.time())) 
    
    main.queryPayResult(access_token,requestId)
    tools.log("queryPayResult End--",'warn')
    time.sleep(nsec) 
    

def main(): 
<<<<<<< HEAD
    #????????
    while 1 == 1:
        threads = [] 
        nloops = range(len(loops)) 
        
        for i in nloops: 
            if i == 0:
                t = threading.Thread(target=runTask, args=(i, loops[i])) 
            elif i == 1:
                t = threading.Thread(target=runQuery, args=(i, loops[i])) 
            threads.append(t) 
           
        for i in nloops:      # start threads 
            threads[i].start() 
           
        for i in nloops:      # wait for all 
            threads[i].join()    # threads to finish 
            
   
if __name__ == '__main__': 
    main()
