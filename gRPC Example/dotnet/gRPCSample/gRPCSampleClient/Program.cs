using Grpc.Core;
using System;
using System.Collections.Generic;
using System.IO;

namespace gRPCSampleClient
{
    class Program
    {
        static void Main(string[] args)
        {
            Channel channel = new Channel("127.0.0.1:8080", ChannelCredentials.Insecure);

            // Ping example:
            var client = new PingPongService.PingPongServiceClient(channel);

            var reply = client.ping(new Ping { Count = 1 });

            Console.WriteLine($"Ping reply: {reply}");


            //// Images example:
            //var client = new ImageService.ImageServiceClient(channel);

            //var src_files = new List<string> {
            //    @"C:\Users\Reuven\Downloads\pic.jpg", @"C:\Users\Reuven\Downloads\pic2.jpg"
            //};

            //var request = new StreamBytes();

            //for (var i = 0; i < src_files.Count; i++) {
            //    using (var fs = new FileStream(src_files[i], FileMode.Open, FileAccess.Read))
            //    {
            //        request.Images.Add(new Image
            //        {
            //            Name = $"image {i + 1}",
            //            Data = Google.Protobuf.ByteString.FromStream(fs)
            //        });
            //    }
            //}

            //var reply = client.save(request);


            channel.ShutdownAsync().Wait();
            Console.WriteLine($"Reply: {reply.ToString()}");

            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}
