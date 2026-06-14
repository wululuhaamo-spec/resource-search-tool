from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import webbrowser
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VERSION_FILE = ROOT / "app-version.json"
UPDATER_DIR = ROOT / ".updater"
BACKUP_DIR = UPDATER_DIR / "backup"
DOWNLOAD_DIR = UPDATER_DIR / "downloads"


def read_json(path: Path, fallback: dict) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_version(value: str) -> tuple[int, ...]:
    cleaned = str(value or "").strip().lstrip("vV")
    parts = []
    for part in cleaned.replace("-", ".").split("."):
        digits = "".join(ch for ch in part if ch.isdigit())
        if digits:
            parts.append(int(digits))
        else:
            break
    return tuple(parts or [0])


def is_newer(remote: str, current: str) -> bool:
    left = parse_version(remote)
    right = parse_version(current)
    size = max(len(left), len(right))
    left += (0,) * (size - len(left))
    right += (0,) * (size - len(right))
    return left > right


def request_json(url: str, timeout: int = 12) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "ResourceSearchTool-Updater/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download_file(url: str, target: Path, timeout: int = 30) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "ResourceSearchTool-Updater/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp, target.open("wb") as out:
        shutil.copyfileobj(resp, out)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_extract_zip(zip_path: Path, target_dir: Path) -> None:
    target_root = target_dir.resolve()
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            destination = (target_dir / member.filename).resolve()
            if target_root not in destination.parents and destination != target_root:
                raise RuntimeError(f"Unsafe zip path: {member.filename}")
        archive.extractall(target_dir)


def package_root(staging: Path) -> Path:
    direct_files = {item.name.lower() for item in staging.iterdir() if item.is_file()}
    if "index.html" in direct_files or "server.py" in direct_files:
        return staging
    dirs = [item for item in staging.iterdir() if item.is_dir()]
    if len(dirs) == 1:
        return dirs[0]
    return staging


def copy_tree(source: Path, destination: Path) -> None:
    skip_names = {".updater", ".git", "__pycache__"}
    for item in source.iterdir():
        if item.name in skip_names:
            continue
        target = destination / item.name
        if item.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def backup_current() -> None:
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    for name in ["index.html", "server.py", "launcher.py", "start-tool.bat", "app-version.json", "SEARCH_SOURCES.md"]:
        source = ROOT / name
        if source.exists():
            target = BACKUP_DIR / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def restore_backup() -> None:
    if BACKUP_DIR.exists():
        copy_tree(BACKUP_DIR, ROOT)


def apply_update(manifest: dict, current_config: dict) -> bool:
    version = str(manifest.get("version") or "").strip()
    package_url = str(manifest.get("package_url") or "").strip()
    expected_sha = str(manifest.get("sha256") or "").strip().lower()
    if not version or not package_url or not expected_sha:
        raise RuntimeError("Update manifest is missing version, package_url, or sha256")

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = DOWNLOAD_DIR / f"resource-search-tool-{version}.zip"
    download_file(package_url, zip_path)
    actual_sha = sha256_file(zip_path)
    if actual_sha.lower() != expected_sha:
        raise RuntimeError("Downloaded update failed SHA256 verification")

    with tempfile.TemporaryDirectory(prefix="resource-tool-update-") as tmp:
        staging = Path(tmp)
        safe_extract_zip(zip_path, staging)
        source_root = package_root(staging)
        backup_current()
        try:
            copy_tree(source_root, ROOT)
            next_config = read_json(VERSION_FILE, current_config)
            next_config["version"] = version
            if current_config.get("manifest_url") and not next_config.get("manifest_url"):
                next_config["manifest_url"] = current_config["manifest_url"]
            write_json(VERSION_FILE, next_config)
        except Exception:
            restore_backup()
            raise
    return True


def check_for_update(force: bool = False) -> bool:
    config = read_json(VERSION_FILE, {})
    if not force and not config.get("check_on_start", True):
        return False
    manifest_url = str(config.get("manifest_url") or "").strip()
    if not manifest_url:
        print("Updater: manifest_url is empty; skipping update check.")
        return False

    current_version = str(config.get("version") or "0.0.0")
    manifest = request_json(manifest_url)
    remote_version = str(manifest.get("version") or "0.0.0")
    print(f"Updater: current {current_version}, remote {remote_version}")
    if not is_newer(remote_version, current_version):
        return False
    print("Updater: update found, downloading...")
    apply_update(manifest, config)
    print("Updater: update installed.")
    return True


def start_server(host: str, port: int) -> int:
    url = f"http://{host}:{port}/index.html"
    print(url)
    time.sleep(0.2)
    webbrowser.open(url)
    return subprocess.call([sys.executable, str(ROOT / "server.py"), "--host", host, "--port", str(port)], cwd=str(ROOT))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--force-check", action="store_true")
    parser.add_argument("--skip-update", action="store_true")
    args = parser.parse_args()

    if not args.skip_update:
        try:
            updated = check_for_update(force=args.force_check or args.check_only)
            if updated and args.check_only:
                return 0
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError, ValueError) as exc:
            print(f"Updater: skipped because update check failed: {exc}")

    if args.check_only:
        return 0
    return start_server(args.host, args.port)


if __name__ == "__main__":
    raise SystemExit(main())
