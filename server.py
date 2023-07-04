import sys
import io
import MolDisplay
from http.server import HTTPServer, BaseHTTPRequestHandler
import molecule
import molsql
import urllib
import cgi
import json

public_files = [ '/select.html', '/home.html', '/elements.html', '/elements.css', '/elements.js', '/home.css', '/sdf.html', '/sdf.js', '/viewer.js', '/display.js', '/display.html']
db = molsql.Database(reset=True)
db.create_tables()
   
class MyHandler(BaseHTTPRequestHandler):
    # variables for class
    curr_mol = "Empty"
    x = 0
    y = 0
    z = 0

    # do get method
    def do_GET(self):

        if self.path in public_files:   # make sure it's a valid file
            self.send_response(200) 
            self.send_header("Content-type", "text/html") # send header info

            fp = open( self.path[1:] ); 
            # [1:] to remove leading / so that file is found in current dir

            # load the specified file
            page = fp.read();
            fp.close();
            self.send_header("Content-length", len(page))
            self.end_headers()

            self.wfile.write(bytes(page, "utf-8")) # write to page, casted in bytes
        
        elif (self.path == "/select"):
            mols = db.get_molecule()

            if len(mols) == 0:
                self.send_response(204)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                return
            
            self.send_response(200) # OK
            self.send_header("Content-type", "application/json")
            self.end_headers()
            jsonf = json.dumps(mols)

            self.wfile.write(bytes(jsonf, "utf-8"))

        elif (self.path == '/createSVG'):
            if (MyHandler.curr_mol == ""):
                self.send_response(204)
                self.send_header("Content-type", "image/svg+xml")
                self.end_headers()
                return

            self.send_response( 200 ) 
            self.send_header("Content-type", "image/svg+xml") 
            self.end_headers() 

            length = int(self.headers.get('Content-Length', 0)) 

            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()
            MolDisplay.header += db.radial_gradients()
            molname = MyHandler.curr_mol
            mol = db.load_mol(molname)

            if (MyHandler.x != 0):
                mx = molecule.mx_wrapper(int(MyHandler.x), 0, 0)
                mol.xform( mx.xform_matrix )
            if (MyHandler.y != 0):
                mx = molecule.mx_wrapper(0, int(MyHandler.y), 0)
                mol.xform( mx.xform_matrix )
            if (MyHandler.z != 0):
                mx = molecule.mx_wrapper(0, 0, int(MyHandler.z))
                mol.xform( mx.xform_matrix )

            mol.sort()

            self.wfile.write(bytes(mol.svg(), "utf-8" ) ) 


        else:
            self.send_response(404) # else, send error response for path not found
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))

    def do_POST(self):

        if self.path == "/input_handler.html":
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )

            type = postvars['type'][0]

            if type == "insert":
                # Extract data from input boxes
                elementNum = postvars['elementNum'][0]
                elementCode = postvars['elementCode'][0]
                elementName = postvars['elementName'][0]
                col1 = postvars['color1'][0]
                col2 = postvars['color2'][0]
                col3 = postvars['color3'][0]
                radius = postvars['radius'][0]

                db['Elements'] = (elementNum, elementCode, elementName, col1[1:], col2[1:], col3[1:], radius)

                print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() )

                # Send response to client
                message = "Information has been stored in the database."
                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "text/plain" )
                self.send_header( "Content-length", len(message) )
                self.end_headers()
            
            elif type == "remove":
                removeElementName = postvars['removeElementName'][0]

                if db.remove_element(removeElementName) == 0:
                    print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() )

                    # Send response to client
                    message = "Information has been removed from the database."
                    self.send_response( 200 ); # OK
                    self.send_header( "Content-type", "text/plain" )
                    self.send_header( "Content-length", len(message) )
                    self.end_headers()
                
                else:
                    self.send_response(400)
        
        elif (self.path == "/uploadsdf"):

            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            name = form['mol-name'].value
            sdf = form['sdf-file'].value

            mol_name = form['mol-name'].value
            sdf_file = form['sdf-file'].value

            content = form['sdf-file'].headers['Content-Disposition']
            fName = cgi.parse_header(content)[1]['filename']
            ext = fName.split('.')[-1]

            if ext != 'sdf':
                response_body = "Invalid SDF file"
                response_length = len(response_body.encode('utf-8'))
                self.send_response(400)
                self.send_header("Content-type", "text/plain")
                self.send_header("Content-length", response_length)
                self.end_headers()
                self.wfile.write(response_body.encode('utf-8'))
                return

            temp = io.BytesIO(sdf)
            file = io.TextIOWrapper(temp)

            db.add_molecule(name, file)

            response_body = "molecule added"
            response_length = len(response_body.encode('utf-8'))
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", response_length)
            self.end_headers()
            self.wfile.write(response_body.encode('utf-8'))
        
        elif (self.path == "/displayPage"):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
          
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )
            
            name = str(postvars['moleculeName'][0])

            MyHandler.curr_mol = name

            response_body = "mol saved"
            response_length = len(response_body.encode('utf-8'))
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", response_length)
            self.end_headers()
            self.wfile.write(response_body.encode('utf-8'))
        
        elif (self.path == "/rotation"):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            postvars = urllib.parse.parse_qs(body.decode('utf-8'))

            print(postvars)
            
            plane = postvars['plane'][0]
            
            if (plane == "x"):
                MyHandler.x = (MyHandler.x + 10) % 360
            elif (plane == "y"):
                MyHandler.y = (MyHandler.y + 10) % 360
            elif (plane == "z"):
                MyHandler.z = (MyHandler.z + 10) % 360
       
            response_body = "rotation applied"
            response_length = len(response_body.encode('utf-8'))
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", response_length)
            self.end_headers()
            self.wfile.write(response_body.encode('utf-8'))
        

        else:
            self.send_response(404) # else, send error response
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))


httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
httpd.serve_forever()
