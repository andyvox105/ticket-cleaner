import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from ticket_cleaner.files import load_ticket_file, read_rows, write_json


# --- 1. Tests cho hàm read_rows ---
def test_read_rows_csv(tmp_path: Path):
    csv_file = tmp_path / "tickets.csv"
    csv_file.write_text("\ufeffid,status,priority\nT01,open,1", encoding="utf-8")
    rows = read_rows(csv_file)
    assert len(rows) == 1
    assert rows[0]["id"] == "T01"


def test_read_rows_json(tmp_path: Path):
    json_file = tmp_path / "tickets.json"
    json_file.write_text('[{"id": "T02", "status": "closed"}]', encoding="utf-8")
    rows = read_rows(json_file)
    assert len(rows) == 1
    assert rows[0]["id"] == "T02"


def test_read_rows_invalid_extension(tmp_path: Path):
    txt_file = tmp_path / "wrong.txt"
    txt_file.write_text("some random text", encoding="utf-8")
    with pytest.raises(
        ValueError, match="cannot read wrong.txt: use a .csv or .json file"
    ):
        read_rows(txt_file)


# --- 2. Tests cho hàm write_json ---
def test_write_json_creates_file_and_directories(tmp_path: Path):
    out_dir = tmp_path / "nested" / "folder"
    out_file = out_dir / "output.json"
    data_to_write = {"project": "ticket_cleaner", "version": 1}

    write_json(data_to_write, out_file)

    assert out_file.exists()
    saved_data = json.loads(out_file.read_text(encoding="utf-8"))
    assert saved_data == data_to_write
    assert not out_dir.joinpath("output.json.tmp").exists()


# --- 3. Tests cho hàm load_ticket_file ---
def test_load_ticket_file_success(tmp_path):
    valid_file = tmp_path / "data.json"
    valid_file.write_text('{"project": "ticket_cleaner"}', encoding="utf-8")
    result = load_ticket_file(valid_file)
    assert result == {"project": "ticket_cleaner"}


def test_load_ticket_file_permission_error(tmp_path, caplog):
    locked_file = tmp_path / "locked.json"
    locked_file.write_text('{"key": "value"}', encoding="utf-8")
    os.chmod(locked_file, 0o000)

    result = load_ticket_file(locked_file)

    assert result is None
    assert "Không có quyền đọc file" in caplog.text
    os.chmod(locked_file, 0o777)


def test_load_ticket_file_file_exists_error(tmp_path, caplog):
    fake_file = tmp_path / "not_exist.json"
    with patch("builtins.open", side_effect=FileExistsError):
        result = load_ticket_file(fake_file)

    assert result is None
    assert "Không thể tìm thấy file dữ liệu" in caplog.text
