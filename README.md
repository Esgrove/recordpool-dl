# Recordpool Downloader

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

### Implementation

`RecordPoolDownloader` contains main and runs the download with a common interface for all recordpools.  
`RecordPool` is an abstract (aka virtual) base class that provides the common interface, which is inherited by all recordpool-specific classes.  
`Bandcamp, Beatjunkies, BPMSupreme, DJCity` are subclasses of `RecordPool` that implement the common functions,
like *get_tracks* and *download_track* for the specific website (if and when a custom implementation is required for each function).
