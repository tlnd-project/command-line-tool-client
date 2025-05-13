#!/bin/sh
#-------------------------------------------------------------------------------
# Shell Script: setup.sh
# Description: This script is used tac-automation project and its dependencies.
# Author: Ricardo Bermudez Bermudez
# Usage:./setup.sh
# Version: 0.1
#-------------------------------------------------------------------------------

current_user=`whoami`
tac_automation_home='/apps/TAL/Scripts/tac-automation'
dtcc_nexus_repo=https://repo.dtcc.com/repository/dtcc-pypi-public/simple
dtcc_nexus_host=repo.dtcc.com

if [ $current_user != taladm ];
then
  echo -e "Command should be executed as taladm user\n"
  exit 3
fi

if [ ! -e "$tac_automation_home/venv/bin/activate" ]; 
then
  python3 -m venv $tac_automation_home/venv
fi

mkdir $tac_automation_home/logs
source $tac_automation_home/venv/bin/activate
pip install --upgrade pip -i $dtcc_nexus_repo --trusted-host $dtcc_nexus_host
pip install -r $tac_automation_home/requirements.txt -i $dtcc_nexus_repo --trusted-host $dtcc_nexus_host

echo "Installation is finished!, you can run the project using run-tac-command"