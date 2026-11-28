# Decisions

A record of what we decided and why. Add new decisions at the bottom.
Never delete an old one: if we change our minds, add a new entry that replaces it.

---

## Team and workflow

**D1. Roles (2026-11-24)**
Partner A handles Backend & Data, and Partner B handles Evaluation & Stats. We swap tasks freely.
*Why:* this follows the roadmap. Swapping keeps both of us learning every part.

**D2. `main` is protected (2026-11-24)**
All changes go through branch → Pull Request → the other partner approves → merge. Nobody pushes directly to `main`, including admins ("Do not allow bypassing" is on).
*Why:* every change gets a second pair of eyes, and `main` always works.

**D3. One branch per task, named after the phase (2026-11-24)**
Examples: `phase0-hello-api`, `phase0-mcp-server`, `phase0-emails`.
*Why:* this keeps PRs small and easy to review.

## Tools and project setup

**D4. Python project managed with uv (2026-11-24)**
We created it with `uv init --package`. The code lives in `src/workbench/`. Libraries are added with `uv add`, and `uv.lock` is committed. Every command runs through `uv run ...`.
*Why:* this gives both laptops exactly the same Python and the same library versions.

**D5. Libraries: `anthropic`, `mcp`, `python-dotenv`, `pytest` (2026-11-24)**
*Why:* they cover the API calls, the MCP server, reading `.env`, and tests.

**D6. A smoke test from day one (2026-11-24)**
`tests/test_smoke.py` checks that the package can be imported.
*Why:* `pytest` with no tests exits with an error code (5). The smoke test also proves the setup works on each laptop.

**D7. Database files are not committed (2026-11-24)**
`*.db` is in `.gitignore`.
*Why:* the SQLite database is created locally and would cause merge conflicts.

## Secrets and money

**D8. The API key lives only in `.env` (2026-11-24)**
`.env` is gitignored. `.env.example` is committed with an empty value.
Check for leaks with: `git log -p | Select-String "sk-ant"`.
*Why:* a leaked key can be used to spend our money. If one is ever committed, delete it in the Console immediately and create a new one.

**D9. Each partner uses their own key, in the same Console organisation (2026-11-24)**
A monthly spend limit is set in the Console.
*Why:* we never send keys over chat, either key can be cancelled without affecting the other, and the spend limit caps any mistake.

**D10. API key setup is postponed until Phase 1 (2026-11-28)**
Testing the MCP server in Claude Desktop uses the Claude Pro subscription and needs no API credits. The API key is only needed once our own code calls models: running prompts and the judge.
*Why:* we don't spend money before we need to. A Pro subscription cannot be used instead of an API key in our own code.

## Models and API

**D11. Model under test: `claude-haiku-5-5` (2026-11-24)**
*Why:* it is cheap (about $0.10 per million input tokens and $0.50 per million output tokens) and fast, so a full run of 60 emails costs about a cent.

**D12. Judge model (later phases): `claude-sonnet-5-5` (2026-11-24)**
*Why:* grading needs a stronger model than the one being graded.

**D13. Use `effort` instead of `temperature` (2026-11-24)**
Current models reject `temperature`. We pass `output_config={"effort": "low"}`. Each run records the effort setting where the roadmap says to store the temperature.
*Why:* the roadmap was written for older models.

**D14. Read the `text` block of a response (2026-11-24)**
A response can start with a "thinking" block, so we take the block where `type == "text"`, not simply `content[0]`.
*Why:* otherwise we would sometimes read the wrong thing.

## MCP server

**D15. Use `MCPServer`, not `FastMCP` (2026-11-24)**
`from mcp.server.mcpserver import MCPServer`
*Why:* version 2 of the `mcp` library renamed `FastMCP`, so the roadmap's import no longer works.

**D16. Never use `print()` in the server; log with `logging` (2026-11-24)**
*Why:* Claude Desktop talks to the server over standard output, so a `print()` corrupts the connection. Log messages go to stderr instead.

**D17. The Claude Desktop config uses absolute paths (2026-11-28)**
The command is the full path to `uv.exe`, and the args are `["--directory", "<project folder>", "run", "src/workbench/server.py"]`. Use `\\` in the JSON. Each partner edits their own config with their own paths: in Claude Desktop, go to ☰ → Developer → Open App Config File, and add an `mcpServers` section without removing the existing settings. After a change, use Developer → Reload MCP Configuration, or fully quit and reopen the app.
*Why:* Claude Desktop starts in a different folder, so relative paths fail.

## Test data

**D18. The task: classify a customer email into exactly one label (2026-11-28)**
The labels are `billing`, `bug` and `feature_request`, in lowercase English, even when the email is in another language.
*Why:* with one fixed set of answers, scoring is a simple exact match.

**D19. Test set v1 format (2026-11-28)**
`data/emails_v1.json` holds 60 emails, each with `id`, `input`, `expected` and `category`.
- Categories: `normal` (30), `short`, `typo`, `mixed_topic` and `non_english` (7–8 each).
- 20 emails per label.
- Ids (`e001`...) are never reused or renumbered.
*Why:* the category lets us see *where* a model fails, not just how often.

**D20. Rule for mixed-topic emails (2026-11-28)**
The label is the customer's **main request**: what they want done.
Example: *"Love the app! Please add CSV export. My last invoice looked fine."* → `feature_request`.
*Why:* both partners must label tricky emails the same way.

**D21. Topic words don't decide the label (2026-11-28)**
*"The payment page won't load"* is a `bug`. *"Please add PayPal"* is a `feature_request`.
*Why:* these cases test whether a model actually understands the email, or only matches keywords.

**D22. Never edit a test set after it is used; make a new version (2026-11-28)**
Fixes go into `emails_v2.json`.
*Why:* old scores stay comparable. The partner who didn't write the set checks 20 random emails before it is merged.
