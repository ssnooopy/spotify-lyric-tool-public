import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lyricsgenius
import tkinter as tk
from tkinter import font
import time

print("LOG ::::::: script run")

# Set up Spotify API credentials
scope = "ADD YOUR OWN INFO HERE"
client_id = "ADD YOUR OWN INFO HERE"
client_secret = "ADD YOUR OWN INFO HERE"
rederect = "ADD YOUR OWN INFO HERE"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=rederect))

print("LOG ::::::: api set")

# create the main window
#root = tk.Tk()

# disable the window bar
#root.overrideredirect(1)

#root.geometry("500x500")

#root.config(bg="#212121") 

# set trasparency and make the window stay on top
#root.attributes('-transparentcolor', 'white', '-topmost', True)

# set the background image
#psg = tk.PhotoImage(file='love.png')
#tk.Label(root, bg='white', image=psg).pack()
# move the window to center
#root.eval('tk::PlaceWindow . Center')
#root.iconbitmap("note.ico")

#loading_text = tk.Label(root, text="loading...", font=spotfont, fg="#b3b3b3", bg="#212121", bd=0)
#loading_text.place(relx=0.5, rely=0.5, anchor="center")

# schedule the window to close after 0.5 seconds
#root.after(500, root.destroy)

# run the main loop
#root.mainloop()

# Set up Genius API credentials
genius = lyricsgenius.Genius("4rb223bBLneeZVL19jmMz0-SyD2-RNd7u1KTItvw9-Mi6bE6hldg1PXI5FgVqaOu-CHwCu3CWUDLobSXooziPA")

print("LOG ::::::: api set pt.2")

# Create a Tkinter window
window = tk.Tk()
window.title("Lyrics Finder V0.2")

print("LOG ::::::: window create")

default_font = font.nametofont("TkDefaultFont")
default_font.configure(family="Circular Std Black", size=12)
spotfont = font.Font(family="Circular Std Black", size=12,)

print("LOG ::::::: font set")

# Set the background color
window.config(bg="#212121") 

# Set the window icon
window.iconbitmap("note.ico")
window.resizable(True, True)

print("LOG ::::::: window configed")

# Create a label for displaying the song title
song_title_label = tk.Label(window, text="None", font=spotfont, fg="#b3b3b3", bg="#212121", bd=0)
song_title_label.pack()

# Create a scroll bar
scrollbar = tk.Scrollbar(window, bg="#212121", troughcolor="#212121", activebackground="#212121")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a Text widget for displaying lyrics
lyrics_text = tk.Text(window, wrap=tk.WORD, yscrollcommand=scrollbar.set, bg="#212121", fg="#b3b3b3", font=spotfont, bd=0)
lyrics_text.pack()

# Configure the scroll bar to work with the Text widget
scrollbar.config(command=lyrics_text.yview)


# Function to search and display lyrics
def search_lyrics():
    print("LOG ::::::: search lyrics command run....")
    lyrics_text.delete(0.01, tk.END)  # Clear previous lyrics
    lyrics_text.insert(tk.END, "Searching for lyrics...")  # Display a message
    print("LOG ::::::: searching with api: ")
    try:
        # Get the current playing track
        current_track = sp.current_user_playing_track()

        if current_track is not None:
            # Get the duration of the track in milliseconds
            duration_ms = current_track['item']['duration_ms']
            # Convert duration to minutes and seconds
            duration_s = duration_ms // 1000
            duration_m = duration_s // 60
            duration_s %= 60
            
            # Extract the track name and artist
            track_name = current_track['item']['name']
            artist_name = current_track['item']['artists'][0]['name']

            # Update the song title label
            song_title_label.config(text="", fg="#1db954", font=spotfont, bg="#212121")
            window.update()

            # Type each letter of the song title one at a time
            for letter in track_name:
                song_title_label.config(text=song_title_label.cget("text") + letter)
                window.update()
                time.sleep(0.1)

            song_title_label.config(text=f"{track_name} - {artist_name} - {duration_m}:{duration_s}")
            window.update()

            # Search for the lyrics using the track and artist names
            song = genius.search_song(track_name, artist_name)

            # Display the lyrics
            if song is not None:
                lyrics_text.delete(0.01, tk.END)  # Clear previous lyrics
                lyrics = song.lyrics.split('\n')  # Split lyrics into lines
                for line in lyrics:
                    if "Contributors" not in line:  # Check if the line contains "contributors"
                        lyrics_text.insert(tk.END, line + '\n')
                        lyrics_text.update()  # Update the text widget
                        time.sleep(0.01)  # Delay between each line
                for line in lyrics:
                    if "Embed" in line: # Check if the line contains "embed"
                        lyrics_text.insert(tk.END, line + '\n')
                        lyrics_text.update()
                        time.sleep(0.01)
            else:
                lyrics_text.delete(0.01, tk.END)  # Clear previous lyrics
                lyrics_text.insert(tk.END, "Lyrics not found for the current song.")
                print(" LOG ::::::: lyrics not found for the current song.")
        else:
            lyrics_text.delete(0.01, tk.END)  # Clear previous lyrics
            lyrics_text.insert(tk.END, "No track is currently playing.")
            print("LOG ::::::: no track is currently playing.")

    except Exception as e:
        print(f"LOG ::::::: an error occurred: {str(e)}")
        lyrics_text.delete(0.01, tk.END)

# Create a button to trigger the lyrics search
search_button = tk.Button(window, text="Search Lyrics", font=spotfont, command=search_lyrics, relief=tk.RAISED, bd=0, bg="#212121", fg="#b3b3b3", activebackground="#212121", activeforeground="#b3b3b3")
search_button.config(width=12, height=2, borderwidth=0, highlightthickness=0, highlightbackground="#212121", highlightcolor="#212121", pady=0, padx=0)
search_button.pack()

# Run the Tkinter event loop
window.mainloop()
