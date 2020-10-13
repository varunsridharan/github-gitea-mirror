import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, "{0}/src/".format(THIS_FOLDER))

from helper import log,getConfig
from repositorySource import repositorySource

config = getConfig()

if config['repositorySource']:
    log('Setting Up Mirror For Source Github Repository')
    repositorySource()
    log('Finished')
