#!/bin/sh
current_user=`whoami`
if [[ $current_user != 'taladm']];
then
  echo -e "Command should be executed as taladm user\n"
  exit 3
fi

if [ ! -e "./venv/bin/activate" ]; 
then
  python3 -m venv venv
fi

python3 -m venv venv
source venv/bin/activate
pip -m pip install --upgrade pip
pip install -r requirements.txt

echo "Installation is finished!, you can run the project using run-tac-command"