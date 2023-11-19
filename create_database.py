import mysql.connector

host = "localhost"
user = "root"
password = "root"
database_name = "spotify"
table_name = "tracks"


# Connect to database and return cursor
def get_connector():
    return mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database_name
    )

class SpotifyDB(object):
    def __init__(self):
        print("Connecting to "+host+": "+database_name+" as "+user)

        try:
            self.con = get_connector()
            if self.con.is_connected():
                self.cursor = self.con.cursor()
        except:
            print("Building database: "+database_name)
            # Connect to server and create database
            mydb = mysql.connector.connect(
                host = host, user = user,
                password = password
            )

            cursor = mydb.cursor();	

            cursor.execute("CREATE DATABASE IF NOT EXISTS " + database_name);

            self.con = get_connector()
            # Check for connection again
            if not self.con.is_connected():
                print("Connection failed")
                raise RuntimeError("Failed to connect to " + database_name)

            self.cursor = self.con.cursor()

            # Create table for spotify tracks
            command = f"CREATE TABLE IF NOT EXISTS {table_name} ("\
                "acousticness float,"\
                "analysis_url varchar(255),"\
                "danceability float,"\
                "duration_ms int,"\
                "energy float,"\
                "id varchar(255) NOT NULL,"\
                "instrumentalness float,"\
                "music_key int,"\
                "liveness float,"\
                "loudness float,"\
                "mode int,"\
                "name varchar(255),"\
                "speechiness float,"\
                "tempo float,"\
                "time_signature int,"\
                "track_href varchar(255),"\
                "type varchar(255),"\
                "uri varchar(255),"\
                "valence float,"\
                "PRIMARY KEY(ID)"\
            ")";

            print("Creating table: " + table_name)
            self.cursor.execute(command);
            self.con

        print("Connected successfully!")

    def __del__(self):
        print("Closing connection")
        if hasattr(self, "con"):    # self.con not set if connection failed
            self.con.close()

    def insert_track(self,acousticness,analysis_url,danceability,duration_ms,energy,
                ID,instrumentalness,music_key,liveness,loudness,mode,name,
                speechiness,tempo,time_signature,track_href,TYPE,uri,valence):
        command = f"""
            INSERT INTO {table_name}
                (acousticness,analysis_url,danceability,duration_ms,energy,
                id,instrumentalness,music_key,liveness,loudness,mode,name,
                speechiness,tempo,time_signature,track_href,type,uri,valence)
            VALUES
                ({acousticness},"{analysis_url}",{danceability},{duration_ms},{energy},
                %s,{instrumentalness},{music_key},{liveness},{loudness},{mode},%s,
                {speechiness},{tempo},{time_signature},%s,%s,%s,{valence});
        """

        print("Executing command: "+command)
        self.cursor.execute(command, [ID,name,track_href,TYPE,uri])
        self.con.commit()

    # XXX
    def cleanup(self):
        try:
            print("Cleaning up database")
            self.cursor.execute("DROP DATABASE spotify;")
            print("commiting")
            self.con.commit()
        except:
            print("Error occurred during cleanup")



if __name__ == '__main__':
   db = SpotifyDB() 
