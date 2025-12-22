#!/usr/bin/env python3
"""
Temporary test script to verify extract_fl_results works correctly on a single instance.
"""

import os
import sys
import json
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath('../..'))

from app.search.search_backend import SearchBackend
from app.data_structures import BugLocation

SETUP_MAP_PATH = '../../SWE-bench/setup_result/setup_map.json'
TASKS_MAP_PATH = '../../SWE-bench/setup_result/tasks_map.json'

def checkout_commit(repo_path, commit_hash):
    """
    해당 레포지토리 경로에서 특정 커밋으로 체크아웃합니다.
    """
    print(f"    [GIT] Checking out commit {commit_hash} in {repo_path}...")
    try:
        # 강제로 체크아웃 (기존 변경사항 무시)
        subprocess.run(
            ['git', 'checkout', '-f', commit_hash], 
            cwd=repo_path, 
            check=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.PIPE
        )
        print(f"    [GIT] Successfully checked out to {commit_hash}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"    [GIT ERROR] Failed to checkout: {e.stderr.decode().strip()}")
        return False

def test_extract_fl_results(instance_dir, fl_base_dir):

    filtered_results = []
    
    print(f"\n{'='*80}")
    print(f"Testing instance: {instance_dir}")
    print(f"{'='*80}\n")

    parts = instance_dir.split('_')
    # Find the index where the date starts (YYYY-MM-DD format)
    date_idx = None
    for i, part in enumerate(parts):
        if len(part) == 4 and part.isdigit():  # Year
            date_idx = i
            break

    if date_idx:
        instance_name_parts = parts[:date_idx]
        instance_name = '_'.join(instance_name_parts)
    else:
        # Fallback
        instance_name = f"{parts[0]}__{parts[2]}" if len(parts) > 2 else instance_dir
    
    print(f"[1] Parsed instance name: {instance_name}")
    print(f"    - Original dir: {instance_dir}")
    print(f"    - Parts: {parts}")
    print(f"    - Date index: {date_idx}")

    with open(SETUP_MAP_PATH, 'r') as f:
        setup_map = json.load(f)
    potential_path = setup_map[instance_name]["repo_path"]

    with open(TASKS_MAP_PATH, 'r') as f:
        tasks_map = json.load(f)
    task_info = tasks_map[instance_name]
    task_commit = task_info.get("base_commit") or task_info.get("commit")
    print(potential_path)
    print(task_commit)

    checkout_commit(potential_path, task_commit)


    # Get project path for SearchBackend
    # Extract repo base: e.g., "astropy__astropy-6938" -> "astropy__astropy"
    # if '-' in instance_name:
    #     repo_base = instance_name.rsplit('-', 1)[0]
    # else:
    #     repo_base = instance_name
    
    # print(f"\n[2] Extracted repo_base: {repo_base}")

    # testbed_base = '../../SWE-bench/testbed'
    project_path = None
    
    # testbed structure: testbed/astropy__astropy/astropy/astropy
    # potential_path = os.path.join(testbed_base, repo_base)

    print(f"\n[3] Looking for project path:")
    print(f"    - Potential path: {potential_path}")
    print(f"    - Exists: {os.path.exists(potential_path)}")

    if os.path.exists(potential_path):
        project_path = potential_path

    # Read before_process
    fl_before_process_path = os.path.join(fl_base_dir, instance_dir, 'output_0', 'search', 'bug_locations_before_process.json')
    try:
        with open(fl_before_process_path, 'r') as f:
            fl_before_process = json.load(f)
    except:
        fl_before_process = []

    if not fl_before_process:
        filtered_results = []
        print("No resuls in fl_before_process")
        return filtered_results
    
    print(f"    - Number of FL requests: {len(fl_before_process)}")
    
    # 수정사항 1: project_path를 못찾으면 빈 리스트
    if not project_path or not os.path.exists(project_path):
        print("No project path")
        return []

    print(f"\n[5] Initializing SearchBackend...")
    # Use SearchBackend
    try:
        backend = SearchBackend(project_path)
        print(f"    - SearchBackend initialized successfully")
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize SearchBackend: {e}")
        return []

    print(f"\n[6] Processing FL requests:")
    for idx, bug_location_dict in enumerate(fl_before_process):
        tmp_file_name = bug_location_dict.get("file", "")
        tmp_method_name = bug_location_dict.get("method", "")
        tmp_class_name = bug_location_dict.get("class", "")
        intended_behavior = bug_location_dict.get("intended_behavior", "")

        print(f"\n    Request #{idx + 1}:")
        print(f"    - File: {tmp_file_name}")
        print(f"    - Class: {tmp_class_name}")
        print(f"    - Method: {tmp_method_name}")

        # Handle Class.method format
        if not tmp_class_name and tmp_method_name and "." in tmp_method_name:
            fragments = tmp_method_name.split(".")
            if len(fragments) == 2:
                tmp_class_name, tmp_method_name = fragments

        if not (tmp_method_name or tmp_class_name or tmp_file_name):
            continue

        call_ok = False
        search_res = []

        # 수정사항 3: 정확한 조건에서만 검색
        # Case 1: method + class

        if tmp_method_name and tmp_class_name:
            output, curr_search_res, call_ok = backend.search_method_in_class(
                tmp_method_name, tmp_class_name
            )
            search_res.extend(curr_search_res)

            # 수정사항 2: inherited methods는 포함하지만 class context는 제외
            if call_ok:
                for res in curr_search_res:
                    if (res.class_name is None or
                        res.func_name is None or
                        res.file_path is None):
                        continue

                    inherited_output, inherited_search_res, _ = (
                        backend._get_inherited_methods(res.class_name, res.func_name)
                    )
                    search_res.extend(inherited_search_res)

        # Case 2: method + file (no class)
        elif tmp_method_name and tmp_file_name and not tmp_class_name:
            output, search_res, call_ok = backend.search_method_in_file(
                tmp_method_name, tmp_file_name
            )

        # Case 3: class + file (no method)
        elif tmp_class_name and tmp_file_name and not tmp_method_name:
            output, search_res, call_ok = backend.search_class_in_file(
                tmp_class_name, tmp_file_name
            )

        # Case 4: class only (no file, no method)
        elif tmp_class_name and not tmp_file_name and not tmp_method_name:
            output, search_res, call_ok = backend.get_class_full_snippet(tmp_class_name)

        # Case 5: method only (no file, no class)
        elif tmp_method_name and not tmp_file_name and not tmp_class_name:
            output, search_res, call_ok = backend.search_method(tmp_method_name)

        # Case 6: file only (no method, no class)
        elif tmp_file_name and not tmp_method_name and not tmp_class_name:
            output, search_res, call_ok = backend.get_file_content(tmp_file_name)
        print(f"    - SearchBackend returned {len(search_res)} results")

        for r_idx, result in enumerate(search_res):
            print(f"      Result {r_idx + 1}:")
            print(f"        - File: {result.file_path}")
            print(f"        - Class: {result.class_name}")
            print(f"        - Method: {result.func_name}")
            print(f"        - Lines: {result.start}-{result.end}")

        # Convert SearchResult to BugLocation
        final_bug_locs = []
        for res in search_res:
            if res.start is None or res.end is None:
                continue
            new_bug_loc = BugLocation(res, project_path, intended_behavior)
            final_bug_locs.append(new_bug_loc)

        # Remove duplicates
        unique_bug_locations = []
        for loc in final_bug_locs:
            if loc not in unique_bug_locations:
                unique_bug_locations.append(loc)

        # Add to result
        if unique_bug_locations:
            for loc in unique_bug_locations:
                bug_loc_dict = loc.to_dict()
                filtered_results.append(bug_loc_dict)
            
    return filtered_results
        
    

if __name__ == "__main__":
    # Test configuration
    fl_base_dir = "/home/kimnal0/auto-code-rover/fl_outputs/only_fl_output_mixtral_2/no_patch"

    # Find a test instance
    test_instance = None
    if os.path.exists(fl_base_dir):
        instances = [d for d in os.listdir(fl_base_dir) if os.path.isdir(os.path.join(fl_base_dir, d))]
        if instances:
            test_instance = instances[0]
            test_instance = 'django__django-13925_2025-12-01_04-00-00'  # Use first available instance
            print(f"Found test instance: {test_instance}")

    if test_instance:
        results = test_extract_fl_results(test_instance, fl_base_dir)

        print(f"\n{'='*80}")
        print(f"TEST COMPLETE")
        print(f"{'='*80}")
        print(f"Results: {len(results)} bug locations extracted")

        # Optionally save to file for inspection
        output_file = "/tmp/test_fl_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {output_file}")
    else:
        print("ERROR: No test instance found!")