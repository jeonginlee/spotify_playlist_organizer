CREATE DATABASE IF NOT EXISTS spotify;

USE spotify;

CREATE TABLE IF NOT EXISTS tracks (
	acousticness float,
	analysis_url varchar(255),
	danceability float,
	duration_ms int,
	energy float,
	id varchar(255) NOT NULL,
	instrumentalness float,
	music_key int,
	liveness float,
	loudness float,
	mode int,
	name varchar(255),
	speechiness float,
	tempo float,
	time_signature int,
	track_href varchar(255),
	type varchar(255),
	uri varchar(255),
	valence float,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS artists (
	id varchar(255) NOT NULL,
	name varchar(255) NOT NULL,
	href varchar(255),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS genres (
	genre varchar(255) NOT NULL,
	PRIMARY KEY (genre)
);

CREATE TABLE IF NOT EXISTS artistToGenre (
	name varchar(255) NOT NULL,
	genre varchar(255) NOT NULL,
	CONSTRAINT PK_artistsToGenre PRIMARY KEY (name, genre)
);

CREATE TABLE IF NOT EXISTS trackToGenre (
	name varchar(255) NOT NULL,
	genre varchar(255) NOT NULL,
	CONSTRAINT PK_trackToGenre PRIMARY KEY (name, genre)
);
