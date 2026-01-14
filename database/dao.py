from database.DB_connect import DBConnect
from model.album import Album

class DAO:
    @staticmethod
    def get_album(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select a.id, a.title, a.artist_id, SUM(t.milliseconds)/60000 as durata
                    from track t, album a
                    where t.album_id = a.id
                    group by a.id, a.title, a.artist_id
                    having  durata > %s"""

        cursor.execute(query, (durata,))

        for row in cursor:
            #print(row)
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessioni():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)


        query = """ select distinct t1.album_id as album1, t2.album_id as album2 
                    from track t1, track t2, playlist_track p1, playlist_track p2
                    where p1.track_id = t1.id 
                    and p2.track_id = t2.id
                    and p1.playlist_id = p2.playlist_id
                    and t1.id != t2.id
                    and t1.album_id < t2.album_id"""

        cursor.execute(query)

        for row in cursor:
            result.append((row['album1'], row['album2']))

        cursor.close()
        conn.close()
        return result