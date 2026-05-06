import os
import requests
import re

def fetch_repos(username):
    url = f"https://api.github.com/users/{username}/repos?sort=updated&direction=desc&per_page=100"
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"User-Agent": "Mozilla/5.0"}
    if token:
        headers["Authorization"] = f"token {token}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching repos: {e}")
        return []

def format_project_list(repos, profile_repo):
    projects = []
    # Filter out the profile repo and limit to 5
    filtered_repos = [r for r in repos if r['name'].lower() != profile_repo.lower()][:5]
    
    if not filtered_repos:
        return "i'm probably in between projects or keeping everything private right now. \ncheck back later i guess."

    for repo in filtered_repos:
        name = repo['name']
        desc = repo['description'] or "no description provided (probably just a mess of code)"
        lang = repo['language'] or "various"
        url = repo['html_url']
        
        projects.append(f"- **[{name}]({url})** — {desc.lower()} `[{lang.lower()}]`")
    
    return "\n".join(projects)

def update_readme(projects_text):
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("README.md not found")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to find the section between markers
    pattern = r"(<!-- START_SECTION:projects -->)(.*?)(<!-- END_SECTION:projects -->)"
    replacement = f"\\1\n{projects_text}\n\\3"
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    USERNAME = "famyXpng"
    repos = fetch_repos(USERNAME)
    projects_text = format_project_list(repos, USERNAME)
    update_readme(projects_text)
    print("README updated with latest projects.")
