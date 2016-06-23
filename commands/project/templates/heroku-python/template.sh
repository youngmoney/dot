# this script is executed when a template is copied
# the current directory is set to the new project
# inheritance:
build project basic .

# add to the git repo
git add Procfile
git add app.py
git add requirements.txt

mv env .env
mv gitignore .gitignore

# replace PROJECT with the name of the folder
projectname=${PWD##*/}
function searchreplace() { cat "$3" | sed "s/$1/$2/g" > "$3".tmp; mv "$3".tmp "$3"; }
searchreplace PROJECT "$projectname" app.py

mv pre-commit .git/hooks

virtualenv --no-site-packages venv
heroku create "$projectname"
build heroku
