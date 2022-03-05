import grpc
import location_pb2
import location_pb2_grpc


print("Retreiving all locations...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

resp = stub.Get(location_pb2.Empty())

print(resp)
