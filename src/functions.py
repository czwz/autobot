from logging import Logger
from typing import List, Optional, Tuple

from .base import Action, Context, Message, Role
from .roles import User


logger = Logger(name="autobot")


class Think(Action):
    ...


class GetReply(Action):
    ...


class ProcessUserInput(Action):
    name: str = "process the input from user."
    description: str = (
        "this action will decide"
        "to think, or to update the history"
        "depending on the type of user input."
    )

    @classmethod
    def execute(
        cls,
        command: str,
        role: Role,
        to_do: List[Tuple[Role, Action]],
        context: Context
    ) -> Optional[Message]:
        """the definition on how to process the input"""
        logger.info("Get the input from the user, start processing ...")
        if to_do and isinstance(to_do[-1][1], GetReply):
            logger.info("the input should be a reply, let's note it down ...")
            message = Message(role=User, content=command)
            context.history.append(message)
        else:
            logger.info("the input is a command, let's think how to do it ...")
            to_do.append((role, Think(command=command)))
