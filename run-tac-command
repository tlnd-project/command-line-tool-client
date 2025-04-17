#!/bin/sh
#-------------------------------------------------------------------------------
# Shell Script: run-tac-command
# Description: This script  is used  to  run automated tasks on Talend Platform.
#              Requires of two parameters,  command name  to  be  run and source
#              data file name in Talend8 repository
# Author: Ricardo Bermudez Bermudez
# Usage:./run-tac-command -c $command_name -f $remote_file_name_and_extension
# Version: 0.1
#-------------------------------------------------------------------------------

timestamp=`date +"%Y-%m-%dT%H.%M.%S.%2N"`
current_user=`whoami`
tac_automation_home='/apps/TAL/Scripts/tac-automation'

if [ $current_user != taladm ];
then
  echo -e "Command should be executed as taladm user\n"
  exit 3
fi

if [ ! -e "$tac_automation_home/venv/bin/activate" ]; 
then
  echo -e "Run the setup script to install all the project dependencies and updates."
  exit 3
fi

while getopts f:c: option;
do
  case "$option"
  in
    f)file="$OPTARG";;
    c)tac_command="$OPTARG";;
  esac
done

log_path="$tac_automation_home/logs/$tac_command.$timestamp.log"
source $tac_automation_home/venv/bin/activate
python $tac_automation_home/bootstrap.py $tac_command $file | tee $log_path
echo "Execution logs are available in $log_path"
