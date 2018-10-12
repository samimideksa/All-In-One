from nets import AllInOneNetwork
from dataset.celeba import CelebAAlignedDataset
from dataset.imdb_wiki import ImdbWikiDataset
from util import get_cmd_args
from util import get_config
import os

INPUT_SIZE = (227,227,1)

def main():
    args = get_cmd_args()
    if not os.path.exists(args.images_path):
        print ("image path given does not exists")
        exit(0)
    if not args.dataset.lower() in ["wiki","imdb", "celeba","aflw", "adience"]:
        print ("currently implemented for only wiki, imdb, aflw, celeba and adience datasets")
        exit(0)
    config = get_config(args)
    net = AllInOneNetwork(config)
    net.train()

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello again sami, %s!' % request.name)    

    def Greetings(self, request, context):
        return helloworld_pb2.HelloReply(message='This is the last message I want to print, %s!' % request.name)


    def run():
        channel = grpc.insecure_channel('localhost:50051')
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)
        response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)

if __name__=="__main__":
    main()
