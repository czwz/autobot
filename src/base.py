from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str


class Role(BaseModel):
    name: str
    description: str
    actions: List[Any] = Field(default_factory=list)


class Context(BaseModel):
    session_id: str
    roles: List[Role] = Field(default_factory=list)
    history: List[Message] = Field(default_factory=list)
    lookup: Dict[str, Any] = Field(default_factory=dict)


class Action(ABC):
    name: str
    command: str
    description: str

    def __init__(self, command: str) -> None:
        self.command = command

    @abstractmethod
    def execute(
        self,
        role: Role,
        to_do: List[Tuple[Role, "Action"]],
        context: Context
    ) -> Optional[Message]:
        ...
    
    def __repr__(self) -> str:
        return f"Action: {self.name}"
