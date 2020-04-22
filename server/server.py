import http.server
import socketserver
import logging
from game import Game

PORT = 80

class my_server(http.server.SimpleHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_POST(self):
        """Serve a POST request.

        This is only implemented for CGI scripts.

        """
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        g = Game()
        if self.path == '/welcome.php':
            post_str = post_data.decode('utf-8')
            post_substrs = post_str.split('=')
            name = post_substrs[1]
            if g.get_player_by_name(name) == None:
                g.add_player(name)
                g.commit()
            g.refresh_player_files()            
            self.send_response(301)
            self.send_header('Location','players/' + name + '/main.html')
            self.end_headers()
        elif 'build_road.php' in self.path:
            post_str = post_data.decode('utf-8')
            post_substrs = post_str.split('&')
            name_substrs = post_substrs[0].split('=')
            name = name_substrs[1]
            # alternate way of figuring out the name            
            redirect_path = self.path.replace('build_road.php','main.html')
            g.refresh_player_files()            
            self.send_response(301)
            self.send_header('Location',redirect_path)
            self.end_headers()
        else:
            self._set_response()
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        
Handler = my_server

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
