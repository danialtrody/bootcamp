from solution.exercise3 import git_command_simulator


def test_git_add_file():

    user_input = "git add test.txt"
    expected_output = "Stage all changes or specific file test.txt for the next commit."

    assert git_command_simulator(user_input) == expected_output


def test_git_rm_cached():

    user_input = "git rm --cached test.txt"
    expected_output = (
        "Unstage file test.txt while retaining the changes in the working directory."
    )

    assert git_command_simulator(user_input) == expected_output


def test_git_commit_m():

    user_input = "git commit -m example_message"
    expected_output = (
        "Commit changes to the repository with a descriptive message example_message."
    )

    assert git_command_simulator(user_input) == expected_output


def test_git_push():

    user_input = "git push"
    expected_output = "Upload your commits to the remote repository."

    assert git_command_simulator(user_input) == expected_output


def test_git_stash():

    user_input = "git stash"
    expected_output = "Temporarily shelves changes in your working directory so you can work on a different task."

    assert git_command_simulator(user_input) == expected_output


def test_git_stash_push_m():

    user_input = "git stash push -m example_message"
    expected_output = (
        "Stashes changes with a custom message example_message for easy identification."
    )

    assert git_command_simulator(user_input) == expected_output


def test_git_stash_apply():

    user_input = "git stash apply"
    expected_output = "Applies the most recently stashed changes."

    assert git_command_simulator(user_input) == expected_output


def test_git_stash_apply_name():

    user_input = "git stash apply stash_name"
    expected_output = "Applies the most recently stashed changes stash_name."

    assert git_command_simulator(user_input) == expected_output


def test_invalid_input():

    user_input = "git foo"
    expected_output = "Invalid Command."

    assert git_command_simulator(user_input) == expected_output
