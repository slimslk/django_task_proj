from enum import Enum


class StatusChoices(Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    PENDING = "Pending"
    BLOCKED = "Blocked"
    DONE = "Done"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]