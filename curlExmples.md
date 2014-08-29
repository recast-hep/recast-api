*Some Examples of RECAST API using curl*


```
$ curl http://recast.perimeterinstitute.ca/api/recast-request
---
- 
    uuid: d3c7a30c-5062-3bd4-1dd9-7c716ef5e766
    title: 1111.0014
    requestor: itay.yavin.tester
    status: 2
- 
    uuid: f4b7e1aa-55bc-0e84-8560-3f6ee1a02032
    title: 1111.0003
    requestor: maxim
    status: 2
- 
    uuid: 2f0266ec-2754-dff4-a928-b64c6df5f352
    title: 1111.0012
    requestor: maxim
    status: 2
```

or

```
cranmer@Kyle-Cranmers-MacBook-Pro:~$ curl http://recast.perimeterinstitute.ca/api/recast-request.xml
<?xml version="1.0" encoding="utf-8"?>
<result is_array="true"><item><uuid>d3c7a30c-5062-3bd4-1dd9-7c716ef5e766</uuid><title>1111.0014</title><requestor>itay.yavin.tester</requestor><status>2</status></item><item><uuid>f4b7e1aa-55bc-0e84-8560-3f6ee1a02032</uuid><title>1111.0003</title><requestor>maxim</requestor><status>2</status></item><item><uuid>2f0266ec-2754-dff4-a928-b64c6df5f352</uuid><title>1111.0012</title><requestor>maxim</requestor><status>2</status></item></result>
```

or

```
cranmer@Kyle-Cranmers-MacBook-Pro:~$ curl http://recast.perimeterinstitute.ca/api/recast-request.json
[{"uuid":"d3c7a30c-5062-3bd4-1dd9-7c716ef5e766","title":"1111.0014","requestor":"itay.yavin.tester","status":"2"},{"uuid":"f4b7e1aa-55bc-0e84-8560-3f6ee1a02032","title":"1111.0003","requestor":"maxim","status":"2"},{"uuid":"2f0266ec-2754-dff4-a928-b64c6df5f352","title":"1111.0012","requestor":"maxim","status":"2"}]
```

and this

```
$ curl http://recast.perimeterinstitute.ca/api/recast-request/d3c7a30c-5062-3bd4-1dd9-7c716ef5e766 
---
- 
    uuid: d3c7a30c-5062-3bd4-1dd9-7c716ef5e766
    title: 1111.0014
    requestor: itay.yavin.tester
    status: 2
    analysis-uuid: 59e01b25-b80c-27c4-2536-faa9e90df9dc
    audience:
    subscribers: blaine
    predefined-model: mSugra
    new-model-information:
    reason-for-request: |
        Because my model is awesome
        test3b
    additional-information: Contact me for more awesome files and benchmarks
    model-type:
    parameter-points:
        parameter-0:
            point-name: x1:100, x2:200
            run-condition:
                - 
                    lhe-file: >
                        http://recast.perimeterinstitute.ca/sites/default/files/recast_request_run_conditions/1111.0014_parm_point1_run_condition1.zip
                    number-of-events: 1
                    reference-x-section: 10
        parameter-1:
            point-name: x1:101, x2:201
            run-condition:
                - 
                    lhe-file: >
                        http://recast.perimeterinstitute.ca/sites/default/files/recast_request_run_conditions/1111.0014_parm_point2_run_condition1.zip
                    number-of-events: 1
```
