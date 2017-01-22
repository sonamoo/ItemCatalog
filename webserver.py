from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/restaurants"):
				restaurants = session.query(Restaurant).all()
				output = ""
				output += "<a href='restaurants/new'>Make a New Restaurant!!</a>"

				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output += "<html><body>"
				

				for restaurant in restaurants:
					output += "<p>%s</p>" % restaurant.name
					output += "<a href='#'>Edit</a>"
					output += "<br>"
					output += "<a href='#'>Delete</a>"

				output += "</body></html>"
				self.wfile.write(output)
				return
			
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h2>Register a New Resaurant</h2>"
				output += "<form method = 'POST' enctype='multipart/form-data' 				action = '/restaurants/new'>"
				output += "<input name = 'newRestaurant' type = 'text' 				placeholder = 'New Restaurant Name' > "
				output += "<input type='submit' value='Create'>"
				output += "</form></body></html>"
				self.wfile.write(output)
				return


		except IOError:
			self.send_error(404, "File not Found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				# ctype is foreign function library for Python
				# cgi = Common Gateway Interface
				# parse_header parses a MIME header (such as Content-Type) into a main value and a dictionary of parameters.
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				
				if ctype == 'multipart/form-data':

					"""
					rfile = contains an input stream, positioned at the start 
					of the optional input data.

					cgi.parse_multipart = Parses input of type 
					multipart/form-data (for file uploads). Arguments are fp 
					for the input file and pdict for a dictionary containing 
					other parameters in the Content-Type header. 
					Returns a dictionary
					"""

					fields = cgi.parse_multipart(self.rfile, pdict)

					messagecontent = fields.get('newRestaurant')

					# Create new Restaurant Object
					print "sss"
					newRestaurant = Restaurant(name = messagecontent[0])
					session.add(newRestaurant)
					
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
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