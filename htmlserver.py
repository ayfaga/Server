from flask import Flask, request, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'RZD.html')

@app.route('/submit_order', methods=['POST'])
def submit_order():
    data = request.json 
    numvag = data.get('numvag', 'Не указано')
    numsit = data.get('numsit', 'Не указано')
    cartContent = data.get('cartContent', 'Не указано')
    print(cartContent)

    with open('./variable_txt/zakaz.txt', 'a', encoding='utf-8') as file:
        file.write(f'{numvag}, {numsit}, ({cartContent}) ПОЛУЧЕНО\n')
    return "Заказ сохранен!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
