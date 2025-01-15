---
layout: post
title: "Data Modeling 101: Logical, Conceptual, and Physical Models"
date: 2025-01-01 00:00:00 +0200
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

- Entities to represent real-world objects, such as a _Customer_ or a _Product_.
- Keys to uniquely identify entities, such as a customer’s email address or a product’s SKU.
- Attributes to represent the properties of entities, such as a customer’s Name or a product’s price.
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

For example, consider a Payment entity. In the real world, cash payments and card payments may not share a single unique identifier, making it difficult to represent them under the same entity in a conceptual model. This might require you to create separate entities, such as _Cash Payment_ and _Card Payment_, increasing complexity at the conceptual level.

Another approach to conceptual modeling involves adding attributes to conceptual entities. This can help you get more detailed information from business stakeholders about the real-world objects you’re modeling. However, it risks losing sight of the big picture and the interactions between entities, focusing instead on details that could be worked out at a later stage.

For example, adding attributes like Passenger Age or Ticket Price at the conceptual level might start discussions with specifics, distracting from general questions like how passengers interact with tickets and flights.

As with any software development artifact, it’s good practice to review your work. An effective review is easier with a checklist to go through step by step, ensuring nothing is overlooked. For a conceptual model, a checklist could look something like this:

- Is it understandable for non-technical users?
- Does it help technical users understand the business?
- Do the entities represent real-world business objects?
- Are these business objects parts of a business processes?
- Are the relationships named in a meaningful way?
- (Optional) Does every entity have a business key?

### Logical Data Model: Adding Details, Not Technology

The logical level adds more structure.

Within the logical data model (LDM), you're defining attributes, keys, and relationships in detail. At the same time you're remaining independent of specific technologies or systems. This means no data types, no workaround mapping-tables, or any other implementation details. It also means no uppercase or hungarian or any other notation, but still be written in natural language.

If you haven't defined the primary keys at the conceptual level, you must define them here at the logical level at the latest. Primary keys are unique identifiers for a row within a dataset. Without them, it becomes difficult to link data, clean duplicate data, or work with data across interfaces.

The primary key is not necessarily the business key. It is recommended that your data model generates its own so-called _surrogate keys_ (as primary keys). and treats the business key as a separate attribute. However, this distinction is typically made at the physical level, as it is an implementation detail. At the logical level, the business key is often used as the primary key, to keep the model independent from the actual implementation.

The logical data model describes relationships in detail.

Relationships connect entities. The so-called _cardinality_ describes how many entities can be related to the connected entity, for example a plane ticket can have one and only one passenger on it, but a passenger can have several tickets. You should specify the cardinality for each relationship on the logical level, including the minimum and maximum possible number of connected entities.

Foreign keys are used to establish relationships between different entities in a data model. They are attributes in one table that reference the primary key of another table, ensuring referential integrity and enabling the linking of related data across tables. The cardinality of the relationship determines how foreign keys are applied, defining whether it is a one-to-one, one-to-many, or many-to-many relationship.

The logical data model adds attributes.

The attributes should be as detailed as possible. They don't need a data type yet–those are assigned in the physical data model. However, the name can already indicate the data type, for example:

- _Booking Date_ for a date type like 2025-12-12
- _Arrival Datetime_ for a date and time type like 2025-12-12T12:25:10Z

If the attribute is in a ISO-unit, the attribute's name should already specify this to prevent confusion, for example:

- _Height in Feet_ instead of just _Height_
- _Weight in Kilogram_ instead of just _Weight_

Don't worry about the length of the attributes' names. The advantage of a readable and unambiguous data model outweighs possible misunderstandings with abbreviations or missing information. The era of limiting attribute field names in databases to a maximum of eight characters is long over (phew).

The logical data model needs a different notation than the conceptual data model because it has much more detail in it. The [entity-relationship diagram](https://en.wikipedia.org/wiki/Entity–relationship_model) is the recommended type for a logical data model. I prefer the so-called [crow's foot notation](https://en.wikipedia.org/wiki/Entity–relationship_model#Crow's_foot_notation) (also called Martin Notation) in the data model to describe relationships with their cardinality.

Building on our airline example, the logical data model looks like this:

![Logical Model](/assets/images/posts/2024_11_17_logical_model.png "Logical Model")

So, how does this differ from the conceptual level?

- **Additional entity flight operation:** There is a new data entity called _Flight Operation_. It connects the two data entities _Flight_ and _Aircraft_. Each flight operation represents the actual flight that took place at the specific _Operating Date_.

- **Primary keys:** Each data entity now has a primary key that identifies individual rows in the dataset. They are marked with "PK" and underlined. This is optional, but helps a lot with readability.

- **Foreign keys and relationships:** Relationships with their cardinality are added. Foreign keys are marked as "FK," following the same notation as primary keys before (again optional but improves readability). The names of foreign keys are identical to the primary key they reference.

- **Attributes:** Attributes are added to the entities. I am using a capitalized notation, but that's not necessary. It just needs to be consistent across different data models.

### Physical Data Model: The Tech Blueprint

The physical data model adds the technical implementation details.

## Why Data Modeling Is Not Just Overhead

## Which Tool Is The Best For The Job

## The Modern Case for Data Modeling

## Literature and Sources

## Final Thoughts
