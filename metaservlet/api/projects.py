from metaservlet.core import call_metaservlet


def project_exists(project_name: str):
  if not project_name:
    raise Exception('Project name can not be empty.')
  request_params = {'projectName': project_name}
  response = call_metaservlet('projectExist' , request_params)
  return response['result']=='true'


def create_project(
    project_name: str,
    storage: str = 'none',
    git_location: str = '',
    git_login: str = '',
    git_password: str = '',
    project_type = 'DI',
):
  if not project_name:
    raise Exception('Project name can not be empty.')
  if not storage:
    raise Exception('<storage> can not be empty.')
  if not storage in ['git', 'none']:
    raise Exception('<storage> invalid value.')
  if storage == 'git':
    if not git_location:
      raise Exception('<git_location> can not be empty.')
    if not git_login:
      raise Exception('<git_login> can not be empty.')
    if not git_password:
      raise Exception('<git_password> can not be empty.')
  
  request_params = {
    'projectName': project_name,
    'storage': storage,
    'projectGitLocation': git_location,
    'gitLogin': git_login,
    'gitPassword': git_password,
    'projectType': project_type,
  }
  if storage=='git': 
    print(request_params)
  else:
    call_metaservlet('createProject' , request_params)


def delete_project(project_name: str) -> dict:
  if not project_name:
    raise Exception('Project name can not be empty.')
  request_params = {'projectName': project_name}
  return call_metaservlet('deleteProject', request_params)
