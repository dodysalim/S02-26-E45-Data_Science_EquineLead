import importlib.util
from pathlib import Path

import pandas as pd

spec = importlib.util.spec_from_file_location(
    "equine_data", Path(__file__).resolve().parents[1] / "app/utils/data_loader.py"
)
loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loader)


def test_dvc_output_is_loaded_without_copying_to_app(tmp_path, monkeypatch):
    monkeypatch.delenv("EQUINE_DATA_DIR", raising=False)
    monkeypatch.setattr(loader, "PROJECT_ROOT", tmp_path)
    data = tmp_path / "data/clean"
    data.mkdir(parents=True)
    pd.DataFrame({"first_seen": ["2025-01-02"], "country": ["Ecuador"]}).to_parquet(
        data / "users_info.parquet"
    )
    actual = loader.load_data.__wrapped__("users_info.parquet")
    assert actual.country.tolist() == ["Ecuador"]
    assert pd.api.types.is_datetime64_any_dtype(actual.first_seen)


def test_complete_dvc_folder_beats_partial_app_snapshot(tmp_path, monkeypatch):
    monkeypatch.delenv("EQUINE_DATA_DIR", raising=False)
    monkeypatch.setattr(loader, "PROJECT_ROOT", tmp_path)
    app = tmp_path / "app/data/clean"
    app.mkdir(parents=True)
    (app / "users_info.parquet").touch()
    dvc = tmp_path / "data/clean"
    dvc.mkdir(parents=True)
    for name in loader.REQUIRED_DATA_FILES:
        (dvc / name).touch()
    assert loader.get_data_directory() == dvc


def test_explicit_data_directory_is_respected(tmp_path, monkeypatch):
    monkeypatch.setenv("EQUINE_DATA_DIR", str(tmp_path))
    assert loader.get_data_directory() == tmp_path.resolve()
