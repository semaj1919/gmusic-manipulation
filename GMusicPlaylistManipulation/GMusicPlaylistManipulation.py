#!/usr/bin/env python
import sys
import argparse

from common import *
from helpers import SongHelper

def assign_globals(username, playlist, size, playcount=1, verbosity='INFO', logging='NONE'):
    ProgramVars(username, logging, verbosity)

    global playlist_name, playlist_max_size, minimum_playcount, log
    playlist_name = playlist
    playlist_max_size = size
    minimum_playcount = playcount
    log = ProgramVars.log

def get_argsparser():
    parser = argparse.ArgumentParser(description="Will create a new playlist of the top songs sorted by play count")
    parser.add_argument("username", help="Your Google Account Username (hint: username@gmail.com)")
    parser.add_argument("playlist", help="The name of the playlist you want to create", type=str)
    parser.add_argument("size", help="The number of songs you want to include in your playlist", type=int)
    parser.add_argument("-m", "--min", help="The minimum number of plays a song needs to be considered", type=int, default=1)
    parser.add_argument('-v', "--verbosity", choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], required=False, default='DEBUG', help='verbosity of console output, default is INFO')
    parser.add_argument('-l', "--logging", choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], required=False, default='NONE', help='verbosity of console output, default is NONE')
    
    #global args
    return parser.parse_args()

def main():

    log.debug('Program loaded.')
    log.debug("Playlist name: " + playlist_name)
    log.debug("Playlist size: " + str(playlist_max_size))
    
    api = login()

    if api:
        try:
            log.info("Successfully logged in.")
        
            log.debug("Grabbing all songs")
            songs = api.get_all_songs()
            log.debug("Successfully grabbed all songs. Count: " + str(len(songs)))

            
            filtered_songs = SongHelper.FilterByPlaycount(songs, minimum_playcount)
                
            top_songs = SongHelper.SortByPlaycount(filtered_songs, True) 
            log.debug("Successfully sorted songs with a play count greater than " + str(minimum_playcount) + ".  Size: " + str(len(top_songs)))
    
            small_top_songs = top_songs[:playlist_max_size]
            log.debug("Successfully grabbed the top " + str(len(small_top_songs)) + "  songs.")

    
            playlist = api.create_playlist(playlist_name)
            log.debug("Successfully created new playlist: " + playlist_name)
        
            log.debug("Adding songs to playlist.")

            api.add_songs_to_playlist(playlist, SongHelper.GetSongIds(small_top_songs))
            log.debug("Successfully added songs to playlist.")
        except:
            log.exception(sys.exc_info()[0])       
        finally:
            api.logout()
    else:
        print "Failed to log in.  Exiting"
        exit(1)

if __name__ == '__main__':
    args = get_argsparser()
    assign_globals(args.username, args.playlist, args.size, args.min, args.verbosity, args.logging)
    main()