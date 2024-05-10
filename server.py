
import sys;
import os;
import glob;
import cgi;
import Physics;
import math;
import json;
import random;
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl;

class MyHandler( BaseHTTPRequestHandler ):
    newGame=None
    
    def javaScript(self):
        javaScriptHtml = """<script>
        // Get the canvas element and its 2d context

        // Get the SVG elements
        const svg = document.getElementById('poolTable');
        const circle = document.getElementById('cueBall');
        const line = document.getElementById('line');
        const body = document.getElementById('body');
        var divContainer= document.getElementById('svg-container');
        let shooting=false;
        let lastX, lastY;
        let maxPower=1000;
        let lineX, lineY, lineX2, lineY2;
        let currentFrame=0
        let totalFrames=0

        

        body.addEventListener('mousemove', (e) => {
            if(!shooting) return;
            let mouseX = e.clientX-svg.getBoundingClientRect().left;
            let mouseY = e.clientY-svg.getBoundingClientRect().top;

            line.setAttribute('x1', circle.getAttribute('cx'));
            lineX=circle.getAttribute('cx')
            lineY=circle.getAttribute('cy')
            line.setAttribute('y1', circle.getAttribute('cy'));
            line.setAttribute('x2', ((mouseX-14.25)*2));
            line.setAttribute('y2', ((mouseY-14.25)*2));
            lineX2=((mouseX-14.25)*2)
            lineY2=((mouseY-14.25)*2)
        });

        body.addEventListener('mousedown', (e)=>{
            let mouseX = e.clientX-svg.getBoundingClientRect().left;
            let mouseY = e.clientY-svg.getBoundingClientRect().top;
            console.log(mouseX);
            console.log(mouseY);
            let cueBallX = parseFloat(circle.getAttribute('cx'));
            let cueBallY = parseFloat(circle.getAttribute('cy'));
            console.log(cueBallX);
            console.log(cueBallY);
            if (isInsideCircle(mouseX*2, mouseY*2, circle)){
                cueBallX = parseFloat(circle.getAttribute('cx'));
                cueBallY = parseFloat(circle.getAttribute('cy'));
                shooting=true;
                line.display="inline";
                [lastX, lastY]= [(cueBallX), (cueBallY)];
            }
        });

        body.addEventListener('mouseup', (e)=>{
            if (!shooting) return;
            shooting=false;
            line.display="none";
            let xDiff=lineX-lineX2
            let yDiff=lineY-lineY2
            let xVel=(xDiff/maxPower)*10000
            let yVel=(yDiff/maxPower)*10000
            
            if (xVel>10000){
                xVel=10000
            }else if(xVel<-10000){
                xVel=-10000
            }
            if (yVel>10000){
                yVel=10000
            }else if(yVel<-10000){
                yVel=-10000
            }
            console.log("xVel: ",xVel)
            console.log("yVel: ",yVel)
            const coordinates = [xVel, yVel];
            e.preventDefault();
            fetch('http://localhost:52891/shooting', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ coordinates})
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.htmlString);
                if (data!=null){
                    const tempElement = document.createElement('div');
                    tempElement.innerHTML = data.htmlString;

                    frames=Array.from(tempElement.querySelectorAll('g'));
                    totalFrames = frames.length;
                    console.log(frames)
                    function loadFrame(frameArray) {
                
                        // Hide all frames
                        if (currentFrame<totalFrames){
                            divContainer.innerHTML=frameArray[currentFrame].innerHTML;
                            currentFrame++;
                            setTimeout(loadFrame, 10, frameArray);
                        }else{
                            fetch('http://localhost:52891/updatingTable', {
                                method: 'POST',
                            })
                            .then(response => { 
                                if (response.status == "404") {
                                    return null;
                                } else if (!response.ok) {
                                    let err = new Error("HTTP status code: " + response.status);
                                    err.status = response.status;
                                    throw err;                     
                                } else {
                                    return response.text()
                                }
                            })
                            .then(data=>{
                                if (data!=null){
                                    console.log(data)
                                    divContainer.innerHTML=data
                                    
                                }
                                
                            })
                        }
                    }
                    loadFrame(frames)
                    fetch('http://localhost:52891/updatePlayer', {
                        method: 'POST',
                    })
                    .then(response => { 
                        if (response.status == "404") {
                            return null;
                        } else if (!response.ok) {
                            let err = new Error("HTTP status code: " + response.status);
                            err.status = response.status;
                            throw err;                     
                        } else {
                            return response.text()
                        }
                    })
                    .then(data=>{
                        if (data!=null){
                            const tempPlayer=document.getElementById('playerTurn')
                            console.log(data)
                            tempPlayer.innerHTML=data

                        
                        }
                        

                    })
                }
            })
            .catch(error => {
                console.error('Error:', error);
            })
        });

        function isInsideCircle(x, y, circle) {
            const circleX = parseFloat(circle.getAttribute('cx'));
            const circleY = parseFloat(circle.getAttribute('cy'));
            const radius = parseFloat(circle.getAttribute('r'));
            const distance = Math.sqrt(((x - circleX)-14.25) ** 2 + ((y - circleY)-14.25) ** 2);
            console.log("distance: ",distance)
            return distance <= radius+3;
        };

    </script> """
        return javaScriptHtml

    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/gamer.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        # check if the web-pages matches the list
        elif parsed.path.startswith('/table-') and parsed.path.endswith('.svg'):

            # retreive the HTML file & insert form data into the HTML file
            fp = open( '.'+parsed.path, 'rb' );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "image/svg+xml" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the browser
            self.wfile.write( content );
            fp.close();

        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

    def do_POST(self):
        # handle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );
        if parsed.path in [ '/display.html' ]:
            #Getting information
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                   );

            #Deleting previous svg files
            for filename in glob.glob('*.svg'):
                os.remove(filename)
            #Getting values and setting up entered values in shoot.html
            gameName=form.getvalue("gameName")
            playerOneName=form.getvalue("playerOne")
            playerTwoName=form.getvalue("playerTwo")
            db=Physics.Database(reset=True)
            db.createDB()
            newGame=Physics.Game(gameName=str(gameName), player1Name=str(playerOneName), player2Name=str(playerTwoName))
            table=Physics.Table()
            # 1 ball
            pos = Physics.Coordinate( 
                            Physics.TABLE_WIDTH / 2.0,
                            Physics.TABLE_WIDTH / 2.0,
                            );

            sb = Physics.StillBall( 1, pos );
            table += sb;

            # 2 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 2, pos );
            table += sb;

            # 3 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 3, pos );
            table += sb;

            #4 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+2.0),
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(12.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 4, pos );
            table += sb;

            #5 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(12)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 5, pos );
            table += sb;

            #6 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+2.0),
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(12)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 6, pos );
            table += sb;

            #7 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 + ((Physics.BALL_DIAMETER*3)/2)+8,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(27.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 7, pos );
            table += sb;

            #8 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 + ((Physics.BALL_DIAMETER+4)/2)+2,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(27)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 8, pos );
            table += sb;

            #9 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 - ((Physics.BALL_DIAMETER+4)/2)-2,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(27)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 9, pos );
            table += sb;

            #10 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 - ((Physics.BALL_DIAMETER*3)/2)-8,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(27)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 10, pos );
            table += sb;

            #11 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 + ((Physics.BALL_DIAMETER*2))+8,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(48.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 11, pos );
            table += sb;

            #12 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 + ((Physics.BALL_DIAMETER))+4,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(48.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 12, pos );
            table += sb;

            #9 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(48.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 13, pos );
            table += sb;

            #9 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER)-4,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(48.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 14, pos );
            table += sb;

            #9 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER*2)-8,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(48)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 15, pos );
            table += sb;

            # cue ball also still
            pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0,
                                    Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
            sb  = Physics.StillBall( 0, pos );

            table += sb
            fileName="table-0.svg"
            file=open(fileName, "w")
            svgString=table.svg()
            file.write(svgString)
            db.writeTable(table)
            file.close()
            #Making html based on all entered svg files, adding back button and making headings
            html="""<!DOCTYPE html>\n<html>\n"""
            html+="""<head>\n<button onclick="history.back()" style="font-size:50px">Back to main menu...</button>\n<h2 style= "text-align:center;font-size:55px">Billiards Simulator</h2>\n"""
            html+="""<title>Billiards Simulator</title>"""
            html+="""<style>
                    #svg-container {
                        position: relative;
                        top: 0;
                        bottom:0;
                        right: 0;
                        left: 0;
                        margin: auto;
                        text-align:center;
                        z-index:-10;
                    }

                    #line{
                        position: relative;
                        z-index:10;
                    }

                }
            </style></head>\n"""
            html+="""<body id="body">\n<div id="svg-container" style="text-align:center;">"""
            html+=svgString
            html+="""</div>"""
            html+=self.javaScript()
            html+="""<p style="text-align:left;font-size:30px">Player One:%s<span style="float:right;font-size:30px">""" % (playerOneName)
            html+="""Player Two: %s</span></p>""" % (playerTwoName)
            ran=random.randint(1,2)
            if (ran % 2 ==0):
                html+="""<p id="playerTurn" style="text-align:center;font-size:30px">Current Player's Turn: %s</p>""" % (playerOneName)
                currentPlayer=playerOneName
            else:
                html+="""<p id="playerTurn" style="text-align:center;font-size:30px">Current Player's Turn: %s</p>""" % (playerTwoName)
                currentPlayer=playerTwoName
            db.cur=db.conn.cursor()
            db.cur.execute("""INSERT INTO CURRENTPLAYER (PLAYERNAME) VALUES (?)""", (currentPlayer,))
            html+="""</body>\n<html>"""
            db.conn.commit()
            db.cur.close()
            db.close()
            self.send_response( 200 ); # OK response
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(html) );
            self.end_headers();

            # send it to the browser
            self.wfile.write( bytes( html, "utf-8" ) );
        
        elif self.path=='/shooting':
             # retreive the HTML file
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            coordinates=data['coordinates']
            db=Physics.Database(reset=False)
            db.cur=db.conn.cursor()
            data=db.cur.execute("""SELECT GAMEID FROM Game ORDER BY GAMEID DESC LIMIT 1""")
            for i in data.fetchall():
                gameID=i[0]
            aGame=Physics.Game(gameID=gameID)
            gameName=aGame.gameName
            data=db.cur.execute("""SELECT TABLEID FROM TTABLE ORDER BY TABLEID DESC LIMIT 1""")
            for i in data.fetchall():
                tableID=i[0]
            table=db.readTable(tableID-1)
            db.cur=db.conn.cursor()
            data=db.cur.execute("""SELECT PLAYERNAME FROM CURRENTPLAYER ORDER BY PLAYERID DESC LIMIT 1""")
            for i in data.fetchall():
                currentPlayer=i[0]
            #Get table
            htmlString = aGame.shoot(gameName, currentPlayer, table, coordinates[0], coordinates[1])
            db.conn.commit()
            db.cur.close()
            self.send_response( 200 );
            self.end_headers();
            self.wfile.write(json.dumps({'htmlString': htmlString}).encode('utf-8'))
        
        elif self.path=='/updatePlayer':
            db=Physics.Database(reset=False)
            db.cur=db.conn.cursor()
            data=db.cur.execute("""SELECT PLAYERID FROM Shot ORDER BY SHOTID DESC LIMIT 1""");
            for i in data.fetchall():
                PlayerNum=i[0]
            data=db.cur.execute("""SELECT * FROM PLAYER WHERE PLAYERID!=? ORDER BY GAMEID DESC LIMIT 1""", (PlayerNum,) )
            for i in data.fetchall():
                PlayerName=i[2]
            htmlString="""<p id="playerTurn" style="text-align:center;font-size:30px">Current Player's Turn: %s</p>""" % (PlayerName,)
            self.send_response( 200 );
            self.end_headers();
            self.wfile.write(bytes(str(htmlString).encode('utf-8')))

        elif self.path=='/updatingTable':
            db=Physics.Database(reset=False)
            db.cur=db.conn.cursor()
            data=db.cur.execute("""SELECT TABLEID FROM TTABLE ORDER BY TABLEID DESC LIMIT 1""");
            for i in data.fetchall():
                tableID=i[0]
            table=db.readTable(tableID-1)
            counter=0
            for ball in table:
                if isinstance(ball,Physics.StillBall):
                    if ball.obj.still_ball.number==0:
                        counter=1
            if counter==0:
                pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0,
                                    Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
                sb  = Physics.StillBall( 0, pos );
                table+=sb
            tableString=table.svg()
            self.send_response(200);
            self.end_headers();
            self.wfile.write(bytes(str(tableString).encode('utf-8')))
        
        #elif self.path=='/updatingScore':
        #    numbers=range(1,16)
        #    onTable=[]
        #    winner=0
        #    db=Physics.Database(reset=False)
        #    db.cur=db.conn.cursor()
        #    data=db.cur.execute("""SELECT TABLEID FROM TTABLE ORDER BY TABLEID DESC LIMIT 1""");
        #    for i in data.fetchall():
        #        tableID=i[0]
        #    table=db.readTable(tableID-1)
        #    counter=0
        #    for ball in table:
        #        if isinstance(ball,Physics.StillBall):
        #            for i in range(1,16):
        #                if ball.obj.still_ball.number==8:
                             #winner=1
        #                if ball.obj.still_ball.number==i:
        #                   numbers.remove(numbers[i])
        #    for i in numbers:
        #        data=db.cur.execute("""SELECT * FROM SHOT JOIN PLAYER ON SHOT.PLAYERID=PLAYER.PLAYERID ORDER BY SHOTID DESC LIMIT 1""");
        #        for j in data.fetchall():
        #            playerName=j[5]
        #            playerID=j[1]
        #        if (i<8):
        #           if playerID==1:
        #                html+="""<p style="text-align:left;font-size:30px">Player One:%s<span style="float:right;font-size:30px">""" % (playerOneName)
        #    data=db.cur.execute("""SELECT * FROM PLAYERSCORES ORDER BY TURNID DESC LIMIT 2""")
        #    for i in data.fetchall():
        #        p1Score=i[5]
        #        p2Score=i[6]
        #    if p1Score=7 and winner=1:
        #         htmlString="""<p id="playerTurn" style="text-align:center;font-size:30px">%s WINSSSSS</p>""" % (playerName,)

        
        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );





if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
