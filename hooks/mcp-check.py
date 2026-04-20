#!/usr/bin/env python3
"""MCP Connection Validator for the /chief skill.

Fires once per session on the first /chief prompt.
Injects a validation instruction into Claude's context so it tests
all required MCP servers before proceeding.

Installation:
  Copy to ~/.claude/hooks/mcp-check.py and register in ~/.claude/settings.json:

  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.claude/hooks/mcp-check.py"
      }]
    }]
  }
"""
import sys
import json
import pathlib

data = json.loads(sys.stdin.read())
prompt = data.get("prompt", "")
session_id = data.get("session_id", "nosession")

# Only trigger for /chief prompts
if not prompt.startswith("/chief"):
    sys.exit(0)

# Session-based dedup — only run once per session
lockfile = pathlib.Path(f"/tmp/.claude_mcp_validated_{session_id}")
if lockfile.exists():
    sys.exit(0)
lockfile.touch()

# Inject context telling Claude to validate MCP connections before proceeding
additional_context = "\n".join([
    "SYSTEM: MCP Health Check (once per session, triggered by first /chief)",
    "",
    "Before fulfilling this request, validate each required MCP server by making a",
    "lightweight test call. Display results, then proceed as described.",
    "",
    "Test calls to make (run in parallel if possible):",
    "  Notion  → notion-search with query \"\"",
    "  Slack   → slack_search_channels with query \"\"",
    "  HubSpot → get_user_details",
    "  Grain   → myself",
    "  Figma   → whoami",
    "  Pylon   → authenticate",
    "  Jira    → mcp__atlassian__atlassianUserInfo (no params needed)",
    "  Gmail   → run: gws gmail users getProfile --params '{\"userId\": \"me\"}'",
    "            (if gws is not installed or auth fails, mark as DOWN)",
    "  GCal    → run: gws calendar +agenda --today",
    "            (if gws is not installed or auth fails, mark as DOWN)",
    "  GDrive  → run: gws drive about get --params '{\"fields\": \"user\"}'",
    "            (if gws is not installed or auth fails, mark as DOWN)",
    "",
    "Output format (print this FIRST, before any other response):",
    "",
    "  MCP Health Check",
    "  ─────────────────────────",
    "  Notion    [ OK | DOWN ]",
    "  Slack     [ OK | DOWN ]",
    "  HubSpot   [ OK | DOWN ]",
    "  Grain     [ OK | DOWN ]",
    "  Figma     [ OK | DOWN ]",
    "  Pylon     [ OK | DOWN ]",
    "  Jira      [ OK | DOWN ]",
    "  Gmail     [ OK | DOWN ]",
    "  GCal      [ OK | DOWN ]",
    "  GDrive    [ OK | DOWN ]",
    "  ─────────────────────────",
    "",
    "If ALL are OK  → proceed with the original request immediately.",
    "If ANY are DOWN → show the table, list which servers failed, and ask",
    "                  whether to proceed anyway or fix the connection first.",
    "DOWN means the tool/binary is unavailable or auth has expired — mention it but do not block on it.",
])

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": additional_context,
    }
}))
