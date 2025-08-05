# ZSim Quick Start Guide

## Download and Launch

Download the latest packaged source code from the [release page](https://github.com/ZZZSimulator/ZSim/releases/latest) or use the `git clone` command to download the latest source code directly.

### Install UV (if not already installed)

Execute in any terminal:

```bash
# If you have python or pip installed, you can use pip to install:
pip install uv
```

If you don't have python:

```bash
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Windows 11 24H2 and above:
winget install --id=astral-sh.uv -e
```

```bash
# Older Windows versions:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or refer to the official installation guide: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

### Install ZZZ Simulator

Execute in the project directory:

```bash
uv sync
uv pip install .  # The '.' here represents the relative path
```

## Running Instructions

Execute in any terminal (some operating systems may require a terminal restart):

```bash
zsim run
```

If you don't want to install this tool, or if the previous step was unsuccessful, you can run it directly:

```bash
uv run ./zsim/run.py run
```

```bash
# Or use:
uv run zsim run
```

---

## How to Start Simulation

1. On the **Character Edit** page, select characters from the drop-down menu (the initial standing order of the characters is the same as the game logic).
2. Expand the configuration list for each character in order to modify their equipment.
3. After completing the modifications, click the **Submit and Save Character Configuration** button at the bottom of the page to save the configuration.
4. Click the **Simulator** button in the left tab bar to switch to the simulator page.
5. Fill in the simulation duration (unit: frames), select the current team's APL through the **APL Selection Button**, and then click the **Save APL Selection** button to save.
6. Click the **Start Simulation** button to start the simulation.
7. On the **"Data Analysis"** page, click the **Start Data Analysis** button to automatically analyze the simulation data. After the analysis is complete, you can expand to view the results.

---

## FAQ

1. This project is currently in the testing and development stage. If you encounter any program errors, please provide the **reproduction steps** and **error log** to the developer team.
2. The front-end interface of this project is for temporary use only. We will re-develop the user interface in the future.
