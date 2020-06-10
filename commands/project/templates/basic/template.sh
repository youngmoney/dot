# this script is executed when a template is copied
# the current directory is set to the new project

# start a git repo, we'll need this
git init
git add README.md
git add LICENSE

# replace PROJECT with the name of the folder
projectname=${PWD##*/}
function searchreplace() { cat "$3" | sed "s/$1/$2/g" > "$3".tmp; mv "$3".tmp "$3"; }
searchreplace PROJECT "${projectname}" README.md
