Data
====

This page lays out the URLs where you can get public filings.

Financial statements
----

Extract financial statement info::

    scrapy crawl financials

Historical Price
----

Extract historical stock prices for all company tickers::

    scrapy crawl stock_price

HKSE
----

Extract company names::

    scrapy crawl hkex_company

Extract filings count for each company (to checksum when scraping filings)::

    scrapy crawl hkex_filing_count

Extract entire history of filings (run once to download all filings)::

    scrapy crawl hkex_filing

Extract recent filings (to run on daily basis)::

    scrapy crawl hkex_new_filings

Singapore
---------

Prospectuses::

    http://www.sgx.com/wps/portal/sgxweb/home/company_disclosure/prospectus_circulars

SSE
---

Filings::

    http://www.sse.com.cn/assortment/stock/list/stockdetails/announcement/index.shtml?COMPANY_CODE=600000&reportType2=%E5%AE%9A%E6%9C%9F%E5%85%AC%E5%91%8A&bt=%E5%AE%9A%E6%9C%9F%E5%85%AC%E5%91%8A&static=t

Tickers::

    http://www.sse.com.cn/assortment/stock/list/name/

SZSE
----

Taiwan
------