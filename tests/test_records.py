from dataclasses import FrozenInstanceError

import pytest

from ticket_cleaner.records import Rejected, Ticket


# 1. Test khởi tạo và hàm is_urgent của Ticket
def test_ticket_is_urgent():
    # Vé khẩn cấp (priority = 1)
    urgent_ticket = Ticket(id="T01", status="open", category="network", priority=1)
    assert urgent_ticket.id == "T01"
    assert urgent_ticket.is_urgent() is True

    # Vé bình thường (priority = 2 hoặc 3)
    normal_ticket = Ticket(id="T02", status="closed", category="hardware", priority=2)
    assert normal_ticket.is_urgent() is False


# 2. Test tính chất bất biến (frozen=True) của Ticket
def test_ticket_is_frozen():
    ticket = Ticket(id="T01", status="open", category="network", priority=1)

    # Cố tình thay đổi thuộc tính sau khi khởi tạo sẽ ném lỗi FrozenInstanceError
    with pytest.raises(FrozenInstanceError):
        ticket.status = "closed"


# 3. Test khởi tạo class Rejected
def test_rejected_creation():
    rejected = Rejected(row=42, problems=["missing id", "unknown status 'done'"])

    assert rejected.row == 42
    assert len(rejected.problems) == 2
    assert "missing id" in rejected.problems
