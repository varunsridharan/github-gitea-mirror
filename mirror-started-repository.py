#!/usr/bin/env python
# https://github.com/PyGithub/PyGithub
from github import Github
import requests
import json
import sys
import os

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
      jsonstring = json.dumps(r.text)
      print("Cannot Create ORG '{0}' Status {1}".format(orgname,jsonstring), file=sys.stderr)
      exit(1)

   return json.loads(r.text)["id"]

for repo in gh.get_user().get_starred():
    real_repo = repo.full_name.split('/')[1]
    if real_repo in repo_map:
        gitea_dest_user = repo_map[real_repo]
    else:
        gitea_dest_user = repo.owner.login

    r = session.get("{0}/api/v1/users/{1}".format(config['gitea']['host'],gitea_dest_user ))
    if r.status_code != 200:
        gitea_uid = createOrgInGitea(gitea_dest_user)
    else:
        gitea_uid = json.loads(r.text)["id"]

    m = {
        "repo_name"         : "{0}".format(real_repo),
        "description"       : (repo.description or "not really known")[:255],
        "clone_addr"        : repo.clone_url,
        "mirror"            : True,
        "private"           : repo.private,
        "uid"               : gitea_uid,
    }

    if repo.private:
        m["auth_username"]  = config['github']['username']
        m["auth_password"]  = "{0}".format(config['github']['accesstoken'])

    jsonstring = json.dumps(m)

    r = session.post("{0}/api/v1/repos/migrate".format(config['gitea']['host']), data=jsonstring)

    if r.status_code == 201:
        print("[Success] : {0} Repository Created\n\r".format(repo.full_name))
    elif r.status_code == 409:
        print("[Warning] : {0} Repository Already Exists\n\r".format(repo.full_name))
    else:
        print(r.status_code, r.text, jsonstring,"\n\r")