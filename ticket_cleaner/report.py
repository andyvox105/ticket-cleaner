from ticket_cleaner.parsing import RejectedRow


def build_summary(tickets: list[dict], rejected: list, status: str = "open") -> dict:
    """Xây dựng báo cáo thống kê từ danh sách vé."""
    target_tickets = [t for t in tickets if t.get("status") == status]

    return {
        "total_rows_processed": len(tickets) + len(rejected),
        "valid_tickets": len(tickets),
        "rejected_tickets": len(rejected),
        "selected": len(target_tickets),
        "rejected": [
            {"row": record.row, "problems": record.problems}
            if isinstance(record, RejectedRow)
            else record
            for record in rejected
        ],
        f"{status}_tickets": len(target_tickets),
    }
