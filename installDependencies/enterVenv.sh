#!/bin/bash

path=$(dirname "${BASH_SOURCE[0]}")


if [ ! -d ${path}/.venv ]; then
 echo -e "Creating virtual environnement \n" 
 python3 -m venv ${path}/.venv
 [ $? -ne 0 ] && echo "Could not create venv. Exiting." && return -1
fi 

echo -e "Entering virtual environnement \n"
source ${path}/.venv/bin/activate
[ $? -ne 0 ] && echo "Could not activate venv. Exiting." && return -1
echo -e "Installing dependencies \n"
pip3 install -r ${path}/requirements.txt
[ $? -ne 0 ] && echo "Could not install all the dependencies. Exiting." && return -1

git submodule init
[ $? -ne 0 ] && echo "Could not init submodules. Exiting." && return -1
git submodule update
[ $? -ne 0 ] && echo "Could not update submodules. Exiting." && return -1
echo "Jobe done! You are in the virtual environnement"
return 0
