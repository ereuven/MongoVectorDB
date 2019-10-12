using System;
using System.Threading.Tasks;
using Grpc.Core;

namespace gRPCSampleServer
{
    class PingPongServiceImpl : PingPongService.PingPongServiceBase
    {
        public override Task<Pong> ping(Ping request, ServerCallContext context)
        {
            Console.WriteLine($"{DateTime.Now.ToString("dd/MM/yyyy HH:mm:ss")} {context.Peer} {context.Host} {context.Method}{Environment.NewLine}{request}");
            Console.WriteLine(request);

            return Task.FromResult<Pong>(new Pong
            {
                Count = request.Count + 1
            });
        }
    }
}
