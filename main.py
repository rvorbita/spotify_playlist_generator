
from bs4 import BeautifulSoup
import requests
import lxml
from pprint import pprint

import spotipy
from spotipy.oauth2 import SpotifyOAuth


#get the date from user.
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
#Scrape from Billboard top 100 get the 100 top songs.
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
billboard_text = response.text
soup = BeautifulSoup(billboard_text, "lxml")

#get the text from top 100 songs and save into a list.
content_tag = soup.select("li ul li h3")
song_names = [ song.get_text().strip() for song in content_tag ]


SPOTIFY_ID = "Get the ID from Spotify Developer ID"
SPOTIFY_SECRET = "Get the SECRET from Spotify Developer SECRET"
SPOTIFY_USERNAME = "Provide your Spotify username"

#API CREDS 
token = (SPOTIFY_ID, SPOTIFY_SECRET)

#authentication parameters
auth_manager = SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=token[0],
        client_secret=token[1],
        show_dialog=True,
        cache_path="token.txt",
        username=SPOTIFY_USERNAME,
        )

sp = spotipy.Spotify(auth_manager=auth_manager) #API Authentication

user_id = sp.current_user()["id"] # get the user id
year = date.split('-')[0] #get only the year
songs_uri = [] #save track uri


#iterate list of songs from the scrape list and search using track and year query.
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    
    #check if the uri is available and save , else except print error message.
    try:
        uri = result["tracks"]["items"][0]["uri"]
        print(f"adding track {song} URI ...")
        songs_uri.append(uri)

    except IndexError:
        pprint(f"{song} is not available in spotify")


if len(songs_uri) != 0:
    #create a playlist.
    playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, description="Billboard top 100 tracks")
    tracks = sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uri)
    pprint("Congrats Playlist successfully created!")

else:
    pprint("Failed to create playlist.")




