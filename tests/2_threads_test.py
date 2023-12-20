from flask import Flask, request
import threading
import queue

app = Flask(__name__)
data_queue = queue.Queue()

# Predefined variables
variables = {
    'var1': 'initial value 1',
    'var2': 'initial value 2',
    # Add more predefined variables here if needed
}


def variable_manager():
    global variables
    while True:
        # Update variables based on data from the API thread
        if not data_queue.empty():
            var_update = data_queue.get()
            variables.update(var_update)
            # Potentially send updates back to the API thread


def api_thread():
    app.run()


@app.route('/update_variable', methods=['POST'])
def update_variable():
    var_name = request.form['name']
    var_value = request.form['value']
    data_queue.put({var_name: var_value})
    return "Variable updated"


if __name__ == '__main__':
    variable_thread = threading.Thread(target=variable_manager)
    api_thread = threading.Thread(target=api_thread)

    variable_thread.start()
    api_thread.start()
