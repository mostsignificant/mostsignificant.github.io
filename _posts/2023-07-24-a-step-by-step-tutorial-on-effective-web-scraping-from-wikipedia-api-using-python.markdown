---
layout: post
title: "A Step-by-Step Tutorial on Effective Web Scraping from Wikipedia API using Python"
date: 2023-07-24 21:00:00 +0200
categories:
comments: true
published: false
excerpt: |
  Wikipedia is a great source for getting data. To effectively ingest Wikipedia's knowledge in a data pipeline it needs
  to be extracted with proper tools. This article shows a way to do this with the Wikipedia API and Python without much
  stress.

image_url: /assets/images/unsplash/PATH.jpg
image_description: |
  Photo by [NAME](https://unsplash.com/USERNAME?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/photos/HASH?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---

## What is Web Scraping?

In order to pull the data from Wikipedia automatically we will use a process called _web scraping_.

> Web scraping, web harvesting, or web data extraction is data scraping used for extracting data from websites. Web
> scraping software may directly access the World Wide Web using the Hypertext Transfer Protocol or a web browser. While
> web scraping can be done manually by a software user, the term typically refers to automated processes implemented
> using a bot or web crawler.
>
> **[https://en.wikipedia.org/wiki/Web_scraping](https://en.wikipedia.org/wiki/Web_scraping)**

The _web crawler_ component will access a web resource, extract data and store it in a data store. For example, the web
crawler could download a Wikipedia website, extract specific HTML tags' content and store it in a database.

![Web Crawler](/assets/images/posts/2023_07_24_web_crawler.png "Web Crawler")

For our example, we will use the Wikipedia API instead of downloading the websites directly. We will store this data in
its raw form in the file system. From there we will extract certain data and transform it. This transformed data will
get stored in a database.

The Wikipedia API provides data in wikitext form. This is a markup language used in the Wikipedia and can be parsed. The
parsed data can be transformed to a semi-structured form - we will use JSON here. This transformed data is perfectly
fitted to be inserted in a NoSQL database, which we will use as our datastore.

![Data Pipeline](/assets/images/posts/2023_07_24_data_pipeline.png "Data Pipeline")

Why not ingesting the data and storing it in the data store directly? The reason is simple: this way we can ensure that
if anything goes wrong in our data pipeline we can:

- Inspect the input data for any data quality issues
- Restart the transformation process without having to ingest the data again

## How to Use the Wikipedia API

Wikipedia is the world's largest free online encyclopedia having 6,688,299 articles and averaging 548 new articles per
day (as of 2023's current [Wikipedia Statistics](https://en.wikipedia.org/wiki/Wikipedia:Statistics)). The articles are
curated by volunteers and open to anyone. This makes it a goldmine of information, but trying to access this data
through traditional web scraping techniques can be complex and time-consuming, and may even violate Wikipedia's terms of
service.

However, the powerful Wikipedia API offers a more efficient, faster, and compliant way to access this data. It exposes
several endpoints that return basically semi-structured data. The documentation for this API can be found on
[MediaWiki](https://www.mediawiki.org/wiki/API:Main_page), the underlying open source software which powers Wikipedia
and other websites operated by the [Wikimedia Foundation](https://en.wikipedia.org/wiki/Wikimedia_Foundation).

Before using the Wikipedia API, we have to read and respect the
[netiquette](https://www.mediawiki.org/wiki/API:Etiquette):

> There is no hard and fast limit on read requests, but be considerate and try not to take a site down. Most system
> administrators reserve the right to unceremoniously block you if you do endanger the stability of their site.
>
> Making your requests in series rather than in parallel, by waiting for one request to finish before sending a new
> request, should result in a safe request rate. It is also recommended that you ask for multiple items in one request
>
> **[https://www.mediawiki.org/wiki/API:Etiquette](https://www.mediawiki.org/wiki/API:Etiquette)**

The Wikipedia API does not need an API key or any other form of authentication. The API also does not need any special
HTTP headers - query parameters are sent as URL parameters. For example, calling

There is a useful
[Sandbox](https://www.mediawiki.org/wiki/Special:ApiSandbox) for stitching together the request and trying it out.

For example, simply getting the content for the Python programming language Wikipedia page in JSON format, the call
needs:

- the basic Wikipedia API url: `https://en.wikipedia.org/w/api.php`
- the action we want to perform, for accessing page content: `action=parse`
- the page's title, in this case: `page=Python\_(programming_language)`
- and the response's format: `format=json`

We stitch it together and just call it:

```sh
curl "https://en.wikipedia.org/w/api.php?action=parse&page=Python_(programming_language)&format=json"
```

The response contains a lot of metadata and the page's raw content (text) in a JSON structure:

```jsonc
{
  "parse": {
    "title": "Python (programming language)",
    "pageid": 23862,
    "revid": 1166944715,
    "text": {
      // ...
    },
    "langlinks": [
      // ...
    ]
    // ...
  }
}
```

However, we need the text in a more parseable form. We will use the `prop` parameter with the `wikitext` value to
retrieve the data in the [wikitext](https://en.wikipedia.org/wiki/Help:Wikitext) markup language.

```sh
curl "https://en.wikipedia.org/w/api.php?action=parse&pageid=23862&prop=wikitext&format=json"
```

## Laying the Data Pipeline

## Going for Robustness

## Next Steps

```

```
