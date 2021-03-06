from sanic import Sanic
from sanic.response import json
from pathlib import os
from datetime import datetime
from service.ocr import pdf2text

import jinja2
import jinja2_sanic

app = Sanic("sanic_jinja2_render")

config = {}
config["upload"] = "./tests/uploads"


@app.route('/upload', methods=['POST'])
def post_json(request):
    if not os.path.exists(config["upload"]):
        os.makedirs(config["upload"])
    test_file = request.files.get('file')
    file_parameters = {
        'body': test_file.body,
        'name': test_file.name,
        'type': test_file.type,
    }
    if file_parameters['name'].split('.')[-1] == 'pdf':
        file_path = f"{config['upload']}/{str(datetime.now())}.pdf"
        with open(file_path, 'wb') as f:
            f.write(file_parameters['body'])
        f.close()
        print('file wrote to disk', file_path)
        ocr_response = pdf2text(file_path)
        return json({"received": True, "file_names": request.files.keys(), "success": True})
    else:
        return json({"received": False, "file_names": request.files.keys(), "success": False, "status": "invalid file uploaded"})


if __name__ == '__main__':
    app.run()
