# Studio Timesheet

A small background tracker that logs time spent working in Roblox Studio. When you open a Studio project, the script asks which project you're working on, measures how long the project stays open, and adds the hours to an Excel timesheet.

> **Status:** Prototype (`v2`). Windows only.

## Features

- Detects when Roblox Studio is running and when a project is open, based on the window title
- Prompts for a project name each time a project opens
- Accumulates hours per project across sessions, so repeat work adds to the same row
- Saves to an Excel file, so the results can be opened and edited in Excel or Sheets

## Requirements

- Windows (uses the Win32 API through `pywin32`)
- Python 3.10 or newer
- Roblox Studio

Python packages:

```bash
pip install psutil pywin32 openpyxl
```

## Setup

The script expects a spreadsheet at `data/hours.xlsx`, one directory above `protype/`. The repository doesn't include it, so create it before the first run:

1. Create a `data/` folder next to `protype/`.
2. In `data/`, create `hours.xlsx`.
3. On the first sheet, use column A for project names and column B for hours. The script writes hours as decimal numbers (for example, `1.25` for 1 hour 15 minutes).

Final layout:

```
studio-timesheet/
├── data/
│   └── hours.xlsx
└── protype/
    └── proto.py
```

## Usage

```bash
cd protype
python proto.py
```

Leave the script running. Then:

1. Open Roblox Studio. The script detects the process and starts watching.
2. Open a project. When its window title changes from a generic title to a project title, the script asks you to enter a project name.
3. Work as usual. The script tracks elapsed time in the background.
4. Close the project. The elapsed time is added to that project's row and the file is saved.
5. Close Studio. Any open session is saved automatically.

Press `Ctrl+C` to stop the script. Note that a session still in progress may not be saved if you stop the script before closing the project or Studio.

## How It Works

The script checks once per second:

- It looks for a running `RobloxStudioBeta.exe` process.
- It reads the visible window titles for that process.
- Titles in `GENERIC_TITLES` (`Roblox Studio`, `Auto-Recovery`) are treated as "no project open." Any other title is treated as a project being open.
- Elapsed time is measured with `time.monotonic_ns()`, so clock changes don't affect it.

## Known Limitations

- **Windows only.** The Win32 imports (`win32gui`, `win32process`) won't run on macOS or Linux.
- **Saves only on session end.** Hours are written to the spreadsheet when a project closes or Studio closes. If the script crashes mid-session, that session's time is lost.
- **Title-based detection.** Project detection depends on Studio's window titles. If Roblox changes how it titles windows, detection will break.
- **Excel file must not be open.** Saving fails if `hours.xlsx` is locked by Excel.
- **Project name is the key.** Entering the same name reuses the existing row. Entering a slightly different name (for example, a typo) creates a new row.

## Roadmap

- [ ] Save periodically during a session, not only on close
- [ ] Add a summary view (hours per project per week)
- [ ] Support macOS
- [ ] Handle errors when the spreadsheet is locked

## Contributing

Contributions are welcome. Open an issue to discuss larger changes before submitting a pull request.

## License

MIT
