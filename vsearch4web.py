from flask import Flask, render_template, request, redirect, escape
from vsearch import search4letters

app = Flask(__name__)

#@app.route('/')
#def hello() -> str:
#    return 'Hello world from Flask!'

#@app.route('/')
#def hello() -> '302':
#    return redirect('/entry')

def log_request(req: 'flask_request', res: str) -> None:
	with open('vsearch.log', 'a') as log:
		#print(req, res, file=log)
		#print(str(dir(req)), res, file=log)
		#print(req.form, file=log, end='|')
		#print(req.remote_addr, file=log, end='|')
		#print(req.user_agent, file=log, end='|')
		#print(res, file=log)
		##print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')
		with open('vsearch.log') as log:
			#contents = log.readlines()
			contents = log.readlines()
		return escape(''.join(contents))

@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
	phrase = request.form['phrase']
	letters = request.form['letters']
	results = str(search4letters(phrase, letters))
	title = 'Here are your results:'

	log_request(request, results)

	return render_template('results.html', the_title = title, the_phrase = phrase, the_letters = letters, the_results = results,)


@app.route('/') #функция связана с двумя url (2 запроса - один ответ, вместо редиректа)
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')


@app.route('/viewlog')
def view_the_log() -> str:
	contents = []
	with open('vsearch.log') as log:
		for line in log:
			contents.append([])
			for item in line.split("|"):
				contents[-1].append(escape(item))
	#	contents = log.read()
	#return escape(contents)
	return str(contents)

if __name__ == '__main__': #__main__ переменная названия модуля (возвращается при запуске в зависимости от платформы)
	app.run(debug=True)
