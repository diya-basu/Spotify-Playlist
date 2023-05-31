from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

print("User please enter a date from which you want the music in yy-mm-dd format")
date=input()

url=f"https://www.billboard.com/charts/hot-100/{date}/"
response=requests.get(url)

soup=BeautifulSoup(response.text,"html.parser")
songs = soup.find_all(name="h3", class_="a-no-trucate")

titles = [title.getText().strip() for title in songs]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_CLIENT_ID",
                                               client_secret="YOUR_CLIENT_SECRET",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"))
results = sp.current_user()
User_id = results['id']

uris = [sp.search(title)['tracks']['items'][0]['uri'] for title in titles]

PLAYLIST_ID = sp.user_playlist_create(user=User_id,public=False,name=f"{date} BillBoard-100")['id']

sp.user_playlist_add_tracks(playlist_id=PLAYLIST_ID,tracks=uris,user=User_id)