from solution.exercise3 import git_command_simulator


def test_git_add_file() -> None:

    user_input: str = "git add test.txt"
    expected_output: str = "Stage all changes or specific file test.txt for the next commit."

    assert git_command_simulator(user_input) == expected_output


def test_git_rm_cached() -> None:

    user_input: str = "git rm --cached test.txt"
    expected_output: str = (
        "Unstage file test.txt while retaining the changes in the working directory."
    )

    assert git_command_simulator(user_input) == expected_output


def test_git_commit_m() -> None:

    user_input: str = "git commit -m example_message"
    expected_output: str = (
        "Commit changes to the repository with a descriptive message example_message."
    )

    assert git_command_simulator(user_input) == expected_output


def test_git_push() -> None:

    user_input: str = "git push"
    expected_output: str = "Upload your commits to the remote repository."

    assert git_command_simulator(user_input) == expected_output


def test_git_stash() -> None:

    user_input: str = "git stash"
    expected_output: str = "Temporarily shelves changes in your working directory so you can work on a different task."

    assert git_command_simulator(user_input) == expected_output


def test_git_stash_push_m() -> None:

    user_input: str = "git stash push -m example_message"
    expected_output: str = (
        "Stashes changes with a custom message example_message for easy identification."
    )

    assert git_command_simulator(user_input) == expected_output


def test_git_stash_apply() -> None:

    user_input: str = "git stash apply"
    expected_output: str = "Applies the most recently stashed changes."

    assert git_command_simulator(user_input) == expected_output


def test_git_stash_apply_name() -> None:

    user_input: str = "git stash apply stash_name"
    expected_output: str = "Applies the most recently stashed changes stash_name."

    assert git_command_simulator(user_input) == expected_output


def test_invalid_input() -> None:

    user_input: str = "git foo"
    expected_output: str = "Invalid Command."

    assert git_command_simulator(user_input) == expected_output
