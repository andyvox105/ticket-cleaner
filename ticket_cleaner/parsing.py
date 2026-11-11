from typing import NamedTuple


class RejectedRow(NamedTuple):
    row: int
    problems: list[str]


# Danh sách chuẩn của khóa học
STATUSES = ["open", "pending", "closed"]
PRIORITIES = [1, 2, 3]
REQUIRED_FIELDS = ["id", "status", "category", "priority"]


def clean_text(value: object) -> str:
    """Xóa khoảng trắng thừa và chuyển thành chữ thường."""
    if value is None:
        return ""
    return str(value).strip().lower()


def split_records(rows: list[dict]) -> tuple[list[dict], list[RejectedRow]]:
    valid_tickets = []
    rejected_tickets = []
    seen_ids = set()  # Dùng để theo dõi ID trùng lặp

    for index, raw in enumerate(rows, start=1):
        # breakpoint() # Dừng chương trình tại đây để "nội soi"
        if not isinstance(raw, dict):
            # Nếu không phải là dictionary, ghi nhận lỗi và nhảy sang dòng tiếp theo
            rejected_tickets.append(RejectedRow(row=index, problems=["not a record"]))
            continue

        problems = []

        # 1. Kiểm tra thiếu các trường bắt buộc
        for field in REQUIRED_FIELDS:
            if clean_text(raw.get(field)) == "":
                problems.append(f"missing {field}")

        # 2. Kiểm tra status (đã chuẩn hóa)
        status = clean_text(raw.get("status"))
        if status and status not in STATUSES:
            # Code chuẩn của khóa học trả về: unknown status '...'
            problems.append(f"unknown status {status!r}")

        # 3. Kiểm tra priority
        priority_str = clean_text(raw.get("priority"))
        if priority_str and not (
            priority_str.isdigit() and int(priority_str) in PRIORITIES
        ):
            problems.append(f"priority must be 1, 2 or 3, not {priority_str!r}")

        # 4. Kiểm tra ID trùng lặp
        if not problems:
            # Chỉ kiểm tra trùng ID nếu vé không có lỗi nào ở trên
            ticket_id = clean_text(raw.get("id")).upper()
            if ticket_id in seen_ids:
                problems.append(f"duplicate id {ticket_id}")
            else:
                seen_ids.add(ticket_id)

        if problems:
            rejected_tickets.append(RejectedRow(row=index, problems=problems))
        else:
            valid_tickets.append(raw)

    return valid_tickets, rejected_tickets
