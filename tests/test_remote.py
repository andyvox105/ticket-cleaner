import httpx
import pytest

from ticket_cleaner.remote import fetch_rows


# 1. Normal Path: Giả lập gọi API thành công
def test_fetch_rows_success():
    # Định nghĩa phản hồi giả với HTTP 200 và dữ liệu JSON
    def mock_handler(request):
        # Đảm bảo request gọi đúng URL mà ta truyền vào
        assert str(request.url) == "https://fake-api.com/data"
        return httpx.Response(200, json=[{"id": "T01", "status": "open"}])

    # Tạo client giả lập sử dụng mock_handler
    mock_client = httpx.Client(transport=httpx.MockTransport(mock_handler))

    # Truyền mock_client vào hàm, hệ thống sẽ KHÔNG gọi mạng thật
    result = fetch_rows("https://fake-api.com/data", client=mock_client)

    assert len(result) == 1
    assert result[0]["id"] == "T01"
    assert result[0]["status"] == "open"


# 2. Error Path: Giả lập gọi API thất bại
def test_fetch_rows_http_error():
    # Giả lập server bị lỗi, trả về HTTP 500
    def error_handler(request):
        return httpx.Response(500, text="Internal Server Error")

    mock_client = httpx.Client(transport=httpx.MockTransport(error_handler))

    # Hàm raise_for_status() của httpx sẽ ném ra HTTPStatusError khi nhận mã lỗi 4xx, 5xx
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        fetch_rows("https://fake-api.com/data", client=mock_client)

    # Kiểm tra thêm xem lỗi có đúng là lỗi 500 không
    assert exc_info.value.response.status_code == 500
