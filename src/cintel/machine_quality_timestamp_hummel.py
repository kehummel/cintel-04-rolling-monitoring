"""
rolling_monitor_case.py - Project script (example).

Author: Denise Case, Kimberly Hummel
Date: 2026-03

Time-Series System Metrics Data

- Data is taken from a system that records a specific machine's operational metrics over time.
- Each row represents one observation at a specific timestamp.
- The CSV file includes these columns:
  - timestamp: when the observation occurred
  - temperature: the temperature measured in Celcius
  - Machine Speed: how fast the machine is going measured in reps per minute
  - Production Quality Score: score based out of 10
  - Vibration Level: the amount of movement/vibration measured in millimeters per second
  - Energy Consumption: amount of energy used per hour, measured in kilowatts per hour
  - Optimal Conditions: whether or not the optimal conditions were met; 1 for yes and 0 for no

Purpose

- Read time-series system metrics from a CSV file.
- Demonstrate rolling monitoring using a moving window.
- Compute rolling averages to smooth short-term variation.
- Save the resulting monitoring signals as a CSV artifact.
- Log the pipeline process to assist with debugging and transparency.

Questions to Consider

- How does system behavior change over time? - Does the machine speed slow down? Does the vibration level increase?
- Why might a rolling average reveal patterns that individual observations hide?
- How can smoothing short-term variation help us understand longer-term trends?

Paths (relative to repo root)

    INPUT FILE: data/machine_quality_hummel.csv
    OUTPUT FILE: artifacts/rolling_machine_quality_hummel.csv

Terminal command to run this file from the root project folder

    uv run python -m cintel.machine_quality_timestamp_hummel

"""

# === DECLARE IMPORTS ===

import logging
from pathlib import Path
from typing import Final

import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P5", level="DEBUG")

# === DEFINE GLOBAL PATHS ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

DATA_FILE: Final[Path] = DATA_DIR / "machine_quality_hummel.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "rolling_machine_quality_hummel.csv"

# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Run the pipeline.

    log_header() logs a standard run header.
    log_path() logs repo-relative paths (privacy-safe).
    """
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    # Ensure artifacts directory exists
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    # ----------------------------------------------------
    # STEP 1: READ CSV DATA FILE INTO A POLARS DATAFRAME (TABLE)
    # ----------------------------------------------------
    df = pl.read_csv(DATA_FILE)

    LOG.info(f"Loaded {df.height} time-series records")

    # ----------------------------------------------------
    # STEP 2: SORT DATA BY TIME
    # ----------------------------------------------------
    # Time-series analysis requires observations to be ordered.
    df = df.sort("Timestamp")

    LOG.info("Sorted records by timestamp")

    # ----------------------------------------------------
    # STEP 3: DEFINE ROLLING WINDOW RECIPES
    # ----------------------------------------------------
    # A rolling window computes statistics over the most recent
    # N observations. The window "moves" forward one row at a time.

    # Example: if WINDOW_SIZE = 3
    # row 1 → mean of rows [1]
    # row 2 → mean of rows [1,2]
    # row 3 → mean of rows [1,2,3]
    # row 4 → mean of rows [2,3,4]

    WINDOW_SIZE: int = 30

    # ----------------------------------------------------
    # STEP 3.1: DEFINE ROLLING MEAN FOR TEMPERATURE
    # ----------------------------------------------------
    # The `temperature` column tells the temperature of the machine at each timestamp.
    temperature_rolling_mean_recipe: pl.Expr = (
        pl.col("Temperature (C)")
        .rolling_mean(WINDOW_SIZE)
        .round(2)
        .alias("temperature_rolling_mean")
    )

    # ----------------------------------------------------
    # STEP 3.2: DEFINE ROLLING MEAN FOR MACHINE SPEED
    # ----------------------------------------------------
    # The `machine speed` column tells how fast the machine is moving at each timestamp.
    machine_speed_rolling_mean_recipe: pl.Expr = (
        pl.col("Machine Speed (RPM)")
        .rolling_mean(WINDOW_SIZE)
        .round(2)
        .alias("machine_speed_rolling_mean")
    )

    # ----------------------------------------------------
    # STEP 3.3: DEFINE ROLLING MEAN FOR VIBRATION LEVEL
    # ----------------------------------------------------
    # The `vibration level` column tells the amount of movement in millimeters per second at each timestamp.
    vibration_level_rolling_mean_recipe: pl.Expr = (
        pl.col("Vibration Level (mm/s)")
        .rolling_mean(WINDOW_SIZE)
        .round(2)
        .alias("vibration_rolling_mean")
    )

    # ----------------------------------------------------
    # STEP 3.4: DEFINE ROLLING MEAN FOR ENERGY CONSUMPTION
    # ----------------------------------------------------
    # The `energy consumption` column tells the amount of energy in kilowatts per hour being used at each timestamp.
    energy_rolling_mean_recipe: pl.Expr = (
        pl.col("Energy Consumption (kWh)")
        .rolling_mean(WINDOW_SIZE)
        .round(2)
        .alias("energy_consumption_rolling_mean")
    )
    # ----------------------------------------------------
    # STEP 3.5: APPLY THE ROLLING RECIPES IN A NEW DATAFRAME
    # ----------------------------------------------------
    # with_columns() evaluates the recipes and adds the new columns
    df_with_rolling = df.with_columns(
        [
            temperature_rolling_mean_recipe,
            machine_speed_rolling_mean_recipe,
            vibration_level_rolling_mean_recipe,
            energy_rolling_mean_recipe,
        ]
    )

    LOG.info("Computed rolling mean signals")

    # ----------------------------------------------------
    # STEP 4: SAVE RESULTS AS AN ARTIFACT
    # ----------------------------------------------------
    df_with_rolling.write_csv(OUTPUT_FILE)
    LOG.info(f"Wrote rolling monitoring file: {OUTPUT_FILE}")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")

    if len(df_with_rolling) > 300:
        for i, row in enumerate(df_with_rolling.iter_rows(named=True)):
            if row["temperature_rolling_mean"] is not None and (i + 1) % 30 == 0:
                LOG.info(
                    f"Row {i + 1}: "
                    f"temp={row['temperature_rolling_mean']:.2f}, "
                    f"speed={row['machine_speed_rolling_mean']:.2f}, "
                    f"vibration={row['vibration_rolling_mean']:.2f}, "
                    f"energy={row['energy_consumption_rolling_mean']:.2f}"
                )

    LOG.info("========================")
    LOG.info("END main()")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
