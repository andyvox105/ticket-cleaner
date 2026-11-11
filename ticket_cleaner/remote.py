import httpx


# Thay `httpx.Client | None` thành `Optional[httpx.Client]`
def fetch_rows(url: str, client: httpx.Client | None = None) -> list[dict]:
    """Tải dữ liệu thô (JSON) từ một dịch vụ web."""
    client = client or httpx.Client(timeout=10.0)
    with client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()
