from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/restaurant"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<a href='restaurant/new'>Make a New Restaurant!!</a>"

				restaurants = session.query(Restaurant)
				for restaurant in restaurants:
					output += "<p>%s</p>" % restaurant.name
					output += "<a href='#'>Edit</a>"
					output += "<br>"
					output += "<a href='#'>Delete</a>"	
					output += "</body></html>"

				self.wfile.write(output)
				return
			
			if self.path.endswith("/restaurant/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h2>Register a New Restaurant</h2>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/new'>"
				output += "<input name='newRestaurant' type='text' placeholder ='Creat a Restaurant'><input type='submit' value='Create'>"
				output += "</form></body></html>"
				self.wfile.write(output)
				return


		except IOError:
			self.send_error(404, "File not Found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/restaurant/new"):
				# ctype is foreign function library for Python
				# cgi = Common Gateway Interface
				# parse_header parses a MIME header (such as Content-Type) into a main value and a dictionary of parameters.
				ctype, pdict = cgi.parse_header(self.headers.getheader(
					'content-type'))

				# rfile contains an input stream, positioned at the start of the optional input data.

				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					newRestaurant = fields.get('newRestaurant')
			
					output = ""
					output += "<html><body>"
					output += "<h2> You just registered a restaurant bellow </h2>"
					output += "<h1> %s </h1>" % newRestaurant[0]
					output += "</body></html>"

					createdRestaurant = Restaurant(name = newRestaurant[0])
					session.add(createdRestaurant)
					sesssion.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurant')
					self.end_headers()

					# myFirstRestaurant = Restaurant(name = "Pizza Palace")
					# session.add(myFirstRestaurant)
					# sesssion.commit()

					self.wfile.write(output)

					print output
		except:
			pass

def main():
	try:
		port = 8000
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	# Built in exception in python that can be triggered when the user holds ctrl+c  
	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()



if __name__ == '__main__':
	main()