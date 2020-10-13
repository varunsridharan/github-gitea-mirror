import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, "{0}/src/".format(THIS_FOLDER))

from helper import log,getConfig
from repositoryForked import repositoryForked

config = getConfig()

if config['repositoryForked']:
    log('Setting Up Mirror For Forked Github Repository')
    repositoryForked()
    log('Finished')
