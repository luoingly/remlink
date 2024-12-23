from app import init, DEBUG

app = init()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
