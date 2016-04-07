#!/usr/bin/env python
from gmusicapi import Mobileclient
from itertools import ifilter
from itertools import islice
import argparse
from common import *
from helpers import *
from utils import *
import sys
import time






#def assign_globals(username, playlist, verbosity='INFO', logging='NONE'):
def assign_globals(username, verbosity='INFO', logging='NONE'):
    ProgramVars(username, logging, verbosity)

    global playlist_name, log, storage
    #playlist_name = playlist
    storage = StorageHelper()

    log = ProgramVars.log

def get_argsparser():
    parser = argparse.ArgumentParser(description="Will print out the songs of a playlist.")
    parser.add_argument("username", help="Your Google Account Username (hint: username@gmail.com)")
    #parser.add_argument("playlist", help="The name of the playlist you want to find songs for", type=str)
    parser.add_argument('-v', "--verbosity", choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], required=False, default='DEBUG', help='verbosity of console output, default is DEBUG')
    parser.add_argument('-l', "--logging", choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], required=False, default='NONE', help='verbosity of console output, default is NONE')
    
    #global args
    return parser.parse_args()

def set_file():
    global file_to_write
    file_to_write = open('output.txt', 'w')
    
def close_file():
    file_to_write.close()

def set_all_songs(songs):
    global all_songs
    all_songs = songs
    print "All songs set"

#def convert_timestamp(timestamp):
#    return time.ctime(float(timestamp)/1000000)

def get_song_from_track(track):
    global storage
    song_id = track['trackId']
    return next((song for song in storage.songs if song['id'] == song_id), None)
    
def get_song_timestamp(song):
    return song['creationTimestamp']

def get_song_name(song):
    return song['title'].encode('ascii','ignore')
    
def get_song_timestamp_from_track(track):   
    song = get_song_from_track(track)
    return get_song_timestamp(song)
    
def print_song_info(index, track, api):
    song = SongHelper.get_song_from_track(track, storage.songs, api)

    song_name = get_song_name(song)
    #print "Entry: " + '{:3}'.format(index) + " - Title: " + '{:<45}'.format(get_song_name(song)[:45]) + " - Artist: " + '{:<35}'.format((song['artist']).encode('ascii','ignore')[:35]) + " - Creation Date:  " + convert_timestamp(get_song_timestamp(song))
    file_to_write.write("Entry: " + '{:3}'.format(index) + " - Title: " + '{:<70}'.format(song_name) + " - Artist: " + '{:<50}'.format((song['artist']).encode('ascii','ignore')) + "\n")


    
def main():
    
    global storage

    #log.debug("Playlist name: " + playlist_name)

    api = login()

    if api:
        log.debug("Successfully logged in.")
        
        storage.songs = api.get_all_songs()

        OutputHelper.write_songs_to_excel(api, storage.songs)

        #storage.playlists = api.get_all_user_playlist_contents()
        #log.debug("Successfully grabbed all playlists.")

        #for index in range(len(storage.playlists)):
        #    log.debug("Playlist " + str(index) + ": " + storage.playlists[index]

        #for index in range(len(storage.playlists)):
        #    log.debug("Playlist name: " + storage.playlists[index]['name'])
        
        #matched_playlist = filter(lambda playlist: playlist['name'] == playlist_name, storage.playlists)
        #log.debug("Successfully matched the playlist: " + playlist_name)
        
        #storage.tracks = matched_playlist[0]['tracks']
        #log.debug("Successfully retrieved tracks.  # of Tracks: " + str(len(storage.tracks)))




        #storage.songs = api.get_all_songs()

        #set_file()        
        #for index in range(len(storage.tracks)):
        #    track = storage.tracks[index]
        #    print_song_info(index, track, api)

        #set_all_songs(api.get_all_songs())
        
        
        #close_file()
        
        api.logout()

    else:
        log.debug("Failed to log in.  Exiting")
        exit(1)
    
if __name__ == '__main__':
    args = get_argsparser()
    assign_globals(args.username, args.verbosity, args.logging)
    #assign_globals(args.username, args.playlist, args.verbosity, args.logging)
    main()