<div align="center">

# GitHub Inventory

![Banner](https://raw.githubusercontent.com/ThatSINEWAVE/GitHub-Inventory/refs/heads/main/.github/SCREENSHOTS/GitHub-Inventory.png)

GitHub Inventory is a Python script that helps you fetch and organize your GitHub repositories into a clean, human-readable report. The script pulls data from the GitHub API, formats it into both text and markdown formats, and saves it in separate files. It also logs important actions and provides status updates for the process. This is useful for quickly reviewing and sharing your GitHub repositories with others or maintaining an inventory of your work.

</div>

## Features

- Fetches repository data from GitHub using the GitHub API.
- Generates two types of output:
  - Text format (.txt)
  - Markdown format (.md)
- Creates necessary directories if they do not exist.
- Saves output files in separate directories for easy management.
- Logs all actions with timestamps, including directory creation and repository fetching.
- Handles both public and private repositories.
- Outputs summary statistics such as the total number of repositories, public and private counts.

<div align="center">

## ☕ [Support my work on Ko-Fi](https://ko-fi.com/thatsinewave)

</div>

## Requirements

- Python 3.x
- `requests` library: Used to interact with the GitHub API.
- `python-dotenv` library: Used to load environment variables from a `.env` file.

## Setup

1. Clone this repository or download the script files.
2. Install the required dependencies:
   ```bash
   pip install requests python-dotenv
   ```

3. Create a `.env` file in the project directory and add your GitHub credentials:
   ```
   GITHUB_TOKEN=your_personal_access_token
   GITHUB_USERNAME=your_github_username
   ```
   - **GITHUB_TOKEN**: A personal access token generated from your GitHub account. Follow [this guide](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) to create one.
   - **GITHUB_USERNAME**: Your GitHub username.

## How to Get a GitHub API Token

In order to use this script, you need a GitHub Personal Access Token (PAT). Follow these steps to generate one:

1. **Log into your GitHub account**:
   - Open your web browser and go to [GitHub](https://github.com/).
   - Log in with your GitHub credentials.

2. **Go to the Developer settings**:
   - Once logged in, click on your profile icon in the top-right corner.
   - Select **Settings** from the dropdown menu.
   - In the left-hand sidebar, scroll down and click on **[Developer settings](https://github.com/settings/apps)**.

3. **Generate a new token**:
   - Under **Developer settings**, click on **[Personal access tokens](https://github.com/settings/tokens)**.
   - Click on the **Generate new token** button.

4. **Set token permissions**:
   - In the **Note** field, give your token a descriptive name (e.g., "GitHub Inventory Script").
   - Under **Select scopes**, choose the necessary permissions for your token. For fetching repository data, at least the following scopes are required:
     - **repo**: Grants full control of private repositories.
     - **read:org**: Allows reading organization membership data.
   - Optionally, you can choose additional scopes if your script needs to access more specific data.

5. **Generate and save the token**:
   - Once you’ve selected the necessary permissions, click the **Generate token** button.
   - GitHub will display your new token. **Make sure to copy it immediately**, as it will not be shown again.

6. **Add the token to your `.env` file**:
   - Open your project directory and create a `.env` file if you haven’t already.
   - Add the following line to the file, replacing `your_personal_access_token` with the token you just copied:
     ```bash
     GITHUB_TOKEN=your_personal_access_token
     ```

## Usage

1. Run the script from your terminal:
   ```bash
   python github_inventory.py
   ```

2. The script will:
   - Fetch your repositories from GitHub.
   - Check if necessary output folders exist (creating them if they don’t).
   - Generate two output files:
     - `text_output_TIMESTAMP.txt`: A plain-text summary of your repositories.
     - `markdown_output_TIMESTAMP.md`: A markdown formatted summary of your repositories.
   - Logs will be saved in the `logs/` directory.

<div align="center">

## [Join my discord server](https://discord.gg/2nHHHBWNDw)

</div>

## Example Output

### Text Output Example

```
GitHub Inventory Report
Total Repositories: 5
Public Repos: 3
Private Repos: 2

- Repo 1 (Public)
  Description for Repo 1

- Repo 2 (Private)
  Description for Repo 2

...
```

### Markdown Output Example

```markdown
# GitHub Inventory Report
**Total Repositories:** 5  
**Public Repos:** 3  
**Private Repos:** 2  

### Repo 1 (Public)
Description for Repo 1

### Repo 2 (Private)
Description for Repo 2

...
```

## Logs

Logs of the script’s operations are stored in the `logs/` directory with filenames following this format: `log_TIMESTAMP.txt`. These logs contain detailed information on the script’s actions, including directory checks, repo fetch status, and file creation.

## Contributing

As this project is in early development, please reach out before submitting pull requests. All contributions are welcome!

## License

This project is open-source and available under the MIT License. See [LICENSE](LICENSE) for more details.