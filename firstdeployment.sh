#!/bin/bash
echo  "Hello man, happy to see you here"
echo "Now you are going to install everything that you need"
echo  "this may require you to insert your root password"
echo  "!-----------IMPORTANT ---------------!"
echo  "if you want to install everything in an enviroment, lunch this script within the enviroment"
echo  "!------------------------------------!"
echo  -n " READY? (y/N)"
read -e WISH
if [ "$WISH" == "y" ] || [ "$WISH" == "Y" ] ; then
    pip install -r requirements.txt
    sudo npm install -g bower
    python manage.py bower_install
else
    echo "you chose no, good bye"
    exit
fi