from enum import Enum
from typing import List


class GitToken(str, Enum):
    GIT = "git"
    ADD = "add"
    RM = "rm"
    CACHED = "--cached"
    COMMIT = "commit"
    MESSAGE_FLAG = "-m"
    PUSH = "push"
    STASH = "stash"
    APPLY = "apply"


INVALID_COMMAND = "Invalid Command."


def git_command_simulator(command: str) -> str:
    parts = command.split()

    match parts:
        case [GitToken.GIT.value, GitToken.ADD.value, filename]:
            result = (
                f"Stage all changes or specific file {filename} "
                f"for the next commit."
            )

        case [
            GitToken.GIT.value,
            GitToken.RM.value,
            GitToken.CACHED.value,
            filename,
        ]:
            result = (
                f"Unstage file {filename} while retaining the changes "
                f"in the working directory."
            )

        case [
            GitToken.GIT.value,
            GitToken.COMMIT.value,
            GitToken.MESSAGE_FLAG.value,
            commit_message,
        ]:
            result = (
                f"Commit changes to the repository with a descriptive "
                f"message {commit_message}."
            )

        case [GitToken.GIT.value, GitToken.PUSH.value]:
            result = "Upload your commits to the remote repository."

        case [GitToken.GIT.value, GitToken.STASH.value, *_]:
            result = _handle_stash_command(parts)

        case _:
            result = INVALID_COMMAND

    return result


def _handle_stash_command(parts: List[str]) -> str:
    match parts:
        case [GitToken.GIT.value, GitToken.STASH.value]:
            result = (
                "Temporarily shelves changes in your working directory "
                "so you can work on a different task."
            )

        case [
            GitToken.GIT.value,
            GitToken.STASH.value,
            GitToken.PUSH.value,
            GitToken.MESSAGE_FLAG.value,
            stash_message,
        ]:
            result = (
                f"Stashes changes with a custom message {stash_message} "
                f"for easy identification."
            )

        case [
            GitToken.GIT.value,
            GitToken.STASH.value,
            GitToken.APPLY.value,
        ]:
            result = "Applies the most recently stashed changes."

        case [
            GitToken.GIT.value,
            GitToken.STASH.value,
            GitToken.APPLY.value,
            stash_name,
        ]:
            result = f"Applies the most recently stashed changes {stash_name}."

        case _:
            result = INVALID_COMMAND

    return result
