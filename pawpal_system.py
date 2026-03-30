from dataclasses import dataclass, field
from typing import List


@dataclass
class Owner:
    owner_name: str
    available_time: int
    preferences: List[str] = field(default_factory=list)

    def update_preferences(self, preferences: List[str]) -> None:
        pass

    def set_available_time(self, available_time: int) -> None:
        pass


@dataclass
class Pet:
    pet_name: str
    pet_type: str
    age: int
    care_notes: str = ""

    def update_pet_info(self, pet_name: str, pet_type: str, age: int, care_notes: str) -> None:
        pass


@dataclass
class Task:
    task_name: str
    duration: int
    priority: int
    category: str
    completed: bool = False

    def edit_task(self, task_name: str, duration: int, priority: int, category: str) -> None:
        pass

    def mark_complete(self) -> None:
        pass


@dataclass
class Scheduler:
    task_list: List[Task] = field(default_factory=list)
    available_time: int = 0
    daily_plan: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def generate_plan(self) -> List[Task]:
        pass

    def explain_plan(self) -> str:
        pass