#!/usr/bin/env python3
import os, json, re, requests

GH_TOKEN = os.environ["GH_TOKEN"]
GIST_ID = os.environ.get("GIST_ID", "10ce3065265ca98f2470b00235db1731")

def main():
    print("Fetching current Gist...")
    resp = requests.get(
        f"https://api.github.com/gists/{GIST_ID}",
        headers={"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    )
    resp.raise_for_status()
    content = resp.json()["files"]["phl7_cross_training_overlay.user.js"]["content"]

    ver_match = re.search(r'@version\\s+([\\d.]+)', content)
    if ver_match:
        old_ver = ver_match.group(1)
        parts = old_ver.split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        new_ver = '.'.join(parts)
        content = content.replace(f'@version      {old_ver}', f'@version      {new_ver}')
        print(f"Version: {old_ver} -> {new_ver}")

    print("Pushing to Gist...")
    resp = requests.patch(
        f"https://api.github.com/gists/{GIST_ID}",
        headers={"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"},
        json={"files": {"phl7_cross_training_overlay.user.js": {"content": content}}}
    )
    resp.raise_for_status()
    print(f"Done! Status: {resp.status_code}")

if __name__ == "__main__":
    main()
