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

    def insertTrack(self,acousticness,analysis_url,danceability,duration_ms,energy,
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
       #     print("Error adding track " + name + " to database: ")
       #     print(e)
            print("1")

    def insertArtist(self,Id,name,href):
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
            #print("Error adding artist " + name + " to database:")
            #print(e)
            print("1")

    def insertGenre(self,name):
        command = f"""
            INSERT INTO genres
                (name)
            VALUES 
                (%s)
        """
        
        try:
            self.cursor.execute(command, [name])
            self.con.commit()
        except Exception as e:
            #print("Error adding genre " + name + " to database:")
            #print(e)
            print("1")

    def insertArtistGenre(self,artistId,genre):
        command = f"""
            INSERT INTO artistToGenre
                (artistId,genre)
            VALUES
                (%s,%s)
        """
        print("inserting mapping")
        print("artist ID: " + artistId)
        print("genre: " + genre)
        
        try:
            self.cursor.execute(command, [artistId,genre])
            self.con.commit()
        except Exception as e:
            print("Error adding mapping for " + artistId + " to " + genre)
            print(e)


    def __cleanup(self):
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
        except Exception as e:
            print("Error cleaning up database:")
            print(e)
         
