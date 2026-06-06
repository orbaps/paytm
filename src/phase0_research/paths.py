from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
SAMPLES_DIR = DATA_DIR / "samples"
PROCESSED_DIR = DATA_DIR / "processed"
RAW_DIR = DATA_DIR / "raw"
SCHEMAS_DIR = PROJECT_ROOT / "schemas"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
ANALYSIS_OUTPUT_DIR = OUTPUTS_DIR / "analysis"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path
