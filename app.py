import os
from time import sleep
import psutil
from prettytable import PrettyTable
from prettytable import DOUBLE_BORDER
import platform
import subprocess
import argparse

# Units of memory sizes
size = ["bytes", "KB", "MB", "GB", "TB"]
command = ""

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description="System Monitor Tool - Monitors CPU, Memory, Network stats, and Ping.",
    epilog="Examples:\n"
    "  python app.py --ping-host 8.8.8.8 --ping-count '5' --interval 5\n"
    "  python app.py --ping-host example.com --interval 10",
    formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument(
    "--ping-host",
    default="8.8.8.8",
    help="Host to ping for latency testing (default: 8.8.8.8)",
)
parser.add_argument(
    "--ping-count",
    type=int,
    default=3,
    help="Number of times to ping the host (default: 3)",
)
parser.add_argument(
    "--interval", type=int, default=3, help="Update interval in seconds (default: 3)"
)
parser.add_argument(
    "--stop",
    type=int,
    default=0,
    help="Number of times to run the app to run the app (default: 0)- Optional",
)
args = parser.parse_args()

ping_host = args.ping_host
ping_count = str(args.ping_count)
interval = int(args.interval)
stop = args.stop


def check_platform(os_name):
    print(f"\nOperating System: {os_name}")
    if os_name == "Windows":
        command = "cls"
        print("Running on Windows")
    elif os_name == "Linux":
        print("Running on Linux")
        command = "clear"
    elif os_name == "Darwin":
        print("Running on macOS")
        command = "clear"
    else:
        print("Unknown Operating System")
        raise Exception("Unknow operating System")


# display cpu and memeory usage
def display_usage(cpu_usage, mem_usage, bars=25):
    cpu_percent = cpu_usage / 100.0
    cpu_bar = "*" * int(cpu_percent * bars) + "-" * (bars - int(cpu_percent * bars))
    mem_percent = mem_usage / 100.0
    mem_bar = "*" * int(mem_percent * bars) + "-" * (bars - int(mem_percent * bars))

    # Create PrettyTable for CPU and Memory Usage
    usage_table = PrettyTable()
    usage_table.field_names = ["Metric", "Usage"]
    usage_table.add_row(["CPU Usage", f"|{cpu_bar}| {cpu_usage:.2f}%"])
    usage_table.add_row(["Memory Usage", f"|{mem_bar}| {mem_usage:.2f}%"])
    print(usage_table)


# Function that returns bytes in a readable format
def getSize(bytes):
    for unit in size:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024


# Prints the Data on the Terminal or Console
def display_network_stats():
    # Getting the network i/o stats again to
    # count the sending and receiving speed
    netStats2 = psutil.net_io_counters()

    # Upload/Sending speed
    uploadStat = netStats2.bytes_sent - dataSent
    # Receiving/Download Speed
    downloadStat = netStats2.bytes_recv - dataRecv

    # Creating an instance of PrettyTable class
    card = PrettyTable()
    card.set_style(DOUBLE_BORDER)
    # Column Names of the table
    card.field_names = ["Received", "Receiving", "Sent", "Sending"]
    # Adding row to the table
    card.add_row(
        [
            f"{getSize(netStats2.bytes_recv)}",
            f"{getSize(downloadStat)}/s",
            f"{getSize(netStats2.bytes_sent)}",
            f"{getSize(uploadStat)}/s",
        ]
    )
    print(f"Network stats\n{card}", end="")


# Display latency and packet loss
def display_ping_stats(
    ping_amount,
    host="8.8.8.8",
):
    try:
        # Ping the host
        if platform.system() == "Windows":
            result = subprocess.run(
                ["ping", host, "-n", ping_amount], capture_output=True, text=True
            )
        else:
            result = subprocess.run(
                ["ping", host, "-c", "3"], capture_output=True, text=True
            )

        # Extract latency and packet loss from the ping output
        output = result.stdout
        latency = "N/A"
        packet_loss = "N/A"

        if "Packets:" in output:
            latency = output.split("Packets:")[1].split("(0% loss),")[0]

        if "Lost = " in output:
            packet_loss = output.split("Lost = ")[1].split(",")[0]

        # Create PrettyTable for Ping stats
        ping_table = PrettyTable()
        ping_table.field_names = ["Latency", "Packet Loss"]
        ping_table.add_row([f"{latency}", packet_loss])
        print(f"\nPing stats\n{ping_table}")

    except Exception as e:
        print(f"\nError getting ping stats: {e}")


# psutil.net_io_counters() returns network I/O statistics as a namedtuple
netStats1 = psutil.net_io_counters()

# Getting the data of total bytes sent and received
dataSent = netStats1.bytes_sent
dataRecv = netStats1.bytes_recv


def update_stats():
    os.system(command)
    check_platform(platform.system())
    display_usage(psutil.cpu_percent(), psutil.virtual_memory().percent)
    display_network_stats()
    display_ping_stats(ping_count, host=ping_host)


if stop > 0:
    while stop != 0:
        sleep(interval)
        update_stats()
        stop -= 1
else:
    while True:
        sleep(interval)
        update_stats()
