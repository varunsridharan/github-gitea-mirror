#!/usr/bin/env python
# https://github.com/PyGithub/PyGithub
from helper import getConfig,giteaSetRepoTopics,giteaSession,giteaCreateRepo,ghApi,giteaCreateOrg,giteaGetUser,config

config = getConfig()
repo_map = config['repomap']
session = giteaSession()
gh = ghApi()

for repo in gh.get_user().get_starred():
    real_repo = repo.full_name.split('/')[1]
    gitea_dest_user = repo.owner.login
    repo_owner=repo.owner.login

    print('⭐  Star\'ed Repository : {0}'.format(repo.full_name))

    if real_repo in repo_map:
        gitea_dest_user = repo_map[real_repo]

    gitea_uid = giteaGetUser(gitea_dest_user)

    if gitea_uid == 'failed':
        gitea_uid = giteaCreateOrg(gitea_dest_user)

    repo_name = "{0}".format(real_repo)

    m = {
        "repo_name"         : repo_name,
        "description"       : (repo.description or "not really known")[:255],
        "clone_addr"        : repo.clone_url,
        "mirror"            : True,
        "private"           : repo.private,
        "uid"               : gitea_uid,
    }

    giteaCreateRepo(m,repo.private)
    topics = repo.get_topics()
    giteaSetRepoTopics(repo_owner,repo_name,topics)
    print(" ")