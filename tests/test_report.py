from ticket_cleaner.report import build_summary


def test_build_summary_default_status():
    # 1. Test với status mặc định ("open")
    tickets = [
        {"id": "T01", "status": "open"},
        {"id": "T02", "status": "closed"},
        {"id": "T03", "status": "open"},
    ]
    # report.py chỉ đếm len(rejected) nên ta chỉ cần truyền list chứa phần tử bất kỳ giả lập lỗi
    rejected = ["error 1", "error 2"]

    summary = build_summary(tickets, rejected)

    assert summary["total_rows_processed"] == 5
    assert summary["valid_tickets"] == 3
    assert summary["rejected_tickets"] == 2
    # Đảm bảo key "open_tickets" được tạo ra và đếm đúng 2 vé
    assert summary["open_tickets"] == 2


def test_build_summary_custom_status():
    # 2. Test truyền tham số status tùy chỉnh
    tickets = [{"id": "T01", "status": "open"}, {"id": "T02", "status": "closed"}]
    rejected = []

    summary = build_summary(tickets, rejected, status="closed")

    assert summary["total_rows_processed"] == 2
    assert summary["valid_tickets"] == 2
    assert summary["rejected_tickets"] == 0
    # Key lúc này phải đổi thành "closed_tickets" theo f-string
    assert summary["closed_tickets"] == 1


def test_build_summary_empty_data():
    # 3. Test trường hợp dữ liệu trống
    summary = build_summary([], [])

    assert summary["total_rows_processed"] == 0
    assert summary["valid_tickets"] == 0
    assert summary["rejected_tickets"] == 0
    assert summary["open_tickets"] == 0
