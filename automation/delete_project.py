from metaservlet.api import delete_project


def main(projects: list):
  for project in projects:
    print('-----', project)
    try:
      delete_project(project[0])
    except Exception as e:
      print('ERROR: ', e.args)
      continue