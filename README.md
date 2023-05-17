# mta_proxy

Sample request testing with `curl`:
```bash
$ curl -X POST 127.0.0.1:8090 -d '{
  "api_key": "YOUR_API_KEY",
  "route_ids": ["F", "G"],
  "station_ids": ["F23N"],
  "directions": ["N"]
}'
```

Sample response:

```
[
  {
    "route_id": "G",
    "arrival_time": "2023-05-03T00:56:30",
    "arrival_delta_mins": 5,
    "directions": "N",
    "extra": "Northbound G to Court Sq, departed origin 00:49:30, Currently STOPPED_AT Church Av, last update at 00:49:30"
  },
  {
    "route_id": "F",
    "arrival_time": "2023-05-03T01:05:42",
    "arrival_delta_mins": 15,
    "directions": "N",
    "extra": "Northbound F to Jamaica-179 St, departed origin 00:41:30, Currently STOPPED_AT Avenue P, last update at 00:50:27"
  },
  {
    "route_id": "G",
    "arrival_time": "2023-05-03T01:11:00",
    "arrival_delta_mins": 20,
    "directions": "N",
    "extra": "Northbound G to Court Sq, departs origin 01:04:00"
  },
  {
    "route_id": "F",
    "arrival_time": "2023-05-03T01:27:00",
    "arrival_delta_mins": 36,
    "directions": "N",
    "extra": "Northbound F to Jamaica-179 St, departs origin 01:01:30"
  },
  {
    "route_id": "G",
    "arrival_time": "2023-05-03T01:31:00",
    "arrival_delta_mins": 40,
    "directions": "N",
    "extra": "Northbound G to Court Sq, departs origin 01:24:00"
  }
]
```
