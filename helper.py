#!/usr/bin/env python
# https://github.com/PyGithub/PyGithub
from github import Github
import requests
import json
import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
config = json.loads(open(os.path.expanduser("{0}/config.json".format(THIS_FOLDER))).read().strip())

def getConfig():
    return config

def giteaHost(endPoint):
    return "{0}/api/v1/{1}".format(config['gitea']['host'],endPoint)

def ghApi():
    return Github(config['github']['accesstoken'])

def giteaSession():
    session = requests.Session()
    session.headers.update({
        "Content-type"  : "application/json",
        "Authorization" : "token {0}".format(config['gitea']['accesstoken']),
    })

    return session


session = giteaSession()

def giteaSetRepoTopics(owner,repo_name,topics):
    m = {
        "topics":topics,
    }

    r = session.put(giteaHost("repos/{0}/{1}/topics".format(owner,repo_name)), data=json.dumps(m))

    if r.status_code == 204:
        print('     ---> Success : Repository Topics Set')
    else:
        print('     ---> Error : Unable To SetRepository Topics')

def giteaCreateRepo(data,isPrivate):
    if isPrivate:
        data["auth_username"]  = config['github']['username']
        data["auth_password"]  = "{0}".format(config['github']['accesstoken'])

    jsonstring = json.dumps(data)
    r = session.post(giteaHost('repos/migrate'), data=jsonstring)

    if r.status_code == 201:
        print("     ---> Success : Repository Created")
        return 'created'
    elif r.status_code == 409:
        print("     ---> Warning : Repository Already Exists")
        return 'exists'
    else:
        print(r.status_code, r.text, jsonstring,"\n\r")
        return 'failure'

def giteaCreateOrg(orgname):
   body = {
	'full_name' : orgname,
	'username'  : orgname,
   }

   jsonstring = json.dumps(body)
   r = session.post(giteaHost('orgs/'), data=jsonstring)

   if r.status_code != 201:
      return 'failed'

   return json.loads(r.text)["id"]

def giteaGetUser(username):
    r = session.get(giteaHost('users/{0}'.format(username)))
    if r.status_code != 200:
        return 'failed'
    return json.loads(r.text)["id"]