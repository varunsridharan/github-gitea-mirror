import sys

sys.path.insert(1, './src/')

from helper import getConfig,log
from gistsSource import gistsSource

config = getConfig()

if config['gistsSource']:
    log('Setting Up Mirror For Source Github Gists')
    gistsSource()
    log('Finished')
