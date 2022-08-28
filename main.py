import requests
import pickle
import math
from bs4 import BeautifulSoup


SEARCH_URI = "https://web.pcc.gov.tw/prkms/tender/common/basic/readTenderBasic?tenderEndDate=2022%2F08%2F27&orgName=&tenderName=&searchType=basic&firstSearch=false&radProctrgCate=%22%29&tenderId=&orgId=&tenderStartDate=2022%2F08%2F21&tenderType=TENDER_DECLARATION&dateType=isDate&tenderWay=TENDER_WAY_ALL_DECLARATION&level_1=on"


def get_page_keys(page_num: int, page_size: int = 100) -> list:
    """Get base64 encoded page keys from specific search result page."""
    url = f"{SEARCH_URI}&pageNum={page_num}&pageSize={page_size}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    divs = soup.body.find_all("div", {"class": "bt_cen1 no_blank"})
    links = [div.a.get('href') for div in divs]
    return [h.split("?pk=")[-1] for h in links]

def fetch_page_keys() -> list:
    """Fetch all page keys from search result pages."""
    # Get Result Record Count First
    page_keys = []
    page_size = 100 # 100 records per page
    r = requests.get(SEARCH_URI)
    soup = BeautifulSoup(r.text, "html.parser")
    span_txt = soup.body.select_one("#pagebanner .red").text
    record_count = int(span_txt.strip().replace(",", ""))
    pages_to_fetch = math.ceil(record_count / page_size) # 無條件進位
    for search_page_num in range(1, pages_to_fetch + 1):
        print(f"Fetching page {search_page_num} of {pages_to_fetch}")
        page_keys.extend(get_page_keys(search_page_num, page_size))
    return page_keys

def save_page_keys() -> None:
    """Save page keys to a file."""
    page_keys = fetch_page_keys()
    with open("page_keys.dat", "wb") as f:
        pickle.dump(page_keys, f)

def load_page_keys() -> list:
    """Load page keys from a file."""
    with open("page_keys.dat", "rb") as f:
        return pickle.load(f)

def get_detail(page_key: str) -> dict:
    """
    Get detail info from a page
    args: page_key - base64 encoded page key
    Example: get_detail("NzAwNzQzOTQ=")
    """
    url = f"https://web.pcc.gov.tw/tps/QueryTender/query/searchTenderDetail?pkPmsMain={page_key}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")



if __name__ == "__main__":
    #save_page_keys()
    page_keys = load_page_keys()
    print(page_keys)