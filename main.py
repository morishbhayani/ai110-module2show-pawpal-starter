from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def print_tasks(title, tasks):
    print(f"\n{title}")
    print("-" * len(title))
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "Completed" if task.completed else "Incomplete"
        print(
            f"{task.due_date} | {task.time} | {task.description} | {task.pet_name} | "
            f"{task.duration} mins | Priority {task.priority} | {status}"
        )


def main():
    today = date.today()

    owner = Owner("Morish", 120, ["important tasks first"])

    dog = Pet("Bruno", "Dog", 3, "Needs regular walks")
    cat = Pet("Milo", "Cat", 2, "Needs medicine")

    dog.add_task(Task("Morning walk", 20, 3, "daily", "08:00", today))
    dog.add_task(Task("Feeding", 10, 2, "daily", "09:00", today))
    cat.add_task(Task("Medicine", 15, 3, "weekly", "08:00", today))
    cat.add_task(Task("Playtime", 20, 1, "none", "19:00", today))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)

    all_tasks = dog.tasks + cat.tasks
    print_tasks("All Tasks", all_tasks)

    conflicts = scheduler.detect_conflicts(all_tasks)

    print("\nConflict Warnings")
    print("-----------------")
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No conflicts detected.")

    today_plan = scheduler.generate_plan()
    print_tasks("Today's Schedule", today_plan)

    print("\nExplanation:")
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()