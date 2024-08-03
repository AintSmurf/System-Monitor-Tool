# System Monitor Tool

## Overview
The System Monitor Tool is a Python-based utility designed to monitor and display real-time system metrics. It provides insights into CPU and memory usage, network statistics, ping latency to a specified host. This tool supports multiple operating systems, including Windows, macOS, and Linux.

# Table of Contents
* [Features](#Features)
* [Requirements](#Requirements)
* [Usage](#Usage)
* [Command-Line Options](#Options)
* [How It Works](#HowItWorks)

# Features
* CPU and Memory Usage: Displays real-time CPU and memory usage with visual progress bars.
* Network Statistics: Shows the amount of data sent and received, as well as upload and download speeds.
* Ping Latency: Measures and displays the latency and packet loss for a specified host.
* Cross-Platform: Compatible with Windows, macOS, and Linux.

# Requirements
* Python 3.x
* psutil library
* prettytable library

You can install the required libraries using pip:
```bash
pip install psutil prettytable
```
# Usage
Run the tool with default settings:
```bash
python app.py [OPTIONS]
```
Ping 8.8.8.8 5 times, updating every 10 seconds, and run for 10 cycles:
```bash
python app.py --ping-host 8.8.8.8 --ping-count 5 --interval 10 --stop 10
```
# Options
* --ping-host
    * **Description:** Host to ping for latency testing.
    * **Default**: 8.8.8.8
    * **Type**: str
* --ping-count
    * **Description:** Number of times to ping the host
    * **Default**: 3
    * **Type**: int
* --interval
    * **Description:** Update interval in seconds.
    * **Default**: 3
    * **Type**: int
* --stop
    * **Description:** Number of times to run the app. If set to 0, the tool runs indefinitely (i.e., forever).
    * **Default**: 0 
    * **Type**: int

# HowItWorks

1) ***CPU and Memory Usage***: The tool measures CPU and memory usage using the 'psutil' library and displays it in a bar chart format using 'PrettyTable'.
2) ***Network Statistics***: It calculates network statistics such as upload and download speeds using 'psutil' and displays them in a formatted table.
3) ***Ping Latency***: The tool pings the specified host and extracts latency and packet loss information, then displays it in a table format.
4) ***Cross-Platform Support***: It detects the operating system and clears the terminal screen accordingly before displaying updated statistics.
