import grpc
from protos import location_pb2
from protos import location_pb2_grpc


from google.protobuf.json_format import MessageToDict

### Simple Client for testing location services ###

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)


def test_LocationServicer_Get():
    resp = stub.Get(location_pb2.Empty())
    assert resp.locations[0].id == 29


def test_LocationServicer_GetLocation():
    resp = stub.GetLocation(location_pb2.GetLocationRequest(id=9))
    assert resp.id == 9


def test_LocationServicer_GetLocationRange():
    resp = stub.GetLocationRange(
        location_pb2.GetLocationRangeRequest(
            person_id=5, start_date="2021-07-07", end_date="2021-07-08"
        )
    )
    assert resp.locations[0].id == 3


def test_LocationServicer_create():
    print("Creating location")
    """"
    resp = stub.Create(
        location_pb2.CreateLocationRequest(
            person_id=5,
            longitude="37.4363",
            latitude="-122.290843",
            creation_time="2021-07-07T10:37:06",
        )
    )
    assert resp.id == 5
    """
