# this script is executed when a template is copied
# the current directory is set to the new project
# inheritance:
build project basic .

# add to the git repo
git add MANIFEST.in
git add bin
git add docs
git add project/*
git add setup.py

# replace PROJECT with the name of the folder
projectname=${PWD##*/}
function searchreplace() { cat "$3" | sed "s/$1/$2/g" > "$3".tmp; mv "$3".tmp "$3"; }
searchreplace PROJECT "$projectname" setup.py
mv project/project.py project/"$projectname".py
mv project "$projectname"

# convert from markdown to rst
pandoc -i README.md -o README.rst
rm README.md
