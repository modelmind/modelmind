## Schema views

The `fs-bq-schema-views` script creates a BigQuery view based on a provided JSON schema configuration file. It queries the data from the `firestore-bigquery-export` extension changelog table to generate the view.

A guide on how to use the script can be found [here](https://github.com/firebase/extensions/blob/master/firestore-bigquery-export/guides/GENERATE_SCHEMA_VIEWS.md)

```bash
$ npx @firebaseextensions/fs-bq-schema-views \
  --non-interactive \
  --project=${param:PROJECT_ID} \
  --big-query-project=${param:BIGQUERY_PROJECT_ID} \
  --dataset=${param:DATASET_ID} \
  --table-name-prefix=${param:TABLE_ID} \
  --schema-files=./test_schema.json
```


## To solve

- Generate the schema given a `questionnaire_id` (based on questions answer type): OK

- Setup Cloud Function to generate the bigquery view given a json `schema` and `questionnaire_id`
    - Write temporary schema to a json file
    - Filter the schema view to only get results from `questionnaire_id`
