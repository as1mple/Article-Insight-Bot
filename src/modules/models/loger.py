import sys
from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum
from enum import auto


class LogLevel(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    DEBUG = auto()
    INFO = auto()


class Sink(Enum):
    console = sys.stderr
    file = "logs/debug.log"


@dataclass
class LogHandler:
    sink: str
    level: str
    format: str
    rotation: str


@dataclass
class LogConfig:
    handlers: List[LogHandler]

    def to_dicts(self) -> List[Dict[str, Any]]:
        return [
            {field: getattr(handler, field) for field in handler.__dataclass_fields__.keys() if getattr(handler, field)}
            for handler in self.handlers
        ]
