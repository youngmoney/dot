#!/usr/bin/env bash
if command -v realpath >/dev/null 2>&1; then
    SCRIPTS="$(dirname $(realpath "${BASH_SOURCE[0]}" 2>/dev/null))"
elif command -v readlink >/dev/null 2>&1; then
    SCRIPTS="$(dirname $(readlink --canonicalize-existing ${BASH_SOURCE[0]}))"
else
    SCRIPTS=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
    if [ "$SCRIPTS" == "${HOME}" ]; then SCRIPTS=~/local/dot; fi
fi
pathadd() { [[ ":$PATH:" != *":$1:"* ]] && PATH="${PATH:+"$PATH:"}$1"; }
pathaddfirst() { [[ ":$PATH:" != *":$1:"* ]] && PATH="$1${PATH:+":$PATH"}"; }

pathaddfirst $SCRIPTS
pathaddfirst $(cd $SCRIPTS/../build; pwd -P)
pathaddfirst /usr/local/bin
pathadd /usr/texbin

export EDITOR=`which vim`; export VISUAL=$EDITOR
export MAILDIR=~/.mail
export KHARD_CONFIG=~/.khard
export LOCALCONF=~/.local-conf

alias todo="build todo";
alias t="build todo"
alias today="status today -l 20";
alias muttr="status mail"
alias gh="build github";
alias gt="build gitolite"
alias s="build search content";
alias f="build search file"
alias ssh-share="build ssh share"
alias dc="cd";
alias ls="ls -1F"
alias gs="git status";
alias gd="git diff"
alias gc="git commit";
alias gl='build git pretty-log'
alias sup="build vagrant sup";
alias refresh=". ~/.bash_profile"
alias n="vim ~/documents/scratch.md '+cd ~/documents'" #+'CtrlP'"
alias vess="vim -R -";
alias vore="vess";
alias vimmd="vess"

ssh-add ~/.ssh/*_rsa > /dev/null 2>&1
command -v launchctl >/dev/null 2>&1 && launchctl unload -w /System/Library/LaunchAgents/com.apple.rcd.plist  > /dev/null 2>&1
command -v brew >/dev/null 2>&1 && source `brew --prefix`/etc/bash_completion

# Git...
git config --global user.name "Taylor L Money"
git config --global core.excludesfile "$SCRIPTS/gitignore"
git config --global color.ui true
if [ "`git version | cut -d. -f1 | cut '-d ' -f3`" == "1" ]; then
    git config --global push.default matching
else
    git config --global push.default simple
fi

# Pretty
if [ ! $LOCALCONF/home.me ]; then COMPNAME=" \e[31m$(id -un)@$(hostname)\e[0m "; fi
export PS1="\[\033[36m\]\u\[\033[m\]:\[\033[33;1m\]\w\[\033[m\]\[\e[1;35m\]\$(build git state)\[\e[0;39m\]$COMPNAME$ "
export CLICOLOR=1: export LSCOLORS=ExFxBxDxCxegedabagacad

ssh-setup() {
    ssh-share $1;
    ssh $1 "mkdir -p ~/local/dot";
    scp -r $SCRIPTS/* $1:~/local/dot/;
    scp -r ~/local/build $1:~/local;
    ssh $1 "
        echo '. ~/local/dot/bashrc'>>.bash_profile;
        echo 'source ~/local/dot/vimrc'>>.vimrc;
        echo 'source-file ~/local/dot/tmux'>>.tmux.conf;
    ";
}

# tmux
alias tmux='tmux -2'; export TERM="xterm-256color"; HISTCONTROL=ignoreboth; SERVE='/tmp/tmux-global'
if command -v tmux>/dev/null && \
   [ -f $LOCALCONF/home.me ] && \
   [[ ! $TERM =~ screen ]] && \
   [ -z "$TMUX" ] && \
   [ "$USER" != "root" ]; then
       tmux -S $SERVE has-session \
       && exec tmux -S $SERVE attach \
       || exec tmux -S $SERVE new -s Global
fi

for f in $LOCALCONF/*.bash; do [ -f "$f" ] && . "$f"; done
PROMPT_COMMAND="build heroku auto-activate; $PROMPT_COMMAND"
