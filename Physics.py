import phylib;
import sqlite3;
import os;
import math
################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS= phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE

VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON

DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME

MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS
FRAME_INTERVAL=0.01
# add more here
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg id="poolTable" width="700" height="1375" viewBox="-25 -25 1400 2750"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink">
    <rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0"" />"""
FOOTER = """<line id="line" x1="100" y1="100" x2="100" y2="100" stroke="black" stroke-width="6" />"""
FOOTER2 = """</svg>\n"""

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall


    # add an svg method here
    def svg(self):
        if self.obj.still_ball.number==0:
            svgString=""" <circle id="cueBall" cx="%d" cy="%d" r="%d" fill="%s""/>\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
        else:
            svgString=""" <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
        return svgString


################################################################################

class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos , vel, acc):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = RollingBall


    # add an svg method here
    def svg(self):
        svgString=""" <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        return svgString

################################################################################

class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       None, 
                                       pos, None, None, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole


    def svg(self):
        
        svgString=""" <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)
        return svgString

################################################################################
        
class VCushion( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, x):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       None, 
                                       None, None, None, 
                                       x, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion


    # add an svg method here
    def svg(self):
        leftCheck=self.obj.vcushion.x
        if leftCheck==0:
            leftCheck=-25
        svgString = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (leftCheck)
        return svgString


################################################################################
        
class HCushion( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, y):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       None, 
                                       None, None, None, 
                                       0.0, y )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion


    # add an svg method here
    def svg(self):
        topCheck=self.obj.hcushion.y
        if topCheck==0:
            topCheck=-25
        svgString=""" <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (topCheck)
        return svgString


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def svg (self):
        svgString=HEADER
        for object in self:
            if object is not None:
                svgString+=object.svg()
        svgString+=FOOTER
        svgString+="""<p style="text-align:center;font-size:40px">Current Time:%f</p>""" % (self.time)
        svgString+=FOOTER2
        return svgString
    
    def cueBall(self):
	#For loop that scans for a cue ball and then returns it, returns none if not found
        for ball in self:
            if isinstance(ball, RollingBall):
                if ball.obj.rolling_ball.number==0:
                    self.current=-1
                    return ball
            elif isinstance(ball, StillBall):
                if ball.obj.still_ball.number==0:
                    self.current=-1
                    return ball
        return None

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                Coordinate(0,0),
                Coordinate(0,0),
                Coordinate(0,0) );  
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                Coordinate( ball.obj.still_ball.pos.x,
                ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;
    # add svg method here

################################################################################
        
class Database( ):

    def __init__( self, reset=False):
      
        if reset and os.path.exists('phylib.db'):
            os.remove( 'phylib.db' )
        self.conn=sqlite3.connect('phylib.db')
        # create database file if it doesn't exist and connect to it

    def createDB(self):
        self.cur=self.conn.cursor();
        self.cur.execute("""CREATE TABLE IF NOT EXISTS
                        BALL
                        (BALLID INTEGER PRIMARY KEY NOT NULL,
                        BALLNO INTEGER NOT NULL,
                        XPOS FLOAT NOT NULL,
                        YPOS FLOAT NOT NULL,
                        XVEL FLOAT,
                        YVEL FLOAT);""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS
                        TTABLE
                        (TABLEID INTEGER PRIMARY KEY NOT NULL,
                        TIME FLOAT NOT NULL);""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS
                        BallTable
                        (BALLID INTEGER NOT NULL,
                        TABLEID INTEGER NOT NULL,
                        FOREIGN KEY (BALLID) REFERENCES BALL,
                        FOREIGN KEY (TABLEID) REFERENCES TTABLE);""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS
                        Shot
                        (SHOTID INTEGER PRIMARY KEY NOT NULL,
                        PLAYERID INTEGER NOT NULL,
                        GAMEID INTEGER NOT NULL,
                        FOREIGN KEY (PLAYERID) REFERENCES Player,
                        FOREIGN KEY (GAMEID) REFERENCES Game);""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS
                        TableShot
                        (TABLEID INTEGER NOT NULL,
                        SHOTID INTEGER NOT NULL,
                        FOREIGN KEY (TABLEID) REFERENCES TTABLE,
                        FOREIGN KEY (SHOTID) REFERENCES Shot);""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS
                        Game
                        (GAMEID INTEGER PRIMARY KEY NOT NULL,
                        GAMENAME VARCHAR(64) NOT NULL);""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS
                        Player
                        (PLAYERID INTEGER PRIMARY KEY NOT NULL,
                        GAMEID INTEGER NOT NULL,
                        PLAYERNAME VARCHAR(64) NOT NULL,
                        FOREIGN KEY (GAMEID) REFERENCES Game);""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS CurrentPlayer(PLAYERID INTEGER PRIMARY KEY NOT NULL, PLAYERNAME VARCHAR(64));""")

        #self.cur.execute("""CREATE TABLE IF NOT EXISTS PlayerScore
        #                 (TURNID INTEGER PRIMARY KEY NOT NULL, PLAYERONENAME VARCHAR(64), PLAYERTWONAME VARCHAR(64), 
        #                 P1STATUS INTEGER, P2STATUS INTEGER, P1SCORE INTEGER, P2SCORE INTEGER);""")

        self.conn.commit()
        self.cur.close()

    def readTable(self, tableID):
        #Finds latest ball table and reads that table into an object
        self.cur=self.conn.cursor()
        data=self.cur.execute("""SELECT COUNT(TABLEID) FROM BallTable WHERE TABLEID=?""", (tableID+1,))
        for i in data.fetchall():
            if i[0]==0:
                return None
        #Inner join across BallTable, Ball and TTable to get accurate information. 
        data=self.cur.execute("""SELECT * FROM BALL INNER JOIN BallTable ON BALL.BALLID=BallTable.BALLID INNER JOIN TTABLE ON TTABLE.TABLEID=BallTable.TABLEID""")
        newTable=Table()
        #After making new table, writes information that matches with tableID found earlier into table object
        for i in data.fetchall():
            if i[7]==tableID+1:
                if i[4] is None and i[5] is None:
                    pos=Coordinate(float(i[2]), float(i[3]))
                    sb=StillBall(i[1], pos)
                    newTable+=sb
                    newTable.time=float(i[9])
                else:
                    velx=float(i[4])
                    vely=float(i[5])
                    pos=Coordinate(float(i[2]), float(i[3]))
                    vel=Coordinate(velx, vely)
                    speedB=phylib.phylib_length(vel)
                    if(speedB>VEL_EPSILON):
                        rb_accx=(float(velx)*-1/speedB)*DRAG
                        rb_accy=(float(vely)*-1/speedB)*DRAG
                    else:
                        rb_accx=0.0
                        rb_accy=0.0
                    acc=Coordinate(float(rb_accx), float(rb_accy))
                    rb=RollingBall(i[1], pos, vel, acc)
                    newTable+=rb
                    newTable.time=float(i[9])
        self.cur.close()
        self.conn.commit()
        return newTable
        
    def writeTable(self, table):
        self.cur=self.conn.cursor()
        #Inserting table into TTable, then keeping TableID for later
        self.cur.execute("""INSERT INTO TTABLE (TIME) VALUES (?)""", (table.time,))
        data=self.cur.execute("""SELECT TABLEID FROM TTABLE ORDER BY TABLEID DESC LIMIT 1""")
        tableID=data.fetchone()
        #For loop that inserts into ball and balltable for every ball in the table (regardless of type)
        for i in table:
            if isinstance(i, StillBall):
                self.cur.execute("""INSERT INTO BALL (BALLNO, XPOS, YPOS) VALUES (?, ?, ?)""", (i.obj.still_ball.number, i.obj.still_ball.pos.x, i.obj.still_ball.pos.y))
                self.cur.execute("""INSERT INTO BallTable (BALLID, TABLEID) VALUES ((SELECT BALLID FROM BALL ORDER BY BALLID DESC LIMIT 1), ? )""", (tableID) )
            elif isinstance(i, RollingBall):
                self.cur.execute("""INSERT INTO BALL (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ? , ? , ? , ? )""", (i.obj.rolling_ball.number, 
                i.obj.rolling_ball.pos.x, i.obj.rolling_ball.pos.y, i.obj.rolling_ball.vel.x, i.obj.rolling_ball.vel.y))
                self.cur.execute("""INSERT INTO BallTable (BALLID, TABLEID) VALUES ((SELECT BALLID FROM BALL ORDER BY BALLID DESC LIMIT 1), ?)""", (tableID))
        self.cur.close()
        self.conn.commit()
        #Returns tableID one less due to starting at 0 in python coding
        tableID=tableID[0]-1
        return tableID
    
    def writeShotCall(self, shotID, tableID):
        self.cur=self.conn.cursor()
        #Inserts shotID and tableID into TableShot
        self.cur.execute("""INSERT INTO TableShot (TABLEID, SHOTID) VALUES(?,?)""", (tableID+1, shotID))
        self.cur.close()
        self.conn.commit()
        

    # add an svg method here
    def close(self):
        #Closes cursor and connection
        #self.cur.close()
        self.conn.commit()
        self.conn.close()


class Game():
    #Member variables
    gameID=0
    gameName=None
    player1Name=None
    player2Name=None
    currentPlayer=None

    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        if (isinstance(gameID, int) and gameName is None and player1Name is None and player2Name is None):
            #Initializing member variables, then using gameID to find game and players in Game and Player tables
            playerCounter=0
            self.db=Database(reset=False)
            self.gameID=gameID
            self.db.createDB()
            self.db.cur=self.db.conn.cursor()
            data=self.db.cur.execute("""SELECT * FROM Game INNER JOIN Player ON Game.GAMEID=Player.GAMEID""")
            for game in data.fetchall():
                if(game[0]==self.gameID):
                    self.gameName=game[1]
                    if(playerCounter==0):
                        self.player1Name=game[4]
                        playerCounter+=1
                    else:
                        self.player2Name=game[4]
            self.db.conn.commit()
            self.db.cur.close()
        elif(isinstance(gameName, str) and isinstance(player1Name, str) and isinstance(player2Name, str) and gameID is None):
            #Writing Game and Player tables with Game name and player name information
            self.db=Database(reset=False)
            self.db.createDB()
            self.db.cur=self.db.conn.cursor()
            self.db.cur.execute("""INSERT INTO Game (GAMENAME) VALUES (?)""", (gameName,))
            self.db.cur.execute("""INSERT INTO Player (GAMEID, PLAYERNAME) VALUES ((SELECT GAMEID FROM Game ORDER BY GAMEID DESC LIMIT 1), ?)""", (player1Name,))
            self.db.cur.execute("""INSERT INTO Player (GAMEID, PLAYERNAME) VALUES ((SELECT GAMEID FROM Game ORDER BY GAMEID DESC LIMIT 1), ?)""", (player2Name,))
            self.db.conn.commit()
            self.db.cur.close()
        else:
            raise TypeError("Invalid Type of Some Kind")
        
    def shoot( self, gameName, playerName, table, xvel, yvel ):
        #Initializing member variables, then inner joining on Game and Player
        self.db.cur=self.db.conn.cursor()
        playerID=None
        shotID=None
        gameID=None
        data=self.db.cur.execute("""SELECT * FROM Game INNER JOIN Player ON Game.GAMEID=Player.GAMEID""")
        #For loop that finds the specified gameID and playerID using names of game and player
        for i in data.fetchall():
            if i[1]==gameName:
                gameID=i[0]
                if i[4]==playerName:
                    playerID=i[2]
                    break
        #If not found, return none
        if playerID is None or gameID is None:
            return None
        #Insert into Shot gameID and PlayerID, then get the shotID for later
        self.db.cur.execute("""INSERT INTO Shot (GAMEID, PLAYERID) VALUES (?, ?)""", (gameID, playerID))
        data=self.db.cur.execute("""SELECT SHOTID FROM Shot ORDER BY SHOTID DESC LIMIT 1""")
        for i in data.fetchall():
            shotID=i[0]
        #Finds cueBall in current table
        cueBall=table.cueBall()
        if cueBall is None:
            return None
        #Conversion of cueBall to rolling ball, regardless of what it was before
        if isinstance(cueBall, StillBall):
            posx=cueBall.obj.still_ball.pos.x
            posy=cueBall.obj.still_ball.pos.y
        elif isinstance(cueBall, RollingBall):
            posx=cueBall.obj.rolling_ball.pos.x
            posy=cueBall.obj.rolling_ball.pos.y
        cueBall.type=phylib.PHYLIB_ROLLING_BALL
        cueBall.obj.rolling_ball.number=0
        cueBall.obj.rolling_ball.pos.x=posx
        cueBall.obj.rolling_ball.pos.y=posy
        cueBall.obj.rolling_ball.vel.x=xvel
        cueBall.obj.rolling_ball.vel.y=yvel
        #After turning cueBall into a rolling ball, calculates acceleration
        vel=Coordinate(float(xvel), float(yvel))
        speed=phylib.phylib_length(vel)
        if(speed>VEL_EPSILON):
            rb_accx=(float(xvel)*-1/speed)*DRAG
            rb_accy=(float(yvel)*-1/speed)*DRAG
        else:
            rb_accx=0.0
            rb_accy=0.0
        acc=Coordinate(float(rb_accx), float(rb_accy))
        cueBall.obj.rolling_ball.acc=acc
        cueBall.obj.rolling_ball.acc.x=rb_accx
        cueBall.obj.rolling_ball.acc.y=rb_accy
        #Then makes a dummy table and a previous time for tracking in the loop
        new_table=table
        prevTime=table.time
        #While loop that keeps going until segment returns none
        frame=1
        html=""
        while(table):
            new_table=table.segment()

            if new_table is None:
                break
            #For loop that takes the individual frames at the FRAME_INTERVAL speed and writes them onto the table
            for i in range (math.floor(100 * (new_table.time-table.time))):

                    #Inverse of what was shown
                floatTime=i*FRAME_INTERVAL
                frameTable=table.roll(floatTime)
                frameTable.time=table.time+floatTime
                html+="""<g id=frame%d>""" % (frame)
                frame+=1
                html+=frameTable.svg()
                html+="</g>"
                
            #Updates previous time and table to make sure time and looping is correct
                
            prevTime=new_table.time
            table=new_table
            

        tableID=self.db.writeTable(table)
        self.db.writeShotCall(shotID, tableID)
        lastTable=table
        lastTable.time=table.time+math.floor(100*(prevTime-table.time))
        html+="""<g id=frame%d>""" % (frame)
        frame+=1
        html+=lastTable.svg()
        html+="</g>"

        self.db.cur.close()
        self.db.conn.commit()
        return html



