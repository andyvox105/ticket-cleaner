import pytest

from ticket_cleaner.parsing import split_records


# 1. Normal Path & Boundary Path: Dữ liệu chuẩn và dữ liệu có khoảng trắng thừa
def test_split_records_valid_cases():
    rows = [
        {"id": "T01", "status": "open", "category": "network", "priority": "1"},
        {
            "id": "T02",
            "status": "  CLOSED  ",
            "category": "hardware",
            "priority": 2,
        },  # Khoảng trắng thừa và in hoa
    ]
    valid, rejected = split_records(rows)

    assert len(valid) == 2
    assert len(rejected) == 0


# 2. Error Path: Kiểm tra hàng loạt các lỗi định dạng bằng parametrize
@pytest.mark.parametrize(
    "bad_row, expected_problem",
    [
        # Thiếu trường bắt buộc
        ({"status": "open", "category": "network", "priority": "1"}, "missing id"),
        ({"id": "T01", "category": "network", "priority": "1"}, "missing status"),
        # Sai giá trị cho phép
        (
            {"id": "T01", "status": "done", "category": "network", "priority": "1"},
            "unknown status 'done'",
        ),
        (
            {"id": "T02", "status": "open", "category": "network", "priority": "high"},
            "priority must be 1, 2 or 3, not 'high'",
        ),
        # Dữ liệu không phải dictionary
        ("this is just a string", "not a record"),
    ],
)
def test_split_records_invalid_cases(bad_row, expected_problem):
    # Truyền vào list chứa 1 row bị lỗi
    valid, rejected = split_records([bad_row])

    assert len(valid) == 0
    assert len(rejected) == 1
    # Kiểm tra xem thông báo lỗi mong muốn có nằm trong list problems không
    assert expected_problem in rejected[0].problems


# 3. Logic Path: Kiểm tra bắt lỗi ID trùng lặp
def test_split_records_duplicate_id():
    rows = [
        {"id": "T01", "status": "open", "category": "network", "priority": "1"},
        {
            "id": "t01",
            "status": "closed",
            "category": "hardware",
            "priority": "2",
        },  # Trùng ID (tính cả chữ hoa/thường)
    ]
    valid, rejected = split_records(rows)

    assert len(valid) == 1
    assert len(rejected) == 1
    assert "duplicate id T01" in rejected[0].problems
