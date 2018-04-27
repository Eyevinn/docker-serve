import SimpleHTTPServer

class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def send_head(self):
    path = self.translate_path(self.path)
    f = None
    if os.path.isdir(path):
      if not self.path.endswith('/'):
        self.send_response(301)
        self.send_header("Location", self.path + "/")
        self.end_headers()
        return None
      else:
        return self.list_directory(path)
    ctype = self.guess_type(path)
    try:
      f = open(path, 'rb')
    except IOError:
      self.send_error(404, "File not found")
      return None
    self.send_response(200)
    self.send_header("Content-Type", ctype)
    fs = os.fstat(f.fileno())
    self.send_header("Content-Length", str(fs[6]))
    self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
    self.send_header("Access-Control-Allow-Origin", "*")
    self.send_header("Cache-Control", "max-age=60")
    self.end_headers()
    return f

if __name__ == "__main__":
  import os
  import SocketServer
  PORT = 8080
  Handler = RequestHandler

  httpd = SocketServer.TCPServer(("0.0.0.0", PORT), Handler)

  print "serving at port", PORT
  httpd.serve_forever()