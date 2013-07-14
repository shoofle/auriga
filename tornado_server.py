import tornado.ioloop
import tornado.web


application = tornado.web.Application([
	(r"/(.*)", tornado.web.StaticFileHandler, {"path":"./"})
], debug=True)

if __name__ == "__main__":
	application.listen(80)
	tornado.ioloop.IOLoop.instance().start()

