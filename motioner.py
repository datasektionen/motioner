from flask import Flask, request, Response, render_template

from latex import build_pdf, LatexBuildError
from latex.jinja2 import make_env

app = Flask(__name__, static_url_path='/static')
texenv = make_env(loader=app.jinja_loader)

@app.route('/')
@app.route('/motion')
@app.route('/proposition')
@app.route('/reply')
def index(): return render_template('index.html')

@app.route('/motion.pdf', methods=['POST'])
def pdf():
    try:
        pdffile = build_pdf(get_tex())
        return Response(pdffile.stream, mimetype='application/pdf')
    except LatexBuildError as e:
        return Response(tex, mimetype='application/x-tex')

@app.route('/motion.tex', methods=['POST'])
def tex():
    return Response(get_tex(), mimetype='application/x-tex')

def get_tex():
    template = texenv.get_template('motion.tex')

    if request.form['document_type'] == 'motion':
        i_or_we = 'vi' if len(request.form.getlist('authors[]')) > 1 else 'jag'
    else:
        i_or_we = 'D-rektoratet'

    return template.render(
            i_or_we=i_or_we,
            document_type=request.form['document_type'],
            title=request.form['title'],
            meeting=request.form['meeting'],
            date=request.form['date'],
            background=request.form['background'],
            items=request.form.getlist('items[]'),
            authors=request.form.getlist('authors[]')
        ).replace('§', '\\S')


if __name__ == '__main__':
    app.run(debug=True)
