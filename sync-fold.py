#!/usr/bin/env python
# coding: utf-8

# # Sync of 2 Folders

# In[9]:


import sys
import os
import shutil
import logging
import logging.config
import schedule
import time


# logging logs to sync.log file
def loggerFunc(fname):
    logging_config = { 
        'version': 1,
        'formatters': { 
            'standard': { 
                'format': '%(asctime)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': { 
            'stream': { 
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'file': { 
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': fname
            },
        },
        'loggers': { 
            __name__: { 
                'handlers': ['stream', 'file'],
                'level': 'INFO',
                'propagate': False
            },
        } 
    }
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    return logger

def copy_files(path_src, path_dest, logger):
    #this loop will go through every folder and file to copy
    for folderName, subfolders, fileNames in os.walk(path_src):
        for subfolder in subfolders:
            try:
                new_path = folderName.replace(path_src, path_dest) 
                logger.info('created folder at destination: ' + subfolder)
                os.mkdir(new_path+'\\'+subfolder)
            except:
                logger.warning("folder exists: " + subfolder)
        for fileName in fileNames:
            new_path = folderName.replace(path_src, path_dest)
            file = folderName + '\\'+ fileName
            shutil.copy(file, new_path)
            logger.info(file + ' is copied to: ' + new_path)
    logger.info('All files and folders from source copied to destination')    

def sync_files(path_src, path_dest, logger):
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

    
def sync_folders(source, dest, logfilename):
    copy_files(source, dest, logger =loggerFunc(logfilename))
    sync_files(source, dest, logger =loggerFunc(logfilename))
    

def syncOnTimeInterval(source, dest, logfilename, mins):
    # runs sync_folders function at given time interval in minutes
    schedule.every(mins).minutes.do(lambda : sync_folders(source, dest, logfilename))
    while True:
        schedule.run_pending()
        time.sleep(300)


# In[ ]:


source = 'C:\\Users\sanju\Documents\sync-folders-project\Source_folder'
dest = 'C:\\Users\sanju\Documents\sync-folders-project\Replica_folder'

syncOnTimeInterval(source, dest, 'loggerNew.txt', 1)


# In[ ]:




