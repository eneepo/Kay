"""cli — an argparse front-end over the task domain.

Usage:
  python -m taskservice.cli add "buy milk"
  python -m taskservice.cli list [--status todo|done]
  python -m taskservice.cli done 1
  python -m taskservice.cli rm 1
  python -m taskservice.cli --file other.json list
"""
import argparse
import sys

from . import domain, storage


def build_parser():
    parser = argparse.ArgumentParser(prog="tasks", description="A tiny task manager.")
    parser.add_argument("--file", default="tasks.json", help="JSON store path")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("title")

    p_list = sub.add_parser("list", help="list tasks")
    p_list.add_argument("--status", choices=["todo", "done"])

    p_done = sub.add_parser("done", help="mark a task complete")
    p_done.add_argument("id", type=int)

    p_rm = sub.add_parser("rm", help="remove a task")
    p_rm.add_argument("id", type=int)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        tasks = storage.load(args.file)
        if args.command == "add":
            task = domain.add(tasks, args.title)
            storage.save(args.file, tasks)
            print(f"added #{task['id']}: {task['title']}")
        elif args.command == "list":
            shown = domain.list_tasks(tasks, args.status)
            if not shown:
                print("(no tasks)")
            for t in shown:
                mark = "x" if t["done"] else " "
                print(f"[{mark}] #{t['id']} {t['title']}")
        elif args.command == "done":
            task = domain.complete(tasks, args.id)
            storage.save(args.file, tasks)
            print(f"completed #{task['id']}: {task['title']}")
        elif args.command == "rm":
            domain.delete(tasks, args.id)
            storage.save(args.file, tasks)
            print(f"removed #{args.id}")
    except (domain.TaskError, storage.StorageError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
