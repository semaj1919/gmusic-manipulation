from getpass import getpass
from gmusicapi import Mobileclient
from utils import logger

class ProgramVars:
    username = None
    log = None
    #logging = 'INFO'
    #verbosity = 'INFO'


    def __init__(self, account, logging='INFO', verbosity='INFO'):
        #self.__class__.logging_level = loglevel
        self.__class__.username = account
        #self.__class__.verbosity_level = verbosity
        self.__class__.log = logger('gmusic-playlist-manipulator', verbosity, logging)

def login():
    api = Mobileclient()
    user_pass = getpass()
    ProgramVars.log.debug("Logging in...")

    try:
        if api.login(ProgramVars.username, user_pass, Mobileclient.FROM_MAC_ADDRESS):
            return api
        else:
            return None
    except:
        ProgramVars.log.exception(sys.exc_info()[0])
        return None

class GMusicKeys:
    class TrackKeys: 
        PlaylistId = 'playlistId'
        EntryIdKey = 'id'
        TrackIdKey = 'trackId'
        CreationTimestampKey = 'creationTimestamp'
        LastModifiedTimestampKey = 'lastModifiedTimestamp'
    class SongKeys:
        SongIdKey = 'id'
        PlayCountKey = 'playCount'
        CreationTimestampKey = 'creationTimestamp'
        TitleKey = 'title'
        AlbumArtRefKey = 'albumArtRef'
        AlbumArtUrlKey = 'url'
        RecentTimestampKey = 'recentTimestamp'
        RatingKey = 'rating'
        TrackTypeKey = 'trackType'
        AlbumKey = 'album'
        AlbumArtistKey = 'albumArtist'
        LastModifiedTimestampKey = 'lastModifiedTimestamp'
    class PlaylistKeys:
        PlaylistIdKey = 'id'
        NameKey = 'name'
        TracksKey = 'tracks'
class PrinterKeys:
    Keys = ['artistId', GMusicKeys.SongKeys.TrackTypeKey, GMusicKeys.SongKeys.SongIdKey, 'composer', 'year', GMusicKeys.SongKeys.AlbumKey, GMusicKeys.SongKeys.TitleKey, GMusicKeys.SongKeys.AlbumArtistKey, 'artist', GMusicKeys.SongKeys.PlayCountKey, 'durationMillis', GMusicKeys.SongKeys.CreationTimestampKey, GMusicKeys.SongKeys.RecentTimestampKey, GMusicKeys.SongKeys.LastModifiedTimestampKey]
    

