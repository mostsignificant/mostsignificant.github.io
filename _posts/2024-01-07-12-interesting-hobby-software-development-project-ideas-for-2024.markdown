---
layout: post
title: "12 Interesting Hobby Software Development Project Ideas for 2024"
date: 2024-01-07 14:00:00 +0200
categories:
comments: true
published: true
excerpt: |
  The new year is here and it is the time for resolutions again. For software development folks starting a new hobby 
  project could be the new plan for the year - and this post should give some inspirations and spark new ideas.
image_url: /assets/images/unsplash/mohdammed-ali-zZvofYjfVXw-unsplash.jpg
image_description: |
  Photo by [Mohdammed Ali](https://unsplash.com/@mohdali_31?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)
  on [Unsplash](https://unsplash.com/photos/a-star-trail-is-shown-in-the-night-sky-zZvofYjfVXw?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)
---

## Overview

The following list is a collection of ideas to implement in 2024. Be aware that these are just rough ideas that you can
iterate on as you see fit. Each idea has a section at the end specifying the following:

- **Architecture**: Recommended architecture for implementation
- **Technology**: Recommended programming languages for implementation
- **Challenge**: Biggest challenges during implementation
- **Size**: T-shirt size estimation from S (weekend) to XXL (months) regarding time investment

## 1. Software Documentation Knowledge Base

Software documentation nowadays is distributed over different sources: markdown documents, code comments, wikis, etc.
There is a spot for a meta-repository managing all these resources and making connections between code, documentation
and Word documents.

The tool could parse different sources and make connections between these sources and code. It should be implemented in
two technologies: one command line tool for parsing and being executable in a CI/CD environment. The results should be
stored in a sort of meta-repository, linking the different sources directly. This repository should be accessible via
web GUI and offer a search functionality. Keeping a history of the documentation would be another bonus feature for
users.

- **Architecture**: Command Line Tool and Web GUI
- **Technology**: System Language (C++, Rust) or Executable Packaged Script (Python, JavaScript) for CLI, database or
  file based for saving the results, Web Technology Stack for browsing the results (e. g. JavaScript frameworks like
  node.js)
- **Challenge**: Parsing different sources and making the connections
- **Size**: XL

## 2. Certificate Manager

Managing certificates on different machines can be overwhelming if not organized intelligently. There are some solutions
out there but there is always room for another one, especially if tailored specifically for system admin needs.

The tool could allow for checking certificates and their expiration dates on remote machines. It could manage its own
repository with metadata information about the certificates on the machines. Additionally the tool could offer features
for easy deployment of new certificates, revoking certificates and other helpful functions for certificate management.

- **Architecture**: Command Line Tool
- **Technology**: System Language (e. g. C++ or Rust) or Executable Packaged Script (e. g. Python or JavaScript)
- **Challenge**: Securing connections and access
- **Size**: L

## 3. Mobile RPG-like Habit Tracker

There are several solutions for tracking habits, but there is always room for another spin on tracking habits. In the
spirit of gamification, this habit tracker could be similar to a role-playing-game like experience. The user could
collect experience points with regular habits, reach new levels and find new items and get achievements. Quests could
bring additional motivation for users to stay true to their habits, e. g. with a five-day streak.

- **Architecture**: Mobile App
- **Technology**: Cross-platform frameworks (e. g. React Native or Flutter) or Native Technology (e. g. Swift or
  Kotlin)
- **Challenge**: Design and usability
- **Size**: XL

## 4. Data Health Monitor

Keeping track of everything that is going on in a big database or data lake is hard. Most teams use their own
implemented solution. The idea for this tool comes from a different approach: it should cover most basic measurements
first: data size, data size increase over time, distributions, minimum and maximum values, null values, etc. It should
detect unusual data anomalies and offer the option for alarms - which can be implemented via a plug-in architecture, e.
g. for e-mails, slack, discord or teams notifications, new tickets in a ticketing system etc.

The tool should follow a convention over configuration philosophy: easy to setup (a connection to a data source should
suffice for first monitoring of a data source) and lots of options for individualization. The tool should run as its own
server, decoupled from the actual data source. This should avoid bogging down a production system just for the health
checks. It should also allow for the inclusion of other data validation and test frameworks, e. g. great expectations in
Python or individual SQL scripts.

- **Architecture**: Server with data access and plug-ins for notifications
- **Technology**: System languages (e. g. C++ or Rust) for the server-part
- **Challenge**: Support for different data sources
- **Size**: XXL

## 5. Online Unit Converter

An online unit converter exists for every unit in existence. However, it seems that every one of these sites is just for
one specific unit conversion (e. g. meters to feet or milliliters to ounces) and they are all separate. Additionally,
each one requires the click of a "Convert!" button before the conversion happens. There is a nice niche for a site
supporting all units on a one-pager and which converts from one unit to another one live as soon as the user types in
the value.

- **Architecture**: Client-side web app
- **Technology**: Client web technology stack (JavaScript) or Webassembly (e. g. Rust with Yew)
- **Challenge**: Usability and full variety of units
- **Size**: S

## 6. Command Line Notification Tool

Sending notifications from command line without a stack of third-party tools is a cumbersome task. Build a tool that
allows for easy sending e-mails, slack messages, teams notifications, calendar reminders, etc., from command line. The
tool could be helpful in a CI/CD environment, too. The power of this tool lies in its adapters for different
notification plug-ins. This means you can determine how much time you want to invest in the implementation by supporting
more or less notification mechanisms and scale your efforts linearly.

- **Architecture**: Command Line Tool
- **Technology**: System Language (e. g. C++ or Rust) or Executable Packaged Script (e. g. Python or JavaScript)
- **Challenge**: Implementing different notification technologies
- **Size**: M

## 7. Gamification Ticketing System

A substantial part of software developers are avid gamers in their free time. Why not combine both worlds and make the
boring old JIRA or any other ticketing system more approachable to this audience. You can include things like experience
earned, leveling up, achievements and quests in the ticketing system.

This can be implemented on top of an existing ticketing system, e. g. JIRA. There are already different plug-ins for a
similar direction out there - so it makes sense to study them first to make yours distinctive from them.

- **Architecture**: Plug-in
- **Technology**: Plug-in language of the ticketing system (e. g. Java)
- **Challenge**: Making it engaging for software developers
- **Size**: M

## 8. Excel REST API

This might be a controversial one - but there exists a need to make Excel documents machine-readable by another system
via an API. The service would read from one or more Excel files and serve the data via a REST endpoint. This project
would benefit from a convention over configuration approach. It should be easy to setup with an existing file without
the need of extensive configuration files.

- **Architecture**: Microservice
- **Technology**: System Language (e. g. Rust) or Script Language (e. g. Python or JavaScript) with libraries
  for accessing Excel files and providing a REST endpoint
- **Challenge**: Easy to setup
- **Size**: M

## 9. Hobby Project Management Software

There is a niche for software between a todo-list and a fully blown ticketing system like JIRA for hobby projects. Think
of hobby projects like building a garden shed, attic conversion, a model train layout, etc. There is a need for managing
tasks, dates, and notes or documents and links. Additionally, sharing the project with others is important, too. If you
have a concrete project yourself, you could tailor the software to your own needs, to follow an
[eating-your-own-dog-food](https://en.wikipedia.org/wiki/Eating_your_own_dog_food) approach. This way it might be easier
to implement for only one use-case, e. g. home remodeling projects, instead of supporting too many different use cases
and making the software to generic.

The software should be hosted, so users can access it to create their projects. It needs user management, a database to
store the projects, etc. The feature creep could cause the implementation to become overwhelming, so be sure to
concentrate on core features first.

- **Architecture**: Web App
- **Technology**: Web technology stack (e. g. JavaScript frameworks like node.js)
- **Challenge**: Design and usability
- **Size**: XXL

## 10. Open Source License Detector SaaS

Companies need to declare which open source software they are using in their projects and which licenses those softwares
are using. However, finding this out and collecting it is no easy task. There are solutions that parse and collect these
informations for one technology - however, most software is a diverse software stack, so there is a need to combine
the found results.

This could be implemented as SaaS: either the companies provide access to their code repositories (e. g. via a GitHub
integration) or they let your client CLI tool run in their own CI/CD environment, which then communicates with the SaaS
to send the found library or license information.

However, be careful to include a chapter in your terms of use to protect yourself against lawsuits: the responsibility
to provide the correct information should always stay at the company and your SaaS is just a tool to help, not be the
actual responsible instance for any lawful matter.

- **Architecture**: SaaS
- **Technology**: Web technology stack (e. g. JavaScript frameworks like node.js) and/or System Language (e. g. Rust)
  for parsing the code repositories
- **Challenge**: Integration of different code repositories and package manager information
- **Size**: XL - XXL

## 11. Code Monitor IDE Plug-in

Next idea is a plug-in for your favorite IDE (which is Visual Studio, of course) to show the current status of your
code. It monitors live metrics like last changes, lines of code, etc. The metrics should update live whenever a file is
modified. They should be easily visible and provide meaningful information. To avoid having to write the plug-in for
every programming language in existence, it should be code-language agnostic: this means, you should not implement a
specific code parser but rather just count lines, measure file meta data, etc.

- **Architecture**: Plug-in
- **Technology**: IDE plug-in language (e. g. JavaScript)
- **Challenge**: Meaningful metrics and code-language-independent
- **Size**: M

## 12. Hobby Software Development Project Idea Generator

In case you are running out of ideas - just build a generator for creating new ideas for your next hobby dev projects!
The generator might take some input or pick random topics, tech stacks, and feature lists to combine to a new idea. It
might get more difficult if you want the generator to create more meaningful ideas. A purely random generator could
spit out a lot of nonsense ideas (e. g. database reverse gateway in Webassembly) but be an inspiration for your next
idea to build upon. You just have to decide between quality and quantity (or provide a slider control to regulate
between quantity and quality to affect randomness).

- **Architecture**: Client-side web app
- **Technology**: Client web technology stack (JavaScript) or Webassembly (e. g. Rust with Yew)
- **Challenge**: Usability and meaningfulness of generated ideas
- **Size**: S

## Conclusion

There are never not enough ideas for hobby projects - and this year might be the best opportunity to start a new one!
Even if you did not find something in this list, you might be able to build upon one of those ideas to implement your
own next project. Keep on coding and keep on creating!
