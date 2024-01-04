from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Optional[Role]
    content: str


class Role(BaseModel):
    name: str
    description: str
    actions: List[Type[Action]] = Field(default_factory=list)


class Context(BaseModel):
    session_id: str
    roles: List[Role] = Field(default_factory=list)
    history: List[Message] = Field(default_factory=list)
    lookup: Dict[str, Any] = Field(default_factory=dict)


class Action(ABC):
    @classmethod
    def __init__subclass__(cls) -> None:
        super().__init_subclass__()
        name = getattr(cls, "name")
        description = getattr(cls, "description")
        if not isinstance(name, str) or not isinstance(description, str):
            raise TypeError("name and description are required for an Action.")

    @abstractmethod
    @classmethod
    def execute(
        cls,
        command: str,
        role: Role,
        to_do: List[Tuple[Role, Type[Action]]],
        context: Context,
    ) -> Optional[Message]:
        raise NotImplementedError("Defined `execute` method when subclassing")


class Team:
    def __init__(
        self, roles: List[Role], to_do: List[Tuple[Role, Type[Action]]]
    ) -> None:
        self.to_do = to_do
        self.roles = roles
        self.context = Context(session_id=str(uuid.uuid4()), roles=roles)

    def execute(self, command: str) -> Message:
        while self.to_do:
            role, action = self.to_do.pop()
            message = action.execute(
                command=command, role=role, to_do=self.to_do, context=self.context
            )
            if message:
                return message
        return Message(role=None, content="no further ado")
