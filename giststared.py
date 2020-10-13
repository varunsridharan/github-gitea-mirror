import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, "{0}/src/".format(THIS_FOLDER))

from helper import log,getConfig
from gistsStared import gistsStared

config = getConfig()

if config['gistsStared']:
    log('Setting Up Mirror For Stared Github Gists')
    gistsStared()
    log('Finished')
