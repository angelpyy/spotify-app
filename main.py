import spotipy
from spotipy import oauth2

from saturday import saturday as get_sat
from scrape import scrape_website as scrape


# Fix Spotify's silly goofy 1hr authetincation token
def refresh():
    global token_info, sp

    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        tokens = token_info['access_token']
        sp = spotipy.Spotify(auth=tokens)


# Set your Spotify API credentials
client_id = '***'
client_secret = '***'
user_id = '***'
scope = 'playlist-modify-public'
redirect_uri = 'http://localhost:8888/callback'

# Authenticate with the Spotify API
sp_oauth = oauth2.SpotifyOAuth(client_id=client_id,
                               client_secret=client_secret,
                               redirect_uri=redirect_uri,
                               scope=scope)
token_info = sp_oauth.get_cached_token()
if not token_info:
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    response = input('Paste the above link into your browser, then paste the redirect url here: ')

    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

    token = token_info['access_token']
else:
    token = token_info['access_token']

if token:
    # Init Spotify API fella
    sp = spotipy.Spotify(auth=token)

    # Retrieve every date necessary for creation
    saturdays = get_sat()

    for saturday in saturdays:

        # Set the parameters for the new playlist
        playlist_name = saturday
        playlist_description = 'it stopped working here so now i gotta fix it'
        public = True

        # URL of the website to scrape
        url = 'https://www.billboard.com/charts/hot-100/{}/'.format(saturday.strip())

        # Scrape the website
        song_names = scrape(url)

        # Create the new playlist
        playlist = sp.user_playlist_create(user_id, saturday, public, description=playlist_description)

        # Get the playlist ID
        playlist_id = playlist['id']

        # Search for each song on Spotify and add it to the playlist
        for song_name in song_names:
            # Search for the song on Spotify
            results = sp.search(q=song_name, limit=10, type='track')
            print('lol?')
            # Get the first track from the search results
            track = results['tracks']['items'][0]

            # Add the track to the playlist
            sp.playlist_add_items(playlist_id, [track['id']])

        # Refresh the Auth Token
        refresh()
else:
    print("Can't get token for", user_id)
