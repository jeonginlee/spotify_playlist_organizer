class Track(object):
	def __init__(self, ID, name, artists):
		self.ID = ID
		self.name = name
		self.artists = artists
		
		'''
		self.genres = []
		print("Adding track: " + self.name)
		for artist in self.artists:
			print("\t"+artist["name"])
			print(artist.keys())
			if "genres" in artist:
				for genre in artist["genres"]:
					self.genres.append(genre)
		'''
