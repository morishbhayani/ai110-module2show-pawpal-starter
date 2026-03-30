from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Morish", 60, ["important tasks first"])

dog = Pet("Bruno", "Dog", 3, "Needs regular walks")
dog.add_task(Task("Morning walk", 20, 3, "daily"))
dog.add_task(Task("Feeding", 10, 2, "daily"))
dog.add_task(Task("Grooming", 40, 1, "weekly"))

cat = Pet("Milo", "Cat", 2, "Needs medicine")
cat.add_task(Task("Medicine", 15, 3, "daily"))
cat.add_task(Task("Playtime", 20, 1, "daily"))

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler(owner)
plan = scheduler.generate_plan()

for task in plan:
    print(task.description, task.duration, task.priority)

print(scheduler.explain_plan())