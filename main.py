from app import create_app
from app.routes import shortener

app = create_app()
app.register_blueprint(shortener)

if __name__ == '__main__':
    app.run(debug=True)
