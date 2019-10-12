from multiprocessing import Process
import ping_client

if __name__ == "__main__":
    COUNT = 10
    PROCESSES = {}
    for x in range(COUNT):
        PROCESSES[x] = Process(target=ping_client.run)

    for x in range(COUNT):
        PROCESSES[x].start()