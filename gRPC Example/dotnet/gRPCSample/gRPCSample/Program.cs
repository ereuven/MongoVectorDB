using System;

namespace gRPCSample
{
    class Program
    {
        /*
         * https://docs.microsoft.com/en-us/aspnet/core/tutorials/grpc/grpc-start?view=aspnetcore-3.0&tabs=visual-studio
         * generated cs files: gRPC Example\dotnet\gRPCSample\gRPCSample\obj\Debug\netcoreapp2.1
         * 
         * Nuget packages:
         *  Grpc
         *  Grpc.Tools
         *  Google.Protobuf
         *  
         *  Add to csproj:
              <ItemGroup>
                <Protobuf Include="proto\*.proto" GrpcServices="Client" />
              </ItemGroup>
         */

        /*
         protoc.exe --proto_path=protos --grpc_out=protos --csharp_out=protos --csharp_opt=file_extension=.g.cs Accounts.proto --plugin=protoc-gen-grpc=C:\Users\Nikhil\.nuget\packages\grpc.tools\1.19.0\tools\windows_x64\grpc_csharp_plugin.exe
        */

        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
        }
    }
}
