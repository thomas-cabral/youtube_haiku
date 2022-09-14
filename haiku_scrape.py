import requests
import time
from bs4 import BeautifulSoup


class YoutubeScrape:
    fetch_limit = 0
    top_time_range = ""
    base_url = ""
    _url = ""
    _next_context = ""
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
                AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}

    def __init__(self, url: str, top_time_range: str = "month", fetch_limit: int = 25):
        self.base_url = url
        self.top_time_range = "&t=%s" % top_time_range
        self.fetch_limit = fetch_limit
        self._url = url + self.top_time_range

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def next_context(self):
        return self._next_context

    @next_context.setter
    def next_context(self, value):
        self._next_context = value

    def get_top_videos(self):
        page = requests.get(self.url, headers=self.headers)

        if page.status_code == 200:
            return page.text
        else:
            raise Exception("Requested URL failed: %i status code" % page.status_code)

    def get_or_retry(self):
        while True:
            try:
                result = self.get_top_videos()
            except Exception as e:
                print(e)
                time.sleep(1)
            else:
                break

        return result

    def parse_youtube_links(self):
        soup = BeautifulSoup(self.get_or_retry(), 'html.parser')
        hrefs = soup.find_all("a", href=True)

        link_set = set()

        for a in hrefs:
            if a['href'].__contains__('//youtu.be') or a['href'].__contains__('www.youtube.com'):
                link_set.add(a['href'])

        things = soup.find_all('div', id=lambda x: x and x.startswith('thing_'))
        if len(things) > 0:
            self.next_context = things[-1]['id'].replace('thing_', '')

        return link_set

    def get_links_for_period(self):
        n = 0
        all_links = set()
        for page in range(0, int(self.fetch_limit / 25)):
            if n >= 25:
                self.url = "%s%s&count=%s&after=%s" % (self.base_url, self.top_time_range, n, self.next_context)
                all_links.update(self.parse_youtube_links())
            else:
                all_links.update(self.parse_youtube_links())
            n += 25
        return all_links
