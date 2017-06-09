import web

urls = (
	'/hello', 'hello',
       )

class Handle(object):
    def __init__(self):
        pass
	def GET(self):
        web.stx.status=200
	    return 'hello world'

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
