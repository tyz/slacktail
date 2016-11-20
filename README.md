# Slacktail

Slacktail allows you to monitor a logfile and display any (optionally filtered)
new lines on [Slack](https://slack.com/). It's meant to make it easier to keep
an eye on a job you have running for example.

## Usage

```
usage: slacktail.py [-h] --url URL [--proxy URL] --file NAME [--wait SEC]
                    [--match REGEXP] [--imatch REGEXP] [--exit-match REGEXP]
                    [--truncate SIZE] [--verbose]

Tail a file and output to Slack

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     The Slack webhook URL
  --proxy URL, -p URL   Optional HTTP or SOCKS proxy to use
  --file NAME, -f NAME  The file to tail
  --wait SEC, -w SEC    Try to read new lines every SEC seconds (default: 60)
  --match REGEXP, -m REGEXP
                        Only output new lines when REGEXP matches
  --imatch REGEXP, -i REGEXP
                        Output all new lines except the ones which match REGEXP
  --exit-match REGEXP, -e REGEXP
                        Stop tailing the file when a new line matches REGEXP
  --truncate SIZE, -t SIZE
                        Limit the size of every message to SIZE bytes. The
                        oldest lines will be removed first. (default: 4096)
  --verbose, -v         Also output on stdout
```

## Examples

Output all new lines of ~/mylog to Slack, every minute. Messages are truncated to 4 kB.

```
slacktail --url https://hooks.slack.com/services/ABCDEF/12345/etcetcetc \
          --file ~/mylog
```

The same as above, but now for all lines which do not match DEBUG or INFO.

```
slacktail --url https://hooks.slack.com/services/ABCDEF/12345/etcetcetc \
          --file ~/mylog \
          --imatch '(DEBUG|INFO)'
```

The same as above, but now to the channel #foo. (The default channel/user is
defined during the configuration of the webhook in Slack)

```
slacktail --url https://hooks.slack.com/services/ABCDEF/12345/etcetcetc \
          --file ~/mylog \
          --imatch '(DEBUG|INFO)' \
          --channel '#foo'
```

The same as above, but now sent new lines every 30 minutes, and connect to
Slack through an HTTP proxy.

```
slacktail --url https://hooks.slack.com/services/ABCDEF/12345/etcetcetc \
          --file ~/mylog \
          --imatch '(DEBUG|INFO)' \
          --channel '#foo' \
          --wait 1600 \
	  --proxy http://proxy:3128/
```

## Webhooks

Setup your own webhook [in your Slack team](https://my.slack.com/services/new/incoming-webhook/)

## SOCKS proxy support

From the [python-requests documentation](http://docs.python-requests.org/en/master/user/advanced/):

New in python-requests version 2.10.0.

In addition to basic HTTP proxies, Requests also supports proxies using the
SOCKS protocol. This is an optional feature that requires that additional
third-party libraries be installed before use.

You can get the dependencies for this feature from pip:

```
$ pip install requests[socks]
```

Once you've installed those dependencies, using a SOCKS proxy is just as easy
as using an HTTP one:

```
--proxy 'socks5://user:pass@host:port'
```
