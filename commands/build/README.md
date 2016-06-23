build
=====

Author: Taylor L Money

`build` is a super command designed to help me with projects (creating and running) hopefully it is helpful for you as well.

The purpose of BUILD is that it holds a bunch of helpful commands which one can
alias to make easier to use, for instance to make github faster use `alias
gh="build github"` and then use `gh` to access the github command.

Install
-------

Clone the repo, and add it to your path, and possibly your .bashrc

```
git clone git@github.com/youngmoney/build.git build
export PATH="build:$PATH"
build -h
```

Usage
-----

To see a list of commands, type:

```
build -h
```


```
Available Commands

  ctag
    generate ctags for current directory
    if arguments present then recursively
    search through directories and find tags
    for each git repo
    (ctags must be install in /usr/local/bin)

  droid
    log [activity]: build (debug), start activity, watch logs
    debug activity: build (debug), start activity, open jdb
    up [emulator]: start emulator (default: ice
    down [emulator]: kill emulator (default all)

  gcalcli
    event: same as gcalcli but has shortcuts:
          no argument creates a new event interactively
          -e edit event (same as gcalcli edit)
          -s search events (gcalcli search)
          -d delete event (gcalcli delete)
    cache: caches the next event and agenda into ~/.gcal_next, ~/.gcal
    next [mins]: next event title, or if minutes then all events for mins

  git
    branch-name: active branch name
    branch-relationship: branch upstream relationship (ahead)
    state: 'name (relationship)'
    pretty-log: show git log in a nice colorful format

  github
    usage: github [-h] [--debug] {repo,collab,key,setup} ...
    
    positional arguments:
      {repo,collab,key,setup}
    
    optional arguments:
      -h, --help            show this help message and exit
      --debug

  gitolite
    list: list gitolite repo's
    create <repo>: create <repo> on the server
    edit <repo>: edit the permisions for <repo>
    delete <repo>: delete <repo> from config
    destroy <repo>: delete config and removes from server
    add-remote <repo>: add the gitolite remote to the repo
    setup: runs the setup script

  heroku
    start heroku project (with python virtualenv)
    pull database connection and environment

  kindle
    notes: echo out clippings (notes/quotes) by book
    books: uses kindlegen to convert optional inputs to mobi
          if kindle is present moves any converted books (even previous)

  license
    create a license (default MIT)
    call with --list to see options

  mac
    ssh [off]: no args enables remote login, false or no diables
    addcontact: add a contact
    notify [title]: reads stdin and makes notification with title
    battery: percent

  mail
    ssh: no args enables remote login, false or no diables
    mail: drop in replacement for mail to send through mail.app
    email: create a new email in markdown
    readmail: echo the body of the current mail.app message

  markdown
    usage: markdown [-h] [-o] filename
    
    Wrapper for Pandoc (must have pandoc installed)
    
    positional arguments:
      filename    Markdown file (if 'bib' then all .ris files in the directory
                  will be processes into a YAML bib for pandoc)
    
    optional arguments:
      -h, --help  show this help message and exit
      -o          Open Created File

  project
    create a project from the passed template
    in current directory (or second arg)
    call with no args to see options

  search
    content <search>: show highlighted content matches
    file <search>: just the files
    file-find <search>: just the files (using find)
    file-grep <search>: just the files (using grep)
    file-mdfind <search>: just the files (using mdfind)

  ssh
    share <remote> [<key.pub>]: sends the key to the remote

  vagrant
    sup: up; ssh; halt (auto up, and halt after ssh is over)

  xcode
    build: build the current project in and open xcode
    clang: create clang_complete file for xcode project
```

License
-------

The MIT License (MIT)

Copyright (c) 2014 Taylor L Money

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


