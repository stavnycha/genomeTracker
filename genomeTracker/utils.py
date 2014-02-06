import os

from genomeTracker.exceptions import *
from genomeTracker import app
from werkzeug import secure_filename

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
		   
def processFile(file):
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		content = file.read()
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return content
	else:
		raise ExtensionNotAllowedException()