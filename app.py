import os
import tornado.ioloop
import tornado.web
import tornado.log
import psycopg2



from jinja2 import \
  Environment, PackageLoader, select_autoescape
ENV = Environment(
  loader=PackageLoader('myapp', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)
class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))

class MainHandler(TemplateHandler):
  def get (self, page='index'):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    page = page + '.html'
    conn = psycopg2.connect("dbname=blog_db user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT * FROM post JOIN authors ON authors.id = post.author_id;")
    all_data = cur.fetchall()
    self.render_template(page, {'all_data': all_data})
    cur.close()
    conn.close()


class BlogPostHandler(TemplateHandler):
    def get (self, slug):
        self.set_header(
        'Cache-Control',
        'no-store, no-cache, must-revalidate, max-age=0')
        conn = psycopg2.connect("dbname=blog_db user=postgres")
        cur = conn.cursor()
        cur.execute("SELECT * FROM post WHERE slug = %(slug)s", {'slug':slug})
        posts = cur.fetchone()
        print(posts)
        print(type(posts))
        self.render_template("post.html", {'posts':posts})
        cur.close()
        conn.close()

def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/(authors)", MainHandler),
    (r"/post/(.*)", BlogPostHandler),
    (r"/static/(.*)", 
      tornado.web.StaticFileHandler, {'path': 'static'}),
  ], autoreload=True)


if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '8000')))
  tornado.ioloop.IOLoop.current().start()