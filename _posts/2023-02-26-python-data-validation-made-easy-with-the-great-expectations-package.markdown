---
layout: post
title: "Python Data Validation Made Easy with the Great Expectations Package"
date: 2023-02-26 14:00:00 +0200
categories: Python
comments: true
published: true
excerpt: |
  Great Expectations is a Python package that helps data engineers set up reliable data pipelines with built-in
  validation at each step. By defining clear expectations for your data, it ensures that your data meets those
  expectations, making it more reliable and easier to work with.
image_url: /assets/images/unsplash/eleonore-kemmel-IJ7HG4woGlk-unsplash.jpg
image_description: |
  Photo by [Eléonore Kemmel](https://unsplash.com/@ekemmel?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/photos/IJ7HG4woGlk?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---

In today's data-driven world, ensuring high data quality is more critical than ever before. The vast amounts of data
available to us are useless if we can't trust the data itself. Fortunately, the Python package Great Expectations
provides an effective solution for handling data quality and validation needs.

In this blog post, we will explore some key features of the Great Expectations package, demonstrate how to use it with
an open data set, and highlight the benefits of this approach. So let's dive in and see how Great Expectations can help
you ensure the reliability of your data.

> With big data comes big responsibility.
>
> **Uncle Ben**

## Overview

Great Expectations is a Python library designed to help data engineers, analysts, and scientists ensure the quality,
accuracy, and completeness of their data. It provides an easy and intuitive way to define and manage expectations (for
example "this column should only contain positive values"), validate data against those expectations, and automatically
alert users when expectations are violated.

Some of the main features of Great Expectations include:

- An extensive library of predefined [expectations](https://docs.greatexpectations.io/docs/terms/expectation), making it
  easy to define expectations for various types of data, such as numerical, textual, and datetime data.
- Customizable [expectation suites](https://docs.greatexpectations.io/docs/terms/expectation_suite) that allow users to
  create their own sets of expectations to apply to specific data sets.
- Interactive data profiling and visualization tools to help users understand their data and quickly identify potential
  issues.
- Support for various data sources and data formats, including
  [Databricks](https://docs.greatexpectations.io/docs/deployment_patterns/how_to_use_great_expectations_in_databricks/),
  SQL databases like
  [PostgreSQL](https://docs.greatexpectations.io/docs/guides/connecting_to_your_data/database/postgres/),
  [Spark](https://docs.greatexpectations.io/docs/deployment_patterns/how_to_instantiate_a_data_context_on_an_emr_spark_cluster/),
  and [Pandas](https://docs.greatexpectations.io/docs/guides/connecting_to_your_data/in_memory/pandas/) data frames.
- The ability to integrate Great Expectations into existing data pipelines, making it easy to add data validation and quality checks to existing workflows.

Great Expectations (GX) is available in two flavors:

- [GX OSS](https://greatexpectations.io/gx-oss)

  This is the open-source version of Great Expectations that can be installed and set up within your own data stack to
  fit your needs. It is freely available and offers all the features of the Great Expectations library. We will be using
  the open-source version in this blog post.

- [GX Cloud](https://greatexpectations.io/gx-cloud)

  This is a cloud-based service that provides an easy way to use Great Expectations without having to manage
  infrastructure or set up pipelines manually. It will be made publicly available in 2023. Although there is not much
  information available on the Great Expectations website yet, you can join a
  [waitlist](https://greatexpectations.io/cloud) to be notified when it becomes available.

## Selecting an open data set

To demonstrate the features of Great Expectations, we will be using the Boston Airbnb open dataset, which is available
for download from [Kaggle](https://www.kaggle.com/datasets/airbnb/boston?resource=download). The dataset includes
information on Airbnb listings in Boston, including the location, price, availability, and other relevant information.

![Boston AirBnB Open Data](/assets/images/posts/2023_02_26_kaggle_boston_airbnb.png "Boston AirBnB Open Data")

The dataset is composed of three files: `listings.csv`, which contains detailed information on the listings and the
average review score; `calendar.csv`, which includes historical price data and availability information; and
`reviews.csv`, which contains user reviews along with unique reviewer IDs and detailed comments. This dataset has common
data quality issues such as missing values, inconsistent data types, and incorrect formatting, making it an excellent
candidate for demonstrating how Great Expectations can be used to ensure data quality and identify issues that may
affect the reliability of the data.

## Setting up Great Expectations

Explain how to install Great Expectations using pip or conda.
Walk through the process of setting up a new project and initializing Great Expectations.
Include any necessary code snippets or screenshots.

It all starts with the installation of Great Expectations:

```sh
pip install great_expectations
```

Check if the installation was successful on the command line. This command should return the installed version number of
Great Expectations:

```sh
great_expectations --version
```

```sh
great_expectations, version 0.15.47
```

After a successful installation, you can set up a so-called data context with the following command:

```sh
great_expectations init
```

This prompts a welcome screen and explains the directory structure which will be set up. Confirm your choice with typing
`Y`.

```sh
Using v3 (Batch Request) API

  ___              _     ___                  _        _   _
 / __|_ _ ___ __ _| |_  | __|_ ___ __  ___ __| |_ __ _| |_(_)___ _ _  ___
| (_ | '_/ -_) _` |  _| | _|\ \ / '_ \/ -_) _|  _/ _` |  _| / _ \ ' \(_-<
 \___|_| \___\__,_|\__| |___/_\_\ .__/\___\__|\__\__,_|\__|_\___/_||_/__/
                                |_|
             ~ Always know what to expect from your data ~

Let's create a new Data Context to hold your project configuration.

Great Expectations will create a new directory with the following structure:

    great_expectations
    |-- great_expectations.yml
    |-- expectations
    |-- checkpoints
    |-- plugins
    |-- .gitignore
    |-- uncommitted
        |-- config_variables.yml
        |-- data_docs
        |-- validations

OK to proceed? [Y/n]:
```

## Creating A Data Source

Start the data discovery by connecting to your data set. As shown before, Great Expectations supports a wide range of
[integrations](https://greatexpectations.io/integrations/). For our example, we will be using the filesystem connector
to access our AirBnB Boston open data set.

Run the following command which prompts you with the available main choices and select `1` for the filesystem:

```sh
great_expectations datasource new
```

```sh
What data would you like Great Expectations to connect to?
    1. Files on a filesystem (for processing with Pandas or Spark)
    2. Relational database (SQL)
:1
```

The next question asks about the library you are using to process your data with. We are selecting the first option
here, Pandas:

```sh
What are you processing your files with?
1. Pandas
2. PySpark
: 1
```

Now we are specifying the path to our data that we downloaded earlier into the folder `./data/`:

```sh
Enter the path of the root directory where the data files are stored. If files
are on local disk enter a path relative to your current working directory or an
absolute path.
: ./data/
```

Great Expectations will now start [Jupyter](https://jupyter.org) and open a notebook to create your data source. I
recommend changing the default name of the datasource to be able to identify it. I named the datasource in this example `boston_airbnb_data`. Execute the cells and delete the notebook if every step was successful.

## Create An Expectations Suite

An expectation suite is a collection of expectations that define the requirements for a specific data asset or set of
assets. This set of expectations serves as a data contract between the data producer and the data consumer, ensuring
that both parties have a shared understanding of what the data should look like and how it should behave. By
establishing a clear data contract through expectation suites, data engineers can ensure that the data is consistent,
reliable, and fit for purpose, reducing the risk of errors and inconsistencies down the line.

Once we've created our data source, we'll need to create an expectations suite that defines the requirements for that
data. To do this, we can run the following command and select the third option, which will launch the Data Assistant.
This interactive tool guides us through the process of defining expectations for our data, making it easy to build a
comprehensive expectations suite without having to write code from scratch.

```sh
great_expectations suite new
```

```sh
How would you like to create your Expectation Suite?
    1. Manually, without interacting with a sample Batch of data (default)
    2. Interactively, with a sample Batch of data
    3. Automatically, using a Data Assistant
: 3
```

The Data Assistant will ask for the batch of data to be used for this expectations suite. We will select the
listings CSV file. Additionally we will name the expectations suite accordingly.

```sh
A batch of data is required to edit the suite - let's help you to specify it.

Select a datasource
    1. calendar.csv
    2. listings.csv
    3. reviews.csv
: 2
```

```sh
Which data asset (accessible by data connector
"default_inferred_data_connector_name") would you like to use?
    1. airbnb.boston.listings.csv

Type [n] to see the next page or [p] for the previous. When
you're ready to select an asset, enter the index.
: 1
```

```sh
Name the new Expectation Suite [stations.json.warning]: airbnb.boston.listings.csv
```

The Data Assistant will sum up your selections and explain the next steps. We will confirm the actions with `Y`.

```sh
Great Expectations will create a notebook, containing code cells that select
from available columns in your dataset and generate expectations about them
to demonstrate some examples of assertions you can make about your data.

When you run this notebook, Great Expectations will store these expectations
in a new Expectation Suite "airbnb.boston.listings.csv" here:

  file:///Users/Chris/Documents/Projects/gx-example/great_expectations/expectations/airbnb/boston/listings/csv.json

Would you like to proceed? [Y/n]: Y
```

Great Expectations will launch a Jupyter Notebook that guides you through the process of creating a new expectation
suite. For our example, we will be starting with the following columns (need to be excluded in the "Select columns"
step):

- `city`
- `state`
- `country_code`
- `country`
- `latitude`
- `longitude`
- `price`

Once we run all the cells of the notebook, an initial expectation suite will be generated for the listings data. This
suite is automatically derived from the values and distribution of the input data, making it a great starting point for
our data validation process. Great Expectations also generates a set of data documentation, known as
[Data Docs](https://docs.greatexpectations.io/docs/terms/data_docs/), which is opened automatically. These Data Docs
provide an overview of the individual expectations that were derived from the input data, giving us a detailed picture
of how our data is expected to behave.

![Data Docs](/assets/images/posts/2023_02_26_data_docs.png "Data Docs")

These are some examples for the expectations that Data Assistant created for the Boston AirBnB open data set:

- The required set of columns
- Values for `state` must belong to this set: `United States`
- Values for `country_code` must belong to this set: `US`
- Values for `latitude` must never be null and greater than or equal to 42.235... and less than or equal to 42.389...
- Values for `longitude` must never be null and greater than or equal to -71.171... and less than or equal to -71.000...

The initial suite of autogenerated expectations should only be considered as a starting point for data validation. It is
important to tailor the expectations to your specific use case and data, which can improve the accuracy and reliability
of your data pipelines. Therefore, we can improve the initial suite by using the following command to edit the
expectation suite, and fine-tuning the expectations based on our domain knowledge and data exploration.

```sh
great_expectations suite edit airbnb.boston.listings.csv
```

Let us edit the `state` and `price` expectations in the opened Jupyter notebook. We scroll to the
"Column Expectation(s)" section and the "state" paragraph. The first expectation is
`expect_column_values_to_not_be_null` and we can leave it as is. The next expectations
`expect_column_value_lengths_to_be_between` and `expect_column_values_to_match_regex` can be removed. We are only
expecting listings from Boston to be in the set, thus we are only expecting the "MA" (Massachusetts) value here.

The only expectation we are leaving regarding the state values is the `expect_column_values_to_be_in_set` expecation:

```py
expectation_configuration = ExpectationConfiguration(**{
  "meta": {
    "profiler_details": {
      "metric_configuration": {
        "domain_kwargs": {
          "column": "state"
        },
        "metric_name": "column.distinct_values",
        "metric_value_kwargs": None
      },
      "num_batches": 1,
      "parse_strings_as_datetimes": False
    }
  },
  "expectation_type": "expect_column_values_to_be_in_set",
  "kwargs": {
    "column": "state",
    "mostly": 1.0,
    "value_set": [
      "MA"
    ]
  }
})
suite.add_expectation(expectation_configuration=expectation_configuration)
```

For the `price` column, the Data Assistant used a simple regular expression to validate the data values: `\\d+`.
However, we know that the values always start with a dollar sign followed by the actual amount as float datatype with
the optional comma sign.

```py
"expectation_type": "expect_column_values_to_match_regex",
"kwargs": {
  "column": "price",
  "mostly": 1.0,
  "regex": "^\\$([0-9],)*[0-9]+\\.[0-9]{2}$"
},
```

## Running validation tests

After completing our first expectation suite, we can create a so-called
[checkpoint](https://docs.greatexpectations.io/docs/terms/checkpoint). This Checkpoint can then be reused for data
validation in the future. Additional checkpoints can be created and configured to cover different use cases. Create the
first checkpoint with the following command:

```sh
great_expectations checkpoint new initial_checkpoint
```

After command opens the according Jupyter notebook, where we can create and set up the checkpoint using the provided
cells. To run the checkpoint and open the associated Data Docs, we simply uncomment the last two cells in the notebook.
Running the checkpoint will validate the data against the specified expectations and generate detailed validation
results that can be viewed in the Data Docs.

```py
context.run_checkpoint(checkpoint_name=my_checkpoint_name)
context.open_data_docs()
```

Once a Checkpoint completes its validation, the results are automatically compiled into Data Docs. These results can be
accessed through the Validation Results tab in the Data Docs. Clicking on an individual Validation Result in the Data
Docs will display a detailed list of all the Expectations that were executed during the validation process, along with
the results indicating which Expectations passed and which ones failed.

## Conclusion

In summary, Great Expectations is a Python package that allows for flexible and customizable data testing and
validation. It can handle a wide range of data quality issues, including data type, range, and consistency checks. Great
Expectations allows for the creation of an expectation suite that can be edited and updated as needed, and it can
generate data documentation for improved data transparency and understanding.

The benefits of using Great Expectations for data testing and validation include improved confidence in data quality,
reduced risk of errors and inaccuracies in downstream analysis, and streamlined data pipeline processes. The package is
flexible and can be integrated into a variety of data stacks, and it offers both open source and cloud-based options for
use. Overall, Great Expectations is a powerful tool for ensuring the reliability and accuracy of data used in analytics
and decision-making.
