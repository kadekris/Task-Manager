import json
import os
from datetime import datetime

TASK_FILE = 'tasks.json'

# Function to load tasks from JSON
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as file:
            return json.load(file)
    return []

# Function to save tasks to JSON
def save_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Function to get the next available task ID
def get_next_task_id(tasks):
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1
        
def add_task(description):
    tasks = load_tasks()
    task = {
        'id': get_next_task_id(tasks),
        'description': description,
        'status': 'todo',
        'createdAt': str(datetime.now()),
        'updatedAt': str(datetime.now())
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{description}' added successfully.")
    
def update_task(task_id, new_description=None, new_status=None):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            if new_description:
                task['description'] = new_description
            if new_status:
                task['status'] = new_status
            task['updatedAt'] = str(datetime.now())
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
    print(f"Task with ID {task_id} not found.")

def mark_task_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = str(datetime.now())
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}.")
            return
    print(f"Task with ID {task_id} not found.") 
    
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully.")
    
def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task['status'] == status]
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(f"{task['id']}: {task['description']} - {task['status']} (Created: {task['createdAt']}, Updated: {task['updatedAt']})")

import argparse

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    parser.add_argument('action', choices=['add', 'update', 'delete', 'list', 'mark'], help="Action to perform")
    parser.add_argument('--task', help="Task description or ID")
    parser.add_argument('--description', help="New description for task")
    parser.add_argument('--status', choices=['todo', 'in-progress', 'done'], help="New status for task")
    
    args = parser.parse_args()

    if args.action == 'add' and args.task:
        add_task(args.task)
    elif args.action == 'update' and args.task:
        new_description = args.description
        new_status = args.status
        update_task(int(args.task), new_description, new_status)
    elif args.action == 'delete' and args.task:
        delete_task(int(args.task))
    elif args.action == 'list':
        list_tasks(args.status)
    elif args.action == 'mark' and args.task and args.status:
        mark_task_status(int(args.task), args.status)
    else:
        print("Invalid usage. Try --help for more details.")

if __name__ == '__main__':
    main()
    