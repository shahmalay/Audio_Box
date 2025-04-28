from .database import db

class Artist(db.Model):
    __tablename__='artist'
    artist_id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    username = db.Column(db.String,nullable=False)
    password = db.Column(db.String)    
    song = db.relationship("Song", secondary ="songs_artist")
    album = db.relationship("Album", secondary ="artist_album")


class Song(db.Model):
    __tablename__='songs'
    song_id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    song_name = db.Column(db.String,nullable=False)
    lyrics = db.Column(db.String)
    total_rating = db.Column(db.Integer)
    date = db.Column(db.String)
    rating_sub=db.Column(db.Integer)
    hits=db.Column(db.Integer)
    artist = db.relationship("Artist", secondary ="songs_artist")
    
class Songs_artist(db.Model):  
    __tablename__='songs_artist'
    song_id= db.Column(db.Integer , db.ForeignKey("songs.song_id") , primary_key=True)
    artist_id= db.Column(db.Integer , db.ForeignKey("artist.artist_id"), unique=True)

class User(db.Model):
    __tablename__='user'
    userid = db.Column(db.Integer, primary_key=True , autoincrement=True)
    username = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)  
    playlist = db.relationship("Playlist", secondary ="user_playlist")

class Admin(db.Model):
    __tablename__='admin'
    username = db.Column(db.String,primary_key=True)
    password = db.Column(db.String)
    
class Playlist(db.Model):
    __tablename__='playlist'
    playlist_id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    name = db.Column(db.String)
    song = db.relationship("Song", secondary ="songs_playlist")
    user = db.relationship("User", secondary ="user_playlist")
    
class Songs_playlist(db.Model):  
    __tablename__='songs_playlist'
    song_id= db.Column(db.Integer , db.ForeignKey("songs.song_id") , primary_key=True)
    playlist_id= db.Column(db.Integer , db.ForeignKey("playlist.playlist_id"), unique=True)

class User_playlist(db.Model):  
    __tablename__='user_playlist'
    userid= db.Column(db.Integer , db.ForeignKey("user.userid") , primary_key=True)
    playlist_id= db.Column(db.Integer , db.ForeignKey("playlist.playlist_id"), unique=True) 
    
class Album(db.Model):
    __tablename__='album'
    album_id = db.Column(db.Integer,primary_key=True)
    aname = db.Column(db.String)
    agenre = db.Column(db.String)
    song = db.relationship("Song", secondary ="songs_album")
    artist = db.relationship("Artist", secondary ="artist_album")
   
class Artist_album(db.Model):  
    __tablename__='artist_album'
    artist_id= db.Column(db.Integer , db.ForeignKey("artist.artist_id") , primary_key=True)
    album_id= db.Column(db.Integer , db.ForeignKey("album.album_id"), unique=True) 

class Songs_album(db.Model):  
    __tablename__='songs_album'
    song_id= db.Column(db.Integer , db.ForeignKey("songs.song_id") , primary_key=True)
    album_id= db.Column(db.Integer , db.ForeignKey("album.album_id"), unique=True)         