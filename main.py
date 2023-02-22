from app import create_app
from app.routes.user import user
from app.routes.workshop import workshop
from flask import send_from_directory, url_for, redirect
app = create_app('development')

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(workshop, url_prefix='/workshop')

@app.route('/')
def index():
    return redirect( url_for('user.loginGet') )

@app.route('/serve-file/<fileDirectory>/<fileName>', methods=['GET'])
def display_files(fileDirectory, fileName):
    # filePath = fileDirectory + '/' + fileName
    return send_from_directory( fileDirectory, fileName, as_attachment=True)

if __name__ == "__main__":
    app.run( debug = True, port = 5555 )