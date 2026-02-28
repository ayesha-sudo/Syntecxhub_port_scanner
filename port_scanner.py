import socket
import threading
import logging
from concurrent.futures import ThreadPoolExecutor

# Logging configuration
logging.basicConfig(
    filename="scan_results.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

print_lock = threading.Lock()

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))

        with print_lock:
            if result == 0:
                message = f"[OPEN] Port {port}"
            else:
                message = f"[CLOSED] Port {port}"

            print(message)
            logging.info(message)

        sock.close()

    except socket.timeout:
        logging.warning(f"[TIMEOUT] Port {port}")
    except Exception as e:
        logging.error(f"Error scanning port {port}: {e}")

def main():
    host = input("Enter host (e.g. 127.0.0.1): ")
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    print(f"\nScanning {host} from port {start_port} to {end_port}...\n")

    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, host, port)

    print("\nScan completed. Results saved in scan_results.txt")

if __name__ == "__main__":
    main()