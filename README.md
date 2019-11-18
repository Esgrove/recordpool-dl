# Recordpool Downloader

A command-line tool for automatically downloading music tracks from DJ [recordpool](https://en.wikipedia.org/wiki/Music_pool) websites. Implemented with Python 3 using [Selenium](https://www.seleniumhq.org/) for interacting with the websites. I use Chromedriver but other browsers could be used as well.

Previewing and manually downloading songs from recordpools can be quite slow and frustrating. The song preview streams load slowly and are commonly low bitrate. Similarly launching donwloads is very slow on some recordpools. The end result is that it takes a lot of time every week to sift through new songs added to the recordpools. Therefore, I made a tool for myself to automatically download all (desired) tracks from various recordpool services I have subscriptions for. I can then go through and sort the files much faster directly from my DJ software(s) and in Finder/Explorer, and just delete all the tracks I don't like. 

Supported pools:
- [DJCity](https://www.djcity.com/)
- [Beatjunkies](https://www.beatjunkies.com/record-pool/)
- [BPMSupreme](https://www.bpmsupreme.com/)

In addition, there's also an option for [Bandcamp](https://bandcamp.com/) to easily download all tracks / releases after a purchase.
