#!/usr/bin/env python
# https://github.com/PyGithub/PyGithub
from helper import log,getConfig,giteaCreateUserOrOrg, giteaSetRepoTopics,giteaSession,giteaCreateRepo,ghApi,giteaCreateOrg,giteaGetUser
from github import GithubException
from localCacheHelper import giteaExistsRepos,saveLocalCache

def gistsSource():
    config = getConfig()
    session = giteaSession()
    gh = ghApi()

    default_gist_user = giteaGetUser('gist')
    if default_gist_user == 'failed':
        default_gist_user = giteaCreateOrg('gist')


    for repo in gh.get_user().get_gists():
        if repo.public:
            isPrivate = False
        else:
            isPrivate= True

        log('Gist : {0}/{1}'.format(repo.owner.login,repo.id))

        prefix = ''
        surfix = ''
        gitea_uid = giteaGetUser(repo.owner.login)
        repo_owner = repo.owner.login

        if gitea_uid == 'failed':
            gitea_uid = giteaCreateUserOrOrg(repo.owner.login,repo.owner.type)

        if gitea_uid == 'failed':
            gitea_uid = default_gist_user
            repo_owner = 'gist'

        if len(config['gitea']['gist']['prefix']) != 0:
            prefix = "{0}-".format(config['gitea']['gist']['prefix'])

        if len(config['gitea']['gist']['surfix']) != 0:
            surfix = "-{0}".format(config['gitea']['gist']['surfix'])

        m = {
            "repo_name"         : "{0}{1}{2}".format(prefix,repo.id,surfix),
            "description"       : (repo.description or "not really known")[:255],
            "clone_addr"        : repo.git_pull_url,
            "mirror"            : True,
            "private"           : isPrivate,
            "uid"               : gitea_uid,
        }

        status = giteaCreateRepo(m,isPrivate)

        if status != 'failed':
            try:
                if status != 'exists':
                    giteaExistsRepos['{0}/{1}'.format(repo.owner.login,repo.id)] = "{0}/{1}".format(repo_owner,m['repo_name'])
                    topics = ['gist','{0}-gist'.format(repo_owner)]
                    if isPrivate:
                        topics.append('secret-gist')
                        topics.append('secret-{0}-gist'.format(repo_owner))
                    else:
                        topics.append('public-gist')
                        topics.append('public-{0}-gist'.format(repo_owner))
                    giteaSetRepoTopics(repo_owner,m["repo_name"],topics)
            except GithubException as e:
                print("###[error] ---> Github API Error Occured !")
                print(e)
                print(" ")

        if status == 'failed':
            log(repo)

        log(False)
    saveLocalCache()