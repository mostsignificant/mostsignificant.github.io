---
layout: post
title: "Why Data Modeling Still Matters in the Era of Modern Tools"
date: 2024-11-17 00:00:00 +0200
categories: Data Modeling
comments: true
published: false
excerpt: |

image_url: /assets/images/unsplash/PATH.jpg
image_description: |
  Photo by [NAME](https://unsplash.com/USERNAME?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/photos/HASH?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---

## What Is Data Modeling, and Why Should You Care?

Data modeling is the process of defining and structuring how data is stored, organized, and used in your systems. A data model is the blueprint for your data infrastructure. It helps understanding your business domain and communication with your stakeholders.

A data model contains the following elements:

- Entities to represent real-world objects, such as a Customer or a Product.
- Keys to uniquely identify entities, such as a Customer’s email address or a Product’s SKU.
- Attributes to represent the properties of entities, such as a Customer’s Name or a Product’s Price.
- Types to define the nature of data for attributes, such as strings, dates, or numbers.
- Relations to represent interactions or associations, for example, a Customer buys a Product.
- (Optional) Boundaries to define the scope of the model, specifying which entities and relationships are included and which are outside its viewpoint.

Without a data model, your data systems can quickly turn into a spaghetti of tables, schemas, and APIs, leaving your engineers tangled up and your analysts wondering, "Where is that attribute?"

What do good data models achieve?

- **Efficiency**\
  Good data models are easy to read, quick to comprehend, and simple to communicate. Teams are saving time by better understanding the business domain and having a clearer vision of what needs to be implemented.

- **Standardization**\
  Having good standards and guidelines is important. It ensures consistency and an easy to follow connection between the deeper technological layers up to high-level concepts.

- **Reusability**\
  Well-structured data models provide reusable components, because writing the same stuff ten times is not fun. For example, a Customer model can be reused across marketing, sales, and support, ensuring consistency and saving time.

- **Collaboration**\
  When your team - and potentially other teams - follows the same set of rules and concepts in data modeling, collaboration becomes much easier. Data can be connected, data can be exchanged and data can be compared without requiring extensive transformation and rework. This accelerates development in general and leads to more robust interaction between systems.

- **Data quality**\
  Good data models inherently promote and build in key data qualities. What does this mean? For example, a good data model ensures that attributes requiring only dates are defined as date fields—not as datetime or, data gods forbid, string or varchar types—which are too broad and prone to errors.

## The Three Levels of Data Modeling

Conceptual, logical, and physical models represent the three levels of data modeling. As you move deeper, more details and complexity are added to the model. As you move higher, the model becomes more abstract and simplified for better understanding.

To better illustrate these levels, we are using a fictional Airline as an example in the following sections.

### Conceptual Data Model: The Big Picture

A conceptual data model (CDM) focusses on broad concepts and is used for representing and understanding business concepts. At this stage, key entities are identified and the important relations between them are identified. It is important that bon-technical users should be able to understand it.

In our airline example, a CDM might look like this:

![Conceptual Model](/assets/images/posts/2024_11_17_conceptual_model.png "Conceptual Model")

The model consists of four entities: Plane, Flight, Passenger, and Ticket. They have relations between them, allowing us to read this model like simple prose:

- A passenger books a flight and holds a ticket.
- A flight is operated by a plane.

There are different schools of thought when it comes to CDMs.

One approach advocates always including a business key for each entity in a CDM. This has the advantage of forcing you to be very precise in your conceptual modeling process, requiring you to ask business stakeholders detailed questions about the real-world objects you are trying to represent. However, this approach can make conceptual modeling more challenging, as it limits your ability to group different real-world objects under a single entity if they do not share a natural business key.

For example, consider a Payment entity. In the real world, cash payments and card payments may not share a single unique identifier, making it difficult to represent them under the same entity in a conceptual model. This might require you to create separate entities, such as CashPayment and CardPayment, increasing complexity at the conceptual level.

Another approach to conceptual modeling involves adding attributes to conceptual entities. This can help you get more detailed information from business stakeholders about the real-world objects you’re modeling. However, it risks losing sight of the big picture and the interactions between entities, focusing instead on details that could be worked out at a later stage.

For example, adding attributes like Passenger Age or Ticket Price at the conceptual level might start discussions with specifics, distracting from general questions like how passengers interact with tickets and flights.

As with any software development artifact, it’s good practice to review your work. An effective review is easier with a checklist to go through step by step, ensuring nothing is overlooked. For a conceptual model, a checklist could look something like this:

- Is it understandable for non-technical users?
- Does it help technical users understand the business?
- Do the entities represent real-world objects?
- Are the relationships named in a meaningful way?
- (Optional) Does every entity have a business key?

### Logical Data Model: Adding Details, Not Technology

The logical level adds more structure, defining attributes, keys, and relationships in detail while remaining independent of specific technologies or systems.

### Physical Data Model: The Tech Blueprint

Physical Model: Shows how this translates into database tables, column types, and indexes.

## Why Data Modeling Is Not Just Overhead

## Which Tool Is The Best For The Job

## The Modern Case for Data Modeling

## Literature and Sources

## Final Thoughts
