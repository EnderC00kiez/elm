from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort, send_from_directory
import os
from json import load
from werkzeug.exceptions import HTTPException


from jinja2 import TemplateNotFound

# load config
with open('settings.json') as config_file:
    config = load(config_file)

app = Flask(__name__, root_path=os.path.dirname(os.path.abspath(__file__)))

# inject headers defined in config
@app.after_request
def add_headers(r):
    """
    Adds headers from settings.json's http-headers
    """
    for header, value in config['http-headers'].items():
        r.headers[header] = value
    return r

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/returnerror/<erorrcode>')
def returnerror(errorcode):
    try:
        abort(int(errorcode))
    except:
        abort(500)

@app.route('/teapot')
def teapot():
    return """<!DOCTYPE html>
    <h3 style="text-align: center">I'm a little teapot<br>
Short and stout<br>
Here is my handle<br>
Here is my spout<br>
When I get all steamed up<br>
I just shout<br>
Tip me over and pour me out<br>

I'm a very special pot<br>
It's true<br>
Here's an example of what I can do<br>
I can turn my handle into a spout<br>
Tip me over and pour me out<br>

I'm a little teapot<br>
Short and stout<br>
Here is my handle<br>
Here is my spout<br>
When I get all steamed up<br>
I just shout<br>
Tip me over and pour me out<br>

I'm a very special pot<br>
It's true<br>
Here's an example of what I can do<br>
I can turn my handle into a spout<br>
Tip me over and pour me out</h3>""", 418

# if customerrorpages is true, return error from templates/error.html. pass error and request page
if config['custom-error-pages']:
    @app.errorhandler(HTTPException)
    def page_not_found(e):
        return render_template('error.html', error=e, request=request.path, websiteuri=request.base_url, statuscode=e.code), e.code

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<page>')
def dynamicpage(page):
    pages = []
    if not page.endswith('.redir'):
        # if page dosn't have a period in it
        if not '.' in page:
            # scan for pages with same filename, but if there are multiple, return 422
            for f in os.listdir(os.path.join(app.root_path, 'templates')):
                if f.startswith(page):
                    pages.append(f)
            if len(pages) > 1:
                abort(422)
            elif len(pages) == 1:
                page = pages[0]
    # if there are no files with the same name, return 404
    if not page in os.listdir(os.path.join(app.root_path, 'templates')):
        abort(404)
    return render_template(page)

                
if __name__ == '__main__' and config['werkzeug-server']:
    app.run(host='0.0.0.0', port=80, debug=config['werkzeug-debug'])
    
