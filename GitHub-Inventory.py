import os
import requests
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

# GitHub API URLs
GITHUB_API_BASE = "https://api.github.com"
USER_REPOS_URL = (
    f"{GITHUB_API_BASE}/users/{GITHUB_USERNAME}/repos?per_page=100&type=all&page="
)
USER_ORGS_URL = f"{GITHUB_API_BASE}/users/{GITHUB_USERNAME}/orgs"
ORG_REPOS_URL = f"{GITHUB_API_BASE}/orgs/{{org}}/repos?per_page=100&page="

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

    for folder in [TEXT_FOLDER, MARKDOWN_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            log_message(
                f"[CREATED] Folder '{folder}' was missing and has been created.",
                log_file,
            )
        else:
            log_message(f"[FOUND] Folder '{folder}' exists.", log_file)

    log_message("[SUCCESS] All necessary folders are ready.\n", log_file)


def make_api_request(url, headers, log_file):
    """Make an API request and handle errors."""
    global response
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log_message(
            f"[ERROR] API request failed: {url} - {str(e)}",
            log_file,
        )
        try:
            log_message(str(response.json()), log_file)  # Print error details
        except:
            pass
        return []


def fetch_user_repos(headers, log_file):
    """Fetch user's personal GitHub repositories."""
    log_message("[INFO] Fetching personal repositories from GitHub...", log_file)
    repos = []
    page = 1

    while True:
        page_repos = make_api_request(USER_REPOS_URL + str(page), headers, log_file)
        if not page_repos:
            break

        repos.extend(page_repos)
        page += 1

    log_message(f"[SUCCESS] Retrieved {len(repos)} personal repositories.", log_file)
    return repos


def fetch_organizations(headers, log_file):
    """Fetch organizations that the user is a member of."""
    log_message("[INFO] Fetching user's organizations...", log_file)
    orgs = make_api_request(USER_ORGS_URL, headers, log_file)

    if orgs:
        org_names = [org["login"] for org in orgs]
        log_message(
            f"[SUCCESS] Found {len(orgs)} organizations: {', '.join(org_names)}",
            log_file,
        )
    else:
        log_message(
            "[INFO] No organizations found or unable to fetch organizations.", log_file
        )

    return orgs


def fetch_org_repos(org_name, headers, log_file):
    """Fetch repositories from a specific organization."""
    log_message(
        f"[INFO] Fetching repositories from organization: {org_name}...", log_file
    )
    repos = []
    page = 1

    while True:
        url = ORG_REPOS_URL.format(org=org_name) + str(page)
        page_repos = make_api_request(url, headers, log_file)
        if not page_repos:
            break

        repos.extend(page_repos)
        page += 1

    log_message(
        f"[SUCCESS] Retrieved {len(repos)} repositories from {org_name}.", log_file
    )
    return repos


def fetch_all_repos(log_file):
    """Fetch all repositories: personal and from organizations."""
    log_message("[INFO] Beginning repository collection process...", log_file)
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # Get personal repos
    user_repos = fetch_user_repos(headers, log_file)

    # Get organization repos
    orgs = fetch_organizations(headers, log_file)
    org_repos = []

    for org in orgs:
        org_name = org["login"]
        org_repos_list = fetch_org_repos(org_name, headers, log_file)

        # Add organization info to each repo
        for repo in org_repos_list:
            repo["organization"] = org_name

        org_repos.extend(org_repos_list)

    # Add source info to personal repos
    for repo in user_repos:
        repo["organization"] = "personal"

    # Combine all repos
    all_repos = user_repos + org_repos

    log_message(f"[SUCCESS] Total repositories collected: {len(all_repos)}\n", log_file)
    return all_repos


def format_repo_list(repos, log_file):
    """Format repo data and generate both text and markdown outputs."""
    total_repos = len(repos)
    public_repos = sum(1 for repo in repos if not repo["private"])
    private_repos = total_repos - public_repos

    # Count repos by source (personal vs organizations)
    personal_repos = sum(1 for repo in repos if repo["organization"] == "personal")
    org_repos = total_repos - personal_repos

    # Get unique organizations
    orgs = {
        repo["organization"] for repo in repos if repo["organization"] != "personal"
    }

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    text_filename = f"{TEXT_FOLDER}/github_inventory_{timestamp}.txt"
    markdown_filename = f"{MARKDOWN_FOLDER}/github_inventory_{timestamp}.md"

    log_message(f"[INFO] Formatting repository data...", log_file)

    # Stats Header
    header_text = (
        f"GitHub Inventory Report\n"
        f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"User: {GITHUB_USERNAME}\n\n"
        f"Repository Statistics:\n"
        f"- Total Repositories: {total_repos}\n"
        f"- Personal Repositories: {personal_repos}\n"
        f"- Organization Repositories: {org_repos}\n"
        f"- Public Repositories: {public_repos}\n"
        f"- Private Repositories: {private_repos}\n"
        f"- Organizations: {len(orgs)}\n\n"
    )

    header_markdown = (
        f"# GitHub Inventory Report\n"
        f"**Generated on:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"**User:** {GITHUB_USERNAME}\n\n"
        f"## Repository Statistics\n"
        f"- **Total Repositories:** {total_repos}\n"
        f"- **Personal Repositories:** {personal_repos}\n"
        f"- **Organization Repositories:** {org_repos}\n"
        f"- **Public Repositories:** {public_repos}\n"
        f"- **Private Repositories:** {private_repos}\n"
        f"- **Organizations:** {len(orgs)}\n\n"
    )

    # Repo List
    text_output = header_text
    markdown_output = header_markdown

    # Sort repos by source (personal first, then by org name) and then by repo name
    sorted_repos = sorted(
        repos,
        key=lambda r: (r["organization"] != "personal", r["organization"], r["name"]),
    )

    # Group by source (personal/organization)
    current_source = None

    for index, repo in enumerate(sorted_repos, 1):
        name = repo["name"]
        desc = repo["description"] or "No description provided."
        visibility = "Public" if not repo["private"] else "Private"
        source = repo["organization"]

        # Add section headers when source changes
        if source != current_source:
            current_source = source

            if source == "personal":
                text_output += f"PERSONAL REPOSITORIES\n{'=' * 20}\n\n"
                markdown_output += f"## Personal Repositories\n\n"
            else:
                text_output += f"\nORGANIZATION: {source}\n{'=' * 20}\n\n"
                markdown_output += f"## Organization: {source}\n\n"

        # Add repository information
        text_output += f"{index}. {name} ({visibility})\n   {desc}\n\n"
        markdown_output += f"### {index}. {name} ({visibility})\n{desc}\n\n"
        # Add URL to markdown version
        if "html_url" in repo:
            markdown_output += f"[View on GitHub]({repo['html_url']})\n\n"

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

    log_filename = (
        f"{LOGS_FOLDER}/log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    )
    with open(log_filename, "a", encoding="utf-8") as log_file:
        log_message(
            "🔹 Starting GitHub Inventory Tool (with Organizations) 🔹\n", log_file
        )
        check_folders(log_file)

        if not GITHUB_TOKEN:
            log_message(
                "[ERROR] GitHub token not found. Please set GITHUB_TOKEN in your .env file.",
                log_file,
            )
            return

        if not GITHUB_USERNAME:
            log_message(
                "[ERROR] GitHub username not found. Please set GITHUB_USERNAME in your .env file.",
                log_file,
            )
            return

        repos = fetch_all_repos(log_file)
        if repos:
            format_repo_list(repos, log_file)
        log_message("✅ Done. Exiting program.\n", log_file)


if __name__ == "__main__":
    main()
