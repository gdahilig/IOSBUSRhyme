
from flask import Flask
from flask import request

from rhymer import Rhymer


app = Flask(__name__)
app.config.from_object(__name__)

rhymer = Rhymer()

@app.route("/rhyme.html")
def hello():
	parmFrom = request.args.get("from")
	cmd = request.args.get("cmd").lower()
	op1 = request.args.get("op1").lower()
	op2 = request.args.get("op2").lower()

	if len(cmd) == 0:
		return rhymer.help()
	if cmd in "n":
		return rhymer.next(parmFrom)

	if cmd in "r":
		print 'remove cmd'
		return rhymer.remove(parmFrom)

	if cmd in "rhyme":
		return rhymer.get(parmFrom, op1)

	if cmd in "learn":
		return rhymer.learn(parmFrom, op1,op2)
	return rhymer.help()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

