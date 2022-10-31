#!/usr/bin/python
from icmplib import ping, traceroute
from itertools import cycle
import signal
import sys
import json
import time
import jsonpickle
import datetime

SECONDS_TO_SLEEP = 20

HOSTS = [
    'google-public-dns-a.google.com',
    'google-public-dns-b.google.com',
    'google.com',
    '1.1.1.1',
    'wp.pl'
]

running = True
network_is_broken = False


def signal_handler(sig, frame):
    print('Program finished')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def run_service():
    print(f"Started pinging every {SECONDS_TO_SLEEP} seconds")
    print(f"HOSTS = {HOSTS}")

    global network_is_broken
    global running
    hosts_cycle = cycle(HOSTS)

    while running:
        next_ping_address = next(hosts_cycle)
        print(f"Sending ping to {next_ping_address}")
        ping_result = ping(next_ping_address, privileged=False)

        try:
            if ping_result.packets_sent != ping_result.packets_received:
                file_name = f"{datetime.datetime.today().isoformat()}.json"
                traceroute_address = next(hosts_cycle)
                print(f"Network outage detected! Performing treceroute to {traceroute_address}")
                network_is_broken = True
                traceroute_result = traceroute(traceroute_address, count=1)
                print(f"Dumping traceroute to {traceroute_address} to file {file_name}")
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(jsonpickle.encode(traceroute_result, f, indent=4))
            else:
                print("Ping successful")
                network_is_broken = False

            time.sleep(SECONDS_TO_SLEEP)
        except Exception as e:
            print("Exception!")
            print(e)


run_service()
