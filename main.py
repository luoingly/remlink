from app import init, DEBUG

app = init()

if __name__ == '__main__':
    app.run(debug=DEBUG)
