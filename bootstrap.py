import sys
from utilities.files_management import load_file
from automation.core import run_command

command = sys.argv[1]
batch_csv_source = sys.argv[2]

#1. Load module (required command).
module_path = f'automation.command.{command}'
module_service = __import__(module_path, fromlist=['object'])
command_function = getattr(module_service, 'process_item')

#2. Load remote CSV.
data_list = load_file(batch_csv_source)

#3. Run process.
run_command(command_function, data_list)
