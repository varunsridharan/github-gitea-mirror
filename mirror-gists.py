#!/usr/bin/env python
# https://github.com/PyGithub/PyGithub
from github import Github
import requests
import json
import sys
import os
from helper import giteaSetRepoTopics

gist_repo_prefix = 'eeee'
config = json.loads(open(os.path.expanduser("./config.json")).read().strip())
repo_map = config['repomap']
session = requests.Session()
session.headers.update({
    "Content-type"  : "application/json",
    "Authorization" : "token {0}".format(config['gitea']['accesstoken']),
})

gh = Github(config['github']['accesstoken'])

def createOrgInGitea(orgname):
   body = {
	'full_name' : orgname,
	'username'  : orgname,
   }

   jsonstring = json.dumps(body)

   r = session.post("{0}/api/v1/orgs/".format(config['gitea']['host'] ), data=jsonstring)
   if r.status_code != 201:
      return orgname

   return json.loads(r.text)["id"]

r = session.get("{0}/api/v1/users/{1}".format(config['gitea']['host'],'gist' ))
if r.status_code != 200:
    default_gist_user = createOrgInGitea('gist')
else:
    default_gist_user = json.loads(r.text)["id"]

for repo in gh.get_user().get_gists():
    if repo.public:
        isPrivate = False
    else:
        isPrivate= True

    print('Gist : {0}/{1}'.format(repo.owner.login,repo.id))

    r = session.get("{0}/api/v1/users/{1}".format(config['gitea']['host'],repo.owner.login ))
    if r.status_code != 200:
        gitea_uid = default_gist_user
        repo_owner = 'gist'
    else:
        gitea_uid = json.loads(r.text)["id"]
        repo_owner = repo.owner.login


    m = {
        "repo_name"         : "{0}-{1}".format(gist_repo_prefix,repo.id),
        "description"       : (repo.description or "not really known")[:255],
        "clone_addr"        : repo.git_pull_url,
        "mirror"            : True,
        "private"           : isPrivate,
        "uid"               : gitea_uid,
    }

    if isPrivate:
        m["auth_username"]  = config['github']['username']
        m["auth_password"]  = "{0}".format(config['github']['accesstoken'])

    jsonstring = json.dumps(m)
    r = session.post("{0}/api/v1/repos/migrate".format(config['gitea']['host']), data=jsonstring)

    if r.status_code == 201:
        if isPrivate:
            topics = ['gist','secret-gist',"{0}-gist".format(repo_owner),"secret-{0}-gist".format(repo_owner)]
        else:
            topics = ['gist','public-gist',"{0}-gist".format(repo_owner),"public-{0}-gist".format(repo_owner)]
        print("     ---> Success : Repository Created\n\r".format(repo_owner,repo.id))
        giteaSetRepoTopics(repo_owner,m["repo_name"],topics)
    elif r.status_code == 409:
        print("     ---> Warning : Repository Already Exists\n\r".format(repo_owner,repo.id))
    else:
        print(r.status_code, r.text, jsonstring,"\n\r")

    print(" ")