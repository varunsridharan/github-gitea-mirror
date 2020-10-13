import sys

sys.path.insert(1, './src/')

from helper import log,getConfig
from repositorySource import repositorySource

config = getConfig()

if config['repositorySource']:
    log('Setting Up Mirror For Source Github Repository')
    repositorySource()
    log('Finished')
