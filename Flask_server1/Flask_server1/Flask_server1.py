import flask
import werkzeug
import time
import face_recognition
from PIL import Image, ImageDraw

image_of_marian = face_recognition.load_image_file('./img/cunoscuti/bill.jpg')
marian_face_encoding = face_recognition.face_encodings(image_of_marian)[0]

image_of_marian1 = face_recognition.load_image_file('./img/cunoscuti/elon.jpg')
marian1_face_encoding = face_recognition.face_encodings(image_of_marian1)[0]



#  Creare vector de nume persoane recunoscute
known_face_encodings = [
  marian_face_encoding,
  marian1_face_encoding,
 
]

known_face_names = [
  "bill ",
  "elon",
  
]
app = flask.Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def handle_request():

    e=0
    n=0
    files_ids = list(flask.request.files)
    print("\nNumber of Received Images : ", len(files_ids))
    image_num = 1
    for file_id in files_ids:
        print("\nSaving Image ", str(image_num), "/", len(files_ids))
        imagefile = flask.request.files[file_id]
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        print("Image Filename : " + imagefile.filename)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        imagefile.save(timestr+'_'+filename)
        image_num = image_num + 1
    print("\n")
    print( "Image(s) Uploaded Successfully. Come Back Soon.")

    #incarcam imaginea pentru testare
    test_image = face_recognition.load_image_file( timestr+'_'+ filename)
    # Cautare fatain imagine
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)

    # Convertim in PIL 
    pil_image = Image.fromarray(test_image)

    # Cream o instanta ImageDraw
    draw = ImageDraw.Draw(pil_image)

    # Cautare fete in imaginea de cautare
    for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    name = "Unknown Person"

    # Stabilim cerintele in functie de cautare 
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]
        e=1
    else:
        n=1
         #Afisam un rezultat, aici putem modifica cu return pentru a trimite raspuns in aplicatie 
    if e==1:
        return("Persoana gasita!")
    elif n==1:
        return("Persoana negasita!")
    return("Nu a reusit")

 

app.run(host="0.0.0.0", port=5000, debug=True)



