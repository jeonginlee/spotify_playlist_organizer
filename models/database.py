import mysql.connector

class SpotifyDB(object):
    def __init__(self):
        print("Connecting to database...")

        try:
            self.con = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "root",
                            database = "spotify"
                        )

            if self.con.is_connected():
                self.cursor = self.con.cursor()
        except:
            print("Error connecting to database. Verify that it is built.") 
            raise 

        print("Connected successfully!")

    def __del__(self):
        print("Closing connection")
        if hasattr(self, "con"):    # self.con not set if connection failed
            self.con.close()

# INSERT ----------------------------------------------------------------------
    def insertTracks(self,acousticness,analysis_url,danceability,duration_ms,energy,
                Id,instrumentalness,music_key,liveness,loudness,mode,name,
                speechiness,tempo,time_signature,track_href,TYPE,uri,valence):
        command = f"""
            INSERT INTO tracks
                (acousticness,analysis_url,danceability,duration_ms,energy,
                id,instrumentalness,music_key,liveness,loudness,mode,name,
                speechiness,tempo,time_signature,track_href,type,uri,valence)
            VALUES
                ({acousticness},"{analysis_url}",{danceability},{duration_ms},{energy},
                %s,{instrumentalness},{music_key},{liveness},{loudness},{mode},%s,
                {speechiness},{tempo},{time_signature},%s,%s,%s,{valence});
        """
        try:
            self.cursor.execute(command, [Id,name,track_href,TYPE,uri])
            self.con.commit()
        except Exception as e:
            if e.args[0] != 1062:   # duplicate entry
                print("Error adding track " + name + " to database: ")
                print(e)

    # takes in json object and unpacks it
    def tracksImport(self, track):
        self.insertTracks(track["acousticness"],
                    track["analysis_url"],
                    track["danceability"],
                    track["duration_ms"],
                    track["energy"],
                    track["id"],
                    track["instrumentalness"],
                    track["music_key"],
                    track["liveness"],
                    track["loudness"],
                    track["mode"],
                    track["name"],
                    track["speechiness"],
                    track["tempo"],
                    track["time_signature"],
                    track["track_href"],
                    track["type"],
                    track["uri"],
                    track["valence"])

    def insertArtists(self,Id,name,href):
        command = f"""
            INSERT INTO artists
                (id,name,href)
            VALUES
                (%s,%s,%s)
        """
        try:
            self.cursor.execute(command, [Id,name,href])
            self.con.commit()
        except Exception as e:
            if e.args[0] != 1062:   # duplicate entry
                print("Error adding artist " + name + " to database:")
                print(e)

    def artistsImport(self, artist):
        self.insertArtists(artist["id"], artist["name"], artist["href"])

    def insertGenres(self,genre):
        command = f"""
            INSERT INTO genres
                (genre)
            VALUES 
                (%s)
        """
        try:
            self.cursor.execute(command, [genre])
            self.con.commit()
        except Exception as e:
            if e.args[0] != 1062:   # duplicate entry
                print("Error adding genre " + genre + " to database:")
                print(e)

    def genresImport(self, genre):
        self.insertGenres(genre["genre"])

    def insertArtistToGenre(self,name,genre):
        command = f"""
            INSERT INTO artistToGenre
                (name,genre)
            VALUES
                (%s,%s)
        """
        try:
            self.cursor.execute(command, [name,genre])
            self.con.commit()
        except Exception as e:
            if e.args[0] != 1062:   # duplicate entry
                print("Error adding mapping for artist " + name + " to " + genre)
                print(e)
    
    def artistToGenreImport(self, data):
        self.insertArtistToGenre(data["name"], data["genre"])

    def insertTrackToGenre(self,name,genre):
        command = f"""
            INSERT INTO trackToGenre
                (name,genre)
            VALUES
                (%s,%s)
        """
        try:
            self.cursor.execute(command, [name,genre])
            self.con.commit()
        except Exception as e:
            if e.args[0] != 1062:   # duplicate entry
                print("Error adding mapping for track " + name + " to " + genre)
                print(e)

    def trackToGenreImport(self, data):
        self.insertTrackToGenre(data["name"], data["genre"])

# SELECT ---------------------------------------------------------------------

    def getTrackData(self):
        command = "SELECT * FROM tracks"
        try:
            self.cursor.execute(command)
            tracks = self.cursor.fetchall()
            print(f"Got data for {len(tracks)} tracks")
            return tracks
        except Exception as e:
            print("Error getting track data")
            print(e)



# Helpers ---------------------------------------------------------------------
    def cleanup(self):
        print("Cleaning up database")
        command = """
            USE spotify;
            DELETE FROM artistToGenre;
            DELETE FROM artists;
            DELETE FROM tracks;
            DELETE FROM genres;
        """
        try:
            for result in self.cursor.execute(command, multi=True):
                pass
            self.con.commit()
            print("Database cleaned up")
        except Exception as e:
            print("Error cleaning up database:")
            print(e)
         
