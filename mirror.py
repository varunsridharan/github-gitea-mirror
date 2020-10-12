#!/usr/bin/env python
from helper import getConfig
from sourceGist import sourceGist
from repositorySource import repositorySource
from repositoryStared import repositoryStared
from repositoryForked import repositoryForked

config = getConfig()

if config['gist']:
    print('Setting Up Mirror For Github Gists')
    sourceGist()

if config['repositorySource']:
    print('Setting Up Mirror For Source Github Repository')
    #repositorySource()

if config['repositoryStared']:
    print('Setting Up Mirror For Stared Github Repository')
    #repositoryStared()

if config['repositoryForked']:
    print('Setting Up Mirror For Forked Github Repository')
    #repositoryForked()
