# Sinhala_Lyrics_Scraper

    1. Install python and pip version 3
    2. Install required python packages by running the following command in the project home directory. $ pip install -r requirements.txt
    
    
 # Running the Crawler
    
    Go to lyrics folder and run the following command.

$ scrapy crawl lyrics -o output.json

# Data Format

Spider will scrape the sinhala song book website based on below fields.

    title: name of the song
    artist: list containing artists
    genre: list containing genres
    lyricist: list containing lyric writers
    music_by: list containing music directors
    views: number of views for the song in original site
    shares: number of shares for the song in original site
    lyric: lyrics of the song




