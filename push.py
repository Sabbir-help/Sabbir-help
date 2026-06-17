#!/usr/bin/env python3
"""
===============================================================================
                     GRAPH-GREENER ULTIMATE v4.0
                       AUTO AI SMART EDITION
===============================================================================
Developer:     ABDULLAH AL SABBIR
Telegram:      @SABBIRX007
License:       MIT
Security:      No shell=True | Input Validated
Features:      Auto Detect | Smart Mode | No Manual Path Entry
Version:       4.0 (2026)
===============================================================================
"""

import os
import random
import subprocess
import re
import sys
from datetime import datetime, timedelta

# ============================================================================
# COLOR CODES
# ============================================================================
if sys.platform == "win32":
    os.system('color')
    
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RED = '\033[91m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_colored(text, color=RESET, bold=False, end='\n'):
    if bold:
        print(f"{BOLD}{color}{text}{RESET}", end=end)
    else:
        print(f"{color}{text}{RESET}", end=end)

def show_creator_info():
    print_colored("="*70, CYAN)
    print_colored("             GRAPH-GREENER ULTIMATE v4.0", YELLOW, True)
    print_colored("                  AUTO AI EDITION", YELLOW)
    print_colored("="*70, CYAN)
    print_colored(f"  Developer:     {WHITE}ABDULLAH AL SABBIR{RESET}", GREEN)
    print_colored(f"  Telegram:      {WHITE}@SABBIRX007{RESET}", BLUE)
    print_colored(f"  Features:      {WHITE}Auto Detect | Smart Mode | No Manual Path{RESET}", GREEN)
    print_colored(f"  Version:       {WHITE}4.0 (2026){RESET}", YELLOW)
    print_colored("="*70, CYAN)
    print()

def show_footer():
    print_colored("\n" + "="*70, CYAN)
    print_colored("  Thank you for using GRAPH-GREENER!", GREEN, True)
    print_colored(f"  Developed by: ABDULLAH AL SABBIR", WHITE)
    print_colored(f"  Telegram: @SABBIRX007", BLUE)
    print_colored("="*70, CYAN)

def show_success(message):
    print_colored(f"  [✓] {message}", GREEN)

def show_error(message):
    print_colored(f"  [✗] {message}", RED)

def show_info(message):
    print_colored(f"  [i] {message}", CYAN)

def show_warning(message):
    print_colored(f"  [!] {message}", YELLOW)

def show_progress(current, total, prefix=""):
    percent = (current / total) * 100
    bar_length = 30
    filled = int(bar_length * current // total)
    bar = '█' * filled + '░' * (bar_length - filled)
    print_colored(f"\r  {prefix} [{bar}] {percent:.1f}% ({current}/{total})", CYAN, end='')
    sys.stdout.flush()

# ============================================================================
# AUTO DETECT FUNCTIONS
# ============================================================================
def find_git_repos():
    """Find all git repositories in current directory and subdirectories"""
    repos = []
    current_dir = os.getcwd()
    
    # Check current directory
    if os.path.exists(os.path.join(current_dir, ".git")):
        repos.append(current_dir)
    
    # Check subdirectories (max 2 levels deep)
    try:
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                if os.path.exists(os.path.join(item_path, ".git")):
                    repos.append(item_path)
                else:
                    # Check one level deeper
                    for subitem in os.listdir(item_path):
                        subitem_path = os.path.join(item_path, subitem)
                        if os.path.isdir(subitem_path) and os.path.exists(os.path.join(subitem_path, ".git")):
                            repos.append(subitem_path)
    except:
        pass
    
    return repos

def get_default_repo():
    """Auto detect or create repository"""
    repos = find_git_repos()
    
    if len(repos) == 0:
        show_warning("No git repository found!")
        print_colored("  Creating new repository in current directory...", YELLOW)
        
        current_dir = os.getcwd()
        run_git_command(["git", "init"], cwd=current_dir)
        
        # Create data.txt
        data_file = os.path.join(current_dir, "data.txt")
        if not os.path.exists(data_file):
            with open(data_file, 'w') as f:
                f.write("# Graph Greener Data File\n")
            show_success("Created data.txt")
        
        show_success(f"Repository initialized at: {current_dir}")
        return current_dir
    
    elif len(repos) == 1:
        show_success(f"Found repository: {repos[0]}")
        return repos[0]
    
    else:
        print_colored("\n  Multiple repositories found:", YELLOW)
        for i, repo in enumerate(repos):
            print_colored(f"    {i+1}. {repo}", CYAN)
        
        print_colored("\n  Use first repository? (y/n): ", CYAN, end='')
        choice = input().strip().lower()
        
        if choice == 'y' or choice == '':
            show_success(f"Selected: {repos[0]}")
            return repos[0]
        else:
            while True:
                try:
                    idx = int(input("  Enter repository number: ")) - 1
                    if 0 <= idx < len(repos):
                        show_success(f"Selected: {repos[idx]}")
                        return repos[idx]
                    else:
                        show_error("Invalid number!")
                except ValueError:
                    show_error("Invalid input!")

def ensure_data_file(repo_path):
    """Ensure data.txt exists in repository"""
    filename = "data.txt"
    filepath = os.path.join(repo_path, filename)
    
    if not os.path.exists(filepath):
        show_info(f"Creating {filename}...")
        with open(filepath, 'w') as f:
            f.write(f"# Graph Greener Data File\n")
            f.write(f"# Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        show_success(f"Created {filename}")
    
    return filename

# ============================================================================
# SECURITY & GIT FUNCTIONS
# ============================================================================
def sanitize_filename(filename):
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    return sanitized

def validate_year(year, max_future_years=1):
    current_year = datetime.now().year
    if year < 1970:
        show_warning(f"Year {year} is too old! Using 2020.")
        return 2020
    if year > current_year + max_future_years:
        show_warning(f"Year {year} is too far in future! Using {current_year}.")
        return current_year
    return year

def run_git_command(cmd_args, cwd=None, env=None, capture=False):
    if not isinstance(cmd_args, list):
        raise ValueError("cmd_args must be a list")
    
    dangerous_patterns = [';', '&&', '||', '`', '$(']
    for arg in cmd_args:
        for pattern in dangerous_patterns:
            if pattern in str(arg):
                show_error(f"Dangerous pattern '{pattern}' detected!")
                return False, "", "Security violation"
    
    try:
        if capture:
            result = subprocess.run(
                cmd_args, cwd=cwd, env=env, capture_output=True,
                text=True, check=False, shell=False
            )
        else:
            result = subprocess.run(
                cmd_args, cwd=cwd, env=env, check=False, shell=False
            )
        return result.returncode == 0, result.stdout if capture else "", result.stderr if capture else ""
    except Exception as e:
        return False, "", str(e)

def init_git_repo(repo_path):
    git_path = os.path.join(repo_path, ".git")
    if not os.path.exists(git_path):
        show_warning("Initializing git repository...")
        success, _, _ = run_git_command(["git", "init"], cwd=repo_path)
        if success:
            show_success("Git repository initialized.")
            return True
        else:
            show_error("Failed to initialize git.")
            return False
    return True

def has_remote(repo_path):
    success, stdout, _ = run_git_command(["git", "remote", "get-url", "origin"], cwd=repo_path, capture=True)
    return success and stdout.strip()

def push_to_remote(repo_path, branch="main"):
    print_colored("\n" + "="*70, BLUE)
    print_colored("  PUSHING TO REMOTE", YELLOW, True)
    print_colored("="*70, BLUE)
    
    success, stdout, _ = run_git_command(["git", "branch", "--show-current"], cwd=repo_path, capture=True)
    if success and stdout.strip():
        current_branch = stdout.strip()
        if current_branch != branch:
            branch = current_branch
    
    show_info(f"Pushing to origin/{branch}...")
    success, _, stderr = run_git_command(["git", "push", "origin", branch], cwd=repo_path, capture=True)
    
    if success:
        show_success("Successfully pushed to remote!")
        return True
    else:
        show_error(f"Push failed: {stderr[:200] if stderr else 'Unknown error'}")
        return False

def make_commit_common(date, repo_path, filename, message):
    filepath = os.path.join(repo_path, filename)
    with open(filepath, "a") as f:
        f.write(f"Commit at {date.isoformat()}\n")
    
    run_git_command(["git", "add", filename], cwd=repo_path)
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_COMMITTER_DATE"] = date.strftime("%Y-%m-%dT%H:%M:%S")
    return run_git_command(["git", "commit", "-m", message], cwd=repo_path, env=env)

# ============================================================================
# MODE 1: Last Year Random Commits
# ============================================================================
def random_date_in_last_year():
    today = datetime.now()
    start_date = today - timedelta(days=365)
    random_days = random.randint(0, 364)
    random_seconds = random.randint(0, 23*3600 + 3599)
    return start_date + timedelta(days=random_days, seconds=random_seconds)

def mode1_last_year_commits(repo_path, filename):
    print_colored("\n" + "="*70, BLUE)
    print_colored("  MODE 1: Last Year Random Commits", YELLOW, True)
    print_colored("="*70, BLUE)
    
    num_commits = get_positive_int("  How many commits to make", 20, max_value=10000)
    
    show_info(f"Making {num_commits} commits in last 365 days...")
    print()
    
    for i in range(num_commits):
        commit_date = random_date_in_last_year()
        show_progress(i + 1, num_commits, "Progress")
        make_commit_common(commit_date, repo_path, filename, "graph-greener!")
    
    print()
    show_success(f"Completed {num_commits} commits!")
    return True

# ============================================================================
# MODE 2: Specific Year Commits
# ============================================================================
def random_date_in_year(year):
    year = validate_year(year)
    start_date = datetime(year, 1, 1)
    days_in_year = 366 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 365
    random_days = random.randint(0, days_in_year - 1)
    random_seconds = random.randint(0, 86399)
    return start_date + timedelta(days=random_days, seconds=random_seconds)

def mode2_specific_year_commits(repo_path, filename):
    print_colored("\n" + "="*70, BLUE)
    print_colored("  MODE 2: Specific Year Commits", YELLOW, True)
    print_colored("="*70, BLUE)
    
    num_commits = get_positive_int("  How many commits to make", 20, max_value=10000)
    target_year = get_positive_int("  Target year (e.g. 2018)", 2018)
    target_year = validate_year(target_year)
    
    show_info(f"Making {num_commits} commits for {target_year}...")
    print()
    
    for i in range(num_commits):
        commit_date = random_date_in_year(target_year)
        show_progress(i + 1, num_commits, "Progress")
        make_commit_common(commit_date, repo_path, filename, "graph-greener!")
    
    print()
    show_success(f"Completed {num_commits} commits for {target_year}!")
    return True

# ============================================================================
# MODE 3: Year Range Random Commits
# ============================================================================
def random_date_in_year_v3(year, repo_path):
    year = validate_year(year)
    start_date = datetime(year, 1, 1)
    current_time = datetime.now()
    if year == current_time.year:
        end_date = current_time
    else:
        end_date = datetime(year, 12, 31, 23, 59, 59)
    
    delta = end_date - start_date
    if delta.total_seconds() <= 0:
        return current_time
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

def mode3_year_range_commits(repo_path, filename):
    print_colored("\n" + "="*70, BLUE)
    print_colored("  MODE 3: Year Range Random Commits", YELLOW, True)
    print_colored("="*70, BLUE)
    
    try:
        print_colored("  Start Year (e.g. 2012, default 2015): ", CYAN, end='')
        start_year_input = input().strip() or "2015"
        start_year = validate_year(int(start_year_input))
        
        print_colored("  How many years? (Max 10y, default 5y): ", CYAN, end='')
        duration_input = input().strip() or "5"
        duration = int(duration_input)
    except ValueError:
        show_error("Invalid input!")
        return False
    
    if duration > 10:
        show_warning("Limiting to 10 years for safety.")
        duration = 10
    if duration <= 0:
        show_error("Duration must be positive!")
        return False
    
    end_year = start_year + duration - 1
    current_year = datetime.now().year
    if end_year > current_year:
        show_warning(f"Limiting to current year ({current_year})")
        end_year = current_year
    
    show_info(f"Syncing from {start_year} to {end_year}")
    show_info("Each year will get 60 to 150 commits randomly.")
    
    total_commits = 0
    for year in range(start_year, end_year + 1):
        yearly_commits = random.randint(60, 150)
        print_colored(f"\n  Year {year}: {yearly_commits} commits", GREEN)
        
        for j in range(yearly_commits):
            commit_date = random_date_in_year_v3(year, repo_path)
            make_commit_common(commit_date, repo_path, filename, f"Sync {year}")
            
            if (j + 1) % 20 == 0:
                show_progress(j + 1, yearly_commits, f"Year {year}")
        
        print()
        show_success(f"Year {year} completed: {yearly_commits} commits")
        total_commits += yearly_commits
    
    print()
    show_success(f"Total commits made: {total_commits}")
    return True

# ============================================================================
# MODE 4: Name Graph Art (Full A-Z Support)
# ============================================================================
CHARACTERS = {
    'A': [(0,2), (1,1), (1,3), (2,0), (2,4), (3,0), (3,1), (3,2), (3,3), (3,4), (4,0), (4,4), (5,0), (5,4), (6,0), (6,4)],
    'B': [(0,0), (0,1), (0,2), (0,3), (1,0), (1,4), (2,0), (2,4), (3,0), (3,1), (3,2), (3,3), (4,0), (4,4), (5,0), (5,4), (6,0), (6,1), (6,2), (6,3)],
    'C': [(0,1), (0,2), (0,3), (1,0), (2,0), (3,0), (4,0), (5,0), (6,1), (6,2), (6,3)],
    'D': [(0,0), (0,1), (0,2), (0,3), (1,0), (1,4), (2,0), (2,4), (3,0), (3,4), (4,0), (4,4), (5,0), (5,4), (6,0), (6,1), (6,2), (6,3)],
    'E': [(0,0), (0,1), (0,2), (0,3), (0,4), (1,0), (2,0), (2,1), (2,2), (3,0), (4,0), (5,0), (6,0), (6,1), (6,2), (6,3), (6,4)],
    'F': [(0,0), (0,1), (0,2), (0,3), (0,4), (1,0), (2,0), (2,1), (2,2), (3,0), (4,0), (5,0), (6,0)],
    'G': [(0,1), (0,2), (0,3), (1,0), (2,0), (3,0), (3,2), (3,3), (4,0), (4,4), (5,0), (5,4), (6,1), (6,2), (6,3)],
    'H': [(0,0), (0,4), (1,0), (1,4), (2,0), (2,4), (3,0), (3,1), (3,2), (3,3), (3,4), (4,0), (4,4), (5,0), (5,4), (6,0), (6,4)],
    'I': [(0,0), (0,1), (0,2), (0,3), (0,4), (1,2), (2,2), (3,2), (4,2), (5,2), (6,0), (6,1), (6,2), (6,3), (6,4)],
    'J': [(1,4), (2,4), (3,4), (4,4), (5,0), (5,4), (6,1), (6,2), (6,3), (6,4)],
    'K': [(0,0), (0,4), (1,0), (1,3), (2,0), (2,2), (3,0), (3,1), (4,0), (4,2), (5,0), (5,3), (6,0), (6,4)],
    'L': [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (6,1), (6,2), (6,3), (6,4)],
    'M': [(0,0), (0,4), (1,0), (1,1), (1,3), (1,4), (2,0), (2,2), (2,4), (3,0), (3,4), (4,0), (4,4), (5,0), (5,4), (6,0), (6,4)],
    'N': [(0,0), (0,4), (1,0), (1,4), (2,0), (2,3), (3,0), (3,2), (4,0), (4,4), (5,0), (5,4), (6,0), (6,4)],
    'O': [(0,1), (0,2), (0,3), (1,0), (1,4), (2,0), (2,4), (3,0), (3,4), (4,0), (4,4), (5,0), (5,4), (6,1), (6,2), (6,3)],
    'P': [(0,0), (0,1), (0,2), (0,3), (1,0), (1,4), (2,0), (2,4), (3,0), (3,1), (3,2), (3,3), (4,0), (5,0), (6,0)],
    'Q': [(0,1), (0,2), (0,3), (1,0), (1,4), (2,0), (2,4), (3,0), (3,4), (4,0), (4,4), (5,0), (5,3), (6,1), (6,2), (6,4)],
    'R': [(0,0), (0,1), (0,2), (0,3), (1,0), (1,4), (2,0), (2,4), (3,0), (3,1), (3,2), (3,3), (4,0), (4,2), (5,0), (5,3), (6,0), (6,4)],
    'S': [(0,1), (0,2), (0,3), (0,4), (1,0), (2,0), (3,1), (3,2), (3,3), (4,4), (5,4), (6,0), (6,1), (6,2), (6,3)],
    'T': [(0,0), (0,1), (0,2), (0,3), (0,4), (1,2), (2,2), (3,2), (4,2), (5,2), (6,2)],
    'U': [(0,0), (0,4), (1,0), (1,4), (2,0), (2,4), (3,0), (3,4), (4,0), (4,4), (5,0), (5,4), (6,1), (6,2), (6,3)],
    'V': [(0,0), (0,4), (1,0), (1,4), (2,0), (2,4), (3,0), (3,4), (4,1), (4,3), (5,2), (6,2)],
    'W': [(0,0), (0,4), (1,0), (1,4), (2,0), (2,4), (3,0), (3,4), (4,0), (4,2), (4,4), (5,0), (5,1), (5,3), (5,4), (6,0), (6,4)],
    'X': [(0,0), (0,4), (1,1), (1,3), (2,2), (3,1), (3,3), (4,0), (4,4), (5,0), (5,4), (6,0), (6,4)],
    'Y': [(0,0), (0,4), (1,0), (1,4), (2,0), (2,4), (3,2), (4,2), (5,2), (6,2)],
    'Z': [(0,0), (0,1), (0,2), (0,3), (0,4), (1,4), (2,3), (3,2), (4,1), (5,0), (6,0), (6,1), (6,2), (6,3), (6,4)],
}

def find_first_sunday(year):
    year = validate_year(year)
    curr_date = datetime(year, 1, 1)
    while curr_date.strftime('%A') != 'Sunday':
        curr_date += timedelta(days=1)
    return curr_date

def mode4_name_graph(repo_path, filename):
    print_colored("\n" + "="*70, BLUE)
    print_colored("  MODE 4: Custom Name Graph Art", YELLOW, True)
    print_colored("="*70, BLUE)
    print_colored("  Supported: A-Z uppercase letters + Space", GREEN)
    print_colored("  Example: SABBIR, ABDULLAH, AL, HELLO, WORLD", CYAN)
    
    print_colored("\n  Target year (e.g. 2024, 2025): ", CYAN, end='')
    target_year_input = input().strip() or str(datetime.now().year)
    target_year = validate_year(int(target_year_input))
    
    print_colored("  Name to draw (A-Z and space only): ", CYAN, end='')
    text_input = input().strip().upper() or "SABBIR"
    text_to_draw = re.sub(r'[^A-Z ]', '', text_input)
    
    if not text_to_draw:
        show_error("No valid characters found!")
        return False
    
    start_date = find_first_sunday(target_year)
    show_success(f"First Sunday of {target_year}: {start_date.strftime('%Y-%m-%d')}")
    show_info(f"Drawing: '{text_to_draw}' (Length: {len(text_to_draw)})")
    show_info("Each pixel = 5 commits for dark green color")
    
    total_pixels = sum(len(CHARACTERS.get(c, [])) for c in text_to_draw if c in CHARACTERS)
    show_info(f"Total pixels to draw: {total_pixels}")
    
    current_start = start_date
    drawn_pixels = 0
    
    for char in text_to_draw:
        if char in CHARACTERS:
            pixels = CHARACTERS[char]
            print_colored(f"\n  Drawing '{char}'... ({len(pixels)} pixels)", GREEN)
            
            for row, col in pixels:
                target_date = current_start + timedelta(weeks=col, days=row)
                for commit_num in range(5):
                    filepath = os.path.join(repo_path, filename)
                    with open(filepath, "a") as f:
                        f.write(f"ART: {target_date.isoformat()} - Pixel for {char}\n")
                    
                    env = os.environ.copy()
                    env["GIT_AUTHOR_DATE"] = target_date.strftime("%Y-%m-%dT12:00:00")
                    env["GIT_COMMITTER_DATE"] = target_date.strftime("%Y-%m-%dT12:00:00")
                    
                    run_git_command(["git", "add", filename], cwd=repo_path, env=env)
                    run_git_command(["git", "commit", "-m", f"Art Pixel {char} ({commit_num+1}/5)"], cwd=repo_path, env=env)
                
                drawn_pixels += 1
                show_progress(drawn_pixels, total_pixels, "Drawing")
            
            current_start += timedelta(weeks=6)
        elif char == " ":
            print_colored(f"\n  Adding space gap (3 weeks)...", YELLOW)
            current_start += timedelta(weeks=3)
    
    print()
    show_success(f"Artwork Complete!")
    show_success(f"Total pixels drawn: {drawn_pixels}")
    show_success(f"Total commits made: {drawn_pixels * 5}")
    return True

# ============================================================================
# HELPER FUNCTION
# ============================================================================
def get_positive_int(prompt, default=20, max_value=None):
    while True:
        try:
            print_colored(prompt, CYAN, end='')
            user_input = input(f" (default {default}): ").strip()
            if not user_input:
                return default
            value = int(user_input)
            if value > 0:
                if max_value and value > max_value:
                    show_warning(f"Please enter a value less than or equal to {max_value}")
                    continue
                return value
            else:
                show_error("Please enter a positive integer.")
        except ValueError:
            show_error("Invalid input. Please enter a valid integer.")

# ============================================================================
# MAIN FUNCTION
# ============================================================================
def main():
    show_creator_info()
    
    # AUTO DETECT REPOSITORY
    show_info("Scanning for git repositories...")
    repo_path = get_default_repo()
    
    if not init_git_repo(repo_path):
        show_error("Failed to initialize repository!")
        return
    
    # AUTO CREATE/ENSURE data.txt
    filename = ensure_data_file(repo_path)
    show_success(f"Working with file: {filename}")
    
    print_colored("\n  SELECT A MODE:", YELLOW, True)
    print_colored("="*70, CYAN)
    print_colored("""
    1. MODE 1: Last Year Random Commits
       -> Random commits in last 365 days

    2. MODE 2: Specific Year Commits
       -> Commits for a specific year

    3. MODE 3: Year Range Random Commits
       -> 60-150 random commits per year

    4. MODE 4: Custom Name Graph Art
       -> Draw any name on GitHub graph
       -> Full A-Z support + Space
""")
    print_colored("="*70, CYAN)
    
    while True:
        try:
            print_colored("\n  Choose mode (1/2/3/4): ", CYAN, end='')
            mode = input().strip()
            if mode in ['1', '2', '3', '4']:
                break
            else:
                show_error("Please enter 1, 2, 3, or 4")
        except KeyboardInterrupt:
            print_colored("\n\n  Goodbye from ABDULLAH AL SABBIR!", YELLOW)
            show_footer()
            return
    
    success = False
    if mode == '1':
        success = mode1_last_year_commits(repo_path, filename)
    elif mode == '2':
        success = mode2_specific_year_commits(repo_path, filename)
    elif mode == '3':
        success = mode3_year_range_commits(repo_path, filename)
    elif mode == '4':
        success = mode4_name_graph(repo_path, filename)
    
    if not success:
        show_error("Operation failed!")
        show_footer()
        return
    
    print_colored("\n" + "="*70, BLUE)
    push_choice = input("  Push to remote? (y/n, default y): ").strip().lower()
    
    if push_choice != 'n':
        if has_remote(repo_path):
            push_to_remote(repo_path)
        else:
            show_warning("No remote origin found. Commits are only local.")
            print_colored("  To push to GitHub, first add remote:", YELLOW)
            print_colored("    git remote add origin <your-repo-url>", WHITE)
    else:
        show_info("Commits made locally. Push later with 'git push'")
    
    print_colored("\n" + "="*70, GREEN)
    print_colored("  ALL DONE! Check your GitHub contribution graph in a few minutes.", YELLOW, True)
    print_colored("="*70, GREEN)
    
    show_footer()

if __name__ == "__main__":
    main()