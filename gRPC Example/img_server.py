from concurrent import futures
import threading
import time
import grpc
import image_pb2, image_pb2_grpc
from PIL import Image
import io


class Listener(image_pb2_grpc.ImageServiceServicer):
    """The listener function implemests the rpc call as described in the .proto file"""

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__

    def save(self, request, context):
        for img in request.Images:
            print('Show image:', img.name)
            image = Image.open(io.BytesIO(img.data))
            image.show()
            del image

        return image_pb2.EmptyResponse()


def serve():
    """The main serve function of the server.
    This opens the socket, and listens for incoming grpc conformant packets"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    image_pb2_grpc.add_ImageServiceServicer_to_server(Listener(), server)
    server.add_insecure_port("[::]:9999")
    server.start()
    try:
        while True:
            print("Server Running : threadcount %i" % (threading.active_count()))
            time.sleep(10)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        server.stop(0)


if __name__ == "__main__":
    serve()
