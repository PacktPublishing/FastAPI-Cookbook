# MongoDB Data Masking Examples

## Introduction

Example project showing how a MongoDB's aggregation pipeline can be used to perform data masking on all the records (documents) contained in a collection, where the changes are non-reversible. For more context on why data masking is an important common requirement and how this can be effectively achieved in MongoDB, first read the blog post that accompanies this project, [MongoDB Data Masking Examples blog post](https://pauldone.blogspot.com/2021/02/mongdb-data-masking.html).

Also, in the book [Practical MongoDB Aggregations](https://www.practical-mongodb-aggregations.com/) by this project's author, there is the [Mask Sensitive Fields chapter](https://www.practical-mongodb-aggregations.com/examples/securing-data/mask-sensitive-fields.html) which describes this same topic.

The example aggregation pipeline used in this project will be used to transform some example __card payments__ records, shown in the left hand side of the screenshot below, into masked records, shown on the right hand side of the screenshot, where sensitive fields have been redacted.

 ![Data Before And After Masking](.datapic.png)

<br/>

## Prerequisites

* A [MongoDB database](https://docs.mongodb.com/manual/installation/) is running and accessible locally or over a network, using MongoDB version 4.4 or greater
* The [Mongo Shell](https://www.mongodb.com/try/download/shell) can be run from the local workstation (the instructions below assume the newer `mongosh` version of the shell has been installed, rather than the _legacy_ `mongo` shell bundled with the `mongod` database installer, although either is fine to use)
* From a command-line terminal on the workstation, the Mongo Shell has been launched referencing a MongoDB database deployment, where the connecting user has sufficient rights to create and modify any database. For example, execute the following (first changing the URL where necessary):

```bash
mongosh 'mongodb://localhost:27017'
```

<br/>

## Populate The Sample Payments Data In The Database

Via the open Mongo Shell, execute the following to remove the old `testdata` database (if it exists), and to then add two new sample payment records to the `payments` collection in the `testdata` database, before querying all the records in the new collection, as a final check:

```javascript
use testdata;

db.dropDatabase();

db.payments.insertMany([
    {
        'card_name': 'Mrs. Jane A. Doe',
        'card_num': '1234567890123456',
        'card_expiry': ISODate('2023-08-31T23:59:59Z'),
        'card_sec_code': '123',
        'card_provider_name': 'Credit MasterCard Gold',
        'card_type': 'CREDIT',        
        'transaction_id': 'eb1bd77836e8713656d9bf2debba8900',
        'transaction_date': ISODate('2021-01-13T09:32:07Z'),
        'transaction_curncy_code': 'GBP',
        'transaction_amount': NumberDecimal('501.98'),
        'settlement_id': '9ccb27aeb8394c2b3547521bcd52a367',
        'settlement_date': ISODate('2021-01-21T14:03:53Z'),
        'settlement_curncy_code': 'DKK',
        'settlement_amount': NumberDecimal('4255.16'),
        'reported': false,
        'customer_info': {
            'category': 'SENSITIVE',
            'rating': 89,
            'risk': 3,
        }
    },
    {
        'card_name': 'Jim Smith',
        'card_num': '9876543210987654',
        'card_expiry': ISODate('2022-12-31T23:59:59Z'),
        'card_sec_code': '987',
        'card_provider_name': 'Debit Visa Platinum',
        'card_type': 'DEBIT',        
        'transaction_id': '634c416a6fbcf060bb0ba90c4ad94f60',
        'transaction_date': ISODate('2020-11-24T19:25:57Z'),
        'transaction_curncy_code': 'EUR',
        'transaction_amount': NumberDecimal('64.01'),
        'settlement_id': 'd53799f94d7ad72f698c5a4f04c031a6',
        'settlement_date': ISODate('2020-12-04T11:51:48Z'),
        'settlement_curncy_code': 'USD',
        'settlement_amount': NumberDecimal('76.87'),
        'reported': true,
        'customer_info': {
            'category': 'NORMAL',
            'rating': 78,
            'risk': 55,
        }
    },
]);

db.payments.find();
```

<br/>

## Create The Data Masking Aggregation Pipeline

You will create 3 aggregation stages, each assigned to a different variable, before these 3 stages are brought together to form the final `pipeline` variable, ready to mask various parts of every record in a collection, when executed later. To define these pipeline stages and final pipeline, execute the following in the Mongo Shell:


```javascript
// PART 1 OF PIPELINE
var simpleMasksPt1Stage = {
    // 1. FULL TEXT REPLACEMENT WITH RANDOM VALUES, eg: '133' -> '472'
    'card_sec_code': {'$concat': [
                        {'$toString': {'$floor': {'$multiply': [{'$rand': {}}, 10]}}},
                        {'$toString': {'$floor': {'$multiply': [{'$rand': {}}, 10]}}},
                        {'$toString': {'$floor': {'$multiply': [{'$rand': {}}, 10]}}},
                     ]},
                     
    // 2. PARTIAL TEXT OBFUSCATION RETAINING LAST NUMBER OF CHARS, eg: '1234567890123456' -> 'XXXXXXXXXXXX3456'
    'card_num': {'$concat': [
                    'XXXXXXXXXXXX',
                    {'$substrCP': ['$card_num', 12, 4]},
                ]},
    
    // 3a. PARTIAL TEXT OBFUSCATION RETAINING LAST WORD, eg: 'Mrs. Jane A. Doe' -> 'Mx. Xxx Doe'  (needs post-processing in a subsequent pipeline stage)
    'card_name': {'$regexFind': {'input': '$card_name', 'regex': /(\S+)$/}},
        
    // 4. PARTIAL DATE OBFUSCATION BY ADDING OR SUBTRACTING A RANDOM TIME AMOUNT UP TO ONE HOUR MAX
    'transaction_date': {'$add': [
                            '$transaction_date',
                            {'$floor': {'$multiply': [{'$subtract': [{'$rand': {}}, 0.5]}, 2*60*60*1000]}},
                        ]},
    
    // 5. FULL DATE REPLACEMENT BY TAKING AN ARBITRARY DATETIME OF 01-Jan-2021 AND ADDING A RANDOM AMOUNT UP TO ONE YEAR MAX
    'settlement_date': {'$add': [
                            {'$dateFromString': {'dateString': '2021-01-01T00:00:00.000Z'}},
                            {'$floor': {'$multiply': [{'$rand': {}}, 365*24*60*60*1000]}},
                       ]},

    // 6. FULL DATE REPLACEMENT BY TAKING THE CURRENT DATETIME AND ADDING A RANDOM AMOUNT UP TO ONE YEAR MAX
    'card_expiry': {'$add': [
                        '$$NOW',
                        {'$floor': {'$multiply': [{'$rand': {}}, 365*24*60*60*1000]}},
                   ]},
    
    // 7. PARTIAL NUMBER OBFUSCATION BY ADDING OR SUBTRACTING A RANDOM PERCENT OF ITS VALUE, UP TO 10% MAX
    'transaction_amount': {'$add': [
                            '$transaction_amount',
                            {'$multiply': [{'$subtract': [{'$rand': {}}, 0.5]}, 0.2, '$transaction_amount']},
                        ]},

    // 8. BOOLEAN RANDOM REPLACEMENT, ie. a 50:50 chance of being true vs false
    'reported': {'$cond': {
                    'if':   {'$gte': [{'$rand': {}}, 0.5]}, 'then': true,
                    'else': false
                }},               

    // 9. FULL FIELD OBFUSCATION USING AN MD5 HASH OF ITS VALUE (note, not 'cryptographically safe')
    'transaction_id': {'$function': {'lang': 'js', 'args': ['$transaction_id'], 'body':                   
                            function(id) {
                                return hex_md5(id);
                            }
                      }},
};


// PART 2 OF PIPELINE
var simpleMasksPt2Stage = {
    // 3b. PARTIAL TEXT OBFUSCATION RETAINING LAST WORD (post processing from previous regex operation to pick out 'match')
    'card_name': {'$concat': ['Mx. Xxx ', {'$ifNull': ['$card_name.match', 'Anonymous']}]},
};


// PART 3 OF PIPELINE
var redactFieldsStage = {
    // 10. EXCLUDE SUB-DOCUMENT DATA BASED ON A FIELD'S VALUE, eg. if customer_info.category = SENSITIVE
    '$cond': {
        'if'  : {'$eq': ['$category', 'SENSITIVE']},
        'then': '$$PRUNE',
        'else': '$$DESCEND'
    }
};


// BRING FULL PIPELINE TOGETHER
var pipeline = [
    {'$set': simpleMasksPt1Stage},
    {'$set': simpleMasksPt2Stage},
    {'$redact': redactFieldsStage},
];
```

 &nbsp;_NOTE_: In this example, the Mongo Shell was used to assemble the pipeline logic using JavaScript. However, any of the [programming languages supported by MongoDB](https://docs.mongodb.com/drivers/) could have been used instead to perform the equivalent aggregation pipeline creation.

<br/>

## Expose The Masked Data In Any Of Four Ways

__OPTION 1__: To expose the results of the __Data Masked Aggregation On Demand__ from a trusted app tier written in any programming language, this can be simulated from the Mongo Shell, using JavaScript, to execute the following which will generate and return the masked versions of all the records, on the fly:

```javascript
db.payments.aggregate(pipeline);
```

 &nbsp;_NOTE_: Ensure you lock down the `payments` collection to only be accessible by trusted mid-tier application code and not by any consumer applications directly, meaning that the consumers can only access payments data by invoking an API exposed via the mid-tier application (which in turn will invoke `aggregate(pipeline)` to return masked results only).

<br/><br/> 
 
__OPTION 2__: To expose a __Data Masked Read-Only View__, from the Mongo Shell execute the following which will define a view called `payments_redacted_view`, based on the aggregation pipeline, and then display the masked version of the records returned by this new view:

```javascript
db.createView('payments_redacted_view', 'payments', pipeline);
db.payments_redacted_view.find();
```

 &nbsp;_NOTE_: Ensure that you use MongoDB's [RBAC capabilities](https://docs.mongodb.com/manual/core/authorization/) to forbid any access to the underlying `payments` collection, and instead, only allow consumers to have access to the view `payments_redacted_view` and thus only the masked data it will return.

<br/><br/>

__OPTION 3__: To expose a __Data Masked Copy Of Original Data__, from the Mongo Shell execute the following which will create a new collection called `payments_redacted`, based on applying the masking aggregation pipeline to the old collection, so that the new collection only contains the masked version of the original payments data:

```javascript
new_pipeline = [].concat(pipeline);  // COPY THE ORIGINAL PIPELINE
new_pipeline.push(
    {'$merge': {'into': { 'db': 'testdata', 'coll': 'payments_redacted'}, 'on': '_id',  'whenMatched': 'fail', 'whenNotMatched': 'insert'}}
);
db.payments.aggregate(new_pipeline);
db.payments_redacted.find();
```

 &nbsp;_NOTE_: Ensure afterwards that you either: __1)__ delete the original unmasked `payments` collection, or __2)__ use MongoDB's [RBAC capabilities](https://docs.mongodb.com/manual/core/authorization/) to prevent access to the underlying `payments` collection, thus only allowing consumers to have access to the new masked data `payments_redacted` collection.

<br/><br/>
 
__OPTION 4__: To expose the __Data Masked Overwritten Original Data__, from the Mongo Shell execute the following which will overwrite each record in the existing collection with a modified version of the record, after which the `payments` collection will only contain the masked data.


```javascript
replace_pipeline = [].concat(pipeline);  // COPY THE ORIGINAL PIPELINE
replace_pipeline.push(
    {'$merge': {'into': { 'db': 'testdata', 'coll': 'payments'}, 'on': '_id',  'whenMatched': 'replace', 'whenNotMatched': 'fail'}}
);
db.payments.aggregate(replace_pipeline);
db.payments.find();
```

 &nbsp;_NOTE_: Ensure that no other processes are inserting, updating or deleting records in the `persons` collection whilst the masking aggregation pipeline is running.

