import argparse
import logging
from pathlib import Path

import httpx

from ticket_cleaner.files import read_rows, write_json
from ticket_cleaner.parsing import split_records
from ticket_cleaner.records import STATUSES
from ticket_cleaner.remote import fetch_rows
from ticket_cleaner.report import build_summary

logger = logging.getLogger("ticket_cleaner")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ticket_cleaner",
        description="Kiểm tra dữ liệu vé và xuất báo cáo tổng hợp.",
    )
    # Đối số bắt buộc (Argument)
    parser.add_argument(
        "input", help="Đường dẫn file .csv hoặc .json, hoặc chữ 'remote' để tải từ web"
    )
    # Tùy chọn (Options)
    parser.add_argument(
        "--status",
        default="open",
        choices=sorted(STATUSES),
        help="Trạng thái vé cần đếm (mặc định: open)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/summary.json"),
        help="Nơi lưu báo cáo (mặc định: reports/summary.json)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Trả về mã thoát 3 nếu có bất kỳ vé nào bị loại (dữ liệu dơ)",
    )
    return parser


def load_rows(source: str) -> list[dict]:
    if source == "remote":
        url = "https://raw.githubusercontent.com/Nextia-Intelligence/nextia-learning-labs/main/C02/data/tickets.json"
        return fetch_rows(url)
    return read_rows(Path(source))


def main(argv: list[str] | None = None) -> int:
    args = make_parser().parse_args(argv)
    logging.basicConfig(level="WARNING", format="%(levelname)s %(name)s: %(message)s")

    try:
        rows = load_rows(args.input)
    except (OSError, ValueError, httpx.HTTPError) as error:
        logger.error("Không thể đọc dữ liệu từ %s: %s", args.input, error)
        return 1

    tickets, rejected = split_records(rows)
    for record in rejected:
        logger.warning("Dòng %d bị loại: %s", record.row, "; ".join(record.problems))

    summary = build_summary(tickets, rejected, args.status)
    write_json(summary, args.output)

    print(f"{len(rows)} vé: {len(tickets)} hợp lệ, {len(rejected)} bị loại.")
    print(f"Báo cáo lưu tại: {args.output}")

    if args.strict and rejected:
        return 3

    return 0
