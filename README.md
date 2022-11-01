# pingcheck

## Usage

```shell
poetry install
poetry run sudo python pingcheck.py
```

```shell
Usage: pingcheck.py [OPTIONS]

  This script periodically pings desired addresses and reports failure to
  .json file as traceroute result or exception description.

Options:
  -f, --frequency INTEGER         Frequency in seconds.  [default: 20]
  -a, --addresses TEXT            Addresses to ping.  [default: google-public-
                                  dns-b.google.com, google.com, 1.1.1.1,
                                  wp.pl, onet.pl, 208.67.222.222,
                                  208.67.220.220, 1.0.0.1]
  -da, --diagnostic-addresses TEXT
                                  Addresses to perform diagnostic traceroute
                                  on.  [default: 1.1.1.1, 208.67.222.222,
                                  208.67.220.220, 1.0.0.1]
  -r, --retries INTEGER           Ping retries count on failure.  [default: 3]
  --help                          Show this message and exit.
```
