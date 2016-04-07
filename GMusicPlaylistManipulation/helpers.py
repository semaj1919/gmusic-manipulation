from common import GMusicKeys, ProgramVars, PrinterKeys
from itertools import ifilter
import xlsxwriter
import utils

class FilterHelper:
    @staticmethod
    def FilterByEqualToKey(list_to_filter, key, filter_value):
        return filter(lambda item: item.has_key(key) and item[key] == filter_value, list_to_filter)


class SongHelper:
    @staticmethod
    def SortByKeySafely(songs_to_sort, key, default, reverse=False):
        return [song for song in sorted(songs_to_sort, key=lambda singleSong: SongHelper.GetKeySafely(singleSong, key, default), reverse=reverse)]

    @staticmethod
    def GetKeySafely(song, key, default):
        if song.has_key(key):
            return song[key]
        else:
            return default

    @staticmethod
    def SortByKey(songs_to_sort, key, reverse=False):
        return [song for song in sorted(songs_to_sort, key=lambda singleSong: singleSong[key], reverse=reverse)]

    @staticmethod
    def SortByPlaycount(songs_to_sort, reverse=False):
        return SongHelper.SortByKey(songs_to_sort, GMusicKeys.SongKeys.PlayCountKey, reverse)

    @staticmethod
    def SortByCreationDate(songs_to_sort, reverse=False):
        return SongHelper.SortByKey(songs_to_sort, GMusicKeys.SongKeys.CreationTimestampKey, reverse)

    @staticmethod
    def SortByLastPlayedDate(songs_to_sort, reverse=False):
        return SongHelper.SortByKey(songs_to_sort, GMusicKeys.SongKeys.RecentTimestampKey, reverse)

    @staticmethod
    def SortByRating(songs_to_sort, reverse=False):
        return SongHelper.SortByKeySafely(songs_to_sort, GMusicKeys.SongKeys.RatingKey, 0, reverse)
        #return [song for song in sorted(songs_to_sort, key=lambda singleSong: SongHelper.GetSongRatingSafely(singleSong), reverse=reverse)]

    @staticmethod
    def FilterByPlaycount(songs_to_filter, minimum_playcount=1):
        return ifilter(lambda track: track.has_key(GMusicKeys.SongKeys.PlayCountKey) and track[GMusicKeys.SongKeys.PlayCountKey] >= minimum_playcount, songs_to_filter)

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
    def get_song_from_track(track, songs, api):
        song_id = track[GMusicKeys.TrackKeys.TrackIdKey]
        if str(song_id).startswith('T'):
            return api.get_track_info(song_id)

        return next((song for song in songs if song[GMusicKeys.SongKeys.SongIdKey] == song_id), None)

    @staticmethod
    def GetSongRatingSafely(song):
        if song.has_key(GMusicKeys.SongKeys.RatingKey):
            return int(song[GMusicKeys.SongKeys.RatingKey])
        else:
            return 0

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

class OutputHelper:
    @staticmethod
    def print_song_info(index, track, api):
        song = SongHelper.get_song_from_track(track, StorageHelper.songs, api)

        song_name = SongHelper.get_song_name(song)
        print "Entry: " + '{:3}'.format(index) + " - Title: " + '{:<70}'.format(song_name) + " - Artist:" + '{:<50}'.format((song['artist']).encode('ascii','ignore'))

    @staticmethod
    def write_song_info_to_text(index, track, api, file_to_write):
        song = SongHelper.get_song_from_track(track, StorageHelper.songs, api)

        song_name = SongHelper.get_song_name(song)

        file_to_write.write("Entry: " + '{:3}'.format(index) + " - Title: " + '{:<70}'.format(song_name) + " - Artist: " + '{:<50}'.format((song['artist']).encode('ascii','ignore')) + "\n")

    @staticmethod
    def write_songs_to_text(tracks, api):
        file_to_write = open('output.txt', 'w')

        for index in range(len(tracks)):
            track = tracks[index]
            OutputHelper.write_song_info_to_text(index, track, api, file_to_write)

        file_to_write.close()

    @staticmethod
    def write_songs_to_excel(api, songs):
        
        #tracks = api.get_all_songs()
        log = ProgramVars.log

        log.debug("Successfully grabbed all songs.")
        
        log.debug("Size of list [pre-filter]: " + str(len(songs)))
        tracks = filter(lambda item: item.has_key(GMusicKeys.SongKeys.TrackTypeKey) and int(item[GMusicKeys.SongKeys.TrackTypeKey]) == 8, songs) #FilterHelper.FilterByEqualToKey(StorageHelper.songs, GMusicKeys.SongKeys.TrackTypeKey, 8)

        log.debug("Size of list [post-filter]: " + str(len(tracks)))

        workbook = xlsxwriter.Workbook('SongList.xlsx')
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0

        format = workbook.add_format()
        format.set_num_format('mm/dd/yy hh:mm AM/PM')
        

        for columnHeader in PrinterKeys.Keys:
            worksheet.write(row, col, columnHeader)
            col += 1
        worksheet.write(row, col, GMusicKeys.SongKeys.AlbumArtRefKey)
        col = 0
        row += 1
        

        for num in range(len(tracks)):
            track = tracks[num]

            for columnHeader in PrinterKeys.Keys:
                #worksheet.write(row, col, columnHeader)
                if (track.has_key(columnHeader)):
                    if type(track[columnHeader]) is list or type(track[columnHeader]) is tuple:
                       val_to_write = track[columnHeader][0]
                       if type(track[columnHeader][0]) is dict:
                           val_to_write = str(track[columnHeader][0])
                    elif type(track[columnHeader]) is dict:
                        val_to_write = str(track[columnHeader])
                    else:
                        if columnHeader.find('Timestamp') > -1:

                            worksheet.set_column(col, col, 20, format)
                            val_to_write = '=(' + str(track[columnHeader]) + '/1000000)/86400+25569+(-8/24)' #utils.convert_timestamp(track[columnHeader])
                        else:
                            val_to_write = track[columnHeader]
                    worksheet.write(row, col, val_to_write)
                col += 1
            worksheet.write(row, col, SongHelper.GetSongAlbumArtUrl(track))

            row += 1
            col = 0

        workbook.close()

class StorageHelper:
    tracks = []
    playlists = []
    songs = []