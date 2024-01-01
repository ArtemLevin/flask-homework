from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("calculation.html")


@app.post('/calculate/')
def calculate():
    num1 = int(request.form['num1'])
    num2 = int(request.form['num2'])
    calculateAction = request.form['calculateAction']
    calculationDict = {
        "Сложить": num1+num2,
        "Вычесть": num1-num2,
        "Умножить": num1*num2,
        "Разделить": num1/num2
    }
    return redirect(url_for('calculationResult', result=str(calculationDict[calculateAction])))


@app.route('/result/<result>')
def calculationResult(result):
    return render_template('calculationResult.html', result=result)


if __name__ == '__main__':
    app.run()