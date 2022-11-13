---
layout: post
title: "Make Your Way Through Apache's Big Data Stack: Spark, Kafka, Hadoop, and Co."
date: 2022-04-20 20:00:00 +0200
categories: big-data
comments: true
published: false
excerpt: |
  
image_url: /assets/images/unsplash/anders-jilden--N2UXcPBIYI-unsplash-2.jpg
image_description: |
  Photo by [anders jilden](https://unsplash.com/@zhangkaiyv?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/s/photos/skyline?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---

## Overview

- Apache Spark
- Apache Kafka
- Apache Zookeeper
- Apache Hadoop (HDFS)
- Apache YARN

### Apache Kafka

> Apache Kafka is an open-source distributed event streaming platform
>
> **- [https://kafka.apache.org](https://kafka.apache.org)**

Apache Kafka's popularity illustrates the shift from designs evolving around state to the event-centered school of thought.

Before understanding Apache Kafka, the concept of an event has to be explained. An event is an indication in time that something took place.

States were largely stored in a database. Events on the other hand are more conveniently stored in a log.

A log is called *topic* in Kafka. These topics in Kafka are kept ...

- persistent (on disk) and
- redundant (on several nodes)

Kafka's architecture is built to avoid a single point of failure. Furthermore, the communication is based on the
Transmission Control Protocol (TCP). This is important for reliable delivery of events.

> Think of events first and things second.
>
> **- [https://www.youtube.com/watch?v=FKgi3n-FyNU&t=162s](https://www.youtube.com/watch?v=FKgi3n-FyNU&t=162s)**

![Apache Kafka Meta Model](/assets/images/posts/2022-04-2_apache_kafka_meta_model.png "Apache Kafka Meta Model")
_Apache Kafka meta model illustrates the connections between Kafka objects_

The need of realtime and flexible analysis meant and end to over-night batch jobs and legacy data warehouse
architectures.

![Apache Kafka example for two producers sending events to a topic with four partitions (P1 - P4)](/assets/images/posts/2022-04-2_apache_kafka.png "Apache Kafka Example")
_Apache Kafka example for two producers sending events to a topic with four partitions (P1 - P4)_

There are five major APIs in Kafka:

- **Producer API** permits applications to publish event streams
- **Consumer API** permits applications to subscribe to topics and processes event streams
- **Connector API** executes producer and consumer APIs linking topics to existing applications
- **Streams API** converts input streams to output and produces a result
- **Admin API** manages topics, brokers and other objects

### Apache Zookeeper

### Apache Hadoop

### Apache Spark

> Apache Spark is an open-source unified analytics engine for large-scale data processing.


## Conclusion

| Technology    | Area            | Interfaces                               |
| ------------- | --------------- | ---------------------------------------- |
| Spark         | Analytics       | Scala, Java, Python, SQL, R              |
| Kafka         | Event Streaming | Scala, Java, Python, Go, C/C++, REST API |
| Hadoop        | Storage         |       |
