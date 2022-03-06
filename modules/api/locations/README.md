# UdaConnect Locations Service

UdaConnect Locations GRPC service:

## Sample Client Calls:

Retrieve all locations:

```
stub = location_pb2_grpc.LocationServiceStub(channel)
stub.Get(location_pb2.Empty())
```

Retrieve location by location_id:

```
stub = location_pb2_grpc.LocationServiceStub(channel)
stub.GetLocation(location_pb2.GetLocationRequest(id=<location_id>))
```

Retrieve location by person_id and date range:

```
stub = location_pb2_grpc.LocationServiceStub(channel)
stub.GetLocationRange(
        location_pb2.GetLocationRangeRequest(
            person_id=<person_id>, start_date="YYYY-MM-DD", end_date="YYYY-MM-DD"
        )
    )
```

Create location:

```
stub = location_pb2_grpc.LocationServiceStub(channel)
stub.Create(
        location_pb2.CreateLocationRequest(
            person_id=<person_id>,
            longitude="<longi.tude>",
            latitude="<lati.tude",
            creation_time="<creation_timestamp>",
        )
    )
```

## Proto file

The proto file for the locations service is located within ```protos/location.proto```

To generate new protocol buffers execute the below from within the root of the locations directory:

```$ python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=./ protos/locations.proto```

## Run Tests (Yes I wrote a few tests :P)

To run tests start the locations serverlet and run pytest:

```
$ python main.py
$ pytest
```


## Installation

Local:

```
pip install -r requirements.txt
```

Docker:


