#!/usr/bin/env python
from helper import getConfig
from gistsSource import gistsSource
from gistsStared import gistsStared
from repositorySource import repositorySource
from repositoryStared import repositoryStared
from repositoryForked import repositoryForked

config = getConfig()

if config['gistsSource']:
    print('Setting Up Mirror For Source Github Gists')
    gistsSource()

if config['gistsStared']:
    print('Setting Up Mirror For Stared Github Gists')
    #gistsStared()

if config['repositorySource']:
    print('Setting Up Mirror For Source Github Repository')
    #repositorySource()

if config['repositoryStared']:
    print('Setting Up Mirror For Stared Github Repository')
    #repositoryStared()

if config['repositoryForked']:
    print('Setting Up Mirror For Forked Github Repository')
    #repositoryForked()
