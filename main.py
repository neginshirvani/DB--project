
import sqlite3


class linkedin:
    def __init__(self):
        self.connection = sqlite3.connect("./myDB.db")
        self.cursor = self.connection.cursor()
        self.username = ""

    def set_myusername(self, username):
        self.username = username

    def create_user_table(self):
        self.cursor.execute("""CREATE TABLE User (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username VARCHAR(50),
                            password VARCHAR(50),
                            fname VARCHAR(50),
                            lname VARCHAR(50),
                            about VARCHAR(500),
                            gender CHAR(1),
                            bday int,
                            joining DATE
                            );""")

    def create_conversation_table(self):
        self.cursor.execute("""CREATE TABLE Conversation (
                            sender_id INTEGER,
                            receiver_id INTEGER,
                            message_id INTEGER,
                            archived VARCHAR(1),
                            unread VARCHAR(1),
                            deleted VARCHAR(1),
                            joining DATE
                            );""")
        self.connection.commit()

    def create_message_table(self):
        self.cursor.execute("""CREATE TABLE Message (
                            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            text VARCHAR(500),
                            joining DATE
                            );""")

    def create_skill_table(self):
        self.cursor.execute("""CREATE TABLE Skill (
                            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            skill_name VARCHAR(100),
                            joining DATE
                            );""")

    def create_endorse_table(self):
        self.cursor.execute("""CREATE TABLE Endorse (
                            skill_id INTEGER,
                            user_id INTEGER,
                            endorsement_id INTEGER,
                            joining DATE
                            );""")

    def create_endorsement_table(self):
        self.cursor.execute("""CREATE TABLE Endorsement (
                            endorsement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            message VARCHAR(100),
                            joining DATE
                            );""")

    def create_invitation_table(self):
        self.cursor.execute("""CREATE TABLE Invitation (
                            invitation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sender_id INTEGER,
                            receiver_id INTEGER,
                            result VARCHAR(1),
                            joining DATE
                            );""")

    def add_new_user(self, username, password, first_name, last_name, gender, bday):
        try:
            self.create_user_table()
        except:
            print("table already existed!")

        command = "INSERT INTO User (username, password, fname, lname, gender, bday) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');".format(username, password, first_name, last_name, gender, bday)
        self.cursor.execute(command)
        self.connection.commit()

    def add_new_message(self, text):
        try:
            self.create_message_table()
        except:
            print("table already existed!")

        command = "INSERT INTO Message (text) VALUES ('{0}');".format(text)
        self.cursor.execute(command)
        self.connection.commit()

        command = "SELECT * FROM Message ORDER BY message_id DESC LIMIT 1;"

        self.cursor.execute(command)
        message_id = self.cursor.fetchall()
        return message_id[0][0]


    def add_new_conversation(self, sender, receiver, message_id):
        # AKA send a message
        try:
            self.create_conversation_table()
        except:
            print("table already existed!")

        command = "INSERT INTO Conversation (sender_id, receiver_id, message_id, archived, unread, deleted) VALUES ('{0}', '{1}', '{2}', 0, 0, 0 );".format(sender, receiver, message_id)
        self.cursor.execute(command)
        self.connection.commit()

    def add_new_skill(self, user_id, skill_name):
        try:
            self.create_skill_table()
        except:
            print("table already existed!")

        command = "INSERT INTO Skill (user_id, skill_name) VALUES ('{0}', '{1}');".format(user_id, skill_name)
        self.cursor.execute(command)
        self.connection.commit()

    def add_new_endorse(self, skill_id, user_id, endorsement_id): #should create an Endorsement first then pass its  id to this function
        try:
            self.create_endorse_table()
        except:
            print("table already existed!")

        command = "INSERT INTO Endorse (skill_id, user_id, endorsement_id) VALUES ('{0}', '{1}', '{2}');".format(skill_id, user_id, endorsement_id)
        self.cursor.execute(command)
        self.connection.commit()

    def add_new_endorsement(self, mssg):
        try:
            self.create_endorsement_table()
        except:
            print("table already existed!")

        command = "INSERT INTO Endorsement (message) VALUES ('{0}');".format(mssg)
        self.cursor.execute(command)
        self.connection.commit()

    def login(self, username, password):
        command = "SELECT * FROM User WHERE username = '{0}' and password = '{1}';".format(username, password)
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        if len(res) == 1: # change this to == pls
            return True
        else:
            return False

    def signup(self, username, password):
        command = "SELECT * FROM User WHERE username = '{0}' and password = '{1}';".format(username, password)
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        if len(res) == 0:
            # This username is available
            command = "INSERT INTO User (username, password) VALUES ('{0}', '{1}');".format(username, password)
            self.cursor.execute(command)
            self.connection.commit()
            return True
        else:
            #This username is taken
            return False

    def get_user_information(self, username):
        command = "SELECT * FROM User WHERE username = '{0}';".format(username)
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        if len(res) == 1:
            return res

    def get_username(self, user_id):
        command = "SELECT * FROM User WHERE user_id = '{0}';".format(user_id)
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        if len(res) == 1:
            return res[0][1]

    def open_conversation(self, sender_id, receiver_id):
        command = "SELECT * FROM Conversation WHERE sender_id = '{0}' and receiver_id = '{1}';".format(sender_id, receiver_id)
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        # returns mssg ids
        return res

    def get_my_contacts(self, user_id):
        command = "SELECT DISTINCT username, user_id FROM Conversation JOIN User ON Conversation.receiver_id = User.user_id WHERE sender_id = '{0}'".format(user_id)
        command += " UNION  "
        command += "SELECT DISTINCT username, user_id FROM Conversation JOIN User ON Conversation.sender_id = User.user_id WHERE receiver_id = '{0}';".format(user_id)
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        return res

    def get_a_conversation(self, user_id1, user_id2):
        command = "SELECT * FROM Conversation JOIN Message ON Conversation.message_id = Message.message_id WHERE receiver_id = '{0}' AND sender_id = '{1}'".format(user_id1, user_id2)
        command += " UNION "
        command += "SELECT * FROM Conversation JOIN Message ON Conversation.message_id = Message.message_id WHERE receiver_id = '{1}' AND sender_id = '{0}'".format(user_id1, user_id2)
        command += " ORDER BY message_id"
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        return res

    def get_archived(self, user_id1, user_id2):
        command = "SELECT * FROM Conversation JOIN Message ON Conversation.message_id = Message.message_id WHERE receiver_id = '{0}' AND sender_id = '{1}' AND archived = '1'".format(user_id1, user_id2)
        command += " UNION "
        command += "SELECT * FROM Conversation JOIN Message ON Conversation.message_id = Message.message_id WHERE receiver_id = '{1}' AND sender_id = '{0}' AND archived = '1'".format(user_id1, user_id2)
        command += " ORDER BY message_id"
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        return res

    def get_unarchived(self, user_id1, user_id2):
        command = "SELECT * FROM Conversation JOIN Message ON Conversation.message_id = Message.message_id WHERE receiver_id = '{0}' AND sender_id = '{1}' AND archived = '0'".format(user_id1, user_id2)
        command += " UNION "
        command += "SELECT * FROM Conversation JOIN Message ON Conversation.message_id = Message.message_id WHERE receiver_id = '{1}' AND sender_id = '{0}' AND archived = '0'".format(user_id1, user_id2)
        command += " ORDER BY message_id"
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        return res

    def search_in_messages(self, user_id1, user_id2, message_subset):
        command = "SELECT * FROM Conversation JOIN Message ON Conversation.message_id = Message.message_id WHERE receiver_id = '{0}' AND sender_id = '{1}' AND Message.text like '%{2}%'".format(user_id1, user_id2, message_subset)
        command += " UNION "
        command += "SELECT * FROM Conversation JOIN Message ON Conversation.message_id = Message.message_id WHERE receiver_id = '{1}' AND sender_id = '{0}' AND Message.text like '%{2}%'".format(user_id1, user_id2, message_subset)
        command += " ORDER BY message_id"
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        return res

    def search_in_users(self, username):
        command = "SELECT * from User WHERE username like '%{0}%'".format(username)
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        return res

    def physical_delete_a_message(self, message_id):
        command = "DELETE FROM Conversation WHERE Conversation.message_id = '{0}';".format(message_id)
        self.cursor.execute(command)
        self.connection.commit()

    def send_invitation(self, sender, receiver):
        try:
            self.create_invitation_table()
        except:
            print("Table already existed!")

        command = "INSERT INTO Invitation (sender_id, receiver_id, result) VALUES ('{0}', '{1}', 0);".format(sender, receiver)
        self.cursor.execute(command)
        self.connection.commit()

    def accept_invitation(self, sender_id, receiver_id):
        command = "UPDATE Invitation SET result = 1 WHERE sender_id = '{0}' AND receiver_id = '{1}'".format(sender_id, receiver_id)
        self.cursor.execute(command)
        self.connection.commit()

    def reject_invitation(self, sender_id, receiver_id):
        command = "DELETE FROM Invitation WHERE sender_id = '{0}' AND receiver_id = '{1}'".format(sender_id, receiver_id)
        self.cursor.execute(command)
        self.connection.commit()

    def get_my_invitations(self, user_id):
        command = "SELECT * FROM Invitation WHERE receiver_id = '{0}' AND result = '0'".format(user_id)
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        return res

    def get_network(self, userid):
        try:
            self.create_invitation_table()
        except:
            print("Table already existed!")

        command = "SELECT * FROM Invitation WHERE sender_id = '{0}' AND result = 1".format(userid)
        command += " UNION "
        command += "SELECT * FROM Invitation WHERE receiver_id = '{0}' AND result = 1".format(userid)
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        return res

    def is_network(self, user_id1, user_id2):
        command = "SELECT * FROM Invitation WHERE sender_id = '{0}' AND receiver_id = '{1}' AND result = 1 ".format(user_id1, user_id2)
        command += " UNION "
        command += "SELECT * FROM Invitation WHERE sender_id = '{0}' AND receiver_id = '{1}' AND result = 1 ".format(user_id2, user_id1)
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        return len(res)

    def is_pending(self, user_id1, user_id2):
        command = "SELECT * FROM Invitation WHERE sender_id = '{0}' AND receiver_id = '{1}' AND result = 0 ".format(user_id1, user_id2)
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        return len(res)

    # Since we are treating a rejected request like a non-existing one,
    # We no longer need a rejected state, it would be highly redundant

    # def is_rejected(self, user_id1, user_id2):
    #     command = "SELECT * FROM Invitation WHERE sender_id = '{0}' AND receiver_id = '{1}' AND result = 2 ".format(user_id1, user_id2)
    #     command += " UNION "
    #     command += "SELECT * FROM Invitation WHERE sender_id = '{0}' AND receiver_id = '{1}' AND result = 2 ".format(user_id2, user_id1)
    #     self.cursor.execute(command)
    #     res = self.cursor.fetchall()
    #     return len(res)

    def print_user_table(self):
        self.cursor.execute("SELECT * FROM User")
        table = self.cursor.fetchall()
        for record in table:
            print(record)

    def print_message_table(self):
        self.cursor.execute("SELECT * FROM Message")
        table = self.cursor.fetchall()
        for record in table:
            print(record)

    def print_conversation_table(self):
        self.cursor.execute("SELECT * FROM Conversation")
        table = self.cursor.fetchall()
        for record in table:
            print(record)

    def print_invitation_table(self):
        self.cursor.execute("SELECT * FROM Invitation")
        table = self.cursor.fetchall()
        for record in table:
            print(record)
    #Negin start

    def create_post_table(self):
        self.cursor.execute("""CREATE TABLE Post (
                            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            image IMAGE,
                            caption TEXT,
                            releaseDate DATE,
                            releaseTime TIME,
                            author_id INTEGER,
                            share_id INTEGER
                            );""")


    def create_comment_table(self):
        self.cursor.execute("""CREATE TABLE Comment (
                            comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            commentText VARCHAR(100),
                            releaseDate DATE,
                            releaseTime TIME
                            );""")


    def create_comment_detail_table(self):
        self.cursor.execute("""CREATE TABLE CommentDetail (
                            CommentPost_id INTEGER,
                            UserID INTEGER,
                            PostID INTEGER
                            );""")


    def create_reply_table(self):
        self.cursor.execute("""CREATE TABLE Reply (
                            parentComment_id INTEGER,
                            childComment_id INTEGER,
                            userid INTEGER
                            );""")


    def create_likes_table(self):
        self.cursor.execute("""CREATE TABLE Likes (
                                    user_id INTEGER,
                                    post_id INTEGER
                                    );""")


    def like_a_post(self, post_id, user_id):
        try:
            self.create_likes_table()
        except:
            print("table already existed!")

        command = "INSERT INTO Likes (user_id, post_id) VALUES ('{0}', '{1}');".format(user_id, post_id)
        self.cursor.execute(command)
        self.connection.commit()

    def remove_a_like(self, post_id, user_id):
        command = "DELETE FROM likes WHERE post_id = '{0}' AND user_id = '{1}'".format(post_id, user_id)
        self.cursor.execute(command)
        self.connection.commit()



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


    def share_post(self, post, user1, user2):

        # change open converstation in a way which we can also call it for a post
        pass

    def add_new_post(self, image, caption, releaseDate, releaseTime, user_id):
        try:
            self.create_post_table()
        except:
            print("table already existed!")

        command = "INSERT INTO Post (image, caption, releaseDate, releaseTime, author_id) VALUES ('{0}', '{1}', '{2}', '{3}', {4});".format(image, caption, releaseDate, releaseTime, user_id)
        self.cursor.execute(command)
        self.connection.commit()

    def get_my_posts(self, user_id):
        try:
            self.create_post_table()
        except:
            print("table already existed!")

        command = "SELECT * FROM Post WHERE author_id = '{0}'".format(user_id)
        self.cursor.execute(command)
        res = self.cursor.fetchall()
        return res

    def print_post_table(self):
        self.cursor.execute("SELECT * FROM Post")
        table = self.cursor.fetchall()
        for record in table:
            print(record)


        #  ***  NEGIN  ***

    def create_likedComment_table(self):
        self.cursor.execute("""CREATE TABLE LikedComment (
                                    comment_id INTEGER,
                                    userid INTEGER
                                    );""")


    def number_of_likes_of_a_post(self, post_id):
        # Returns the number of likes on a post
        command = "SELECT user_id FROM Likes WHERE Likes.post_id = post_id;".format(post_id)
        self.cursor.execute(command)
        table = self.cursor.fetchall()
        print(len(table))


    def add_new_comment(self, text):
        # Adds a new comment to the Comment table
        # And returns the comment_id of that newly added comment
        # This part is super important
        # You may need to commit more than one query
        try:
            self.create_comment_table()
        except:
            print("table already existes!")

        command = "INSERT INTO Comment (commentText) VALUES ('{0}');".format(text)
        self.cursor.execute(command)
        self.connection.commit()

        command = "SELECT * FROM Comment ORDER BY comment_id DESC LIMIT 1;"
        self.cursor.execute(command)
        comment_id = self.cursor.fetchall()
        return comment_id[0][0]

    def add_new_comment_detail(self, CommentPost_id, UserID, PostID):
        try:
            self.create_comment_detail_table()
        except:
            print("table already exists!")

        command = "INSERT INTO CommentDetail (CommentPost_id, UserID, PostID) VALUES ('{0}', '{1}', '{2}');".format(CommentPost_id, UserID, PostID)
        self.cursor.execute(command)
        self.connection.commit()

    def add_new_reply(self, parentComment_id, childComment_id, userid):
        try:
            self.create_reply_table()
        except:
            print("table already exists!")

        command = "INSERT INTO Reply (parentComment_id, childComment_id, userid) VALUES ('{0}', '{1}', '{2}');".format(parentComment_id, childComment_id, userid)
        self.cursor.execute(command)
        self.connection.commit()

    def get_a_posts_comments(self, post_id):
        # Returns a list including the AUTHOR and CONTEXT of that comment
        # And please specify which one is in which index
        # Negin added cm starts
        # index 0 is text and index 1 is userid
        # IDK why it doesn't print the recordes -_-
        command = "SELECT Comment.commentText, CommentDetail.UserID FROM Comment JOIN CommentDetail ON Comment.comment_id = CommentDetail.CommentPost_id WHERE CommentDetail.PostId = '{0}';".format(post_id)
        self.cursor.execute(command)
        table = self.cursor.fetchall()
        for rec in table:
            print(rec)

    # I'm not sure if this query is logical or not -_-
    def get_a_comments_replys(self, comment_id):
        # Same as the previous one but for a comment
        command = "SELECT Reply.* FROM Comment JOIN Reply ON Comment.comment_id = Reply.childComment_id WHERE Reply.parentComment_id = '{0}';".format(comment_id)
        self.cursor.execute(command)
        table = self.cursor.fetchall()
        for rec in table:
            print(rec)



    def like_a_comment(self, comment_id, user_id):
        try:
            self.create_likedComment_table()
        except:
            print("table already exists")

        command = "INSERT INTO LikedComment (comment_id, userid) VALUES ('{0}', '{1}');".format(comment_id, user_id)
        self.cursor.execute(command)
        self.connection.commit()

    def unlike_a_comment(self, comment_id, user_id):

        command = "DELETE FROM likedComment WHERE comment_id = '{0}' AND userid = '{1}'".format(comment_id, user_id)
        self.cursor.execute(command)
        self.connection.commit()
        print("comment deleted")

    def number_of_likes_of_a_comment(self, comment_id):
        # Pretty self explanatory I guess
        # Returns just an integer
        command = "SELECT userid FROM LikedComment WHERE LikedComment.comment_id = comment_id;".format(comment_id)
        self.cursor.execute(command)
        table = self.cursor.fetchall()
        print(len(table))

    def get_home_posts(self, user_id):
        # Three kinds of posts we need in home:
        # 1. Posted by someone in the users network
        # 2. Liked by someone in the users network
        # 3. Commented by someone in the users network
        # may need to perform UNION
        # Return the table with descending order

        command = "CREATE VIEW Net AS SELECT * FROM Invitation WHERE sender_id = '{0}' AND result = 1".format(user_id)
        command += " UNION "
        command += "SELECT * FROM Invitation WHERE receiver_id = '{0}' AND result = 1".format(user_id)
        self.cursor.execute(command)
        self.connection.commit()
        # print("table network is created")


        # we have all posts, comments, and likes which some one in our netweork has shared BUT DO WE HAVE THE CONTENTS OF THE LIKED POSTS TOO?

        command = "SELECT * FROM Net JOIN Post ON Post.author_id = Net.'{0}'".format(user_id)
        command += " UNION "
        command += "SELECT * FROM Net JOIN CommentDetail ON CommentDetail.UserID = Net.'{0}'".format(user_id)
        command += " UNION "
        command += "SELECT * FROM Net JOIN Likes ON Likes.user_id = Net.'{0}'".format(user_id)

        self.cursor.execute(command)
        self.connection.commit()






        #  ***  MITRA  ***

    def create_notification_table(self):
        # A table having 3 columns:
        # sender_id, receiver_id, type
        # type -> VARCHAR(1)
        # '1' -> birthday
        # '2' -> profile visit
        # ...
        pass

    def add_notification(self, sender_id, receiver_id, type):
        # Tnsert into the Notification table
        pass

    def get_notifications(self, user_id):
        # Return a table including the records
        # that in which this user is the receiver end
        pass

    def get_people_you_may_know(self, user_id):
        # Quite complex
        pass

    def search_by_location(self, user_id, location):
        # Have to alter the User table first
        pass



if __name__ == "__main__":
    l = linkedin()
    # l.add_new_reply(1,2,3)
    #l.add_new_user("Y", "0000", "", "", "", "")
    # l.add_new_user("S", "0000", "", "", "", "")
    # l.invite()
    # l.add_new_post(None, "caption", None, None, 1)
    # l.like_a_post(1, 2)
    # l.number_of_likes_of_a_post(1)
    # print("hi")
    # l.get_a_posts_comments(1)
    # l.like_a_comment(1, 1)
    # l.unlike_a_comment(1,1)
    # l.print_post_table()
    # l.add_new_conversation("","","")
    # m1 = l.add_new_message("hi")
    # m2 = l.add_new_message("This is admin")
    # m3 = l.add_new_message("This is P")
    # l.add_new_comment_detail("","","")
    l.get_home_posts("")
    # m1 = l.add_new_comment("hi")
    # m2 = l.add_new_comment("hello")
    # print(l.get_a_posts_comments(""))
    # print("is done till here")
    # l.print_message_table()
    #l.print_invitation_table()
    #l.add_new_user("JaneJason100", "1111", "Jane", "Jason", "F", 32)
    #l.print_user_table()
    #print(l.login("SS97", "0000"))
    #l.signup("MBFD", "1245")
    #l.print_user_table()
    #l.get_network(1)
    #l.add_new_conversation(2, 1, m1)
    #l.add_new_conversation(4, 1, m3)
    #l.add_new_conversation(2, 1, m2)
    #l.add_new_conversation("SS97", "Y", m3)
    #l.get_a_conversation(1,2)
    #print("---------")
    #l.get_network(1)
    #l.print_conversation_table()
    #l.print_post_table()
    #l.physical_delete_a_message(6)
    #l.print_conversation_table()
    #print("---------")
    #print(l.search_in_messages(1, 2, 'i'))
    #print(l.get_my_contacts(4))
    #print(l.get_a_conversation(1,4))
    #print(l.get_unarchived(1,4))
    #l.print_invitation_table()
    #print(l.get_my_invitations(1))
