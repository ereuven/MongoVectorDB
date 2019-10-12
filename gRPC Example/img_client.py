import grpc
import image_pb2, image_pb2_grpc

sb = image_pb2.StreamBytes()
for i, fpath in enumerate([r"C:\Users\Reuven\Downloads\pic.jpg", r"C:\Users\Reuven\Downloads\pic2.jpg"]):
    img = sb.Images.add()
    img.name = 'img_{}'.format(i)

    in_file = open(fpath, "rb")
    img.data = in_file.read()
    in_file.close()

channel = grpc.insecure_channel('localhost:9999')
stub = image_pb2_grpc.ImageServiceStub(channel)

response = stub.save(sb)

channel.unsubscribe(channel.close)

print('Response:', response)
