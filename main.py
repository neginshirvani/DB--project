

import sqlite3


class linkedin:
    def __init__(self):
        self.connection = sqlite3.connect("myDB.db")
        self.cursor = self.connection.cursor()
        self.username = ""




    def create_post_table(self):
        self.cursor.execute("""CREATE TABLE Post (
                            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            image IMAGE,
                            caption TEXT,
                            releaseDate DATE,
                            releaseTime TIME,
                            FOREIGN KEY (SharePost) REFERENCES User(user_id),
                            FOREIGN KEY (LikePost) REFERENCES User(user_id)
                            );""")


    # def create_likes_table(self):
    #     pass

    def create_comment_table(self):
        self.cursor.execute("""CREATE TABLE Comment (
                            comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            commentText VARCHAR(100),
                            releaseDate DATE,
                            releaseTime TIME
                            );""")


    def comment_detail(self):
        self.cursor.execute("""CREATE TABLE CommentDetail (
                            FOREIGN KEY (CommentPost) REFERENCES Comment(comment_id),
                            FOREIGN KEY (UserID) REFERENCES User(user_id),
                            FOREIGN KEY (PostID) REFERENCES Post(post_id)
                            );""")


    def create_reply_table(self):
        self.cursor.execute("""CREATE TABLE Reply (
                            FOREIGN KEY (CommentPost) REFERENCES Comment(comment_id),
                            text VARCHAR(150),
                            FOREIGN KEY (UserID) REFERENCES User(user_id)
                            );""")


    def likes(self):
        self.cursor.execute("""CREATE TABLE Likes (
                                    FOREIGN KEY (UserID) REFERENCES User(user_id),
                                    FOREIGN KEY (PostID) REFERENCES Post(post_id)
                                    );""")


    def show_likes(self, postid):
        command = "SELECT Likes.UserID FROM Likes WHERE Likes.PostID = postid;".format(postid)
        self.cursor.execute(command)
        # self.connection.commit()
        likes = self.cursor.fetchall()
        for record in likes:
            print(record)


    def show_comments(self):
        command = "SELECT Comment.commentText FROM Comment"
        self.cursor.execute(command)
        # self.connection.commit()
        comments = self.cursor.fetchall()
        for record in comments:
            print(record)


    def add_new_comment(self, text, postid, userid):
        command = "INSERT INTO Comment (text) VALUES ('{0}') WHERE EXISTS (SELECT * FROM CommentDetail WHERE CommentDetail.UserID = userid AND CommentDetail.PostID = postid);".format(text, userid, postid)
        self.cursor.execute(command)
        self.connection.commit()


    def share_post(self, post, user1, user2):
        pass


    def reply_comment(self, commentid, text):
        command = "INSERT INTO Reply (text) VALUES ({0}) WHERE EXISTS (SELECT Comment.comment_id from Comment WHERE Comment.comment_id = commentid);".format(text, commentid)
        self.cursor.execute(command)
        self.connection.commit()


    def add_new_post(self, image, caption, releaseDate, releaseTime):
        try:
            self.create_post_table()
        except:
            print("table already exister!")

        command = "INSERT INTO Post (image, caption, releaseDate, releaseTime) VALUES ('{0}', '{1}', '{2}', '{3}');".format(
            image, caption, releaseDate, releaseTime)
        self.cursor.execute(command)
        self.connection.commit()


# if __name__ == "__main__":
#     l = linkedin()
#     l.add_new_comment("hi", 2, 3)