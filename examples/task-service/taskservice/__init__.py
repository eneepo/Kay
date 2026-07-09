"""task-service — a tiny task manager with a shared core and two front-ends.

Layers (each is a Kay capability):
  storage      load/save tasks to a JSON file
  domain       add / list / complete / delete, with validation
  cli          argparse front-end  (python -m taskservice.cli)
  api          stdlib HTTP front-end (python -m taskservice.api)
"""
