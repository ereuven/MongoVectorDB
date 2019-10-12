using Grpc.Core;
using System;

namespace gRPCSampleServer
{
    class Program
    {
        const string Host = "localhost";
        const int Port = 8080;

        public static void Main(string[] args)
        {
            // Build server
            var server = new Server
            {
                Services = { PingPongService.BindService(new PingPongServiceImpl()) },
                Ports = { new ServerPort(Host, Port, ServerCredentials.Insecure) }
            };
            
            // Start server
            server.Start();

            Console.WriteLine("Ping Pong server listening on port " + Port);
            Console.WriteLine("Press any key to stop the server...");
            Console.ReadKey();

            server.ShutdownAsync().Wait();
        }
    }
}
