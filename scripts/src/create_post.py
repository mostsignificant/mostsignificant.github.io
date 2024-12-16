import argparse
import jinja2

from datetime import datetime

TEMPLATE = """---
layout: post
title: "{{ title }}"
date: {{ date }}
categories: {{ categories }}
comments: true
published: false
excerpt: |
  
image_url: /assets/images/unsplash/PATH.jpg
image_description: |
  Photo by [NAME](https://unsplash.com/USERNAME?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/photos/HASH?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---
"""


def main(title: str, categories: str, date: datetime):
    environment = jinja2.Environment()
    template = environment.from_string(TEMPLATE)
    content = template.render(
        title=title,
        categories=categories,
        date=date.strftime("%Y-%m-%d %H:%M:%S +0200"),
    )

    title = title.lower()
    title = title.replace("?", "")
    title = title.replace(".", "")
    title = title.replace(",", "")
    title = title.replace("!", "")
    title = title.replace("-", "")
    title = title.replace(":", "")
    title = title.replace(" ", "-")
    title = title.replace("/", "-")

    date = date.strftime("%Y-%m-%d")

    filename = f"{date}-{title}.markdown"

    with open(filename, mode="w", encoding="utf-8") as file:
        file.write(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("title", type=str)
    parser.add_argument("--categories", type=str, default="")
    parser.add_argument("--date", type=datetime, default=datetime.now())

    args = parser.parse_args()

    main(args.title, args.categories, args.date)
