#!/usr/bin/env bash
if command -v realpath >/dev/null 2>&1; then
    SCRIPT=`realpath "${BASH_SOURCE[0]}" 2>/dev/null`
    SCRIPTS=`dirname "$SCRIPT"`
else
    SCRIPTS=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
fi
export PATH=$SCRIPTS:$PATH
export PATH=$SCRIPTS/../build:$PATH
export PATH=/usr/local/bin:$PATH
export EDITOR=`which vim`; export VISUAL=$EDITOR
export MAILDIR=~/.mail
export KHARD_CONFIG=~/.khard.conf

export PATH=/usr/texbin:$PATH

alias event="build gcalcli event"; alias e="build gcalcli event"
alias todo="build todo"; alias t="build todo"
alias today="status today -l 20"; alias muttr="status mail"
alias gh="build github"; alias gt="build gitolite"
alias s="build search content"; alias f="build search file"
alias ssh-share="build ssh share"
alias dc="cd"; alias ls="ls -1F"
alias gs="git status"; alias gd="git diff"
alias gc="git commit"; alias gl='build git pretty-log'
alias sup="build vagrant sup";
alias refresh="source ~/.bash_profile"
alias n="vim ~/documents/scratch.md '+cd ~/documents'" #+'CtrlP'"

ssh-add ~/.ssh/*_rsa > /dev/null 2>&1
command -v launchctl >/dev/null 2>&1 && launchctl unload -w /System/Library/LaunchAgents/com.apple.rcd.plist  > /dev/null 2>&1
command -v brew >/dev/null 2>&1 && source `brew --prefix`/etc/bash_completion

# Git...
git config --global user.name "Taylor L Money"
git config --global core.excludesfile "$SCRIPTS/gitignore"
git config --global push.default simple
git config --global merge.ff no
git config --global color.ui true

# Pretty
if [ ! -f ~/.my_home ]; then COMPNAME=" \e[31m$(id -un)\e[0m "; fi
export PS1="\[\033[36m\]\u\[\033[m\]:\[\033[33;1m\]\w\[\033[m\]\[\e[1;35m\]\$(build git state)\[\e[0;39m\]$COMPNAME$ "
export CLICOLOR=1: export LSCOLORS=ExFxBxDxCxegedabagacad

# Functions
function ssh-setup { ssh-share $1; ssh $1 "mkdir -p ~/local/scripts"; scp $SCRIPTS/* $1:~/local/scripts/; scp -r ~/local/build $1:~/local; ssh $1 "echo 'source ~/local/scripts/bashrc'>>.bash_profile;echo 'source ~/local/scripts/vimrc'>>.vimrc; echo 'source-file ~/local/scripts/~tmux'>>.tmux.conf; rm -f ~/local/scripts/build; ln -s ~/local/build/build ~/local/scripts/build"; }

# tmux
alias tmux='tmux -2'; export TERM="xterm-256color"; HISTCONTROL=ignoreboth; SERVE='/tmp/tmux-global'
if command -v tmux>/dev/null && [ -f ~/.my_home ] && [[ ! $TERM =~ screen ]] && [ -z "$TMUX" ] && [ "$USER" != "root" ]; then tmux -S $SERVE has-session && exec tmux -S $SERVE attach || exec tmux -S $SERVE new -s Global; fi

for f in $SCRIPTS/secret/*.bash; do source "$f"; done
PROMPT_COMMAND="build heroku auto-activate; $PROMPT_COMMAND"
