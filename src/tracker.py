# This is a program using the CLI to manage a list of tasks

import sys
import json
from datetime import datetime
import os

# Returns the next id for a task. Starts with 1 and gets the next id after the max id present, so is not affected if an id less than current max has been deleted.
def get_id(tasks):
    if len(tasks) == 0:
        return 1
    return max(task['id'] for task in tasks) + 1


def load_tasks():
    if not os.path.exists('tasks.json'):
        return []
    with open('tasks.json') as f:
        return json.load(f)
    

def add_task():
    tasks = load_tasks()
    id = get_id(tasks)
    new_task = {
        'id': id,
        'description': sys.argv[2],
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    tasks.append(new_task)
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)
    return f'Task added successfully ID: {id}'


def delete_task():
    tasks = load_tasks()
    id = int(sys.argv[2])
    if id in [task['id'] for task in tasks]:
        index = [task['id'] for task in tasks].index(id)
        tasks.pop(index)
    else:
        return "ID not present"
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)
        return "Task deleted"
    

def update_task():
    tasks = load_tasks()
    id = int(sys.argv[2])
    if id in [task['id'] for task in tasks]:
        index = [task['id'] for task in tasks].index(id)
        tasks[index]['description'] = sys.argv[3]
    else:
        return "ID not present"
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)
        return "Task updated"
    

def mark_task(status):
    tasks = load_tasks()
    id = int(sys.argv[2])
    if id in [task['id'] for task in tasks]:
        index = [task['id'] for task in tasks].index(id)
        tasks[index]['status'] = status
    else:
        return "ID not present"
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)
        return f'Task marked at {status}' 
    

def list_by_status(status):
    tasks = load_tasks()
    filtered_tasks = []
    for task in tasks:
        if task['status'] == status: filtered_tasks.append(task)
    return filtered_tasks

command = sys.argv[1]

if command == "list":
    print(load_tasks())
elif command == "add":
    print(add_task())
elif command == "delete":
    print(delete_task())
elif command == "update":
    print(update_task())
elif command == "mark-in-progress":
    print(mark_task("in-progress"))
elif command == "mark-done":
    print(mark_task("done"))
elif command == "list-done":
    print(list_by_status("done"))
elif command == "list-todo":
    print(list_by_status("todo"))
elif command == "list-in-progress":
    print(list_by_status("in-progress"))