import sys
import argparse
from common import *
from helpers import *


def assign_globals(username, song, artist, verbosity='INFO', logging='NONE'):
    ProgramVars(username, logging, verbosity)

    global song_name, artist_name, log, storage
    song_name = song
    artist_name = artist
    storage = StorageHelper()

    log = ProgramVars.log

def get_argsparser():
    parser = argparse.ArgumentParser(description="Will create a duplicate playlist, ordered by Date Added")
    parser.add_argument("username", help="Your Google Account Username (hint: username@gmail.com)")
    parser.add_argument("song", help="The name of the song you want to find", type=str)
    parser.add_argument("artist", help="The artist of the song you want to find", type=str)
    parser.add_argument('-v', "--verbosity", choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], required=False, default='DEBUG', help='verbosity of console output, default is DEBUG')
    parser.add_argument('-l', "--logging", choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], required=False, default='NONE', help='verbosity of console output, default is NONE')
    
    #global args
    return parser.parse_args()

def main():
    global storage
    log.debug("Program loaded")
    log.debug("Song name: " + song_name)

    api = login()
    
    if api:
        try:
            log.debug("Successfully logged in.")
        
            storage.songs = api.get_all_songs()
            
            log.debug("Successfully grabbed all songs.")
        
            #matched_playlist = filter(lambda playlist: playlist[GMusicKeys.PlaylistKeys.NameKey] == song_name, storage.playlists)
            matched_song = SongHelper.FilterByTitle(storage.songs, song_name)
            log.debug("Successfully matched the playlist: " + song_name)
        
            song_album_art_url = SongHelper.GetSongAlbumArtUrl(matched_song)
        
            log.debug("Successfully grabbed Song Album Art Url: " + song_album_art_url)
        
            
        except:
            log.exception(sys.exc_info()[0])  
        finally:
            api.logout()

    else:
        log.debug("Failed to log in.  Exiting")
        exit(1)
    
if __name__ == '__main__':
    args = get_argsparser()
    assign_globals(args.username, args.song, args.artist, args.verbosity, args.logging)
    main()