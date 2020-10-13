import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, "{0}/src/".format(THIS_FOLDER))

from helper import getConfig,log
from gistsSource import gistsSource

config = getConfig()

if config['gistsSource']:
    log('Setting Up Mirror For Source Github Gists')
    gistsSource()
    log('Finished')
