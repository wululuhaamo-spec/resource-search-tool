# GitHub Auto Update

This folder is ready to publish as a GitHub repository.

## How updates work

1. `launcher.py` starts before `server.py`.
2. It reads `app-version.json`.
3. If `manifest_url` is configured, it downloads `latest.json`.
4. If the remote version is newer, it downloads the release zip.
5. It verifies SHA256.
6. It backs up current files, replaces them, and starts the app.
7. If replacement fails, it restores the backup.

## How source updates work

The app also has source subscriptions. On startup it fetches:

```text
https://raw.githubusercontent.com/wululuhaamo-spec/resource-search-tool/main/sources/source-registry.json
```

Most source changes can be made by updating that JSON file, without publishing a new app release.

## Required GitHub URL

This repository is configured to use:

```json
{
  "manifest_url": "https://github.com/wululuhaamo-spec/resource-search-tool/releases/latest/download/latest.json"
}
```

If you fork or move the repository later, update this URL to the new `OWNER/REPO`.

## Publish a new version without command line

Open the GitHub repository:

1. Go to `Actions`.
2. Open `Release`.
3. Click `Run workflow`.
4. Enter a version number, for example `1.0.3`.
5. Click the green `Run workflow` button.

GitHub Actions will create a Release with:

- `resource-search-tool-1.0.3.zip`
- `latest.json`

The next time users start the tool, it will update automatically.

## Local test

Run this to test that the updater can start without a configured update URL:

```powershell
python launcher.py --check-only
```

Run this to start the app:

```powershell
python launcher.py
```

## Security note

SHA256 prevents corrupted or mismatched downloads. Anyone who can publish releases in the GitHub repository can ship updates, so keep repository access limited.
