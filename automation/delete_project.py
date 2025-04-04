from metaservlet.api import delete_project


def main(projects: list):
  for project in projects:
    print('-----', project)
    project_name = project[0]
    try:
      delete_project(project_name)
    except Exception as e:
      print('ERROR: ', e.args)
      continue