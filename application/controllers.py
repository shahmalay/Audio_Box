from flask import Flask, request , redirect, url_for,render_template 
from flask import current_app as app
from sqlalchemy import desc
from application.models import Artist , Song , Songs_artist , User , Admin , Playlist ,Songs_playlist , User_playlist ,Album ,Songs_album , Artist_album
import sqlite3

from .database import db


@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usertype = request.form['usertype']
        
        if usertype=='admin' :
            user = Admin.query.filter_by(username=username).first()
            pas = Admin.query.filter_by(password=password).first()
            if pas==user:
                return redirect(url_for('admin'))
        
            else:
               error="* INVALID USERNAME OR PASSWORD *"
               return render_template('login.html',errors=error)
           
        if usertype=='artist' :
            user = Artist.query.filter_by(username=username).first()
            pas = Artist.query.filter_by(password=password).first()
            if pas==user:
                return redirect(url_for('artist',singer=username))
            else:
               error="* INVALID USERNAME OR PASSWORD *"
               return render_template('login.html',errors=error)   

        if usertype=='user' :
            user = User.query.filter_by(username=username).first()
            pas = User.query.filter_by(password=password).first()
            if pas==user:
                return redirect(url_for('dashboard',user=username))
        
            else:
               error="* INVALID USERNAME OR PASSWORD *"
               return render_template('login.html',errors=error)

    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usertype = request.form['usertype']
        if usertype == "User" :
            x = User.query.with_entities(User.username).all()
            y=[]
            for i in range(len(x)):
                y.append(x[i][0])
            if username in y :
                error="REGISTERED USER ALREADY EXIST"
                render_template('Register.html',errors=error)
            else : 
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                success="REGISTERED SUCCESSFULLY"
                render_template('Register.html',success=success)
    return render_template('Register.html')
    
@app.route('/dashboard_of/<user>', methods=['GET','POST'])
def dashboard(user):
    song=Song.query.order_by(desc(Song.song_id)).all()
    playlist=Playlist.query.filter(Playlist.user.any(username=user))
    album=Album.query.all()
    return render_template('dashboard.html',songs=song,user=user,playlist=playlist,album=album)    

@app.route('/admin', methods=['GET','POST'])
def admin():
    user_count,album_count,song_count,artist_count=0,0,0,0
    for x in User.query.all():
        user_count+=1
    for x in Album.query.all():
        album_count+=1
    for x in Song.query.all():
        song_count+=1
    for x in Artist.query.all():
        artist_count+=1     
    return render_template('admin.html',uc=user_count,ac=album_count,sc=song_count,arc=artist_count) 

@app.route('/userlist', methods=['GET','POST'])
def userlist():
    user=User.query.order_by(User.userid).all()
    return render_template('user_list.html',users=user) 

@app.route('/artistlist', methods=['GET','POST'])
def artistlist():
    artist=Artist.query.order_by(Artist.artist_id).all()
    return render_template('artist_list.html',artists=artist) 

@app.route('/albumlist', methods=['GET','POST'])
def albumlist():
    albums=Album.query.order_by(Album.album_id).all()
    return render_template('album_list.html',album=albums)

@app.route('/songlist', methods=['GET','POST'])
def songlist():
    songs=Song.query.order_by(Song.song_id).all()
    return render_template('songs_list.html',songs=songs) 

@app.route('/<singer>', methods=['GET','POST'])
def artist(singer):
    sc,ac=0,0
    songs=Song.query.filter(Song.artist.any(username=singer))
    album=Album.query.filter(Album.artist.any(username=singer))
    for i in songs:
        sc+=1
    for i in album:
        ac+=1
    return render_template('artist.html',songs=songs,artist=singer,album=album,sc=sc,ac=ac) 

@app.route('/newsong_by/<singer>', methods=['GET','POST'])
def newsong(singer):
    if request.method == 'POST':
        songname = request.form['song_name']
        lyrics = request.form['lyrics']
        date = request.form['date']
        new_song = Song(song_name=songname,lyrics=lyrics,date=date,total_rating=0,rating_sub=0,hits=0)
        db.session.add(new_song)
        db.session.commit()
        sid=Song.query.filter(Song.song_name == songname).first().song_id
        aid=Artist.query.filter(Artist.username == singer).first().artist_id
        new_rel=Songs_artist(song_id=sid,artist_id=aid)
        db.session.add(new_rel)
        db.session.commit()
        success="SONG ADDED SUCCESSFULLY"
        render_template('Register.html',success=success)
    return render_template('newsong.html',artist=singer) 

@app.route('/newartist/<user>', methods=['GET','POST'])
def newsartist(user):
    x = Artist.query.with_entities(Artist.username).all()
    y=[]
    for i in range(len(x)):
        y.append(x[i][0])
    if user in y :
        return redirect(url_for('artist',singer=user))
    else :
        password=User.query.filter(User.username == user).first().password
        new_artist = Artist(username=user,password=password)
        db.session.add(new_artist)
        db.session.commit()
        return redirect(url_for('artist',singer=user))
        
@app.route('/new_playlist/<user>', methods=['GET','POST'])
def newplaylist(user):
    if request.method == 'POST':
        playlist_name = request.form['name']
        new_playlist = Playlist(name=playlist_name)
        db.session.add(new_playlist)
        db.session.commit()
        pid=Playlist.query.filter(Playlist.name == playlist_name).first().playlist_id
        uid=User.query.filter(User.username == user).first().userid
        new_rel=User_playlist(userid=uid,playlist_id=pid)
        db.session.add(new_rel)
        db.session.commit()
    return render_template('playlist.html',user=user)

@app.route('/new_album/<artist>', methods=['GET','POST'])
def newalbum(artist):
    if request.method=='POST':
        aname = request.form["aname"]
        agenre = request.form["genre"]
        new_album = Album(aname=aname,agenre=agenre)
        db.session.add(new_album)
        db.session.commit()
        amid = Album.query.filter(Album.aname == aname).first().album_id
        arid = Artist.query.filter(Artist.username == artist).first().artist_id
        new_rel = Artist_album(artist_id=arid,album_id=amid)
        db.session.add(new_rel)
        db.session.commit()
    return render_template('album.html',artist=artist)  

@app.route('/lyrics/<song>/<user>', methods=['GET','POST'])
def lyrics(song,user):
    if request.method=="POST":
        rate = request.form["rating"]
        crate=Song.query.filter(Song.song_name == song).first().total_rating
        crates=Song.query.filter(Song.song_name == song).first().rating_sub
        Song.query.filter_by(song_name=song).update({"total_rating": crate+int(rate)})
        Song.query.filter_by(song_name=song).update({"rating_sub": crates+1})
        db.session.commit()
    hits=Song.query.filter(Song.song_name == song).first().hits
    Song.query.filter_by(song_name=song).update({"hits": hits+1})  
    Song.query.filter_by(song_name=song).update({"hits": hits+1})
    db.session.commit()
    sg=Song.query.filter(Song.song_name == song).first()
    us=User.query.filter(User.username == user).first()
    return render_template('lyrics.html',us=us,sg=sg) 

@app.route('/addplaylist/<user>/<playlist>/<song>', methods=['GET','POST'])
def songplaylist(user,playlist,song):
    sid=Song.query.filter(Song.song_name == song).first().song_id
    pid=Playlist.query.filter(Playlist.name == playlist).first().playlist_id
    new_rel=Songs_playlist(song_id=sid,playlist_id=pid)
    db.session.add(new_rel)
    db.session.commit()
    return redirect(url_for('lyrics',song=song,user=user))

@app.route('/addalbum/<artist>/<album>/<song>', methods=['GET','POST'])
def songalbum(artist,album,song):
    sid=Song.query.filter(Song.song_name == song).first().song_id
    aid=Album.query.filter(Album.aname == album).first().album_id
    new_rel=Songs_album(song_id=sid,album_id=aid)
    db.session.add(new_rel)
    db.session.commit()
    return redirect(url_for('artist',singer=artist))

@app.route('/view_playlist/<user>/<playlist>', methods=['GET','POST'])
def view_playlist(user,playlist):
    pid=Playlist.query.filter(Playlist.name == playlist).first()
    return render_template("view_playlist.html",playlist=pid,user=user)

@app.route('/album/<album>/<artist>', methods=['GET','POST'])
def view_album(album,artist):
    aid=Album.query.filter(Album.aname == album).first()
    return render_template("view_album.html",album=aid,artist=artist)

@app.route('/edit_song/<song>', methods=['POST','GET'])
def edit_song(song):
    if request.method =="POST":
        id=request.form['id']
        new_name = request.form["song_name"]
        new_lyrics = request.form["lyrics"]
        new_date =request.form["date"]
        Song.query.filter_by(song_id=id).update({"song_name": new_name})
        Song.query.filter_by(song_id=id).update({"lyrics": new_lyrics})
        Song.query.filter_by(song_id=id).update({"date": new_date})
        db.session.commit()
    songs=Song.query.filter(Song.song_name==song).first()
    return render_template("/edit_song.html",song=songs)

@app.route('/edit_album/<album>', methods=['POST','GET'])
def edit_album(album):
    if request.method =="POST":
        id=request.form['id']
        new_name = request.form["aname"]
        new_genre = request.form["genre"]
        Album.query.filter_by(album_id=id).update({"aname": new_name})
        Album.query.filter_by(album_id=id).update({"agenre": new_genre})
        db.session.commit()
    albums=Album.query.filter(Album.aname==album).first()
    return render_template("/edit_album.html",album=albums)

@app.route('/delete/<song>', methods=['POST','GET'])
def delete_song(song):
    Songs_playlist.query.filter_by(song_id = song).delete()
    Songs_album.query.filter_by(song_id = song).delete()
    Songs_artist.query.filter_by(song_id = song).delete()
    db.session.commit()
    Song.query.filter_by(song_id = song).delete()
    db.session.commit()
    return redirect(url_for('songlist'))
    
@app.route('/delete/<artist>/<song>', methods=['POST','GET'])
def delete_songa(artist,song):
    Songs_playlist.query.filter_by(song_id = song).delete()
    Songs_album.query.filter_by(song_id = song).delete()
    Songs_artist.query.filter_by(song_id = song).delete()
    db.session.commit()
    Song.query.filter_by(song_id = song).delete()
    db.session.commit()
    return redirect(url_for('artist',singer=artist))

@app.route('/delete_album/<artist>/<album>', methods=['POST','GET'])
def delete_album(artist,album):
    Songs_album.query.filter_by(album_id = album).delete()
    Artist_album.query.filter_by(album_id = album).delete()
    db.session.commit()
    Album.query.filter_by(album_id = album).delete()
    db.session.commit()
    return redirect(url_for('artist',singer=artist))

@app.route('/delete_album/<album>', methods=['POST','GET'])
def delete_albuma(album):
    Songs_album.query.filter_by(album_id = album).delete()
    Artist_album.query.filter_by(album_id = album).delete()
    db.session.commit()
    Album.query.filter_by(album_id = album).delete()
    db.session.commit()
    return redirect(url_for('albumlist'))

       