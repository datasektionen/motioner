from os import getenv
from requests import get, post

from flask import Flask, request, Response, render_template, session, redirect, jsonify

from werkzeug.urls import url_quote

from latex import build_pdf, LatexBuildError
from latex.jinja2 import make_env

app = Flask(__name__, static_url_path='/static')
app.secret_key = getenv('APP_SECRET_KEY') or 'some-secret'

LOGIN_API_KEY = getenv('LOGIN_API_KEY')
SPAM_API_KEY = getenv('SPAM_API_KEY')

texenv = make_env(loader=app.jinja_loader)

@app.route('/')
@app.route('/motion')
@app.route('/proposition')
@app.route('/reply')
@app.route('/change')
def index():
    session['callback_url'] = request.base_url
    return render_template('index.html', user=session.get('user'))

@app.route('/logout')
def logout():
    session['user'] = False
    return redirect(session['callback_url'])

@app.route('/login')
def login():
    redirect_url = 'https://login2.datasektionen.se/login?callback=' + url_quote(request.base_url) + '?token='
    token = request.values.get('token')
    if not session.get('user') and not token:
        print(redirect_url)
        return redirect(redirect_url)

    verify_url = 'https://login2.datasektionen.se/verify/{}'.format(token)
    params = {'format': 'json', 'api_key': LOGIN_API_KEY}
    response = get(verify_url, params=params)

    if response.status_code == 200:
        session['user'] = response.json()
    else:
        session['user'] = False

    return redirect(session['callback_url'])

@app.route('/motion.pdf', methods=['POST'])
def pdf():
    try:
        pdffile = build_pdf(get_tex())
        return Response(pdffile.stream,
            mimetype='application/pdf',
            headers={'Content-Disposition': 'attachment; filename=motion.pdf'}
        )
    except LatexBuildError as e:
        return Response(tex, mimetype='application/x-tex')

@app.route('/motion.tex', methods=['POST'])
def tex():
    return Response(get_tex(), mimetype='application/x-tex')

@app.route('/mail', methods=['POST'])
def mail():
    if not session.get('user'):
        return 'Ooooooh you can\'t do that!'

    try:
        tex = get_tex()
        pdffile = build_pdf(tex)

        url = 'https://spam.datasektionen.se/api/sendmail'
        post_data = {
            'subject': f'{request.form["document_type"]} från {session["user"]["first_name"]}',
            'from': 'no-reply@datasektionen.se',
            'to': 'drek@d.kth.se',
            'content': get_email(),
            'key': SPAM_API_KEY
        }

        post_files = [
            ('attachments[]', ('motion.tex', tex, 'application/x-tex')),
            ('attachments[]', ('motion.pdf', pdffile.stream, 'application/pdf'))]
        r = post(url, data=post_data, files=post_files)

        if r.status_code == 200:
            return jsonify(r.json())
        else:
            return jsonify({'error': 'Failed to send mail'})

    except LatexBuildError as e:
        return jsonify({'error': 'Failed to build PDF'})

def i_or_we():
    if request.form['document_type'] == 'motion':
        return 'vi' if len(request.form.getlist('authors[]')) > 1 else 'jag'
    else:
        return 'D-rektoratet'

def get_tex():
    template = texenv.get_template('motion.tex')

    return template.render(
            i_or_we=i_or_we(),
            document_type=request.form['document_type'],
            title=request.form['title'],
            meeting=request.form['meeting'],
            date=request.form['date'],
            background=request.form['background'],
            items=request.form.getlist('items[]'),
            authors=request.form.getlist('authors[]')
        ).replace('§', '\\S')

def get_email():
    return render_template('email.md',
        **session['user'],
        i_or_we=i_or_we(),
        document_type=request.form['document_type'],
        title=request.form['title'],
        meeting=request.form['meeting'],
        date=request.form['date'],
        background=request.form['background'],
        items=request.form.getlist('items[]'),
        authors=request.form.getlist('authors[]'))

if __name__ == '__main__':
    app.run(debug=True, port=int(getenv('PORT')))
