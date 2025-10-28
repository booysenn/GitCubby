import sys

from .constants import EXTERNAL_GIT_SSH_URL, EXTERNAL_GIT_HTTP_URL


class UserInterface():
    @staticmethod
    def print_success(message):
        """Print success message (green text)"""
        print(f"\033[32m{message}\033[0m")

    @staticmethod
    def print_error_and_exit(message):
        """Print error message and exit"""
        print(f"\033[31mError: {message}\033[0m", file=sys.stderr)
        sys.exit(1)

    @staticmethod
    def print_repo_urls(repo_type, repo_name, title="Clone URLs"):
        """Print SSH and HTTPS clone URLs for a repository
        
        Args:
            repo_type: Repository type ('private' or 'public')
            repo_name: Repository name
            title: Optional title to display (default: "Clone URLs")
        """
        print(f"\nRepository: {repo_type}/{repo_name}")
        print("=" * 50)
        
        if title:
            print(f"\n{title}:")
        
        print("\nSSH:")
        UserInterface().print_success(f"  git clone {EXTERNAL_GIT_SSH_URL}/{repo_type}/{repo_name}")
        
        print("\nHTTPS:")
        UserInterface().print_success(f"  git clone {EXTERNAL_GIT_HTTP_URL}/{repo_type}/{repo_name}")
        
        print()

    @staticmethod
    def print_colored(color_code, message, end="\n"):
        """Print colored text using ANSI escape codes"""
        # ANSI color mapping (similar to tput setaf)
        colors = {
            0: '\033[30m',  # black
            1: '\033[31m',  # red
            2: '\033[32m',  # green
            3: '\033[33m',  # yellow
            4: '\033[34m',  # blue
            5: '\033[35m',  # magenta
            6: '\033[36m',  # cyan
            7: '\033[37m',  # white
        }
        reset = '\033[0m'
        
        color = colors.get(color_code, '')
        print(f"{color}{message}{reset}", end=end)