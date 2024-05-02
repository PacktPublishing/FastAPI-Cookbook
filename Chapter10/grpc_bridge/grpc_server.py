import asyncio
import logging

import grpc

from grpcserver_pb2 import MessageResponse
from grpcserver_pb2_grpc import (
    GrpcServerServicer,
    add_GrpcServerServicer_to_server,
)


class Service(GrpcServerServicer):
    async def GetServerResponse(
        self, request, context
    ):
        message = request.message
        logging.info(f"Received message: {message}")
        result = (
            f"Hello I am up and running received: {message}"
        )
        result = {
            "message": result,
            "received": True,
        }
        return MessageResponse(**result)


async def serve():
    server = grpc.aio.server()
    add_GrpcServerServicer_to_server(
        Service(), server
    )
    server.add_insecure_port("[::]:50051")
    logging.info("Starting server on port 50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
