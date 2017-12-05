from flask import Flask, request, jsonify

app = Flask('test')

@app.route('/', methods=["POST","GET"])
def index():
    print(request.form)
    response = {"status":"success"}
    response['method'] = request.method
    response['body'] = []
    response['args'] = []

    for key, value in request.args.items():
        response['args'].append({key:value})

    if request.method == "GET":
        pass

    if request.method == "POST":
        for key, value in request.form.items():
            response['form_type'] = ""
            response['body'].append({key:value})

        # for key, value in request.files.items():
        #     print(key, value)

    return jsonify(response)

app.run()