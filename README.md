# spotify-ad-muter
Python script for muting Spotify during advertisements on linux.

Works by reading the names of getting a list of windows from the X Window manager and checking against a blacklist of names in ads_list.txt then muting the Spotify client through PulseAudio while a match is found.

Most ads will be blocked with the provided list but that also change the name of the window need to be added to the list as you encounter them.
