import sys

sys.path.insert(1, './src/')

from helper import log,getConfig
from gistsStared import gistsStared

config = getConfig()

if config['gistsStared']:
    log('Setting Up Mirror For Stared Github Gists')
    gistsStared()
    log('Finished')
