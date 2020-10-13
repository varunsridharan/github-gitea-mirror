import sys

sys.path.insert(1, './src/')

from helper import log,getConfig
from repositoryStared import repositoryStared

config = getConfig()

if config['repositoryStared']:
    log('Setting Up Mirror For Stared Github Repository')
    repositoryStared()
    log('Finished')
