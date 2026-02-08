# Usage Guide for NECHTO Runtime (v4.8)

This guide explains how to install the runtime, run measurements locally, understand where the results are stored, and trigger the GitHub workflow to measure a text prompt. The goal is to make it easy for newcomers to get started.

## Installation

1. Install **Python 3.8 or newer** on your system.
2. Clone this repository or download its source code.
3. From the repository root, install the package in editable mode:
   ```sh
   python -m pip install -e .
   ```

This will install the `nechto_runtime` package and its dependencies so that you can run it from the command line.

## Measuring a prompt locally

You can run the runtime locally on any input text. The command reads from **STDIN** and writes results to files inside the `docs/` folder. For example:

```sh
echo "Your text prompt goes here" | python -m nechto_runtime measure
```

After the command finishes, two result files will be generated (or overwritten):

- `docs/latest_contract.md` – a human‑readable summary of the extracted epistemic claims and metrics.
- `docs/latest_metrics.json` – a machine‑readable JSON file containing all computed metrics and values.

If the `docs/` folder does not exist yet, it will be created automatically.

## Understanding the results

- **latest_contract.md** contains a table of epistemic claims extracted from your prompt and shows harm probability, alignment score and ethical coefficient. It serves as the contract explaining how the system interpreted the input.
- **latest_metrics.json** includes numerical metrics (GED proxy, harm probability, identity alignment, ethical coefficient, etc.) used by the runtime. Use this file for programmatic analysis or further processing.

## Running the GitHub workflow

The repository contains a workflow that allows you to run the measurement in the cloud directly from GitHub. To trigger it:

1. Navigate to the **Actions** tab of the GitHub repository.
2. Select the workflow named **NECHTO Measure** (defined in `.github/workflows/measure.yml`).
3. Click **Run workflow** and enter your prompt into the input field. The workflow will run the same command as shown above and commit the updated `docs/latest_contract.md` and `docs/latest_metrics.json` back to the `nechto-runtime` branch (or a metrics branch if configured).

After the workflow completes, you can view the updated results files in the repository. These files are version controlled so that each run is recorded.
