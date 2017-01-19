from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import sqlite3

import cgi

conn = sqlite3.connect('restaurantmenu.db')
c = conn.cursor()


class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "Hello!"
				output += "<form method='Post' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='submit'> </form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "&#161Hola <a href = '/hello'>Back to Hello</a>"
				output += "<form method='Post' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='submit'> </form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
			
			
			if self.path.endswith("/restaurant"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				QUERY = "SELECT * FROM Restaurant;"

				c.execute(QUERY)
				restaurants = c.fetchall()
				

				output = "<h2>hello</h2>"
				for restaurant in restaurants :
					output = "<h2>%s</h2>" % restaurant[3]
				self.wfile.write(output)
				return

		except IOError:
			self.send_error(404, "File not Found %s" % self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.end_headers()

			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				messageContent = fields.get('message')

				output = ""
				output += "<html><body>"
				output += " <h2> Okay, how about this: </h2>"
				output += "<h1> %s </h1>" % messageContent[0]

				output += "<form method='Post' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='submit'> </form>"
				output += "</body></html>"
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