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
        elif 'refresh.php' in self.path:
            post_str = post_data.decode('utf-8')
            post_substrs = post_str.split('&')
            name_substrs = post_substrs[0].split('=')
            name = name_substrs[1]
            #clear player's ret msg
            player = g.get_player_by_name(name)
            g.set_ret_msg(player['id'],'')
            g.commit()
            # alternate way of figuring out the name            
            redirect_path = self.path.replace('refresh.php','main.html')
            g.refresh_player_files()            
            self.send_response(301)
            self.send_header('Location',redirect_path)
            self.end_headers()
        elif 'status.php' in self.path:
            post_str = post_data.decode('utf-8')
            post_substrs = post_str.split('&')
            name_substrs = post_substrs[0].split('=')
            name = name_substrs[1]
            status_substrs = post_substrs[1].split('=')
            status = status_substrs[1]           
            #set player's ret msg
            player = g.get_player_by_name(name)
            g.set_status_msg(player['id'],status)
            g.commit()
            # alternate way of figuring out the name            
            redirect_path = self.path.replace('status.php','main.html')
            g.refresh_player_files()            
            self.send_response(301)
            self.send_header('Location',redirect_path)
            self.end_headers()            
        elif 'roll_dice.php' in self.path:
            post_str = post_data.decode('utf-8')
            post_substrs = post_str.split('&')
            name_substrs = post_substrs[0].split('=')
            name = name_substrs[1]
            g.roll_dice(name)
            g.commit()
            # alternate way of figuring out the name            
            redirect_path = self.path.replace('roll_dice.php','main.html')
            g.refresh_player_files()            
            self.send_response(301)
            self.send_header('Location',redirect_path)
            self.end_headers()            
        elif 'build_village.php' in self.path:
            post_str = post_data.decode('utf-8')
            post_substrs = post_str.split('&')
            name_substrs = post_substrs[0].split('=')
            name = name_substrs[1]
            at_substrs = post_substrs[1].split('=')
            atstr = at_substrs[1]
            g.build_village(name,atstr)
            g.commit()
            # alternate way of figuring out the name            
            redirect_path = self.path.replace('build_village.php','main.html')
            g.refresh_player_files()            
            self.send_response(301)
            self.send_header('Location',redirect_path)
            self.end_headers()
        elif 'build_city.php' in self.path:
            post_str = post_data.decode('utf-8')
            post_substrs = post_str.split('&')
            name_substrs = post_substrs[0].split('=')
            name = name_substrs[1]
            at_substrs = post_substrs[1].split('=')
            atstr = at_substrs[1]
            g.build_city(name,atstr)
            g.commit()
            # alternate way of figuring out the name            
            redirect_path = self.path.replace('build_city.php','main.html')
            g.refresh_player_files()            
            self.send_response(301)
            self.send_header('Location',redirect_path)
            self.end_headers()            
        elif 'build_road.php' in self.path:
            post_str = post_data.decode('utf-8')
            post_substrs = post_str.split('&')
            name_substrs = post_substrs[0].split('=')
            name = name_substrs[1]
            from_substrs = post_substrs[1].split('=')
            fromstr = from_substrs[1]
            to_substrs = post_substrs[2].split('=')
            tostr = to_substrs[1]
            g.build_road(name,fromstr,tostr)
            g.commit()
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
