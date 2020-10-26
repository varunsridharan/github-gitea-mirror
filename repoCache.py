import sys
import os
import json

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, "{0}/src/".format(THIS_FOLDER))

from helper import giteaGetAllUsersOrgs,logError,log,giteaHost,giteaSession,giteaGetUserRepos
from localCacheHelper import writeLocalCache

giteaExistsRepos = dict()
session = giteaSession()

##########################################
## Fetches All Users & Its Repository  ####
##########################################
log('Fetching All Users & Repositories')
allusers = giteaGetAllUsersOrgs('users')
log(' {0} Users Found '.format(len(allusers)))

for user in allusers:
    username = user['username']
    repos = giteaGetUserRepos(user['id'])

    if repos != 'failed':
        log(' {0} Repository Found For {1}'.format(len(repos),username))
        for repo in repos:
            giteaExistsRepos[ repo['full_name']] = True
    else:
        logError("Unable To Get [{0}] Repository !".format(username))

##########################################
## Fetches All Orgs & Its Repository  ####
##########################################
log('')
log('')
log('')
log('')

log('Fetching All Organizations & Repositories')
allorgs = giteaGetAllUsersOrgs('orgs')

log(' {0} Organizations Found '.format(len(allorgs)))
for org in allorgs:
    username = org['username']
    repos = giteaGetUserRepos(org['id'])

    if repos != 'failed':
        log(' {0} Repository Found For {1}'.format(len(repos),username))
        for repo in repos:
            giteaExistsRepos[ repo['full_name']] = True
    else:
        logError("Unable To Get [{0}] Repository !".format(username))

writeLocalCache(giteaExistsRepos)

