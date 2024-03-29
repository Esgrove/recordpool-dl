# Recordpool Downloader

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

:warning: **NOTE (06/2023):** I am no longer actively maintaining this since DJCity updated their site to work much better.
I made this tool for own use and do not offer any support or help for others to run it.
I only use it for Bandcamp currently, the pool interactions are likely outdated...

A command-line tool for automatically downloading music tracks from DJ [recordpool](https://en.wikipedia.org/wiki/Music_pool) websites.
Implemented with Python 3 using [Selenium](https://www.seleniumhq.org/) for interacting with the websites.
I use Chromedriver but other browsers could be used as well.

Supported pools:

- [DJCity](https://www.djcity.com/)
- [Beatjunkies](https://www.beatjunkies.com/record-pool/)
- [BPMSupreme](https://www.bpmsupreme.com/)

In addition, there's also an option for [Bandcamp](https://bandcamp.com/) to download all tracks / releases after a purchase,
though this could be implemented in a nicer way, as now it is just hacked on top of the recordpool base class.

## Motivation

Previewing and manually downloading new songs from record pools can be quite slow and frustrating.
The song preview streams load slowly and are typically low bitrate.
Similarly, launching downloads can be very slow on some record pools.
The end result is that it takes a lot of time every week to sift through new songs added to the record pools.

Therefore, I made a tool for myself to automatically download all (desired) tracks from various recordpool services I have / had subscriptions for.
After auto-downloading, I can then go through and sort the files much faster directly from my DJ software(s) and in Finder/Explorer,
and just delete all the tracks I don't like.

## Implementation

- `RecordPoolDownloader` contains main and runs the download with a common interface for all recordpools.
- `RecordPool` is an abstract (aka virtual) base class that provides the common interface, which is inherited by all recordpool-specific classes.
- `Bandcamp`, `Beatjunkies`, `BPMSupreme`, `DJCity` are subclasses of `RecordPool` that implement the common functions,
  like *get_tracks* and *download_track* for the specific website (if and when a custom implementation is required for each function).

It is arguably a bit over-engineered,
but since this project doubled as a learning opportunity for Selenium and web automation for me,
I would say over-engineering is to be expected :bowtie:

## Todo

- Proper CLI argument handling using argparse, Click or Typer.
- Improve Bandcamp downloads
