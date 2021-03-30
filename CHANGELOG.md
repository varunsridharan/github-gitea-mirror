# 📝  Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
<!--
## Unreleased

## 1.0 - 01/02/2020
### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security
-->

## 1.3 - 30/03/2021
* Repository Topics Are Updated Only if new repository created
* Added Sleep Timer for every 50 loops to avoid getting caught in github api limits
* Minor code improvements. 

## 1.2 - 25/10/2020
* Due to `ytdl-org/youtube-dl` **DCMAed** i was able to understand the error & fix it. 
```y
 Traceback (most recent call last):
    File "./mirror-handler/repoStared.py", line 14, in <module>
      repositoryStared()
    File "/github/workspace/mirror-handler/src/repositoryStared.py", line 39, in repositoryStared
      topics = repo.get_topics()
    File "/usr/lib/python3.8/site-packages/github/Repository.py", line 2982, in get_topics
      headers, data = self._requester.requestJsonAndCheck(
    File "/usr/lib/python3.8/site-packages/github/Requester.py", line 317, in requestJsonAndCheck
      return self.__check(
    File "/usr/lib/python3.8/site-packages/github/Requester.py", line 342, in __check
      raise self.__createException(status, responseHeaders, output)
  github.GithubException.GithubException: 451 {"message": "Repository access blocked", "block": {"reason": "dmca", "created_at": "2020-10-23T19:13:29Z", "html_url": "https://github.com/github/dmca/blob/master/2020/10/2020-10-23-RIAA.md"}}
```

## 1.1 - 13/10/2020
### Major Improvements

1. users are created as users instead of org
2. option to run each and every mirror script seperate

```
/usr/bin/python3 $HOME/mirror/gist.py
/usr/bin/python3 $HOME/mirror/giststared.py
/usr/bin/python3 $HOME/mirror/repoSource.py
/usr/bin/python3 $HOME/mirror/repoStared.py
/usr/bin/python3 $HOME/mirror/repoForked.py
```

## 1.0 - 12/10/2020
**First Release**
