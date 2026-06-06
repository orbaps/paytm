from base import BankNoticeTarget, PlaceholderNoticeScraper


BANK_NOTICE_TARGETS = [
    BankNoticeTarget(
        "State Bank of India",
        "TODO: verify SBI digital banking maintenance notice URL",
        "Track UPI, mobile banking, and internet banking notices.",
    ),
    BankNoticeTarget(
        "HDFC Bank",
        "TODO: verify HDFC service outage or scheduled maintenance URL",
        "Track scheduled netbanking and UPI maintenance notices.",
    ),
    BankNoticeTarget(
        "ICICI Bank",
        "TODO: verify ICICI maintenance notice URL",
        "Track digital channels, cards, and UPI notices.",
    ),
    BankNoticeTarget(
        "Axis Bank",
        "TODO: verify Axis Bank service notification URL",
        "Track UPI collect, app, and netbanking notices.",
    ),
    BankNoticeTarget(
        "Kotak Mahindra Bank",
        "TODO: verify Kotak maintenance notice URL",
        "Track core banking and mobile banking notices.",
    ),
    BankNoticeTarget(
        "Punjab National Bank",
        "TODO: verify PNB public notice URL",
        "Track mobile banking and UPI availability notices.",
    ),
    BankNoticeTarget(
        "Bank of Baroda",
        "TODO: verify Bank of Baroda maintenance notice URL",
        "Track UPI and digital banking notices.",
    ),
    BankNoticeTarget(
        "Canara Bank",
        "TODO: verify Canara Bank public notice URL",
        "Track internet banking, mobile banking, and UPI notices.",
    ),
]


def collect_placeholder_notices() -> list[dict[str, str]]:
    return [PlaceholderNoticeScraper(target).collect() for target in BANK_NOTICE_TARGETS]
