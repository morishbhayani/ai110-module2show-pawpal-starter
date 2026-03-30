from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    description: str
    duration: int
    priority: int
    frequency: str
    time: str
    due_date: date
    pet_name: str = ""
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.completed = False

    def update_task(
        self,
        description: Optional[str] = None,
        duration: Optional[int] = None,
        priority: Optional[int] = None,
        frequency: Optional[str] = None,
        time: Optional[str] = None,
        due_date: Optional[date] = None,
    ) -> None:
        """Update the task details."""
        if description is not None:
            self.description = description
        if duration is not None:
            self.duration = duration
        if priority is not None:
            self.priority = priority
        if frequency is not None:
            self.frequency = frequency
        if time is not None:
            self.time = time
        if due_date is not None:
            self.due_date = due_date


@dataclass
class Pet:
    pet_name: str
    pet_type: str
    age: int
    care_notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def update_pet_info(
        self,
        pet_name: Optional[str] = None,
        pet_type: Optional[str] = None,
        age: Optional[int] = None,
        care_notes: Optional[str] = None,
    ) -> None:
        """Update the pet's information."""
        if pet_name is not None:
            self.pet_name = pet_name
        if pet_type is not None:
            self.pet_type = pet_type
        if age is not None:
            self.age = age
        if care_notes is not None:
            self.care_notes = care_notes

    def add_task(self, task: Task) -> None:
        """Add a task to the pet."""
        task.pet_name = self.pet_name
        self.tasks.append(task)

    def get_incomplete_tasks(self) -> List[Task]:
        """Return all incomplete tasks for the pet."""
        return [task for task in self.tasks if not task.completed]

    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return [task for task in self.tasks if task.completed == completed]


@dataclass
class Owner:
    owner_name: str
    available_time: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def update_preferences(self, preferences: List[str]) -> None:
        """Update the owner's preferences."""
        self.preferences = preferences

    def set_available_time(self, available_time: int) -> None:
        """Set the owner's available time."""
        self.available_time = available_time

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all incomplete tasks across the owner's pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_incomplete_tasks())
        return all_tasks

    def get_tasks_by_pet_name(self, pet_name: str) -> List[Task]:
        """Return all tasks for a specific pet name."""
        for pet in self.pets:
            if pet.pet_name == pet_name:
                return pet.tasks
        return []


@dataclass
class Scheduler:
    owner: Owner
    daily_plan: List[Task] = field(default_factory=list)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by time in HH:MM format."""
        return sorted(tasks, key=lambda task: task.time)

    def filter_by_status(self, tasks: List[Task], completed: bool) -> List[Task]:
        """Filter tasks by completion status."""
        return [task for task in tasks if task.completed == completed]

    def filter_by_pet_name(self, tasks: List[Task], pet_name: str) -> List[Task]:
        """Filter tasks by pet name."""
        return [task for task in tasks if task.pet_name == pet_name]

    def get_due_today_tasks(self) -> List[Task]:
        """Return incomplete tasks due today."""
        today = date.today()
        all_tasks = self.owner.get_all_tasks()
        return [task for task in all_tasks if task.due_date == today]

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return warning messages for tasks scheduled at the same date and time."""
        warnings: List[str] = []
        sorted_tasks = sorted(tasks, key=lambda task: (task.due_date, task.time, task.pet_name))

        for i in range(len(sorted_tasks)):
            for j in range(i + 1, len(sorted_tasks)):
                first = sorted_tasks[i]
                second = sorted_tasks[j]

                if first.due_date == second.due_date and first.time == second.time:
                    warnings.append(
                        f"Conflict detected: '{first.description}' for {first.pet_name} and "
                        f"'{second.description}' for {second.pet_name} are both scheduled at "
                        f"{first.time} on {first.due_date}."
                    )

        return warnings

    def mark_task_complete(self, pet_name: str, task_description: str) -> Optional[Task]:
        """Mark a task complete and create the next recurring instance if needed."""
        for pet in self.owner.pets:
            if pet.pet_name != pet_name:
                continue

            for task in pet.tasks:
                if task.description == task_description and not task.completed:
                    task.mark_complete()

                    if task.frequency.lower() == "daily":
                        next_due_date = task.due_date + timedelta(days=1)
                    elif task.frequency.lower() == "weekly":
                        next_due_date = task.due_date + timedelta(weeks=1)
                    else:
                        return None

                    new_task = Task(
                        description=task.description,
                        duration=task.duration,
                        priority=task.priority,
                        frequency=task.frequency,
                        time=task.time,
                        due_date=next_due_date,
                        pet_name=pet.pet_name,
                        completed=False,
                    )
                    pet.add_task(new_task)
                    return new_task
        return None

    def generate_plan(self) -> List[Task]:
        """Generate a daily plan based on priority, time, and available time."""
        tasks = self.get_due_today_tasks()

        sorted_tasks = sorted(
            tasks,
            key=lambda task: (-task.priority, task.time)
        )

        selected_tasks: List[Task] = []
        used_time = 0

        for task in sorted_tasks:
            if used_time + task.duration <= self.owner.available_time:
                selected_tasks.append(task)
                used_time += task.duration

        self.daily_plan = selected_tasks
        return self.daily_plan

    def explain_plan(self) -> str:
        """Explain why the selected tasks were included in the plan."""
        if not self.daily_plan:
            return "No tasks were added to the daily plan because none fit within the available time."

        task_names = [task.description for task in self.daily_plan]
        return (
            f"The scheduler selected these tasks: {', '.join(task_names)}. "
            f"It prioritized higher-priority tasks first and used task time to break ties."
        )