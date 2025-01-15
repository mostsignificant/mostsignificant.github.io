---
layout: post
title: "Software Development Must-Reads: Domain-Driven Design by Eric Evans"
date: 2025-01-01 08:00:00 +0000
categories:
comments: true
published: true
excerpt: |
  There are few exceptional books in software development that every programmer should read at least once. One of them is _Domain-Driven Design_ by Eric Evans.
image_url: /assets/images/posts/2025_01_15_eric_evans_domain_driven_design_book.jpg
image_description: |
  Domain-Driven Design by Eric Evans: Book Cover with a painting by [Wassily Kandinsky](https://www.guggenheim.org/artwork/1924)
---

To quote Eric Evans, the inventor of Domain-Driven Design (DDD):

> In its essence, Domain-Driven Design is a way of using models for creating software, especially the part of the software that handles complex business requirements [...].

The domain model and the focus on modeling the business are at the heart of Domain-Driven Design. In his book _Domain-Driven Design: Tackling Complexity in the Heart of Software_, Eric Evans explains these concepts and provides guidance for applying them. It is a must-read for anyone involved in software development.

Domain-Driven Design has been around since the early 2000s and has made a significant impact on the software development world.

It has sparked a big movement that includes conferences, meetups, and countless other resources on Domain-Driven Design, such as [additional](https://amzn.to/3ZUud7u) [books](https://amzn.to/4fGUV9D), [online tutorials](https://www.youtube.com/playlist?list=PLYpjLpq5ZDGtR5nMKGDCa031hx1jVuHXn), [certification modules](https://www.isaqb.org/certifications/cpsa-certifications/cpsa-advanced-level/ddd-domain-driven-design/), and blog posts like this one.

Today, Domain-Driven Design remains as relevant as ever and is central for designing robust and maintainable systems that align with complex business requirements.

## Key Takeaways

The book introduces many techniques and principles to help you apply Domain-Driven Design to your project. It's impossible to remember them all from a single book or apply them all directly. However, it's crucial to understand and focus on the three important core concepts of Domain-Driven Design: ubiquitous language, bounded context, and strategic design.

### Ubiquitous Language

If there’s one key takeaway from Domain-Driven Design, it’s this.

> To create a supple, knowledge-rich design calls for a versatile, shared team language, and a lively experimentation with language that seldom happens in software projects.

Chances are, you’ve already experienced this.

Domain experts and business stakeholders speak their own domain-specific language. Without learning this language and acquiring the necessary domain knowledge, it's difficult to keep up. On the other hand, the software engineers and technical team members often communicate in tech jargon. Sometimes, even when speaking or writing about the same thing, they use entirely different vocabularies.

Translating between the daily business terminology and the language implemented in the code creates overhead (for example classes, tables, files, etc.). Misunderstandings are very likely at this point. Questions are raised about why requirements weren’t met by the implemented software.

For example, in the railway business, there is a very specific language.

You don't use the word _locomotive_–instead you talk about _traction units_. There is a distinction between _stations_ and _stops_. A train _ticket_ from a sales perspective is different than a _ticket_ from a conductor's perspective.

If your implementation class is called `loco` but it actually represents a `traction unit`, there's a mismatch in language. Developers have to perform heavy mental gymnastics if there is an [ICE](<https://en.wikipedia.org/wiki/Siemens_Velaro#Velaro_MS_(DB_class_408)>) (a high-speed electric multiple unit train consisting of eight cars) represented by the `loco` class. Yet, many software developers hesitate to rename things.

The easiest and most straightforward way to establish a ubiquitous language is by creating a glossary:

- **Identify the terminology of the business:** Start by listing core entities and key terms used in the business context.
- **Work on definitions with stakeholders:** Collaborate with business stakeholders to define these terms precisely, ensuring everyone has the same understanding.
- **Maintain consistency across glossary, documentation, and code:** Ensure that the agreed-upon terms are consistently used across all aspects of the project, including the glossary, documentation, and codebase.

### Bounded Context

The book explains why you need bounded contexts.

Many projects, many departments in a larger organizations, many interactions with external entities have their own context. A model used in one project and its context cannot be applied 1:1 in another project for a different client. Combining code from different distinct contexts can lead to problems in interaction and understanding. Models that were implemented without following Domain-Driven Design principles are often difficult to understand: specifically, in which context they are valid and in which context they are not.

Eric Evans sums up bounded contexts straight forward:

> Explicitly define the context within which a model applies. Explicitly set boundaries in terms of team organization, usage within specific parts of the application, and physical manifestations such as code bases and database schemas. Keep the model strictly consistent within these bounds, but don't be distracted or confused by issues outside.

Continuing with our railway example, imagine a booking application for train tickets. The application has its own database with schemas, microservices with APIs and UI frontend. It interacts with other contexts, for example:

- **Timetable Context:** Handles train schedules, routes, and features (like a dining car, quiet seating area, and other amenities). It provides accurate data about when which train is going for the booking application, while remaining separate from ticket pricing or seat reservations.
- **Customer Context:** Manages customer profiles, loyalty points, and preferences. The booking application might use this data for personalized experiences, it is not concerned with train schedules or ticketing.

These contexts need to stay bounded to maintain proper separation, avoiding confusion and mistakes while ensuring loose coupling and minimal dependencies.

Each model can then serve its unique purpose effectively.

This aligns with the popular [Single-Responsibility Principle](https://en.wikipedia.org/wiki/Single-responsibility_principle), which states: "A module should be responsible to one, and only one, actor."

### Strategic Design

Strategic design in Domain-Driven Design focuses on the big picture.

Systems become big quickly. Big systems become complex easily. And complex systems become inevitably overwhelming.

> A system that is hard to understand is hard to change.

To conquer this, strategic design provides a deliberate way to guide the evolution of your growing system consisting of several steps:

- Divide large, complex systems in individual _bounded contexts_.
- Describe their relationships and translations in a _context map_.
- Combine reusable overlaps into a _core domain_ or _shared kernel_.

Eric Evans called this creation of the core domain strategic distillation. This core domain is essential for the communication and language within the team.

> The core domain is where the most value should be added in your system.

This is where the money is. The quality of your core domain modeling influences the other domain models. Focus on your core domain.

In our railway example, the timetable could be considered a core domain. It is essential for scheduling trains, coordinating routes with their capacities, and selling train tickets. It directly impacts customer experience and business efficiency. Being integral to booking, operations, and customer-facing systems, its clarity and consistency are vital for overall success.

## Conclusion

Eric Evans wrote extensively about the concept of Domain-Driven Design, introducing key ideas and how to implement them.

I read the book in two stages. First, I scanned the important chapters for the concepts I had heard of before. The second read was more thorough: I read the chapters from start to finish and researched more about them on the internet. The book is a great resource for looking up specific concepts from Domain-Driven Design and refreshing your memory on them.

This book is a staple for any software developer's bookshelf.

### Getting the Book

The book has 560 pages and was published in August 2003 by Pearson Education.

You can order the book in either physical or digital format from Amazon through these links:

- [Amazon Hardcover](https://amzn.to/407bTZg)
- [Amazon Kindle](https://amzn.to/4iXkq9A)

These and the previous book links are affiliate links. I earn a commission if you order the book through one of these links.

### Further Resources

- [Software Engineering Podcast Episode 226: Eric Evans on Domain-Driven Design at 10 Years](https://se-radio.net/2015/05/se-radio-episode-226-eric-evans-on-domain-driven-design-at-10-years/)
- [Eric Evan's Talk at the DDD Europe 2019: "What is DDD?"](https://www.youtube.com/watch?v=pMuiVlnGqjk)
- [GitHub Repo of the DDD Crew](https://github.com/ddd-crew)

Please share your impressions of the book or your feedback on my review and as always: keep on coding and keep on creating!
