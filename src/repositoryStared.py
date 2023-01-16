#!/usr/bin/env python
# https://github.com/PyGithub/PyGithub
from helper import isBlacklistedRepository, log,getConfig,giteaSetRepoTopics,giteaSession,giteaSetRepoStar,giteaCreateRepo,ghApi,giteaCreateUserOrOrg,giteaGetUser,config
from github import GithubException
from localCacheHelper import giteaExistsRepos,saveLocalCache
import time

def repositoryStared():
    config = getConfig()
    repo_map = config['repomap']
    session = giteaSession()
    gh = ghApi()
    loop_count = 0

    for repo in gh.get_user().get_starred():
        loop_count = loop_count + 1
        real_repo = repo.full_name.split('/')[1]
        gitea_dest_user = repo.owner.login
        repo_owner=repo.owner.login

        log('⭐  Star\'ed Repository : {0}'.format(repo.full_name))

        if isBlacklistedRepository(repo.full_name):
            print("     ---> Warning : Repository Matches Blacklist")
            continue

        if real_repo in repo_map:
            gitea_dest_user = repo_map[real_repo]

        gitea_uid = giteaGetUser(gitea_dest_user)

        if gitea_uid == 'failed':
            gitea_uid = giteaCreateUserOrOrg(gitea_dest_user,repo.owner.type)

        repo_name = "{0}".format(real_repo)

        m = {
            "repo_name"         : repo_name,
            "description"       : (repo.description or "not really known")[:255],
            "clone_addr"        : repo.clone_url,
            "mirror"            : True,
            "private"           : repo.private,
            "uid"               : gitea_uid,
        }

        status = giteaCreateRepo(m,repo.private,True)
        if status != 'failed':
            try:
                if status != 'exists':
                    giteaExistsRepos['{0}/{1}'.format(repo.owner.login,repo_name)] = "{0}/{1}".format(gitea_dest_user,repo_name)
                    topics = repo.get_topics()
                    topics.append('starred-repo')
                    topics.append('starred-{0}-repo'.format(repo_owner))
                    giteaSetRepoTopics(repo_owner,repo_name,topics)
                    giteaSetRepoStar(repo_owner,repo_name)
            except GithubException as e:
                print("###[error] ---> Github API Error Occured !")
                print(e)
                print(" ")
        else:
            log(repo)
            
        if loop_count % 10 == 0:
            log(False)
            log('Time To Sleep For 10 Seconds')
            log(False)
            time.sleep(5)
        else:
            log(False)
    saveLocalCache()
