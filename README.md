# spotify_playlist_organizer

Dependencies:
MySQL

To load the project locally:
1. Open up to project directory
2. Create database and tables

	-> mysql -u root -p

	-> source C:/Users/jeong/projects/spotify_playlist_organizer/create_tables.sql
3. Run main module



To do:
Error handling on API responses
Error handling for sql responses
Sanitizing sql parameters
Front end for allowing user to create playlists
Cleaning up flask endpoints to only appropriate endpoints
Clean up branch use so that main is the clean version! use different
    branches while working between machines
Move up lifetime of database connection to avoid reconnecting all the time (not
    needed yet)
Flask controllers to organize endpoints? Is this needed for a project of this
    size/scope?
