from RecordPool import RecordPool


class Beatjunkies(RecordPool):
    def __init__(self):
        super().__init__(self.__class__.__name__, "BEATJUNKIES")
        self.url = "https://www.beatjunkies.com/record-pool/page/1/"

    def get_tracks(self, number=0) -> list:
        tracks = []
        playlist = self.driver.find_element_by_css_selector(
            ".widget.widget-beats.playlist"
        )
        songs = playlist.find_elements_by_css_selector(
            ".glyphicon.glyphicon-arrow-down.icon-right.inline-exclude"
        )
        num = min(number, len(songs)) if number > 0 else len(songs)
        for song in songs[:num]:
            url = song.get_attribute("href")
            if url:
                tracks.append(url)

        return tracks

    def next_page(self):
        self.current_num += 1

        if self.driver.current_url != self.current_url:
            self.driver.get(self.current_url)

        link = self.driver.find_elements_by_class_name("nextpostslink")
        if not link:
            return False

        link[0].click()

        self.current_url = self.driver.current_url
        return True
