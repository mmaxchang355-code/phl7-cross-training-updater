import os, re, requests

GH_TOKEN = os.environ["GH_TOKEN"]
GIST_ID = os.environ.get("GIST_ID", "e0bf2670bf5b474e9f7017b116d5bd22")

def main():
    h = {"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    print("Fetching current Gist...")
    r = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=h)
    r.raise_for_status()
    
    content = r.json()["files"]["universal_cross_training.user.js"]["content"]
    print(f"Current size: {len(content)} chars")
    
    m = re.search(r"@version\s+([\d.]+)", content)
    if m:
        old_ver = m.group(1)
        parts = old_ver.split(".")
        parts[-1] = str(int(parts[-1]) + 1)
        new_ver = ".".join(parts)
        content = content.replace(f"@version      {old_ver}", f"@version      {new_ver}")
        
        print(f"Bumping version: {old_ver} -> {new_ver}")
        resp = requests.patch(
            f"https://api.github.com/gists/{GIST_ID}",
            headers=h,
            json={"files": {"universal_cross_training.user.js": {"content": content}}}
        )
        resp.raise_for_status()
        print(f"Gist updated: {resp.status_code}")
    else:
        print("No version found in script")

if __name__ == "__main__":
    main()
