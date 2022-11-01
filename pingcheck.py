#!/usr/bin/python
import datetime
import subprocess
import time
from itertools import cycle

import click
import jsonpickle
from icmplib import ping
from loguru import logger

DEFAULT_FREQUENCY = 20

DEFAULT_ADDRESSES = [
    'google-public-dns-b.google.com',
    'google.com',
    '1.1.1.1',
    'wp.pl',
    'onet.pl',
    '208.67.222.222',
    '208.67.220.220',
    '1.0.0.1',
]

DEFAULT_TRACEROUTE_ADDRESSES = [
    '1.1.1.1',
    '208.67.222.222',
    '208.67.220.220',
    '1.0.0.1',
]

DEFAULT_RETRIES = 3


@click.command()
@click.option('--frequency', '-f', default=DEFAULT_FREQUENCY, help='Frequency in seconds.', show_default=True)
@click.option('--addresses', '-a', default=DEFAULT_ADDRESSES, help='Addresses to ping.', multiple=True,
              show_default=True)
@click.option('--diagnostic-addresses', '-da', default=DEFAULT_TRACEROUTE_ADDRESSES, help='Addresses to perform '
                                                                                          'diagnostic traceroute '
                                                                                          'on.', multiple=True,
              show_default=True)
@click.option('--retries', '-r', default=DEFAULT_RETRIES, help='Ping retries count on failure.', show_default=True)
def pingcheck(frequency, addresses, diagnostic_addresses, retries):
    """This script periodically pings desired addresses and
    reports failure to .json file as traceroute result or exception description."""

    logger.info(f"Started pinging every {frequency} seconds")
    logger.info(f"Ping addresses = {addresses}")
    logger.info(f"Diagnostic addresses = {diagnostic_addresses}")
    logger.info(f"Max ping retries = {retries}")

    hosts_cycle = cycle(addresses)
    traceroute_hosts_cycle = cycle(diagnostic_addresses)

    while True:
        ping_was_successful = False
        fallbacks_performed = 0

        while (not ping_was_successful) and fallbacks_performed <= retries:
            next_ping_address = next(hosts_cycle)
            try:
                logger.info(f"Sending ping to {next_ping_address}")
                ping_result = ping(next_ping_address, count=1, timeout=5)
                ping_was_successful = ping_result.is_alive
            except Exception as e:
                logger.warning(e)
                ping_was_successful = False
            fallbacks_performed = fallbacks_performed + 1

        if not ping_was_successful:
            file_name = f"{datetime.datetime.today().isoformat()}.json"
            diagnostic_address = next(traceroute_hosts_cycle)
            logger.warning(f"Network outage detected! Performing treceroute to {diagnostic_address}")
            try:
                traceroute_result = subprocess.Popen(["traceroute", diagnostic_address],stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                message_to_write = jsonpickle.encode({
                    "traceroute": traceroute_result.communicate()[0],
                    "error": traceroute_result.communicate()[1]
                }, indent=4)
            except Exception as e:
                logger.warning(e)
                message_to_write = jsonpickle.encode({
                    "reason": str(e)
                }, indent=4)
            with open(file_name, 'w', encoding='utf-8') as f:
                logger.warning(f"Dumping reason to {file_name}")
                f.write(message_to_write)
        else:
            logger.info(f"Ping successful")

        logger.info(f"Waiting {frequency} seconds...")
        time.sleep(frequency)


if __name__ == '__main__':
    pingcheck()
