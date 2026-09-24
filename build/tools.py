import subprocess
import os
import sys
import shutil
import configparser
import zipfile
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

_cfg = configparser.ConfigParser()
_cfg.read(os.path.join(SCRIPT_DIR, "tools.ini"))

_tools = configparser.ConfigParser()
_tools.read(os.path.join(os.path.expanduser("~"), ".game_tools", "tools.ini"))

GAME         = _cfg["game"]["name"]
NVGT_FILE    = _cfg["game"]["nvgt_file"]
NVGT_OUT     = os.path.splitext(NVGT_FILE)[0]
SRC_DIR      = os.path.join(REPO_DIR, "src")    # the .nvgt source lives here

# --- Compile / package / release ---
NVGT2     = r"C:\nvgt2\nvgt2.exe"                 # miniaudio NVGT compiler this game uses
RG_DIR    = os.path.join(REPO_DIR, "rg")          # the game's data folder
# Packs live in the player's app data (…\Oriol Gomez\RhythmRage\packs), not in the build. The pack-index
# generator reads pack names from here.
APPDATA_PACKS = os.path.join(os.environ.get("APPDATA", ""), "Oriol Gomez", "RhythmRage", "packs")
# Copied from rg/ into every build. data/ holds runtime game data - assets/ (engine sound packs) and saves/
# (the portable profile). docks/ holds the player-facing docs. NOT: sounds/ (raw sound source, built into
# data/assets), *.py launchers, or lib (bundler-supplied). Packs are NOT shipped here - the game keeps its packs
# in an app-data folder and gets them there separately. From mypacks/, only the two default pack SOURCE folders
# ship (see _copy_default_sources), so the game can compile the defaults offline when it can't download them.
SHIP      = ["data", "docks"]

# copytree ignore callback for _copy_ship: drops the dev's save (rg.dat, plus the rg.dat.tmp/rg.dat.bak the
# safe-save swap leaves beside it) and any .gitkeep, anywhere.
def _ship_ignore(src_dir, names):
    ignored = set()
    for n in names:
        if n.lower() in ("rg.dat", "rg.dat.tmp", "rg.dat.bak", ".gitkeep"):
            ignored.add(n)
    return ignored

# The default pack SOURCE folders (under rg/mypacks) shipped inside the build's mypacks/, so the game can compile
# the defaults locally as an offline fallback when they can't be downloaded. Other authoring sources don't ship.
DEFAULT_PACK_SOURCES = ("default", "default_espanol")

def _copy_default_sources(mypacks_dest):
    # Copy each default pack source folder from rg/mypacks into mypacks_dest. A missing source is a warning, not
    # fatal (players can still download that default in-game).
    os.makedirs(mypacks_dest, exist_ok=True)
    for name in DEFAULT_PACK_SOURCES:
        src = os.path.join(RG_DIR, "mypacks", name)
        if not os.path.isdir(src):
            print(f"WARNING: default pack source not found, skipping: {src}")
            continue
        shutil.copytree(src, os.path.join(mypacks_dest, name), dirs_exist_ok=True, ignore=_ship_ignore)
        print(f"Shipped default pack source: mypacks/{name}")
    return True
# Destination for each platform: the bundle (named after the script) goes inside the existing RhythmRage_<platform> folder.
WIN_DEST  = os.path.join(REPO_DIR, "releases", "windows", "RhythmRage_windows", NVGT_OUT)          # ...\rg  (folder: rg.exe + lib + data)
MAC_DEST  = os.path.join(REPO_DIR, "releases", "mac", "RhythmRage_mac", NVGT_OUT + ".app")         # ...\rg.app
ARCHIVES_DIR = os.path.join(REPO_DIR, "releases", "archives")  # .zip packages land here
GH        = _tools["tools"]["gh"]                 # GitHub CLI, from ~/.game_tools/tools.ini (used by the release step)

def ask(prompt):
    return input(f"{prompt} (Y/N): ").strip().upper() == "Y"

def run(args, capture=False):
    return subprocess.run(args, cwd=REPO_DIR, capture_output=capture, text=True)

def run_out(args):
    return run(args, capture=True).stdout.strip()

def run_cmd(args, cwd=None):
    return subprocess.run(args, cwd=cwd).returncode == 0

def clip(text):
    subprocess.run("clip", input=text.strip(), text=True)

def get_version():
    with open(os.path.join(SCRIPT_DIR, "version.txt"), "r") as f:
        return f.read().strip()

# ── Commit ────────────────────────────────────────────────────────────────────

def unpushed_count():
    out = run_out(["git", "log", "origin/HEAD..HEAD", "--oneline"])
    return len([l for l in out.splitlines() if l.strip()])

def do_commit():
    status = run_out(["git", "status", "--short"])
    changes = len([l for l in status.splitlines() if l.strip()])
    print(f"Changes: {changes}")
    print()
    if changes == 0:
        print("No changes to commit.")
        return
    print(status)
    print()
    if not ask("Do you want to commit?"):
        print("Cancelled.")
        return
    print()
    summary = input("Commit summary: ").strip()
    if not summary:
        print("Summary cannot be empty.")
        return
    print()
    print("Commit description (enter lines one by one, blank line to finish):")
    desc_lines = []
    while True:
        line = input(f"Line {len(desc_lines) + 1}: ")
        if not line.strip():
            break
        desc_lines.append(line)
    description = "\n".join(desc_lines)
    print()
    print(f"Summary:     {summary}")
    if description:
        print(f"Description: {description}")
    print()
    if not ask("Is this correct?"):
        print("Cancelled.")
        return
    print()
    run(["git", "add", "-A"])
    args = ["git", "commit", "-m", summary]
    if description:
        args += ["-m", description]
    result = run(args)
    if result.returncode != 0:
        print("ERROR: Commit failed.")
        return
    print()
    print(f"Committed {changes} file(s).")
    print()
    if not ask("Do you want to push?"):
        print("Changes committed but not pushed.")
        return
    print()
    result = run(["git", "push"])
    if result.returncode != 0:
        print("ERROR: Push failed.")
    else:
        print("Push complete.")

def do_undo(unpushed):
    if unpushed == 0:
        print("Nothing to undo. All commits have been pushed.")
        return
    last_msg = run_out(["git", "log", "-1", "--format=%s"])
    print(f"Last commit: {last_msg}")
    print()
    if not ask("Undo this commit? Your changes will remain staged."):
        print("Cancelled.")
        return
    result = run(["git", "reset", "--soft", "HEAD~1"])
    if result.returncode != 0:
        print("ERROR: Undo failed.")
    else:
        print("Commit undone. Your changes are still staged.")

def do_push(unpushed):
    if unpushed == 0:
        print("Nothing to push. All commits are already on the remote.")
        return
    log = run_out(["git", "log", "origin/HEAD..HEAD", "--oneline"])
    print(f"Unpushed commits ({unpushed}):")
    print()
    print(log)
    print()
    if not ask("Push these commits to the remote?"):
        print("Cancelled.")
        return
    result = run(["git", "push"])
    if result.returncode != 0:
        print("ERROR: Push failed.")
    else:
        print("Push complete.")

def do_history():
    raw = run_out(["git", "log", "-50", "--decorate-refs=refs/tags", "--format=%h~%ar~%s%d"])
    commits = []
    print()
    print("Last 50 commits:")
    print()
    for i, line in enumerate(raw.splitlines(), 1):
        parts = line.split("~", 2)
        if len(parts) < 3:
            continue
        sha, date, msg = parts
        commits.append((sha, msg))
        print(f"  {i}. {sha}  {msg}  (Time: {date})")
    print()
    pick = input("Select a commit number (or 0 to go back): ").strip()
    if pick == "0" or pick == "":
        return
    try:
        index = int(pick) - 1
        if index < 0 or index >= len(commits):
            raise ValueError
    except ValueError:
        print("Invalid selection.")
        return
    sha, msg = commits[index]
    print()
    print(f"Selected: {sha} {msg}")
    commit_menu(sha, msg)

def commit_menu(sha, msg):
    while True:
        print()
        print("========================")
        print(" Commit Options")
        print("========================")
        print(" 1. Show description")
        print(" 2. Copy SHA")
        print(" 3. Create tag")
        print(" 4. Copy tag")
        print(" 5. Reset to this commit")
        print(" 6. Go back")
        print("========================")
        choice = input("Choose an option: ").strip()
        print()
        if choice == "1":
            show_desc(sha)
        elif choice == "2":
            copy_sha(sha)
        elif choice == "3":
            create_tag(sha)
        elif choice == "4":
            copy_tag(sha)
        elif choice == "5":
            if do_reset(sha):
                return
        elif choice == "6":
            do_history()
            return
        else:
            print("Invalid choice.")

def show_desc(sha):
    desc = run_out(["git", "log", "-1", "--format=%B", sha])
    print(desc if desc else "(No description)")
    print()

def copy_sha(sha):
    full = run_out(["git", "rev-parse", sha])
    clip(full)
    print(f"SHA copied to clipboard: {full}")

def create_tag(sha):
    tag_name = input("Enter tag name: ").strip()
    if not tag_name:
        print("Tag name cannot be empty.")
        return
    result = run(["git", "tag", tag_name, sha])
    if result.returncode != 0:
        print("ERROR: Failed to create tag.")
        return
    print(f'Tag "{tag_name}" created.')
    if ask("Push tag to remote?"):
        run(["git", "push", "origin", tag_name])
        print("Tag pushed.")

def copy_tag(sha):
    tag = run_out(["git", "tag", "--points-at", sha])
    if not tag:
        print("No tag found on this commit.")
    else:
        clip(tag)
        print(f"Tag copied to clipboard: {tag}")

def do_create_tag():
    raw = input("Commit to tag (press Enter for HEAD): ").strip()
    target = raw if raw else "HEAD"
    sha = run_out(["git", "rev-parse", "--verify", target])
    if not sha:
        print(f"ERROR: Could not resolve commit '{target}'.")
        return
    short = sha[:7]
    msg = run_out(["git", "log", "--format=%s", "-1", sha])
    print(f"{target} is at: {short} {msg}")
    if not ask(f"Tag this commit?"):
        print("Cancelled.")
        return
    create_tag(sha)

def do_reset(sha):
    print("WARNING: Resetting will move HEAD to this commit.")
    print()
    print(" 1. Soft (keeps changes staged)")
    print(" 2. Hard (discards all changes permanently)")
    print(" 3. Cancel")
    print()
    choice = input("Choose reset type: ").strip()
    if choice == "3" or choice == "":
        print("Cancelled.")
        return False
    if choice == "1":
        flag = "--soft"
    elif choice == "2":
        flag = "--hard"
        print()
        print("WARNING: Hard reset will permanently discard all uncommitted changes.")
    else:
        print("Invalid choice.")
        return False
    print()
    if not ask(f"Reset to {sha}?"):
        print("Cancelled.")
        return False
    result = run(["git", "reset", flag, sha])
    if result.returncode != 0:
        print("ERROR: Reset failed.")
        return False
    print("Reset complete.")
    return True

# ── Build (compile Windows + Mac) ───────────────────────────────────────────────

def _copy_ship(asset_dest):
    # Copy the ship-list from rg/ into asset_dest (next to the exe on Windows, Contents/Resources on Mac).
    os.makedirs(asset_dest, exist_ok=True)
    for item in SHIP:
        src_item = os.path.join(RG_DIR, item)
        if not os.path.exists(src_item):
            print(f"ERROR: missing ship item in rg/: {item}")
            return False
        dst_item = os.path.join(asset_dest, item)
        if os.path.isdir(src_item):
            shutil.copytree(src_item, dst_item, dirs_exist_ok=True, ignore=_ship_ignore)
        else:
            shutil.copy2(src_item, dst_item)
    return True

def _build_one(platform, bundle_name, dest, assets_subpath):
    bundle = os.path.join(SRC_DIR, bundle_name)  # e.g. src/rg (Windows folder) or src/rg.app (Mac)
    # Remove any stale bundle first: nvgt -c fails if a directory named after the script already sits beside it.
    if os.path.isdir(bundle):
        shutil.rmtree(bundle)
    elif os.path.exists(bundle):
        os.remove(bundle)
    print(f"Compiling for {platform}...")
    if not run_cmd([NVGT2, f"-p{platform}", "-c", "-Q", NVGT_FILE], cwd=SRC_DIR):
        print(f"ERROR: {platform} compilation failed.")
        return False
    if not os.path.isdir(bundle):
        print(f"ERROR: {platform} compile produced no bundle at {bundle}.")
        return False
    asset_dest = os.path.join(bundle, assets_subpath) if assets_subpath else bundle
    if not _copy_ship(asset_dest):
        return False
    # Move the finished bundle into its release folder, replacing any previous build.
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    elif os.path.exists(dest):
        os.remove(dest)
    shutil.move(bundle, dest)
    print(f"{platform} build ready: {dest}\n")
    return True

def _build_level_tool_windows():
    # Compile the level tool (lt.nvgt) as a bare Windows exe -- lt.properties has bundling off -- and drop it into
    # the game folder next to rg.exe. It shares the game's lib/ folder there (NVGT looks for libs in the exe's
    # folder or its lib/ subfolder), so no second lib copy is needed.
    lt_exe = os.path.join(SRC_DIR, "lt.exe")
    if os.path.exists(lt_exe):
        os.remove(lt_exe)
    print("Compiling level tool for windows...")
    if not run_cmd([NVGT2, "-pwindows", "-c", "-Q", "lt.nvgt"], cwd=SRC_DIR):
        print("ERROR: level tool compilation failed.")
        return False
    if not os.path.isfile(lt_exe):
        print(f"ERROR: level tool compile produced no exe at {lt_exe}.")
        return False
    shutil.move(lt_exe, os.path.join(WIN_DEST, "lt.exe"))
    # Ship the default pack SOURCE folders in mypacks/ beside the tool: the level tool scans "mypacks" here, and
    # the game compiles these locally as its offline fallback when the default packs can't be downloaded.
    _copy_default_sources(os.path.join(WIN_DEST, "mypacks"))
    print(f"Level tool added: {os.path.join(WIN_DEST, 'lt.exe')} (with default pack sources in mypacks/)\n")
    return True

def do_build():
    if not os.path.isfile(NVGT2):
        print(f"ERROR: NVGT compiler not found at {NVGT2}.")
        return
    script = os.path.join(SRC_DIR, NVGT_FILE)
    if not os.path.isfile(script):
        print(f"ERROR: source script not found: {script}")
        return
    if not ask("Compile the game (plus the Windows level tool) for Windows and Mac?"):
        print("Cancelled.")
        return
    print()
    # Windows: game bundle, then the level tool exe dropped into the same folder so it shares the game's lib/.
    if not _build_one("windows", NVGT_OUT, WIN_DEST, ""):
        return
    if not _build_level_tool_windows():
        return
    # Mac: game only for now (the level tool is Windows-first).
    if not _build_one("mac", NVGT_OUT + ".app", MAC_DEST, os.path.join("Contents", "Resources")):
        return False
    # Ship the default pack sources into the Mac app's mypacks/ too, so its offline compile fallback works.
    _copy_default_sources(os.path.join(MAC_DEST, "Contents", "Resources", "mypacks"))
    print("Build complete.\n")
    return True

# ── Package (zip) ───────────────────────────────────────────────────────────────

def _zip_windows():
    # Zip the game folder so the archive contains rg/ at its root: extracting RhythmRage_windows.zip
    # yields an rg/ folder (rg.exe, lt.exe, lib, data, docks, ...). No exec-bit concerns on Windows.
    if not os.path.isdir(WIN_DEST):
        print(f"ERROR: no Windows build found at {WIN_DEST}. Compile it first (option 6).")
        return False
    os.makedirs(ARCHIVES_DIR, exist_ok=True)
    base = os.path.join(ARCHIVES_DIR, "RhythmRage_windows")
    zip_path = base + ".zip"
    if os.path.exists(zip_path):
        os.remove(zip_path)
    print("Packaging Windows build...")
    # root_dir = the platform folder, base_dir = "rg" -> entries are rg/..., so the zip extracts to an rg/ folder.
    shutil.make_archive(base, "zip", root_dir=os.path.dirname(WIN_DEST), base_dir=os.path.basename(WIN_DEST))
    print(f"Package ready: {zip_path}\n")
    return True

def _zip_mac():
    # Zip rg.app so the archive contains rg.app at its root (extract -> rg.app). The app's main executable must
    # keep its Unix execute bit or macOS won't launch it -- and shutil/zipfile default to 0 perms when zipping on
    # Windows. So we build the archive by hand and stamp 0755 on Contents/MacOS/rg (0644 for everything else).
    if not os.path.isdir(MAC_DEST):
        print(f"ERROR: no Mac build found at {MAC_DEST}. Compile it first (option 6).")
        return False
    os.makedirs(ARCHIVES_DIR, exist_ok=True)
    zip_path = os.path.join(ARCHIVES_DIR, "RhythmRage_mac.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)
    print("Packaging Mac build...")
    top_parent = os.path.dirname(MAC_DEST)  # releases/mac/RhythmRage_mac  (archive entries are relative to here)
    exec_arcname = f"{os.path.basename(MAC_DEST)}/Contents/MacOS/{NVGT_OUT}"  # rg.app/Contents/MacOS/rg
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(MAC_DEST):
            for name in files:
                full = os.path.join(root, name)
                arcname = os.path.relpath(full, top_parent).replace(os.sep, "/")  # rg.app/...
                zi = zipfile.ZipInfo(arcname, date_time=time.localtime(os.path.getmtime(full))[:6])
                zi.compress_type = zipfile.ZIP_DEFLATED
                mode = 0o755 if arcname == exec_arcname else 0o644
                zi.external_attr = (mode & 0xFFFF) << 16
                with open(full, "rb") as f:
                    zf.writestr(zi, f.read())
    print(f"Package ready: {zip_path} (0755 set on {exec_arcname})\n")
    return True

def do_package():
    if not ask("Package the Windows and Mac builds into zips?"):
        print("Cancelled.")
        return False
    print()
    ok_win = _zip_windows()
    ok_mac = _zip_mac()
    return ok_win and ok_mac

# ── Pack index (pack_index.txt for the downloader) ────────────────────────────────

def do_packindex():
    # The in-game pack downloader (getpacks) fetches pack_index.txt from the pack-server ROOT and reads one line
    # per pack: just "<name>.pack" (the game keys on filename only). Packs live in the player's app data now, so
    # this scans APPDATA_PACKS and writes the index into rg/ for uploading, mirroring the VPS layout:
    # pack_index.txt at RhythmRage/ (root), packs at RhythmRage/packs/.
    packs_dir = APPDATA_PACKS
    if not os.path.isdir(packs_dir):
        print(f"ERROR: packs folder not found at {packs_dir}.")
        return False
    packs = sorted(f for f in os.listdir(packs_dir)
                   if f.lower().endswith(".pack") and os.path.isfile(os.path.join(packs_dir, f)))
    if not packs:
        print(f"No .pack files found in {packs_dir} to index.")
        return False
    lines = list(packs)
    out_path = os.path.join(RG_DIR, "pack_index.txt")
    with open(out_path, "w", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {out_path} with {len(lines)} pack(s):")
    for l in lines:
        print("  " + l)
    print("\nUpload pack_index.txt to RhythmRage/ (root) and the .pack files to RhythmRage/packs/ on the VPS.")
    return True

# ── Release (tag + GitHub release) ──────────────────────────────────────────────

def do_release():
    # Version comes only from build/version.txt (the game code never reads it). Tag keeps the trailing-0 form
    # (1.1 -> V1.10); the GitHub release is titled "<GAME> V1.1". Attaches the two zips built by Compile (6) + Package (7).
    version = get_version()
    if not version:
        print("ERROR: could not read build/version.txt.")
        return False
    tag = f"V{version}0"        # e.g. 1.1 -> V1.10
    title = f"{GAME} V{version}"  # e.g. RhythmRage V1.1
    win_zip = os.path.join(ARCHIVES_DIR, "RhythmRage_windows.zip")
    mac_zip = os.path.join(ARCHIVES_DIR, "RhythmRage_mac.zip")
    assets = [z for z in (win_zip, mac_zip) if os.path.exists(z)]
    print(f"\nVersion: {version}")
    print(f"Tag:     {tag}")
    print(f"Release: {title}")
    print("Assets:  " + (", ".join(os.path.basename(a) for a in assets) if assets else "(none found)"))
    print()
    if not assets:
        print("ERROR: no archives in releases/archives/. Run Compile (6) then Package (7) first.")
        return False
    if len(assets) < 2:
        print("WARNING: only one platform archive was found; the other is missing.\n")
    # Overwrite guard: warn if the tag or release already exists.
    head_sha = run_out(["git", "rev-parse", "--verify", "HEAD"])
    existing_tag_sha = run_out(["git", "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}"])
    existing_release = subprocess.run([GH, "release", "view", tag], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=REPO_DIR).returncode == 0
    if existing_tag_sha or existing_release:
        print(f"WARNING: {tag} already exists.")
        if existing_tag_sha and existing_tag_sha != head_sha:
            print("  The tag will be MOVED to the current HEAD.")
        if existing_release:
            print(f"  The GitHub release {tag} will be deleted and recreated with new assets.")
        print()
    if not ask(f"Create GitHub release {title} (tag {tag}) with {len(assets)} asset(s)?"):
        print("Cancelled.")
        return False
    print(f"\nTagging HEAD as {tag}...")
    run_cmd(["git", "tag", "-f", tag], cwd=REPO_DIR)
    run_cmd(["git", "push", "origin", "-f", tag], cwd=REPO_DIR)
    print("Deleting any existing release for this tag...")
    subprocess.run([GH, "release", "delete", tag, "--yes"], cwd=REPO_DIR, stderr=subprocess.DEVNULL)
    print(f"Creating GitHub release {title}...")
    cmd = [GH, "release", "create", tag] + assets + ["--title", title, "--notes", ""]
    if not run_cmd(cmd, cwd=REPO_DIR):
        print("ERROR: GitHub release creation failed.")
        return False
    print("\nRelease complete.\n")
    return True

def do_full_release():
    # Compile -> package -> release in one go. Each step self-confirms; abort the chain if a step fails/cancels.
    if not do_build():
        return
    if not do_package():
        return
    do_release()

# ── Main menu ─────────────────────────────────────────────────────────────────

def menu():
    while True:
        unpushed = unpushed_count()
        print()
        print("========================")
        print(f"  {GAME} Tools")
        print("========================")
        print(" --- Commit ---")
        print(" 1. Make a commit")
        print(f" 2. Undo last commit (unpushed: {unpushed})")
        print(f" 3. Push commits (unpushed: {unpushed})")
        print(" 4. Show commit history")
        print(" 5. Create tag manually")
        print(" --- Build ---")
        print(" 6. Compile (Windows + Mac)")
        print(" 7. Package (Windows + Mac zip)")
        print(" 8. Generate pack index (pack_index.txt for the downloader)")
        print(" --- Release ---")
        print(" 9. Release (tag + GitHub release)")
        print(" 10. Full release (compile + package + release)")
        print(" ---")
        print(" 11. Exit")
        print("========================")
        choice = input("Choose an option: ").strip()
        print()
        if choice == "1":
            do_commit()
        elif choice == "2":
            do_undo(unpushed)
        elif choice == "3":
            do_push(unpushed)
        elif choice == "4":
            do_history()
        elif choice == "5":
            do_create_tag()
        elif choice == "6":
            do_build()
        elif choice == "7":
            do_package()
        elif choice == "8":
            do_packindex()
        elif choice == "9":
            do_release()
        elif choice == "10":
            do_full_release()
        elif choice == "11":
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1-11.")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        menu()
    else:
        # This tool is interactive only -- build, package, and release all live in the menu; it takes no arguments.
        print("tools.py takes no arguments. Run it with no arguments for the menu.")
        sys.exit(2)
