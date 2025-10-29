def clean_repo_name(repo_name):
    if repo_name.endswith('.git'):
        return repo_name[:-4]
    else:
        return repo_name