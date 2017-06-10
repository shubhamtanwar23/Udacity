from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

class webServerHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Hello!<h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
		    		  <h2>What would you like me to say?</h2><input name="message" type="text" >
		    		  <input type="submit" value="Submit"></form>'''
				output += "</body></html>"

				self.wfile.write(output.encode("utf-8"))
				print(output)
				return 

		except IOError:
			self.send_error(404,'File not found : %s' % self.path)


	def do_POST(self):
		try:
		    self.send_response(301)
		    self.send_header('Content-type', 'text/html')
		    self.end_headers()
		    print ("Header Send")
		    ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
		    print("Header parsed")
		    pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
		    if ctype == 'multipart/form-data':
		        fields = cgi.parse_multipart(self.rfile, pdict)
		        messagecontent = fields.get('message')
		    print ("Message value retrieved")
		    output = ""
		    output += "<html><body>"
		    output += " <h2> Okay, how about this: </h2>"
		    output += "<h1> %s </h1>" % str(messagecontent[0])
		    print("Half output done")
		    output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
		    		  <h2>What would you like me to say?</h2><input name="message" type="text" >
		    		  <input type="submit" value="Submit"></form>'''
		    output += "</body></html>"
		    self.wfile.write(output.encode("utf-8"))
		    print (output)
		    return
		except KeyboardInterrupt:
		    return



def main():
	try:
		port = 8080
		server = HTTPServer(("",port), webServerHandler)
		print("Web Server running on port %d" % port)
		server.serve_forever()

	except KeyboardInterrupt:
		print ("^C entered, stopping web server.....")
		server.socket.close()

if __name__ == '__main__':
	main()		