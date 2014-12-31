#!/usr/bin/env python
from gmusicapi import Mobileclient
from itertools import ifilter
from itertools import islice
import sys
import time

def set_file():
    global file_to_write
    file_to_write = open('output.txt', 'w')
    
def close_file():
    file_to_write.close()

def set_all_songs(songs):
    global all_songs
    all_songs = songs
    print "All songs set"

def convert_timestamp(timestamp):
    return time.ctime(float(timestamp)/1000000)

def get_song_from_track(track):
    song_id = track['trackId']
    return next((song for song in all_songs if song['id'] == song_id), None)
    
def get_song_timestamp(song):
    return song['creationTimestamp']

def get_song_name(song):
    return song['title'].encode('ascii','ignore')
    
def get_song_timestamp_from_track(track):   
    song = get_song_from_track(track)
    return get_song_timestamp(song)
    
def print_song_info(index, track):
    song = get_song_from_track(track)
    #print "Entry: " + '{:3}'.format(index) + " - Title: " + '{:<45}'.format(get_song_name(song)[:45]) + " - Artist: " + '{:<35}'.format((song['artist']).encode('ascii','ignore')[:35]) + " - Creation Date:  " + convert_timestamp(get_song_timestamp(song))
    file_to_write.write("Entry: " + '{:3}'.format(index) + " - Title: " + '{:<70}'.format(get_song_name(song)) + " - Artist: " + '{:<50}'.format((song['artist']).encode('ascii','ignore')) + " - Creation Date:  " + convert_timestamp(get_song_timestamp(song)) + "\n")
    
def main():
    
    print "Program loaded"
    
    if len(sys.argv) != 2:
        print "USAGE:"
        print "./reorder_playlist_by_dateadded.py \"{playlist name}\""
        print
        print "     Will reorder your playlist by date added" 
        exit(0)

    playlist_name_to_reorder = sys.argv[1].decode('utf-8')
    print "Playlist name: " + playlist_name_to_reorder

    api = Mobileclient()


    if logged_in:
        print "Successfully logged in."
        
        playlists = api.get_all_user_playlist_contents()
        print "Successfully grabbed all playlists."
        
        matched_playlist = filter(lambda playlist: playlist['name'] == playlist_name_to_reorder, playlists)
        print "Successfully matched the playlist: " + playlist_name_to_reorder
        
        tracks = matched_playlist[0]['tracks']
        
        set_all_songs(api.get_all_songs())
        
        #newest entries first
        sorted_tracks = [track for track in sorted(tracks, key=get_song_timestamp_from_track, reverse=True)]    
        print "Successfully sorted by Date Added (Asc)"
        
        #playlist_create = api.create_playlist(playlist_name_to_reorder + str(1))
        
        set_file()        
        for index in range(len(sorted_tracks)):
            track = sorted_tracks[index]
            print_song_info(index, track)
            #api.add_songs_playlist(playlist_create, track['trackId'])
          
        
        
        
        for index in range(len(sorted_tracks)):
            
            #newest entry
            if index == 0:
                print "First Entry." #  Creation Date: ", convert_timestamp(get_song_timestamp_from_track(sorted_tracks[index]))
                api.reorder_playlist_entry(sorted_tracks[index], None, sorted_tracks[index+1]  )
            #oldest entry
            elif index == len(sorted_tracks)-1:
                print "Last Entry." #  Creation Date: ", convert_timestamp(get_song_timestamp_from_track(sorted_tracks[index]))
                
                api.reorder_playlist_entry(sorted_tracks[index], sorted_tracks[index-1], None)
            else:
                #print "Entry: " + str(index) + ".  Creation Date: ", convert_timestamp(get_song_timestamp_from_track(sorted_tracks[index]))
                api.reorder_playlist_entry(sorted_tracks[index], sorted_tracks[index-1], sorted_tracks[index+1])
            
        print "Successfully reordered playlist."
        
        playlists = api.get_all_user_playlist_contents()
        print "Successfully grabbed all playlists."
        
        matched_playlist = filter(lambda playlist: playlist['name'] == playlist_name_to_reorder, playlists)
        print "Successfully matched the playlist: " + playlist_name_to_reorder
        
        tracks = matched_playlist[0]['tracks']
        
        for index in range(len(tracks)):
            track = tracks[index]
            print_song_info(index, track)
        close_file()
        
        api.logout()

    else:
        print "Failed to log in.  Exiting"
        exit(1)
    
if __name__ == '__main__':
    main()