from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Optional[Role]
    content: str


class Role(BaseModel):
    name: str
    description: str
    actions: List[Action] = Field(default_factory=list)


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
        to_do: List[Tuple[Role, Action]],
        context: Context
    ) -> Optional[Message]:
        ...
    
    def __repr__(self) -> str:
        return f"Action: {self.name}"


class Team:
    def __init__(
        self,
        roles: List[Role],
        to_do: List[Tuple[Role, Action]]
    ) -> None:
        self.to_do = to_do
        self.roles = roles
        self.context = Context(session_id=uuid.uuid4(), roles=roles)
    
    def execute(self, command: str) -> Message:
        while self.to_do:
            role, action = self.to_do.pop()
            message = action.execute(role=role, context=self.context)
            if message:
                return message
        return Message(role=None, content="no further ado")
