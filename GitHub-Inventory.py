import os
import requests
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

# GitHub API URL
GITHUB_API_URL = (
    f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100&type=all"
)

# Output directories
TEXT_FOLDER = "output/text"
MARKDOWN_FOLDER = "output/markdown"
LOGS_FOLDER = "logs"


def log_message(message, log_file):
    """Log a message with a timestamp to a log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file.write(f"{timestamp} - {message}\n")
    print(f"[LOG] {message}")


def check_folders(log_file):
    """Check if output directories exist, create if not, and log status."""
    log_message("[INFO] Checking output directories...", log_file)

    if not os.path.exists(TEXT_FOLDER):
        os.makedirs(TEXT_FOLDER)
        log_message(
            f"[CREATED] Folder '{TEXT_FOLDER}' was missing and has been created.",
            log_file,
        )
    else:
        log_message(f"[FOUND] Folder '{TEXT_FOLDER}' exists.", log_file)

    if not os.path.exists(MARKDOWN_FOLDER):
        os.makedirs(MARKDOWN_FOLDER)
        log_message(
            f"[CREATED] Folder '{MARKDOWN_FOLDER}' was missing and has been created.",
            log_file,
        )
    else:
        log_message(f"[FOUND] Folder '{MARKDOWN_FOLDER}' exists.", log_file)

    log_message("[SUCCESS] All necessary folders are ready.\n", log_file)


def fetch_repos(log_file):
    """Fetch GitHub repositories and return a list of repo details."""
    log_message("[INFO] Fetching repositories from GitHub...", log_file)
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(GITHUB_API_URL, headers=headers)

    if response.status_code != 200:
        log_message(
            f"[ERROR] Failed to fetch repositories. Status Code: {response.status_code}",
            log_file,
        )
        log_message(str(response.json()), log_file)  # Print error details
        return []

    repos = response.json()
    log_message(f"[SUCCESS] Retrieved {len(repos)} repositories.\n", log_file)
    return repos


def format_repo_list(repos, log_file):
    """Format repo data and generate both text and markdown outputs."""
    total_repos = len(repos)
    public_repos = sum(1 for repo in repos if not repo["private"])
    private_repos = total_repos - public_repos

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    text_filename = f"{TEXT_FOLDER}/text_output_{timestamp}.txt"
    markdown_filename = f"{MARKDOWN_FOLDER}/markdown_output_{timestamp}.txt"

    log_message(f"[INFO] Formatting repository data...\n", log_file)

    # Stats Header
    header_text = f"GitHub Inventory Report\nTotal Repositories: {total_repos}\nPublic Repos: {public_repos}\nPrivate Repos: {private_repos}\n\n"
    header_markdown = f"# GitHub Inventory Report\n**Total Repositories:** {total_repos}\n**Public Repos:** {public_repos}\n**Private Repos:** {private_repos}\n\n"

    # Repo List
    text_output = header_text
    markdown_output = header_markdown

    for repo in repos:
        name = repo["name"]
        desc = repo["description"] or "No description provided."
        visibility = "Public" if not repo["private"] else "Private"

        text_output += f"- {name} ({visibility})\n  {desc}\n\n"
        markdown_output += f"### {name} ({visibility})\n{desc}\n\n"

    # Writing to files
    with open(text_filename, "w", encoding="utf-8") as text_file:
        text_file.write(text_output)
    log_message(f"[SAVED] Text report generated: {text_filename}", log_file)

    with open(markdown_filename, "w", encoding="utf-8") as markdown_file:
        markdown_file.write(markdown_output)
    log_message(f"[SAVED] Markdown report generated: {markdown_filename}", log_file)

    log_message("[COMPLETE] All reports have been successfully created.", log_file)


def main():
    """Main execution function."""
    if not os.path.exists(LOGS_FOLDER):
        os.makedirs(LOGS_FOLDER)
        print(f"[INFO] Logs folder created at '{LOGS_FOLDER}'")

    log_filename = f"{LOGS_FOLDER}/log.txt"
    with open(log_filename, "a", encoding="utf-8") as log_file:
        log_message("🔹 Starting GitHub Inventory Tool 🔹\n", log_file)
        check_folders(log_file)
        repos = fetch_repos(log_file)
        if repos:
            format_repo_list(repos, log_file)
        log_message("✅ Done. Exiting program.\n", log_file)


if __name__ == "__main__":
    main()
