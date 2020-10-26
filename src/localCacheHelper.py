#!/usr/bin/env python

giteaExistsRepos = dict()

from helper import logError,log,getConfig
import json

config = getConfig()

def writeLocalCache(content):
    try:
        with open(config['local_cache']['file_path'], 'w') as file:
            file.write(json.dumps(content, indent=4, sort_keys=True))
    except:
        logError('Unable To Save Local Cache !')

def readLocalCache():
    try:
        with open(config['local_cache']['file_path'],'r') as file:
            filedata = file.read()
            return json.loads(filedata)
    except:
        logError('Local Cache File Not Found !  / Unable To Ready It')

    return dict()

giteaExistsRepos = readLocalCache()
useLocalCache = config['local_cache']['enabled']

def saveLocalCache():
    writeLocalCache(giteaExistsRepos)