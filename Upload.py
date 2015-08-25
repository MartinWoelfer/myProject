

# mainly copied from https://cherrypy.readthedocs.org/en/3.2.6/progguide/files/uploading.html

import os
localDir = os.path.dirname(__file__) # current working directory
absDir = os.path.join(os.getcwd(), localDir) # os.getcwd() : Return a string representing the current working directory.
import cherrypy

class FileUpload(object):
    @cherrypy.expose
    def index(self):
        #Open the index webpage
        return """
            <html>
                <body>
                <h2>Upload a file</h2>
                <link rel="stylesheet" href="stylesheet.css">
                <script type="text/javascript">

                    // Check for the various File API support.
                    if (window.File && window.FileReader && window.FileList && window.Blob) {
                    // Great success! All the File APIs are supported.
                    } else {
                        alert('The File APIs are not fully supported in this browser.');
                    }
                </script>

                    <form action="upload" method="post" enctype="multipart/form-data" name="uploadForm" id="uploadForm">
                        <div id="drop_zone">Drop files here</div>
                        <!-- Damit ich einen Parameter �bergeben kann -->
                        <input type="hidden" name="myFile" id="myFile" value="">
                        <script>
                            function handleFileSelect(evt) {
                                //Methoden damit der Normalablauf gestoppt wird
                                evt.stopPropagation();
                                evt.preventDefault();

                                //Ein File Array erstellen
                                var files = evt.dataTransfer.files;
                                //File aus dem Array nehmen
                                var file = files.item(0);
                                //zum testen
                                alert(file.name);
                                alert(file.size);
                                //value von dem versteckten input feld auf das File setzen (Dieser Schritt funktioniert anscheinend nicht)
                                document.getElementById("myFile").setAttribute('value', file);

                                alert(document.getElementById("myFile").value.name); //Gibt undefined aus -> funktioniert nicht :(
                                //Automatisches submitten bei Drag and Drop
                                document.getElementById('uploadForm').submit();
                            }

                            function handleDragOver(evt) {
                                evt.stopPropagation();
                                evt.preventDefault();
                                evt.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
                            }

                            // Setup the dnd listeners.
                            var dropZone = document.getElementById('drop_zone');
                            dropZone.addEventListener('dragover', handleDragOver, false);
                            dropZone.addEventListener('drop', handleFileSelect, false);
                        </script>
                    </form>
                </body>
            </html>
            """

    def upload(self, myFile):
        out = """<html>
	            <body>
		                myFile Size: %s kb<br />
		                myFile filename: %s<br />
		                myFile mime-type: %s
	                </body>
                </html>"""
        # Although this just counts the file length, it demonstrates
        # how to read large files in chunks instead of all at once.
        # CherryPy reads the uploaded file into a temporary file;
        # myFile.file.read reads from that.
        size = 0
        whole_data = bytearray() # Neues Bytearray
        while True:
            data = myFile.file.read(8192) #8192 entsprechen 8 KiB
            whole_data += data # Save data chunks in ByteArray whole_data

            if not data:
                break
            size += len(data)

            written_file = open(myFile.filename, "wb") # open file in write bytes mode
            written_file.write(whole_data) # write file

        #Nach dem Uploaden wird Daten ueber das geuploadete File geschrieben
        return out % (size / 1000, myFile.filename, myFile.content_type)
    upload.exposed = True


if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(FileUpload())
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(FileUpload())