# ticket-cleaner

Checks support-ticket records from a CSV file, a JSON file or a web service, and writes a summary report. Every record that is not valid is listed in the report, with the reason.

## Requirements

- Python 3.12 or newer. Check with `python3 --version` (`python --version` on Windows).
- No account. The `remote` input downloads a public file.

## Set up

Do these steps once, in a terminal in this folder.

1. Make a virtual environment: `python3 -m venv .venv`. On Windows, type `python` instead of `python3`.
2. Activate it. On macOS and Linux: `source .venv/bin/activate`. On Windows (PowerShell): `.venv\Scripts\Activate.ps1`. The prompt now starts with `(.venv)`.
3. Install the exact versions of the dependencies: `python -m pip install -r requirements-lock.txt`

## Run

```sh
python -m ticket_cleaner data/tickets.csv
```

Expected output (the last lines):

```text
15 vé: 9 hợp lệ, 6 bị loại.
Báo cáo lưu tại: reports/summary.json
```