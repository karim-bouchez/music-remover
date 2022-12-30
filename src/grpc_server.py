import static_ffmpeg
static_ffmpeg.add_paths()

from time import sleep
import json
import grpc
from concurrent import futures
import moubah_pb2
import moubah_pb2_grpc

class MusicRemoverServicer(moubah_pb2_grpc.MusicRemoverServicer):
    def Ping(self, request, context):
        return moubah_pb2.GenericResponse(succeeded=True)

    def RemoveMusic(self, request, context):
        print(f"Get request for: {request.input_path}")
        # TODO: see if it's still true ⬇️
        # The import has to be local to avoid infinite loop on frozen app
        from src.libs.spleeter import Spleeter
        
        try:
            print(f"Remove music from: {request.input_path}")
            # sleep(3)
            # TODO: remove the WARNING logs from tensorflow
            Spleeter.remove_music(
                audio_path=request.input_path,
                output_path=request.output_path,
                remove_original=request.remove_original
            )
        except Exception as exc:
            return moubah_pb2.GenericResponse(succeeded=False, error=str(exc))
        else:
            return moubah_pb2.GenericResponse(succeeded=True)


def serve():
    # Spleeter's libs are imported here, before running the gRPC server because it takes time to load
    print("Importing libraries...")
    from src.libs.spleeter import Spleeter
    print("Libraries imported!")
    
    with open("src/protobuf/config.json") as config_file:
        config = json.load(config_file)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    moubah_pb2_grpc.add_MusicRemoverServicer_to_server(MusicRemoverServicer(), server)
    # TODO: use specific port
    server.add_insecure_port(f"{config['url']}:{config['port']}")
    server.start()
    print("Server running...")
    server.wait_for_termination()
