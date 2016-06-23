# this script is executed when a template is copied
# the current directory is set to the new project

# replace PROJECT with the name of the folder

projectname=${PWD##*/}
function searchreplace() { cat "$3" | sed "s/$1/$2/g" > "$3".tmp; mv "$3".tmp "$3"; }
searchreplace PROJECT "$projectname" command
chmod u+x command
mv command "$projectname"
