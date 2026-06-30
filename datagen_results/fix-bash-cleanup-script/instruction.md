You are given a bash cleanup script that is supposed to remove temporary files and directories but fails with an error message about not using the `-r` flag with `rm`. The script currently tries to remove a directory named `temp_dir` without the recursive flag, which causes it to fail. Your task is to modify the script to properly remove the directory and all its contents using the correct `rm` command syntax.

The script should:
1. Create a temporary directory structure with some files inside
2. Clean up by removing the entire directory tree recursively
3. Exit successfully

Fix the script so it works correctly when executed.