from solution.exercise3 import git_command_simulator


def test_git_add_file():

    input = "git add test.txt"
    excepted_output = "Stage all changes or specific file test.txt for the next commit."

    assert git_command_simulator(input) == excepted_output


def test_git_rm_cached():

    input = "git rm --cached test.txt"
    excepted_output = (
        "Unstage file test.txt while retaining the changes in the working directory."
    )

    assert git_command_simulator(input) == excepted_output


def test_git_commit_m():

    input = "git commit -m example_message"
    excepted_output = (
        "Commit changes to the repository with a descriptive message example_message."
    )

    assert git_command_simulator(input) == excepted_output


def test_git_push():

    input = "git push"
    excepted_output = "Upload your commits to the remote repository."

    assert git_command_simulator(input) == excepted_output


def test_git_stash():

    input = "git stash"
    excepted_output = "Temporarily shelves changes in your working directory so you can work on a different task."

    assert git_command_simulator(input) == excepted_output


def test_git_stash_push_m():

    input = "git stash push -m example_message"
    excepted_output = (
        "Stashes changes with a custom message example_message for easy identification."
    )

    assert git_command_simulator(input) == excepted_output


def test_git_stash_apply():

    input = "git stash apply"
    excepted_output = "Applies the most recently stashed changes."

    assert git_command_simulator(input) == excepted_output


def test_git_stash_apply_name():

    input = "git stash apply stash_name"
    excepted_output = "Applies the most recently stashed changes stash_name."

    assert git_command_simulator(input) == excepted_output


def test_invalid_input():

    input = "git foo"
    excepted_output = "Invalid Command."

    assert git_command_simulator(input) == excepted_output
