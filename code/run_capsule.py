import json
import logging
import os

from aind_physiology_fip import data_qc
from log_schema import setup_logging
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings
from qc_exporter import to_ads, QCCli


class InputSettings(BaseSettings, cli_parse_args=True):
    """
    Settings for Harp Fiber Data NWB Packaging
    """

    input_directory: Path = Field(
        default=Path("/data/fiber_raw_data"), description="Directory where data is"
    )
    output_directory: Path = Field(
        default=Path("/results/"), description="Output directory"
    )

def run() -> None:
    """
    Entrypoint for executing
    """
    settings = InputSettings()
    paths = tuple(settings.input_directory.glob("fib/*"))
    primary_data_path = [path for path in paths if path.is_dir()]
    if not primary_data_path:
        raise FileNotFoundError("No primary data asset attached")

    if len(primary_data_path) > 1:
        raise ValueError(
            "Multiple primary data assets attached. Only single asset needed"
        )

    with open(settings.input_directory / "data_description.json", "r") as f:
        data_description = json.load(f)
    
    acquisition_name = data_description["name"]
    ### logging setup
    process_name = os.getenv("PROCESS_NAME", "aind-fip-harp-qc-raw")
    pipeline_name = os.getenv("PIPELINE_NAME", "")
    setup_logging(
        (Path(__file__).parent / "logging.yml").as_posix(),
        model={
            "acquisition_name": acquisition_name,
            "process_name": process_name,
            "pipeline_name": pipeline_name    
        },
    )

    logging.info("Begin processing...", extra={"event_type": "stage_start"})
    logging.info(f"Running qc on primary data {acquisition_name}")
    parsed_args = QCCli(
        data_path=primary_data_path[0], qc_json_path=settings.output_directory, asset_path=settings.output_directory / "qc-raw"
    )
    dataset = data_qc.dataset(parsed_args.data_path)

    runner = data_qc._run_tests(dataset)
    qc_json = to_ads(runner, parsed_args)
    if parsed_args.qc_json_path is not None:
        with open(parsed_args.qc_json_path / "quality_control.json", "w", encoding="utf-8") as f:
            f.write(qc_json.model_dump_json(indent=2))
    
    logging.info(f"Finished qc. Output saved to {settings.output_directory}")
    logging.info("Pipeline stage completed", extra={"event_type": "stage_complete"})

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logging.exception("Pipeline stage failed", extra={"event_type": "stage_error"})
