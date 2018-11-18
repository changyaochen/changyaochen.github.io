---
layout: single
title:  "Pivot a Hive table"
date:   2018-11-18 12:00:01 -0600
published: false
tag: [misc]
excerpt: There is no built-in pivot function in Hive, but one can still do it with relative ease.
toc: false
header:
  teaser: /assets/images/hive_teaser.png
---
[Pivoting a table](https://en.wikipedia.org/wiki/Pivot_table) is a handy function in much of our data analysis, and one can do it easily with Excel or [pandas](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.pivot.html), but there is no built-in Hive function that will do the same job for us. However, there are days one really wish such function exists, let me describe just one of them.

Let's say we have a large sparse matrix, with a dimension of 1 million rows, and 1,000 columns. For each row, there are only 10 non-zero elements. To represent this matrix as a table in its natural form, there will be 1 billion (= 1 million x 1,000) entries required, that's very wasteful for those many zeros. One solution is to represent the matrix in the long format, such that this table will have only 3 columns: row index, column index, and value. Only the non-zero elements of the matrix will be recorded in this table. Therefore, this table will have only 30 million (= 1 million x 10 x 3) elements. That is substantially smaller than the previous solution, and yet we don't lose any information. 

However, there are situations we would prefer the nice 1 million x 1,000 wide format, for example, in certain machine learning scenario. Here we need to convert the matrix from long format to the wide format. This is where pivoting comes into play, and below is how you can do it in Hive.

Let's make a toy Hive table, to represent a sparse matrix in long format:
~~~sql
CREATE TABLE test_table
(
    id BIGINT,
    key1 STRING,
    key2 STRING,
    value INT
) STORED AS ORC;
 
INSERT INTO TABLE test_table VALUES
    (1001, 'key_11', 'key_21', 111),
    (1002, 'key_11', 'key_22', 222),
    (1003, 'key_11', 'key_23', 333),
    (1001, 'key_12', 'key_21', 111),
    (1002, 'key_12', 'key_22', 222),
    (1003, 'key_12', 'key_23', 333)
;
~~~
Here I spiced things up a little bit. The `id` column corresponds to the row index, but the column index is represented as the combination of the `key1` and `key2` columns. In this way, if I know for sure (*e.g.*, by design) that, there are only `p` unique values of `key1`, and `q` unique values for `key2`, then instead for spell out all the unique column indices multiplicatively (`p x q`), I can just represent them additively (`p + q`).

### Method 1:
The first method is rather straightforward: since we know, a priori, all the column indices, let's just scan the long table row by row, checking for this row index (`id` in the toy table), what is the corresponding column index. Therefore, it will just be an exhaustive `CASE` statements, such as the one below: 
~~~sql
SELECT
    id,
    MAX(CASE WHEN key1 = 'key_11' AND key2 = 'key_21' THEN value ELSE NULL END) AS key_11_key_21,
    MAX(CASE WHEN key1 = 'key_11' AND key2 = 'key_22' THEN value ELSE NULL END) AS key_11_key_22,
    MAX(CASE WHEN key1 = 'key_11' AND key2 = 'key_23' THEN value ELSE NULL END) AS key_11_key_23,
    MAX(CASE WHEN key1 = 'key_12' AND key2 = 'key_21' THEN value ELSE NULL END) AS key_12_key_21,
    MAX(CASE WHEN key1 = 'key_12' AND key2 = 'key_22' THEN value ELSE NULL END) AS key_12_key_22,
    MAX(CASE WHEN key1 = 'key_12' AND key2 = 'key_23' THEN value ELSE NULL END) AS key_12_key_23
FROM
    test_table
GROUP BY
    1
;
~~~
It will do the job just fine: the `MAX` function is put in place as a trick to satisfy the `GROUP BY` clause, since we assume there is only one value for each column index anyway. All those `CASE` statements might seem daunting, but they can be easily populated by nested `for` loops, with a scripting language such as `python`. Below is the result, exactly what we wanted.
~~~sql
id     key_11_key_21   key_11_key_22   key_11_key_23   key_12_key_21   key_12_key_22   key_12_key_23
-----+---------------+---------------+---------------+---------------+---------------+--------------
1001   111             NULL            NULL            111             NULL            NULL
1002   NULL            222             NULL            NULL            222             NULL
1003   NULL            NULL            333             NULL            NULL            333
~~~
However, when I used this method on a real table, which has more than 3 billion rows, it took me a whopping 5+ hours to get the wide format table, which has about 50 million rows and 100 columns. I need a real pivot.

### Method 2
Let me just show the query first:
~~~sql
SELECT
    mapped.id,
    COLLECT_LIST(group_map["key_11_key_21"])[0] AS key_11_key_21,
    COLLECT_LIST(group_map["key_11_key_22"])[0] AS key_11_key_22,
    COLLECT_LIST(group_map["key_11_key_23"])[0] AS key_11_key_23,
    COLLECT_LIST(group_map["key_12_key_21"])[0] AS key_12_key_21,
    COLLECT_LIST(group_map["key_12_key_22"])[0] AS key_12_key_22,
    COLLECT_LIST(group_map["key_12_key_23"])[0] AS key_12_key_23
FROM
    (
        SELECT
            id,
            MAP(CONCAT_WS('_', key1, key2), value) AS group_map
        FROM       
            test_table
    ) mapped
GROUP BY mapped.id
;
~~~
If you trust me, this will return the same results. 

What is going on here? We have first make a sub-query, whose results is assigned with the alias `mapped`. In this sub-query, we have only a simple `MAP` function (this is the first trick), as well as the [`CONCAT_WS` function ](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF)to stitch all the "key"s together, as the column index. Below is what `mapped` looks like:
~~~sql
id     group_map
-----+----------------------
1001   {"key_11_key_21":111}
1002   {"key_11_key_22":222}
1003   {"key_11_key_23":333}
1001   {"key_12_key_21":111}
1002   {"key_12_key_22":222}
1003   {"key_12_key_23":333}
~~~
Essentially, we have made a dictionary from each row, with just one key-value pair. Then in the outer query, as the second trick, we invoke the [`COLLECT_LIST` function](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF) to pick all values from the dictionaries, and then `GROUP BY` with `id` (row index). Again, here we assume:

1. There is only one value for each (row index, column index)
2. We can exhaustively populate all the column indices.

We then just pick the first element from the `COLLECT_LIST` call, instead of using any other reduction function. This is based on the first assumption listed above. If we forgo the `[0]` part, below is the result:
~~~sql
id     key_11_key_21   key_11_key_22   key_11_key_23   key_12_key_21   key_12_key_22   key_12_key_23
-----+---------------+---------------+---------------+---------------+---------------+--------------
1001   [111]           []              []              [111]           []              []
1002   []              [222]           []              []              [222]           []
1003   []              []              [333]           []              []              [333]
~~~
Each element now is a list, with just one or zero entry. If it so happened that there will be more than one entry, *e.g.*, there are multiple values for the same (row index, column index), then one can probably do further aggregation, using another outer query with another `GROUP BY`.

How does it work in practice? Using this method, for the same 3 billion+ row task, it took less than 40 minutes! Although the run time depends on the actual Hadoop cluster load, wchih can fluctuate, but given such a large difference, I can comfortably reject the null hypothesis, and happily adopt Method 2.