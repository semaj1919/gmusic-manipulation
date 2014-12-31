import sys
import argparse
from common import *
from helpers import *


def assign_globals(username, playlist, verbosity='INFO', logging='NONE'):
    ProgramVars(username, logging, verbosity)

    global playlist_name, log, storage
    playlist_name = playlist
    storage = StorageHelper()

    log = ProgramVars.log

def get_argsparser():
    parser = argparse.ArgumentParser(description="Will create a duplicate playlist, ordered by Date Added")
    parser.add_argument("username", help="Your Google Account Username (hint: username@gmail.com)")
    parser.add_argument("playlist", help="The name of the playlist you want to reorder", type=str)
    parser.add_argument('-v', "--verbosity", choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], required=False, default='DEBUG', help='verbosity of console output, default is DEBUG')
    parser.add_argument('-l', "--logging", choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], required=False, default='NONE', help='verbosity of console output, default is NONE')
    
    #global args
    return parser.parse_args()

def get_song_timestamp_from_track(track):
    song = SongHelper.get_song_from_track(track, storage.songs)
    return SongHelper.get_song_timestamp(song)

def main():
    global storage
    log.debug("Program loaded")
    log.debug("Playlist name: " + playlist_name)

    api = login()
    
    if api:
        try:
            log.debug("Successfully logged in.")
        
            storage.playlists = api.get_all_user_playlist_contents()
            log.debug("Successfully grabbed all playlists.")
        
            #matched_playlist = filter(lambda playlist: playlist[GMusicKeys.PlaylistKeys.NameKey] == playlist_name, storage.playlists)
            matched_playlist = PlaylistHelper.FilterByName(storage.playlists, playlist_name)
            log.debug("Successfully matched the playlist: " + playlist_name)
        
            storage.tracks = PlaylistHelper.GetTracks(matched_playlist)
        
            storage.songs = api.get_all_songs()
        
            #newest entries first
            sorted_tracks = [track for track in sorted(storage.tracks, key=get_song_timestamp_from_track, reverse=True)]    
            log.debug("Successfully sorted by Date Added (DESC)")
        
            new_playlist = api.create_playlist(playlist_name + str(1))
            api.add_songs_to_playlist(new_playlist, SongHelper.GetSongIdsFromTracks(sorted_tracks))
        
            log.debug("Successfully created duplicate playlist.")
            #set_file() 
                   
            #for index in range(len(sorted_tracks)):
            #    track = sorted_tracks[index]
            #    print_song_info(index, track)
                #api.add_songs_playlist(playlist_create, track['trackId'])
          
        
        
        
            #for index in range(len(sorted_tracks)):
            
            #    #newest entry
            #    if index == 0:
            #        log.debug("First Entry.") #  Creation Date: ", convert_timestamp(get_song_timestamp_from_track(sorted_tracks[index]))
            #        api.reorder_playlist_entry(sorted_tracks[index], None, sorted_tracks[index+1]  )
            #    #oldest entry
            #    elif index == len(sorted_tracks)-1:
            #        log.debug("Last Entry.") #  Creation Date: ", convert_timestamp(get_song_timestamp_from_track(sorted_tracks[index]))
                
            #        api.reorder_playlist_entry(sorted_tracks[index], sorted_tracks[index-1], None)
            #    else:
            #        #print "Entry: " + str(index) + ".  Creation Date: ", convert_timestamp(get_song_timestamp_from_track(sorted_tracks[index]))
            #        api.reorder_playlist_entry(sorted_tracks[index], sorted_tracks[index-1], sorted_tracks[index+1])
            
            
        
            #playlists = api.get_all_user_playlist_contents()
            #log.debug("Successfully grabbed all playlists.")
        
            #matched_playlist = filter(lambda playlist: playlist['name'] == playlist_name, playlists)
            #log.debug("Successfully matched the playlist: " + playlist_name)
        
            #tracks = matched_playlist[0]['tracks']
        
            #for index in range(len(tracks)):
            #    track = tracks[index]
            #    print_song_info(index, track)
            #close_file()
        except:
            log.exception(sys.exc_info()[0])  
        finally:
            api.logout()

    else:
        log.debug("Failed to log in.  Exiting")
        exit(1)
    
if __name__ == '__main__':
    args = get_argsparser()
    assign_globals(args.username, args.playlist, args.verbosity, args.logging)
    main()