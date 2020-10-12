#!/usr/bin/env python
# https://github.com/PyGithub/PyGithub
from github import Github
import requests
import json
import sys
import os

config = json.loads(open(os.path.expanduser("./config.json")).read().strip())

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
    r = session.put("{0}/api/v1/repos/{1}/{2}/topics".format(config['gitea']['host'],owner,repo_name), data=json.dumps(m))

    if r.status_code == 204:
        print('     ---> SUCCESS : Repository Topics Set')
    else:
        print('     ---> ERROR : Unable To SetRepository Topics')