import mysql.connector

# Creating connection object
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root"
)

cursor = mydb.cursor();	

database_name = "spotify"
# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS "+database_name);

# Connected to database
mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "root",
	database = database_name
)

cursor = mydb.cursor();

# Create table for spotify tracks
command = "CREATE TABLE IF NOT EXISTS tracks ("\
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
	"speechniess float,"\
	"tempo float,"\
	"time_signature int,"\
	"track_href varchar(255),"\
	"type varchar(255),"\
	"uri varchar(255),"\
	"valence float,"\
	"PRIMARY KEY(ID)"\
")";

cursor.execute(command);

mydb.commit();
mydb.close();
