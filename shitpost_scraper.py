import html

import requests

from glowing_hat.custodian import Custodian

server = "mastodon.me.uk"
# from e.g. https://mastodon.me.uk/api/v1/accounts/lookup?acct=pikesley_ebooks
id = 109522710510081274


def get_latest_toot():
    """Get the latest shitpost."""
    statuses_url = f"https://{server}/api/v1/accounts/{id}/statuses"
    latest_status = requests.get(statuses_url).json()[0]  # noqa: S113

    status_url = f"https://{server}/api/v1/statuses/{latest_status['id']}"
    return html.unescape(requests.get(status_url).json()["content"][3:-4])  # noqa: S113


if __name__ == "__main__":
    cust = Custodian()
    cust.set("toot", get_latest_toot())
