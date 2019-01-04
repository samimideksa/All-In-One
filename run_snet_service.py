import pathlib
import subprocess
import signal
import time
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(prog="run-snet-service")
    parser.add_argument("--daemon-config-path", help="Path to daemon configuration file", required=True)
    args = parser.parse_args(sys.argv[1:])

    def handle_signal(signum, frame):
        snetd_p.send_signal(signum)
        service_p.send_signal(signum)
        snetd_p.wait()
        service_p.wait()
        exit(0)

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    root_path = pathlib.Path(__file__).absolute().parent.parent
    snetd_p = start_snetd(root_path, args.daemon_config_path)
    service_p = start_service(root_path)

    while True:
        if snetd_p.poll() is not None:
            snetd_p = start_snetd(root_path, args.daemon_config_path)
        if service_p.poll() is not None:
            service_p = start_service(root_path)
        time.sleep(5)


def start_snetd(cwd, daemon_config_path=None):
    cmd = ["./snetd-linux-amd64"]
    if daemon_config_path is not None:
        cmd.extend(["--config", daemon_config_path])
    return subprocess.Popen(cmd)


def start_service(cwd):
    return subprocess.Popen(["python3.6", "script.py"])


if __name__ == "__main__":
    main()