#!/usr/bin/env python
# coding: utf-8

import sys
import os
import shutil
import schedule
import time
import loggerMod
import click


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
    #check destination folder with source for exact match
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
    copy_files(source, dest, logger=loggerMod.loggerFunc(logfilename))
    sync_files(source, dest, logger=loggerMod.loggerFunc(logfilename))
    

def sync(source_folder, dest, name_of_logfile, interval_mins):
    # runs sync_folders function at given time interval in minutes
    minutes = int(interval_mins)
    schedule.every(minutes).minutes.do(lambda : sync_folders(source_folder, dest, name_of_logfile))
    while True:
        schedule.run_pending()
        time.sleep(300)

@click.command()
@click.argument('source_folder')
@click.argument('destination_folder',)
@click.argument('name_of_logfile')
@click.argument('interval_mins')


def main(source_folder, destination_folder, name_of_logfile, interval_mins):
    doSync = sync(source_folder, destination_folder, name_of_logfile, interval_mins)
    print(f"The sync is in progress..")


if __name__ == '__main__':
    main()