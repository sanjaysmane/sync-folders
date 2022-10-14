#!/usr/bin/env python
# coding: utf-8

# # Sync of 2 Folders

# In[4]:


import sys
import os
import shutil
import logging

 
logging.basicConfig(level=logging.INFO, format=f"%(levelname)-8s: \t %(filename)s %(funcName)s %(lineno)s - %(message)s")
logger = logging.getLogger("mylogger")

# logging onto console output
logStreamFormatter = logging.Formatter(
  fmt="%(asctime)s %(message)s", 
  datefmt="%H:%M:%S"
)
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setFormatter(logStreamFormatter)
consoleHandler.setLevel(level=logging.INFO)
logger.addHandler(consoleHandler)


# logging logs to sync.log file
logFileFormatter = logging.Formatter(
    fmt=f"%(levelname)s %(asctime)s (%(relativeCreated)d) \t %(pathname)s F%(funcName)s L%(lineno)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
fileHandler = logging.FileHandler(filename='sync-log.txt')
fileHandler.setFormatter(logFileFormatter)
fileHandler.setLevel(level=logging.INFO)
logger.addHandler(fileHandler)

def copy(path_src, path_dest):
    # copy the file
    try:
        logger.info("From: " + path_src + "To:" + path_dest)
        shutil.copy(path_src, path_dest)
    except:
        logger.info("file exists")
        
def copy_files(path_src, path_dest):
    #this loop will go through every folder and file to copy
    for folderName, subfolders, fileNames in os.walk(path_src):
        for subfolder in subfolders:
            try:
                new_path = folderName.replace(path_src, path_dest) 
                logger.info('created folder at destination: ' + subfolder)
                os.mkdir(new_path+'\\'+subfolder)
            except:
                logger.info("folder exists: " + subfolder)
        for fileName in fileNames:
            new_path = folderName.replace(path_src, path_dest)
            file = folderName + '\\'+ fileName
            copy(file, new_path)
    logger.info('All files and folders from source copied to destination')    

def sync_files(path_src, path_dest):
    for filename in os.listdir(path_dest):
        try:
            filename_s=path_src + os.sep + filename
            filename_t=path_dest + os.sep + filename
            if not os.path.exists(filename_s):   
                if os.path.isdir(filename_t):
                    logger.info('This folder do not exist in source so removed: '+ filename_t)
                    shutil.rmtree(filename_t)
                else:
                    logger.info('This file do not exist in source so removed: '+ filename_t)
                    os.remove(filename_t)      
        except:
                logger.error("something went wrong while removing files")
    
    for folderName, subfolders, fileNames in os.walk(path_dest):
        for subfolder in subfolders:
            try:
                new_path_src = folderName.replace(path_dest, path_src) 
                folderNameSrc = new_path_src+'\\'+subfolder
                new_path_dest = folderName.replace(path_src, path_dest)
                folderNameDest = new_path_dest+'\\'+subfolder
                if not os.path.exists(folderNameSrc):
                    logger.info('this folder does not exist in source, so removing' + folderNameDest)
                    shutil.rmtree(folderNameDest)
                else:
                    for filename in os.listdir(folderNameDest):
                        fileToCheck = folderNameSrc+'\\'+filename
                        fileToRemove = folderNameDest+'\\'+filename
                        if not os.path.exists(fileToCheck):
                            logger.info('this file in subfolder does not exist in source, so removing' + folderNameDest)
                            os.remove(fileToRemove)
            except:
                logger.error("something went wrong while removing file or folder")
    logger.info('all files and folders from destination are matched and updated as per source folder')
    

def sync_folders(source, dest):
    copy_files(source, dest)
    sync_files(source, dest)


# In[6]:


source = 'C:\\Users\sanju\Documents\sync-folders-project\Source_folder'
dest = 'C:\\Users\sanju\Documents\sync-folders-project\Replica_folder'

sync_folders(source, dest)


# In[ ]:




