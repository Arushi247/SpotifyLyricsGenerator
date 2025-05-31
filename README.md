## Spotify Lyrics Generator
The Spotify Lyrics Python script utilizes the Spotify API and the Genius API to retrieve lyrics for songs on Spotify. The script prompts the user to enter a song title and artist name and then utilizes the Spotify API to obtain the song's ID. Next, the script uses the Genius API to search for and retrieve the lyrics associated with the song's ID. Finally, the script outputs the lyrics to the user. The Spotify Lyrics Python script provides a convenient way for Spotify users to access song lyrics without having to leave the Spotify app.

Data parsing is used to extract relevant information from the JSON response objects returned by the APIs. The script parses the JSON response from the Spotify API to extract the song ID and other metadata, and then uses that information to make a subsequent API call to Genius API to retrieve the lyrics for that song. Similarly, the script uses data parsing to extract the lyrics from the response object returned by the Genius API.

Data manipulation is used to format and present the retrieved data to the user in a readable and user-friendly way. The script uses string manipulation techniques to remove unnecessary characters such as brackets and quotation marks from the retrieved lyrics, and also formats the output to be aligned with the song title and artist name entered by the user.

The Spotify Lyrics Generator demonstrates the practical application of compiler design principles in solving real-world problems.
