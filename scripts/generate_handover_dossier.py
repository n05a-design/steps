"""
STEPS AI Context Handover Dossier Generator.

Generates the complete 15-document handover package in AI_CONTEXT_HANDOVER/
and builds the ZIP archive "Antigravity Steps Bericht.zip".

Adheres to:
- MASTER-PROMPT: VOLLSTÄNDIGE KI-ARBEITSREKONSTRUKTION, KONTEXTSICHERUNG, PROJEKTÜBERGABE UND ÜBERGABEREIFEPRÜFUNG
- User instruction: "Datei später zum Download als Zip anbieten mit dem Namen 'Antigravity Steps Bericht'"
"""

import os
import sys
import json
import re
import zipfile
import subprocess
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(REPO_ROOT, "AI_CONTEXT_HANDOVER")
TRANSCRIPT_PATH = r"C:\Users\Timvo\.gemini\antigravity\brain\b744fb20-9665-4dda-ad3a-675b8210adfa\.system_generated\logs\transcript.jsonl"
TRANSCRIPT_FULL_PATH = r"C:\Users\Timvo\.gemini\antigravity\brain\b744fb20-9665-4dda-ad3a-675b8210adfa\.system_generated\logs\transcript_full.jsonl"
ARTIFACT_DIR = r"C:\Users\Timvo\.gemini\antigravity\brain\b744fb20-9665-4dda-ad3a-675b8210adfa"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_transcript():
    user_inputs = []
    planner_responses = []
    with open(TRANSCRIPT_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            obj = json.loads(line)
            stype = obj.get('type')
            if stype == 'USER_INPUT':
                user_inputs.append(obj)
            elif stype == 'PLANNER_RESPONSE':
                planner_responses.append(obj)
    return user_inputs, planner_responses

def get_git_commits():
    try:
        out = subprocess.check_output(
            ['git', 'log', '--pretty=format:%H|%an|%ad|%s', '--date=iso'],
            cwd=REPO_ROOT, text=True
        )
        commits = []
        for line in out.strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) >= 4:
                    commits.append({
                        'sha': parts[0],
                        'author': parts[1],
                        'date': parts[2],
                        'subject': parts[3]
                    })
        return commits
    except Exception as e:
        return []

def get_git_branches():
    try:
        out = subprocess.check_output(['git', 'branch', '-a'], cwd=REPO_ROOT, text=True)
        return [b.strip() for b in out.strip().split('\n') if b.strip()]
    except Exception:
        return []

print(f"Loaded base extraction functions for REPO_ROOT={REPO_ROOT}")
