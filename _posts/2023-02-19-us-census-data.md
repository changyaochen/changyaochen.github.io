---
layout: single
title:  "How to use US Census Bureau data"
date:   2023-02-20 12:00:00 -0600
published: false
tag: [misc]
toc: true
toc_sticky: true
excerpt: "A quick primer on how to leverage the rich data from the US Census Bureau."
header:
  teaser: /assets/images/us-census-bureau-data.png
---

Recently I have to explore the US Census Bureau data, and explore the demographic information at the ZIP code level.
In the past, I usually just Google search for nicely parsed data, _e.g._, total population at each ZIP code,
and chances are there are someone already made the data available. After all:

* The data is free (from the US Census Bureau).
* The size of the data is (usually) small enough to be download (after all there are about
400,000 ZIP codes across US).

However this time around, I am interested in more than the common demographic information, therefore, I reckon it
is better to query directly from the data source, and I did learn quite a few things about the US Census data.

## US Census Bureau does not know ZIP code, use ZCTA
The commonly known concept of [ZIP code](https://en.wikipedia.org/wiki/ZIP_Code) is defined by US Postal Service (USPS),
in order to facilitate efficient mail delivery. However, the US Census Bureau operates and organize data under its own
[geography entity hierarchy](https://www.census.gov/programs-surveys/geography/guidance/hierarchy.html), and it does
not honor the USPS ZIP code. As shown below, the smallest geographic entity is a Census Block (think it as a city block),
and rolling all the way up to the Nation level. As such, US Census Bureau data can not directly answer the question such as
"what is the population of ZIP code 10027".

<figure>
<center>
<a href="/assets/images/US_census_bureau_geography.png"><img style="width:100%;" src="/assets/images/US_census_bureau_geography.png"></a>
</center>
</figure>

To map the US Census Bureau data at the ZIP code level, the closet geographic entity is the Census Tract (there are about 70,000).
However, it is a many-to-many mapping, _i.e._, a Census Tract can contain multiple ZIP codes, and a ZIP code can cover multiple
Census Tract as well. I have found convenient [crosswalk files](https://www.huduser.gov/portal/datasets/usps_crosswalk.html)
that provides such a mapping.

There is an easier way. Since 2000, the US Census Bureau introduced the geographic entity of
**ZIP Code Tabulation Areas (ZCTAs)**. Per [Wikipedia](https://en.wikipedia.org/wiki/ZIP_Code_Tabulation_Area):

> This new entity was developed to overcome the difficulties in precisely defining the land area covered by each ZIP code.

The [documentation](https://www.census.gov/programs-surveys/geography/guidance/geo-areas/zctas.html) from US Census Bureau
provides the details of how ZCTAs are created, and the important aspect to a data consumer is probably:

> In most instances the ZCTA code is the same as the ZIP Code for an area.

Good enough for me! It would be nice to quantify *most*, but I will give the benefit of the doubt and operate under the
mode of `ZIP code == ZCTA`.

## Use ACS, not the Census itself
The colloquial of "US Census" usually refers to the [decennial census](https://en.wikipedia.org/wiki/United_States_census),
that conducted once every 10 years (the most recent
one is in 2020). It is a *complete count* of the entire U.S. population, and asks just a few questions about every person
and household. The public artifact of the Census is the Public Law (P.L.) 94-171
[Redistricting Data](https://data.census.gov/all?q=Population+Total&y=2020&d=DEC+Redistricting+Data+(PL+94-171)). From the name, it
is not hard to guess the purpose of the data: to re-draw the US congressional districts and reapportioning the
House of Representatives. Therefore, we can consider it only provides the population count, and nothing more.

The treasure trove of the US Census Bureau data, is the American Community Survey (ACS). It conducts continuously since the early 2000s,
and is an ongoing survey of just a portion of the population. The ACS asks dozens of questions on a wide variety of topics
to gather information about the demographic, social, economic, and housing characteristics of the population. The main differences
between the decennial census and ACS are:

* The decennial census, well, is a census. It is an one-time, complete count of population.
* The ACS is an ongoing survey, designed to provide ongoing and up-to-date information about communities throughout the United States,
enabling policymakers, businesses, and individuals to make informed decisions.

As a data consumer, I'm almost always interested in ACS, given the rich information it provides. However,
being a survey, we need to keep in mind we are dealing with point estimates. Fortunately, for each of the information
(_e.g._, family income), US Census Bureau also provides the margin of error. Another factor to consider is how many
samples are used to derive the point estimate. In ACS case, this is conveyed through how many years of survey results
are used. Currently there are only two options: 1-year estimate and 5-year estimate. The tradeoff is pretty intuitive:
the former reflects more recent trend, whereas the latter provides smaller margin of error.

## Accessing the ACS data
To be honestly, it is not very intuitive how to access the US Bureau data, at least for someone who is new to it.
After a few days' digging, hopefully the following steps would save you some time. Here I assume we are interested
in the bulk download, not API calls (which is [available](https://www.census.gov/data/developers/data-sets.html)).

### Search for the table of your interest
US Census Bureau provides a handy [entrypoint](https://data.census.gov/table) to search for all available tables.
Apply the appropriate filters (from the left panel),
[for example](https://data.census.gov/table?y=2021&d=ACS+5-Year+Estimates+Detailed+Tables),
with the 2021 ACS 5-year estimate data. This will result in more than 1000 tables. We can then further
filter by the topics, [for example](https://data.census.gov/table?t=Education&y=2021&d=ACS+5-Year+Estimates+Detailed+Tables), education.
In this case, there are less than 100 tables left.

Each of the table comes with an alphanumerical table identifier (_e.g._, "B06009"), and the long description (_e.g._,
"PLACE OF BIRTH BY EDUCATIONAL ATTAINMENT IN THE UNITED STATES"). The default view will be at the national level,
and one can apply "Geography" filter to obtain aggregation at different geographic entities (_e.g._, ZCTA).
Since our goal to make bulk downloads, knowing the table identifier is enough.
With the table identifier in hand, we can leverage the FTP service provided by the US Census Bureau, to directly
download the raw files.

### Data dictionary

The raw data will be in tabular format, and a key information is the data dictionary, _i.e._, what does each column mean.
To understand it, one should probably (highly recommended) first read the ACS
[manual](https://www.census.gov/content/dam/Census/library/publications/2020/acs/acs_general_handbook_2020.pdf).

For the 2021 ACS 5-year estimate,
[this](https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/documentation/ACS20215YR_Table_Shells.txt)
is the data dictionary, _i.e._, mapping between the table identifier, name of each column in the tables, and the semantic.
For example, the first few lines reads:

```
Table ID|Line|Indent|Unique ID|Label|Title|Universe|Type
B01001|1.0|0|B01001_001|Total:|SEX BY AGE|Total population|int
B01001|2.0|1|B01001_002|Male:|SEX BY AGE|Total population|int
...
```
It indicates for the table with id of "b01001", the columns with names of
"B01001_E002" and "B01001_M002" means the **E**stimate and **M**argin of error
for "total population of male", respectively. Note that the injected letter **E** and **M** in the column names.

### Download from FTP
All the tables are accessible, even from your browser. A better way to access the data is to
download them programmatically. [This](https://github.com/uscensusbureau/acs-summary-file/pull/14/files#diff-6e7bdc9416f82cbd97963c90ec0fa91c52a47ab3dec8db17dd5f81498097e62b)
is a simple Python snippet I coded it up, to download a single table, and filter at the given geographic entity level.
Here I use the ZCTA (`summary_level=860`) as an example.

Note that, for the ACS 5-year estimate, each table contains aggregation at all geographic entity level (aka, summary level).
The geographic entity is identified by the column `GEO_ID`, while there doesn't seem to have an
official definition of the `GEO_ID`, [this](https://mcdc.missouri.edu/geography/sumlevs/) is a very good resource to use.

## Conclusion
Here we describe the how to understand and access US Census Bureau data. Hopefully it can save you
some time Googling around for nicely parsed US demographic related information, as you can easily
download them from the source!
