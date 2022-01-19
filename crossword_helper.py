import random 

class CrossWordSolved:
    def __init__(self, sol_g, across, down, not_included, matrix):
        self.sol_g = sol_g
        self.across = across 
        self.down = down 
        self.not_included = not_included
        self.matrix = matrix


class SpotifySong:
    def __init__(self, json):
        self.name = json['name'].split("(")[0].split("-")[0].strip()
        self.artist = json['artists'][0]['name']
        self.duration = int(json['duration_ms'] / 1000)  
        self.total_tracks = json['album']['total_tracks'] 
        self.release_date = json['album']['release_date']
        self.album_name = json['album']['name']
        self.popularity = json['popularity']

    def __str__(self):
        start = "{name} is a {duration} second song by {artist}.".format(name=self.name, artist=self.artist, duration=self.duration)
        if self.total_tracks > 1: 
            middle = "Released on {release_date}, it is part of a {total_tracks} track album called {album_name} and is currently {popularity} on the Spotify charts.".format(release_date=self.release_date, total_tracks=self.total_tracks, album_name=self.album_name, popularity=self.popularity)
        else: 
            middle = "Released on {release_date}, it is {popularity} on the Spotify charts as a single.".format(release_date=self.release_date, total_tracks=self.total_tracks, album_name=self.album_name, popularity=self.popularity)

        return start + middle

    def song_name(self): 
        return self.name.upper()

    def artist_name(self):
        return self.artist.upper()

    def get_song_clue(self): 
        clue_1 = "A {duration} second song by {artist}.".format(artist=self.artist, duration=self.duration)
        clue_2 = "Song by {artist} released on {release_date}.".format(artist=self.artist, release_date=self.release_date)
        if self.total_tracks > 1: 
            clue_3 = "Part of a {total_tracks} track album called {album_name}.".format(total_tracks=self.total_tracks, album_name=self.album_name)
        else: 
            clue_3 = "A single by {artist} that is currently {popularity} on Spotify.".format(artist=self.artist, popularity=self.popularity)
        return random.choice([clue_1, clue_2, clue_3])

    def get_artist_clue(self): 
        clue_1 = "This band wrote {name}.".format(song_name=self.name)
        clue_2 = "This band wrote this song {name} released on {release_date}.".format(song_name=self.name, release_date=self.release_date)
        return random.choice([clue_1, clue_2])

def get_song_to_artist(songs): 
    song_to_artist = {}
    for song in songs: 
        s = SpotifySong(song)
        print(s.get_song_clue())
        song_to_artist[s.song_name()] = s 
    return song_to_artist