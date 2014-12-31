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
    if api.login(ProgramVars.username, user_pass):
        return api
    else:
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
        playCountKey = 'playCount'
        CreationTimestampKey = 'creationTimestamp'
        TitleKey = 'title'
        AlbumArtRefKey = 'albumArtRef'
        AlbumArtUrlKey = 'url'
    class PlaylistKeys:
        PlaylistIdKey = 'id'
        NameKey = 'name'
        TracksKey = 'tracks'
    

