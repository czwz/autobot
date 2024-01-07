from logging import Logger
from typing import List, Optional, Tuple, Type

from src.base import Action, Context, Message, Role
from src.roles import User


logger = Logger(name="autobot")


class Think(Action):
    name: str = "think about what to do next"
    description: str = (
        "this action decides what will be the"
        "next action in order to acheive the"
        "user command."
    )

    @classmethod
    def execute(
        cls,
        command: str,
        role: Role,
        to_do: List[Tuple[Role, Type[Action]]],
        context: Context,
    ) -> Optional[Message]:
        if role.name == "Master":
            chosen_role = next(r for r in context.roles if r != role)
            chosen_action = chosen_role.actions[0]
        else:
            chosen_role = role
            chosen_action = chosen_role.actions[1]

        to_do.append((chosen_role, chosen_action))


class GetReply(Action):
    name: str = "get user's input as reply."
    description: str = (
        "this action will treat last message in history"
        "as the reply for key opened by the last action."
    )

    @classmethod
    def execute(
        cls,
        command: str,
        role: Role,
        to_do: List[Tuple[Role, Type[Action]]],
        context: Context,
    ) -> Optional[Message]:
        for key, val in context.lookup.items():
            if val is not None:
                continue
            else:
                reply = context.history[-1].content
                context.lookup[key] = reply
            break
        return


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
        to_do: List[Tuple[Role, Type[Action]]],
        context: Context,
    ) -> Optional[Message]:
        """the definition on how to process the input"""
        logger.info("Get the input from the user, start processing ...")
        if to_do and isinstance(to_do[-1][1], GetReply):
            logger.info("the input should be a reply, let's note it down ...")
            message = Message(role=User, content=command)
            context.history.append(message)
        else:
            logger.info("the input is a command, let's think how to do it ...")
            to_do.append((role, Think))
