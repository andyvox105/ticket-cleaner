import csv
import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def read_rows(path: Path) -> list[dict]:
    """Read raw records from a .csv or .json file."""
    if path.suffix == ".csv":
        with open(path, encoding="utf-8-sig", newline="") as file:
            return list(csv.DictReader(file))
    if path.suffix == ".json":
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    raise ValueError(f"cannot read {path.name}: use a .csv or .json file")


def write_json(data: dict, path: Path) -> None:
    """Save data as JSON. Write a temporary file first, so a failure never leaves half a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with open(temporary, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")
    os.replace(temporary, path)


def load_ticket_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except (FileExistsError, FileNotFoundError):
        logger.error("Không thể tìm thấy file dữ liệu tại đường dẫn: %s", file_path)
        # Quan trọng: Trả về một giá trị an toàn (None hoặc list rỗng) để hệ thống không bị crash
        return None
    except PermissionError:
        # Bạn có thể xếp chồng nhiều except để bắt các lỗi khác nhau
        logger.error("Không có quyền đọc file: %s", file_path)
        return None
