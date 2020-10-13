import sys

sys.path.insert(1, './src/')

from helper import log,getConfig
from repositoryForked import repositoryForked

config = getConfig()

if config['repositoryForked']:
    log('Setting Up Mirror For Forked Github Repository')
    repositoryForked()
    log('Finished')
