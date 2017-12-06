# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 14:11:38 2017

@author: ****
"""

import threading 
import task
import openapi
import tools
import time


<<<<<<< HEAD
#loops 字典代表了两个函数的运行频率，例如第一个函数每隔5分钟跑一次，第二个每隔30分钟跑一次
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
    #无限循环
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
