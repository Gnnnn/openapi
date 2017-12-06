# -*- coding: utf-8 -*- 
""" Created on Thu Nov 16 10:48:45 2017 @author: pub_Treasurysystem xiaokexiao """ 

import config 
import pymssql 
import json
import logging 
import logging.handlers 


#连接数据库-查询
def database(sql): 
    conn = pymssql.connect(config.DatabaseInfo['DatabaseUrl'],config.DatabaseInfo['UserName'],config.DatabaseInfo['Password'],config.DatabaseInfo['Database']) 
    cursor = conn.cursor() 
    if not cursor: 
        raise Exception('数据库连接失败！') 
    cursor.execute(sql) 
    results = cursor.fetchall() 
    cursor.close() 
    conn.close() 
    i = 0 
    datas = [] 
    while i < len(results): 
        i = i+1 
        result = results[i-1] 
        result = checkdata(result) 
        datas.append(result) 
    return datas 



#连接数据库-增删改
def databasesql(sql): 
    conn = pymssql.connect(config.DatabaseInfo['DatabaseUrl'],config.DatabaseInfo['UserName'],config.DatabaseInfo['Password'],config.DatabaseInfo['Database']) 
    cursor = conn.cursor() 
    if not cursor: 
        raise Exception('数据库连接失败！') 
    cursor.execute(sql) 
    conn.commit() 
    cursor.close() 
    conn.close() 
    return 


#用于将sql查出的不同格式的数据格式化为[[str],[str],[str],[str]]
def checkdata(data): 
    j = 0 
    datas = []    
    while j < len(data): 
        if isinstance(data[j],unicode): 
            items = data[j].encode('unicode-escape') 
            datas.append(items) 
            j += 1 
        elif isinstance(data[j],(float,bool)) or data[j] is None: 
            item = str(data[j]) 
            datas.append(item) 
            j += 1 
        else: 
            item = str(data[j]) 
            datas.append(item) 
            j += 1 
    return datas


#Python logging库类
class FinalLogger: 
    logger=None 
    levels={"n":logging.NOTSET, "d":logging.DEBUG, "i":logging.INFO, "w":logging.WARN, "e":logging.ERROR, "c":logging.CRITICAL} 
    log_level="d" 
    log_file=config.logfile 
    log_max_byte=10*1024*1024; 
    log_backup_count=5 

    @staticmethod 
    def getLogger(): 
        if FinalLogger.logger is not None: 
            return FinalLogger.logger 
        FinalLogger.logger=logging.Logger("oggingmodule.FinalLogger") 
        log_handler=logging.handlers.RotatingFileHandler(filename=FinalLogger.log_file,maxBytes=FinalLogger.log_max_byte,backupCount=FinalLogger.log_backup_count) 
        log_fmt=logging.Formatter("[%(asctime)s] [%(filename)s:%(lineno)s] [%(levelname)s] %(message)s") 
        log_handler.setFormatter(log_fmt) 
        FinalLogger.logger.addHandler(log_handler) 
        FinalLogger.logger.setLevel(FinalLogger.levels.get(FinalLogger.log_level)) 
        return FinalLogger.logger 


class QueryFinalLogger: 
    logger=None 
    levels={"n":logging.NOTSET, "d":logging.DEBUG, "i":logging.INFO, "w":logging.WARN, "e":logging.ERROR, "c":logging.CRITICAL} 
    log_level="d" 
    log_file=config.querylogfile 
    log_max_byte=10*1024*1024; 
    log_backup_count=5 

    @staticmethod 
    def getLogger(): 
        if QueryFinalLogger.logger is not None: 
            return QueryFinalLogger.logger 
        QueryFinalLogger.logger=logging.Logger("oggingmodule.QueryFinalLogger") 
        log_handler=logging.handlers.RotatingFileHandler(filename=QueryFinalLogger.log_file,maxBytes=QueryFinalLogger.log_max_byte,backupCount=FinalLogger.log_backup_count) 
        log_fmt=logging.Formatter("[%(asctime)s] [%(filename)s:%(lineno)s] [%(levelname)s] %(message)s") 
        log_handler.setFormatter(log_fmt) 
        QueryFinalLogger.logger.addHandler(log_handler) 
        QueryFinalLogger.logger.setLevel(QueryFinalLogger.levels.get(QueryFinalLogger.log_level)) 
        return QueryFinalLogger.logger 

#log函数，输入格式
# ============================================================================= 
# log("thisisadebugmsg!",'debug') 
# log("thisisainfomsg!",'info') 
# log("thisisawarnmsg!",'warn') 
# log("thisisaerrormsg!",'error') 
# log("thisisacriticalmsg!",'critical') 
# ============================================================================= 
#log函数，输出格式
# ============================================================================= 
# console：msg
# logFile: [datetime] [fileName:lineNum] [level] msg
# logFile: [2017-11-20 14:51:24,470] [tools.py:93] [INFO] this is the msg
# ============================================================================= 
#输出文件在config中定义
def log(msg,typeName): 
    print msg; 
    logger=FinalLogger.getLogger() 
    if typeName == 'debug': 
        logger.debug(msg) 
    elif typeName == 'info': 
        logger.info(msg) 
    elif typeName == 'warn': 
        logger.warn(msg) 
    elif typeName == 'error': 
        logger.error(msg) 
    elif typeName == 'critical': 
        logger.critical(msg) 
    return msg



def querylog(msg,typeName): 
    print msg; 
    logger=QueryFinalLogger.getLogger() 
    if typeName == 'debug': 
        logger.debug(msg) 
    elif typeName == 'info': 
        logger.info(msg) 
    elif typeName == 'warn': 
        logger.warn(msg) 
    elif typeName == 'error': 
        logger.error(msg) 
    elif typeName == 'critical': 
        logger.critical(msg) 
    return msg


#任务开始处理，更新task表状态为 TaskState = 1,TaskStartTime = TaskStartTime
def taskStartUpdate(TaskStartTime,TaskId):
    sql = 'update '+ config.DatabaseInfo['DatabaseInterfaceTable'] + ' set TaskState = 1,TaskStartTime = ' + TaskStartTime +' where TaskId = ' + str(TaskId) 
    databasesql(sql)
    return 


#任务处理成功，更新task表状态为 TaskState = 2,TaskStartTime = TaskStartTime,TaskEndTime = TaskEndTime
def successUpdate(TaskStartTime,TaskEndTime,TaskId):
    sql = 'update '+ config.DatabaseInfo['DatabaseInterfaceTable'] + ' set TaskState = 2,TaskStartTime = ' + TaskStartTime+ ',TaskEndTime = '+ TaskEndTime + ' where TaskId = ' + str(TaskId)
    databasesql(sql)
    return 


#任务处理失败，更新task表状态为 TaskState = 3,TaskStartTime = TaskStartTime,TaskEndTime = TaskEndTime
def failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId):
    sql = 'update '+ config.DatabaseInfo['DatabaseInterfaceTable'] + ' set TaskState = 3,TaskStartTime = ' + TaskStartTime + ',TaskEndTime = '+ TaskEndTime + ",ErrorInfo = N'" + errorInfo + "' where TaskId = " + str(TaskId) 
    sql= sql.encode('unicode-escape') 
    databasesql(sql) 
    return 

#返回时间
def sleeptime(hour,min,sec):
    return hour*3600 + min*60 + sec;

def strtojson(r):
    dataStart = r.find("{",1)
    dataEnd = r.find("}",-1)
    if dataStart == -1:
        re = json.loads(r)
        data = {u'status':u'',u'message':u''}
        return re,data
    
    else:
        data = r[dataStart:dataEnd-1]
        rightdata = data.replace("\"","'")
        rightjson = r.replace(data,rightdata)
        re = json.loads(rightjson)
        #data = str(re['data'])
        data = data.replace("'","\"")
        data = json.loads(data)
        return re,data