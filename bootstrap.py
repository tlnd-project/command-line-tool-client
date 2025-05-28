import sys
from utilities.bitbucket_files_management import list_csv_file_rows
from automation.automation_core import run_command

command = sys.argv[1]
batch_csv_source = sys.argv[2]

#1. Load module (required command).
module_path = f'automation.command.{command}'
module_service = __import__(module_path, fromlist=['object'])
command_function = getattr(module_service, 'process_item')

#2. Load remote CSV.
data_list = list_csv_file_rows(batch_csv_source)

# TODO: add verification WARNING. if the "sso" in TAC_URL, maybe crashed the run command

#3. Run process.
run_command(command_function, data_list)
