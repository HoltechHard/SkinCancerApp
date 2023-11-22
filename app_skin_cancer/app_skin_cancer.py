from flask import Flask, render_template, request, jsonify
from models.model import Patient, TypeImage, Scores
from controllers.config import settings

app = Flask(__name__)

@app.route('/')

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

# classification template
@app.route('/diagnosis/classification', methods=['GET', 'POST'])
def classification():
    data = None
    url_image = None

    # register patient
    if request.method == 'POST':
        # data from frmPatientData
        full_name = request.form.get("txtFullName")
        age = request.form.get("txtAge")
        anatomy = request.form.get("txtAnatomy")
        sex = request.form.get("gender")
        type_image = request.form.get("cboTypeImage")

        print(f"type image: {type_image}")

        # data from frmImageUpload
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':                
                url_image = f"static/storage/{file.filename}"
                file.save(url_image)

        patient = Patient(None, full_name, age, anatomy, sex, None, None, url_image, type_image)
        patient.insert_patient()

        last_patient = Patient.recover_patient_id()
        print(f'id query: {last_patient}')

        # generate prediction
        from controllers.vit_controller import vit_inference
        class_pred, label_pred, probs = vit_inference.predict(patient.url_image)

        # save prediction
        Patient.save_patient_prediction(last_patient, label_pred, probs[int(class_pred)])

        # save scores
        for index, prob in enumerate(probs):
            score = Scores(index + 1, last_patient, prob)
            score.insert_scores()

        # collect all data to asynchronous jquery sending
        data = {
            "class_pred": int(class_pred),
            "label_pred": label_pred,
            "prob_pred": probs[int(class_pred)],
            "probs": probs,
            "classes": settings["class_names"]
        }

        return jsonify(data)
    
    # show content of web page and combo box data if is not register
    return render_template("diagnosis/classification.html", 
                            lst_type_imgs = TypeImage.generate_type_img(), data = data)

# reports template
@app.route('/reports/patient_reports', methods=['GET', 'POST'])
def reports():

    # collect and process id-patient data
    if request.method == "POST":
        # id patient data
        id_patient = request.form.get("id_patient")
        
        # recover the url of image
        url_image = Patient.generate_searched_patient(id_patient)[0]["url_image"]

        # get the prob scores
        lst_scores = []
        for i in range(7):
            lst_scores.append(Scores.generate_scores(id_patient)[i]["prob_score"])

        # collect all data to asynchronous jquery sending
        data = {
            "url_image": url_image,
            "type_cancer": settings["class_names"],
            "prob_scores": lst_scores
        }

        return jsonify(data)

    # show list of patients if not press button
    return render_template("reports/reports.html", 
                           lst_patients = Patient.generate_patient())

if __name__ == "__main__":
    app.run(debug = True)

