@echo off
@rem see: https://github.com/meteatamel/grpc-samples-dotnet/blob/master/dotnet_desktop/generate_protos.bat

setlocal

@rem enter this directory
cd /d %~dp0

set TOOLS_PATH=..\packages\Grpc.Tools.2.24.0\tools\windows_x64

%TOOLS_PATH%\protoc.exe proto\pingpong.proto --csharp_out protos_out --grpc_out protos_out --plugin=protoc-gen-grpc=%TOOLS_PATH%\grpc_csharp_plugin.exe
%TOOLS_PATH%\protoc.exe proto\image.proto --csharp_out protos_out --grpc_out protos_out --plugin=protoc-gen-grpc=%TOOLS_PATH%\grpc_csharp_plugin.exe


@rem %TOOLS_PATH%\protoc.exe proto\pingpong.proto --csharp_out protos_out
@rem %TOOLS_PATH%\protoc.exe proto\pingpong.proto --grpc_out protos_out --plugin=protoc-gen-grpc=%TOOLS_PATH%\grpc_csharp_plugin.exe

@rem %TOOLS_PATH%\protoc.exe proto\image.proto --csharp_out protos_out
@rem %TOOLS_PATH%\protoc.exe proto\image.proto --grpc_out protos_out --plugin=protoc-gen-grpc=%TOOLS_PATH%\grpc_csharp_plugin.exe

endlocal