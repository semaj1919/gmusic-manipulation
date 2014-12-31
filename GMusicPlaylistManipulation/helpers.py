from common import GMusicKeys
from itertools import ifilter

class FilterHelper:
    @staticmethod
    def FilterByEqualToKey(list_to_filter, key, filter_value):
        return filter(lambda item: item.has_key(key) and item[key] == filter_value, list_to_filter)


class SongHelper:
    @staticmethod
    def SortByKey(songs_to_sort, key, reverse=False):
        return [song for song in sorted(songs_to_sort, key=lambda singleSong: singleSong[key], reverse=reverse)]

    @staticmethod
    def SortByPlaycount(songs_to_sort, reverse=False):
        return SongHelper.SortByKey(songs_to_sort, GMusicKeys.SongKeys.playCountKey, reverse)

    @staticmethod
    def FilterByPlaycount(songs_to_filter, minimum_playcount=1):
        return ifilter(lambda track: track.has_key(GMusicKeys.SongKeys.playCountKey) and track[GMusicKeys.SongKeys.playCountKey] >= minimum_playcount, songs_to_filter)

    @staticmethod
    def FilterByTitle(songs_to_filter, song_title):
        matched_song = FilterHelper.FilterByEqualToKey(songs_to_filter, GMusicKeys.SongKeys.TitleKey, song_title)   #(lambda song: song.has_key(GMusicKeys.SongKeys.TitleKey) and song[GMusicKeys.SongKeys.TitleKey] == song_title, songs_to_filter)
        return matched_song[0]

    @staticmethod
    def GetSongIds(songs):
        return [song[GMusicKeys.SongKeys.SongIdKey] for song in songs]

    @staticmethod
    def GetSongIdsFromTracks(tracks):
        return [track[GMusicKeys.TrackKeys.TrackIdKey] for track in tracks]

    @staticmethod
    def get_song_timestamp(song):
        return song[GMusicKeys.SongKeys.CreationTimestampKey]

    @staticmethod
    def get_song_name(song):
        return song[GMusicKeys.SongKeys.TitleKey].encode('ascii','ignore')

    @staticmethod
    def get_song_from_track(track, songs):
        song_id = track[GMusicKeys.TrackKeys.TrackIdKey]
        return next((song for song in songs if song[GMusicKeys.SongKeys.SongIdKey] == song_id), None)

    @staticmethod
    def GetSongAlbumArtUrl(song):
        albumArtRef = song[GMusicKeys.SongKeys.AlbumArtRefKey]
        return albumArtRef[0][GMusicKeys.SongKeys.AlbumArtUrlKey]

class PlaylistHelper:
    @staticmethod
    def FilterByName(playlists_to_filter, name):
        matched_playlist = FilterHelper.FilterByEqualToKey(playlists_to_filter, GMusicKeys.PlaylistKeys.NameKey, name)
        return matched_playlist[0]

    @staticmethod
    def GetTracks(playlist):
        return playlist[GMusicKeys.PlaylistKeys.TracksKey]

class StorageHelper:
    tracks = []
    playlists = []
    songs = []