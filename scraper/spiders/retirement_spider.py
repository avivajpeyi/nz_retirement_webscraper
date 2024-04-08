import scrapy
from pathlib import Path
import os
from scrapy.linkextractors import LinkExtractor
from tqdm.auto import tqdm


MAIN_URL = "https://www.eldernet.co.nz/retirement-villages/available-properties?sort=latest&maxProviders=1000"
OURDIR = "out_retirement_villages_pages"
os.makedirs(OURDIR, exist_ok=True)

class RetirementSpider(scrapy.Spider):
    name = "retirement"


    def start_requests(self):
        self.logger.info(f"Starting to scrape {MAIN_URL}")
        yield scrapy.Request(url=MAIN_URL, callback=self.parse)

    def parse(self, response):
        self.logger.info(f"Received response from {response.url}")
        URLS = LinkExtractor(allow='retirement-villages', restrict_text='', deny=['enquire', '/available-properties'],
                             unique=True).extract_links(response)
        urls = [url.url for url in URLS if "/retirement-villages/" in url.url]
        self.logger.info(f"Found {len(urls)} urls")

        prog_bar = tqdm(urls, total=len(urls))

        for url in prog_bar:
            pid = self._pageid(url)
            prog_bar.set_description(f"Processing {pid}")
            yield scrapy.Request(url=url, callback=self.parse_single_page)


    def _pageid(self, l):
        s=  l.split("/retirement-villages/")[-1].split("/")
        # ignore last element and join
        return "_".join(s[:-1])

    def parse_single_page(self, response):
        page_id = self._pageid(response.url)
        filename = f"{OURDIR}/page-{page_id}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

        # try to extract data
        data = {}
        data['page_id'] = page_id
        data['url'] = response.url
        data['description'] = response.xpath("//div[@class='well']").getall()
        data['at-a-glance'] = response.xpath("//div[@class='col-sm-5 col-sm-push-7 at-a-glance-column']").getall()
        yield data