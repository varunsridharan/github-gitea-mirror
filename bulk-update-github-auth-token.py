#!/usr/bin/env python
import glob
from pathlib import Path

BASEPATH = "/var/lib/gitea/gitea-repositories/"
SEARCH_PATH = "*/*/config"
SEARCH_TOKEN = "OLD_GITHUB_AUTH_TOKEN"
REPLACE_TOKEN = "NEW_GITHUB_AUTH_TOKEN"

for path in glob.glob("{0}{1}".format(BASEPATH,SEARCH_PATH), recursive=True):
    LOG_HEAD = path.replace(BASEPATH,"")
    print("Updating : {0}".format(LOG_HEAD.replace(".git/config","")))

    with open(path, 'r') as file :
        filedata = file.read()

    filedata = filedata.replace("{0}@".format(SEARCH_TOKEN),"{0}@".format(REPLACE_TOKEN))

    with open(path, 'w') as file:
        file.write(filedata)

    print(" ")