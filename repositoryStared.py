import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, "{0}/src/".format(THIS_FOLDER))

from helper import log,getConfig
from repositoryStared import repositoryStared

config = getConfig()

if config['repositoryStared']:
    log('Setting Up Mirror For Stared Github Repository')
    repositoryStared()
    log('Finished')
