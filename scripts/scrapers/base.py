from dataclasses import dataclass


@dataclass(frozen=True)
class BankNoticeTarget:
    bank_name: str
    url_hint: str
    notes: str


class PlaceholderNoticeScraper:
    """Phase 0 placeholder for future bank maintenance notice scraping.

    The current implementation does not fetch websites. It records which banks
    need scraper coverage and writes placeholder rows that analysts can replace
    with observed notices.
    """

    def __init__(self, target: BankNoticeTarget) -> None:
        self.target = target

    def collect(self) -> dict[str, str]:
        return {
            "bank_name": self.target.bank_name,
            "announcement_date": "",
            "maintenance_start": "",
            "maintenance_end": "",
            "description": f"TODO: implement notice collection. {self.target.notes}",
            "source_url": self.target.url_hint,
            "notice_status": "placeholder",
        }
