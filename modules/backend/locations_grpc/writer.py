import grpc
import location_pb2
import location_pb2_grpc


print("Sending sample location...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

location = location_pb2.LocationMessage(
    person_id=5,
    longitude="42.4363",
    latitude="12.3",
    creation_time="2021-07-07T10:40:00",
)


response = stub.Create(location)
