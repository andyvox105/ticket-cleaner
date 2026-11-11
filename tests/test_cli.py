import json

from ticket_cleaner.cli import main


def test_report_for_pending_tickets(tmp_path):
    output = tmp_path / "pending.json"
    exit_code = main(
        ["data/tickets.csv", "--status", "pending", "--output", str(output)]
    )
    assert exit_code == 0
    summary = json.loads(output.read_text(encoding="utf-8"))
    assert summary["selected"] == 2
    assert len(summary["rejected"]) == 6


def test_missing_file_gives_exit_code_1(tmp_path):
    assert main([str(tmp_path / "missing.csv")]) == 1


def test_strict_voi_data_bi_loi_tra_ve_code_3(tmp_path):
    output = tmp_path / "summary.json"
    exit_code = main(["data/tickets.csv", "--strict", "--output", str(output)])
    assert exit_code == 3
    assert output.exists()  # Đảm bảo báo cáo vẫn được tạo ra dù bị lỗi


def test_strict_voi_data_sach_tra_ve_code_0(tmp_path):
    # Tạo một file csv sạch ảo ngay trong bộ nhớ test
    clean_csv = tmp_path / "clean.csv"
    clean_csv.write_text(
        "id,status,category,priority\nT-1,open,login,1\n", encoding="utf-8"
    )

    exit_code = main([str(clean_csv), "--strict", "--output", str(tmp_path / "s.json")])
    assert exit_code == 0
