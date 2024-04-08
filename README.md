# NZ Retirement Webscrapper

1. Get retirement village phone numbers from: https://www.retirementvillages.org.nz/tools/clients/directory.aspx?SECT=Auckland#Auckland
2. Get text from: https://www.eldernet.co.nz/retirement-villages/available-properties/central-auckland?sort=latest&center=-36.890978759264385%2C174.77768049999997&zoom=11&maxProviders=40

## Instructions

```
pip install -r requirements.txt
scrapy crawl retirement -o data.json
cd scripts
python load_all_pages.py
```