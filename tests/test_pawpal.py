from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task("Medicine", 15, 3, "daily", "07:30", date.today())
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Bruno", "Dog", 3, "Needs regular walks")
    task = Task("Morning walk", 20, 3, "daily", "08:00", date.today())

    initial_count = len(pet.tasks)
    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1


def test_sort_by_time_returns_tasks_in_chronological_order():
    today = date.today()
    owner = Owner("Morish", 120)
    scheduler = Scheduler(owner)

    tasks = [
        Task("Evening walk", 20, 2, "daily", "18:00", today, "Bruno"),
        Task("Medicine", 15, 3, "daily", "07:30", today, "Milo"),
        Task("Feeding", 10, 2, "daily", "09:00", today, "Bruno"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [task.time for task in sorted_tasks] == ["07:30", "09:00", "18:00"]


def test_daily_recurrence_creates_next_day_task():
    today = date.today()
    owner = Owner("Morish", 120)
    pet = Pet("Bruno", "Dog", 3, "Needs regular walks")
    task = Task("Morning walk", 20, 3, "daily", "08:00", today)

    pet.add_task(task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    new_task = scheduler.mark_task_complete("Bruno", "Morning walk")

    assert task.completed is True
    assert new_task is not None
    assert new_task.description == "Morning walk"
    assert new_task.due_date == today + timedelta(days=1)
    assert new_task.completed is False
    assert len(pet.tasks) == 2


def test_conflict_detection_flags_duplicate_times():
    today = date.today()
    owner = Owner("Morish", 120)
    dog = Pet("Bruno", "Dog", 3)
    cat = Pet("Milo", "Cat", 2)

    task1 = Task("Morning walk", 20, 3, "daily", "08:00", today)
    task2 = Task("Medicine", 15, 3, "weekly", "08:00", today)

    dog.add_task(task1)
    cat.add_task(task2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts(dog.tasks + cat.tasks)

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]
    assert "Morning walk" in conflicts[0]
    assert "Medicine" in conflicts[0]