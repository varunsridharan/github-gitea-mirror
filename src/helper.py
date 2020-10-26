#!/usr/bin/env python
# https://github.com/PyGithub/PyGithub
from github import Github
import requests
import json
import sys
import os
from datetime import datetime

giteaGetUserCache = dict()
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
config = json.loads(open(os.path.expanduser("{0}/config.json".format(THIS_FOLDER))).read().strip())

def logError(val):
    log('')
    log('################# ERROR ####################')
    log(val)
    log('################# ERROR ####################')
    log('')

def log(val):
    if val == False:
        print(" ")
    else:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("[{0}]    {1}".format(dt_string,val))


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
        print(r.text,json.dumps(m))

def giteaSetRepoStar(owner,repo_name):
    r = session.put(giteaHost("user/starred/{0}/{1}/".format(owner,repo_name)))

    if r.status_code == 204:
        print('     ---> Success : Repository Starred')
    else:
        print('     ---> Error : Unable To Star The Repository')

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
        return 'failed'

def giteaCreateOrg(orgname):
   body = {
	'full_name' : orgname,
	'username'  : orgname,
   }

   jsonstring = json.dumps(body)
   r = session.post(giteaHost('orgs/'), data=jsonstring)

   if r.status_code != 201:
      return 'failed'

   giteaGetUserCache["{0}".format(orgname)] = json.loads(r.text)["id"]
   return giteaGetUserCache[orgname]

def giteaCreateUser(orgname):
   body = {
	'email' : "{0}@gitea.dev".format(orgname),
	'full_name'  : orgname,
	'login_name'  : orgname,
	'username'  : orgname,
	'password'  : config['gitea']['default_userpassword'],
	}

   jsonstring = json.dumps(body)
   r = session.post(giteaHost('admin/users'), data=jsonstring)

   if r.status_code != 201:
      return 'failed'

   giteaGetUserCache["{0}".format(orgname)] = json.loads(r.text)["id"]
   return giteaGetUserCache[orgname]

def giteaCreateUserOrOrg(name,type):
    if type == 'User':
        return giteaCreateUser(name)

    return giteaCreateOrg(name)

def giteaGetUser(username):
    if username in giteaGetUserCache:
        return giteaGetUserCache[username]

    r = session.get(giteaHost('users/{0}'.format(username)))
    if r.status_code != 200:
        return 'failed'
    giteaGetUserCache["{0}".format(username)] = json.loads(r.text)["id"]
    return giteaGetUserCache[username]

def giteaGetUserRepos(user_uid):
    loopCount = 1
    results = dict()

    while loopCount != 0 :
        r = session.get(giteaHost('repos/search?uid={0}&page={1}&limit=50'.format(user_uid,loopCount)))

        if r.status_code != 200:
            loopCount = 0
            break

        data = json.loads(r.text)

        if data['ok'] == True:
            if len(data['data']) == 0:
                loopCount = 0
                break
            else:
                if len(results) == 0:
                    results = data['data']
                else:
                    results = results + data['data']

        loopCount += 1

    return results


def giteaGetAllUsersOrgs(type):
    loopCount = 1
    results = dict()

    if type == 'users':
        type = 'admin/users'
    else:
        type = 'orgs'

    while loopCount != 0 :
        r = session.get(giteaHost('{0}?page={1}&limit=50'.format(type,loopCount)))

        if r.status_code != 200:
            loopCount = 0
            break

        data = json.loads(r.text)

        if len(data) == 0:
            loopCount = 0
            break
        else:
            if len(results) == 0:
                results = data
            else:
                results = results + data

        loopCount += 1

    return results
