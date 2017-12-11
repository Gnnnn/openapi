# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 14:11:38 ****

<<<<<<< HEAD:Script/autoRunAll.py
@author: Gn
=======
@author: ****
>>>>>>> 6d016066d07e0a58c7a778636273b2e278395dab:autoRunAll.py
"""

import threading 
import task
import openapi
import tools
import time


<<<<<<< HEAD:Script/autoRunAll.py
<<<<<<< HEAD
=======
#loops 字典代表了两个函数的运行频率，例如此时为5分钟运行一次函数1，30分钟秒运行一次函数2
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
<<<<<<< HEAD:Script/autoRunAll.py

    #这是一个无限循环
=======
    #无限循环
>>>>>>> 6d016066d07e0a58c7a778636273b2e278395dab:autoRunAll.py
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
