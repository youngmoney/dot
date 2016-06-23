# this script is executed when a template is copied
# the current directory is set to the new project

# start a git repo, we'll need this
git init
git add README.md
git add LICENSE.txt

# copy the default license into README
cat LICENSE.txt >> README.md

# replace PROJECT with the name of the folder
projectname=${PWD##*/}
function searchreplace() { cat "$3" | sed "s/$1/$2/g" > "$3".tmp; mv "$3".tmp "$3"; }
searchreplace PROJECT "$projectname" README.md

# get a response
PROMPT_RESPONSE=""
function prompt() {
    while true; do
        read -p "$@: " ans
        case $ans in
            "" ) ;;
            * ) PROMPT_RESPONSE="$ans"; break;;
        esac
    done
}

CONFIRM_RESPONSE=""
function confirm() {
    while true; do
        read -p "$@? " ans
        case $ans in
            [Nn]* ) CONFIRM_RESPONSE="NO"; break;;
            * ) CONFIRM_RESPONSE="YES"; break;;
        esac
    done
}

echo "Let's create an Android Project Together:"
prompt "Target SDK of this project"
TARGET="$PROMPT_RESPONSE"

confirm "Name this project $projectname"
if [ "$CONFIRM_RESPONSE" == "NO" ]; then
    prompt "Name of this project"
    NAME="$PROMPT_RESPONSE"
else
    NAME="$projectname"
fi

confirm 'Name the main activity '"$NAME"'Activity'
if [ "$CONFIRM_RESPONSE" == "NO" ]; then
    prompt "Name of the main activity"
    ACTIVITY="$PROMPT_RESPONSE"
else
    ACTIVITY="$NAME"'Activity'
fi

prompt "Package name (com.example.app)"
PACKAGE="$PROMPT_RESPONSE"

android create project \
--target $TARGET \
--name $NAME \
--path . \
--activity $ACTIVITY \
--package $PACKAGE
