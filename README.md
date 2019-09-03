# Recordpool Downloader

Command-line tool for automatically downloading music tracks from DJ [recordpool](https://en.wikipedia.org/wiki/Music_pool) websites.

Previewing and manually downloading songs from recordpools can be quite slow and frustrating. The song previews load slowly and are commonly low bitrate. Similarly launching donwloads are super slow for some recordpools. Therefore, I made a tool for myself to automatically download all tracks from various recordpools. I can then go through and sort the files much faster directly from my DJ-software and in finder/explorer, and just delete all the tracks I don't like. 

Implemented in Python. Uses [Selenium](https://www.seleniumhq.org/) for interacting with the websites. I use Chromedriver but other browsers could be used as well.

Supported pools:
- DJCity
- Beatjunkies
- BPMSupreme

In addition, there's also an option for Bandcamp to download all tracks / releases after a purchase.
