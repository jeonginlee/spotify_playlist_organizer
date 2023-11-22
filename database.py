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

    def insert_track(self,acousticness,analysis_url,danceability,duration_ms,energy,
                ID,instrumentalness,music_key,liveness,loudness,mode,name,
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

#XXX        print("Executing command: "+command)
        try:
            self.cursor.execute(command, [ID,name,track_href,TYPE,uri])
            self.con.commit()
        except Exception as e:
            print("Error adding " + name + " to database: ")
            print(e)

    # XXX
    def cleanup(self):
        try:
            print("Cleaning up database")
            self.cursor.execute("DROP DATABASE spotify;")
            print("commiting")
            self.con.commit()
        except:
            print("Error occurred during cleanup")
