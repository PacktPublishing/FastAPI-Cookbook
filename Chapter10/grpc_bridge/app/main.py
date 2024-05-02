import grpc
from fastapi import FastAPI
from pydantic import BaseModel

from grpcserver_pb2 import Message
from grpcserver_pb2_grpc import GrpcServerStub

app = FastAPI()


class GRPCResponse(BaseModel):
    message: str
    received: bool


grpc_channel = grpc.aio.insecure_channel(
    "localhost:50051"
)


@app.get("/grpc")
async def call_grpc(message: str) -> GRPCResponse:
    async with grpc_channel as channel:
        grpc_stub = GrpcServerStub(channel)
        response = await grpc_stub.GetServerResponse(
            Message(message=message)
        )
        return response
