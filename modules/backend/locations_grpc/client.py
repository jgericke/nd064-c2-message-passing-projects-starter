import grpc
import location_pb2
import location_pb2_grpc


print("Retreiving all locations...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

resp = stub.Get(location_pb2.Empty())
# resp = stub.GetLocation(location_pb2.GetLocationRequest(id=99999))
"""
resp = stub.Create(
    location_pb2.CreateLocationRequest(
        person_id=5,
        longitude="37.4363",
        latitude="-122.290843",
        creation_time="2021-07-07T10:37:06",
    )

"""
resp = stub.GetLocationRange(
    location_pb2.GetLocationRangeRequest(
        person_id=5, start_date="2021-07-07", end_date="2021-07-08"
    )
)
print(resp)
