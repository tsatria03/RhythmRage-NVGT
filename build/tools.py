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
# PASSWORD     = _cfg["game"]["password"]  # disabled with the release pipeline (not in tools.ini)
NVGT_FILE    = _cfg["game"]["nvgt_file"]
NVGT_OUT     = os.path.splitext(NVGT_FILE)[0]
SRC_DIR      = os.path.join(REPO_DIR, "src")    # the .nvgt source now lives here (post-reorg)
ASSETS_DIR   = os.path.join(REPO_DIR, "sf")     # assets (data, docks, lib, sounds) live here
BUNDLE       = os.path.join(SRC_DIR, NVGT_OUT)  # nvgt -c (run from src) produces this bundle folder
VERSION_NVGT = os.path.join(SRC_DIR, "includes", "version.nvgt")  # generated mirror of version.txt (the source of truth)
ASSET_FOLDERS = ["data", "docks", "lib"]  # NOT sounds: the 2.3 GB sounds/ folder is downloaded on first run (downloadsounds), never bundled

# --- Compile step (Windows + Mac) ---
NVGT2     = r"C:\nvgt2\nvgt2.exe"                 # miniaudio NVGT compiler this game uses (the shared ~/.game_tools nvgt is the legacy engine)
RG_DIR    = os.path.join(REPO_DIR, "rg")          # the game's data folder
# Copied from rg/ into every build. NOT: mypacks/ (authoring), sounds/ (raw source), *.py launchers, or lib (the
# bundler already supplies the correct per-platform libraries).
SHIP      = ["docks", "packs", "parser.md", "sounds1.pack", "sounds2.pack"]
# Destination for each platform: the bundle (named after the script) goes inside the existing RhythmRage_<platform> folder.
WIN_DEST  = os.path.join(REPO_DIR, "releases", "windows", "RhythmRage_windows", NVGT_OUT)          # ...\rg  (folder: rg.exe + lib + data)
MAC_DEST  = os.path.join(REPO_DIR, "releases", "mac", "RhythmRage_mac", NVGT_OUT + ".app")         # ...\rg.app
ARCHIVES_DIR = os.path.join(REPO_DIR, "releases", "archives")  # .zip packages land here

NVGT    = _tools["tools"]["nvgt"]  # shared across all the legacy-engine games; set to the legacy build in ~/.game_tools/tools.ini
SEVENZIP = _tools["tools"]["sevenzip"]
GH      = _tools["tools"]["gh"]

# Release/packaging paths disabled with the release pipeline (they depend on PASSWORD):
# WIN_SOURCE   = os.path.join(REPO_DIR, "releases", "windows", f"{GAME}_password_is_{PASSWORD}", NVGT_OUT)
# ARCHIVE_DIR  = os.path.join(REPO_DIR, "releases", "archives")
# ARCHIVE_NAME = f"{GAME}_password_is_{PASSWORD}.7z"
# ARCHIVE      = os.path.join(ARCHIVE_DIR, ARCHIVE_NAME)
# RELEASE_DIR  = os.path.join(REPO_DIR, "releases", "windows", f"{GAME}_password_is_{PASSWORD}")

SKIP = 0
DO = 1
SILENT_SKIP = 2

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

def sync_version_file(version):
    # Mirror version.txt into version.nvgt so the compiled build carries the right version;
    # a compiled release has no build/version.txt beside it to read at runtime. CRLF like the repo.
    with open(VERSION_NVGT, "w", newline="", encoding="utf-8") as f:
        f.write(f'string version = "{version}";\r\n')
    print(f"Synced version {version} into version.nvgt.\n")

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

# ── Release ───────────────────────────────────────────────────────────────────

def run_release(skip_compile, skip_package, skip_release, skip_empty_release, interactive=True):
    version = get_version()
    if not version:
        print("ERROR: Could not read version from version.txt.")
        return

    title = f"{GAME} V{version}"
    tag = f"V{version}0"

    print(f"\nVersion: {version}")
    print(f"Tag:     {tag}")
    print(f"Title:   {title}\n")

    if skip_release != SILENT_SKIP:
        head_sha = run_out(["git", "rev-parse", "--verify", "HEAD"])
        existing_tag_sha = run_out(["git", "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}"])
        existing_release = subprocess.run([GH, "release", "view", tag], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=REPO_DIR).returncode == 0
        if existing_tag_sha or existing_release:
            print(f"WARNING: {tag} already exists.")
            if existing_tag_sha:
                short = existing_tag_sha[:7]
                msg = run_out(["git", "log", "--format=%s", "-1", existing_tag_sha])
                if existing_tag_sha != head_sha:
                    head_short = head_sha[:7] if head_sha else "?"
                    head_msg = run_out(["git", "log", "--format=%s", "-1", "HEAD"])
                    print(f"  Tag points to {short} {msg}")
                    print(f"  This release will MOVE the tag to HEAD ({head_short} {head_msg}).")
                else:
                    print(f"  Tag already points to HEAD, so it will not move.")
            if existing_release:
                print(f"  GitHub release {tag} will be deleted and recreated with new assets.")
            print()
            if interactive:
                if not ask("Continue with the release?"):
                    print("Release cancelled.")
                    return
            else:
                print("ERROR: Refusing to overwrite an existing tag or release in non-interactive mode.")
                print("       Delete the tag and release manually first, or run tools.py interactively.")
                return

    # Compile
    do_compile = False
    if skip_compile == DO:
        do_compile = True
    elif skip_compile == SKIP:
        do_compile = ask("Do you want to compile this project?")

    if do_compile:
        print("Compiling NVGT source...")
        sync_version_file(version)
        # The source lives in src/; run nvgt -c from there so the bundle lands in src/<name>.
        if not run_cmd([NVGT, "-c", "-Q", NVGT_FILE], cwd=SRC_DIR):
            print("ERROR: NVGT compilation failed.")
            return
        print("Compilation successful.\n")
        print("Copying assets into the compiled bundle...")
        # The assets live in sf/; copy them into the bundle so they sit cwd-relative beside the exe
        # (lib merges with the runtime DLLs nvgt -c already placed there).
        for folder in ASSET_FOLDERS:
            asset_src = os.path.join(ASSETS_DIR, folder)
            if not os.path.isdir(asset_src):
                print(f"ERROR: missing asset folder: {asset_src}")
                return
            shutil.copytree(asset_src, os.path.join(BUNDLE, folder), dirs_exist_ok=True)
        print("Replacing compiled output in release folder...")
        cst_dest = os.path.join(RELEASE_DIR, NVGT_OUT)
        if os.path.exists(cst_dest):
            shutil.rmtree(cst_dest)
        shutil.move(BUNDLE, cst_dest)
        print("Release folder updated.\n")
    elif skip_compile == SKIP:
        print("Skipping compilation.\n")

    # Package
    do_package = False
    if skip_package == DO:
        do_package = True
    elif skip_package == SKIP:
        do_package = ask("Do you want to package this project?")

    if do_package:
        if not os.path.exists(WIN_SOURCE):
            print("ERROR: cst folder not found in release directory. Please compile the full project first.")
            return
        print("Building Windows 7z archive...")
        if os.path.exists(ARCHIVE):
            os.remove(ARCHIVE)
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        if not run_cmd([SEVENZIP, "a", "-t7z", ARCHIVE, WIN_SOURCE, "-mx=9", "-m0=LZMA2", "-md=64m", "-mfb=64", "-ms=on", "-mmt=12", f"-p{PASSWORD}", "-mhe=on"]):
            print("ERROR: 7z archive build failed.")
            return
        print("Archive built successfully.\n")
    elif skip_package == SKIP:
        print("Skipping packaging.\n")

    # Release
    do_rel = False
    if skip_release == DO:
        do_rel = True
    elif skip_release == SKIP:
        do_rel = ask("Do you want to release this project?")

    if not do_rel:
        if skip_release == SKIP:
            print("Skipping release.\n")
        return

    assets = []
    if os.path.exists(ARCHIVE):
        assets.append(ARCHIVE)

    if not assets:
        print("WARNING: No assets found.\n")
        proceed = False
        if skip_empty_release == DO:
            proceed = True
        elif skip_empty_release == SKIP:
            proceed = ask("Do you still want to create an empty release?")
        if not proceed:
            print("Release cancelled.\n")
            return

    print(f"Tagging latest commit as {tag}...")
    run_cmd(["git", "tag", "-f", tag], cwd=REPO_DIR)
    run_cmd(["git", "push", "origin", "-f", tag], cwd=REPO_DIR)

    print("\nDeleting existing release if it exists...")
    subprocess.run([GH, "release", "delete", tag, "--yes"], cwd=REPO_DIR, stderr=subprocess.DEVNULL)

    print(f"\nCreating GitHub release {title} with tag {tag}...\n")
    cmd = [GH, "release", "create", tag] + assets + ["--title", title, "--notes", ""]
    if not run_cmd(cmd, cwd=REPO_DIR):
        print("ERROR: GitHub release creation failed.")
        return

    print("\nRelease complete.\n")

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
            shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
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
    # Ship an empty mypacks/ beside the tool so pack authors have a ready place to drop source folders (the
    # compiled tool scans "mypacks" in its own folder). We create it empty rather than copying rg/mypacks sources.
    os.makedirs(os.path.join(WIN_DEST, "mypacks"), exist_ok=True)
    print(f"Level tool added: {os.path.join(WIN_DEST, 'lt.exe')} (with empty mypacks/)\n")
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
        return
    print("Build complete.\n")

# ── Package (zip) ───────────────────────────────────────────────────────────────

def _zip_windows():
    # Zip the game folder so the archive contains rg/ at its root: extracting RhythmRage_windows.zip
    # yields an rg/ folder (rg.exe, lt.exe, lib, packs, ...). No exec-bit concerns on Windows.
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
        return
    print()
    _zip_windows()
    _zip_mac()

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
        # Release options hidden for now (the GitHub-release pipeline is deferred):
        # print(" --- Release ---")
        # print(" 8. Full release")
        # print(" 9. Release only")
        print(" ---")
        print(" 8. Exit")
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
        # Release options hidden for now (functions kept above for when the pipeline is finalized):
        # elif choice == "8":
        #     run_release(SKIP, SKIP, SKIP, SKIP)            # full release
        # elif choice == "9":
        #     run_release(SILENT_SKIP, SILENT_SKIP, DO, DO)  # release only
        elif choice == "8":
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1-8.")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        menu()
    else:
        # Release pipeline is disabled for now, so the scripted (flag-based) release entry point is guarded
        # off. The original argument handling is kept below, commented out, for when compilation/release is
        # finalized.
        print("The release pipeline is currently disabled. Run tools.py with no arguments for the git menu.")
        sys.exit(2)
        # usage = (
        #     "Usage: tools.py <skip_compile> <skip_package> <skip_release> <skip_empty_release>\n"
        #     f"  Each flag must be {SKIP} (ask), {DO} (force run), or {SILENT_SKIP} (skip silently)."
        # )
        # if len(args) != 4:
        #     print(f"Error: expected 4 args, got {len(args)}.\n{usage}")
        #     sys.exit(2)
        # try:
        #     flags = [int(a) for a in args]
        # except ValueError:
        #     print(f"Error: all args must be integers.\n{usage}")
        #     sys.exit(2)
        # if any(f not in (SKIP, DO, SILENT_SKIP) for f in flags):
        #     print(f"Error: each flag must be {SKIP}, {DO}, or {SILENT_SKIP}.\n{usage}")
        #     sys.exit(2)
        # run_release(*flags, interactive=False)
