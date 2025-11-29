import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from dotenv import load_dotenv
from datetime import datetime

# -----------------------------------------------------
# PAS DE CORRECTION → le texte doit rester intact
# -----------------------------------------------------
def smart_correct(text):
    return text   # NE RIEN CHANGER, IMPORTANT POUR LES SENTIMENTS


# Charger variables .env
load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "")
HF_MODEL_NAME = os.getenv("HF_MODEL_NAME", "cardiffnlp/twitter-roberta-base-sentiment-latest")
USE_GPU = int(os.getenv("USE_GPU", "0"))

logging.basicConfig(level=logging.INFO)

app = Flask(__name__, template_folder="templates")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sentiment.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# ---------------------- Base de données -------------------------
class Prediction(db.Model):
    __tablename__ = "predictions"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    corrected_text = db.Column(db.Text, nullable=False)
    label = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
# ----------------------------------------------------------------


# ---------------------- Chargement du modèle --------------------
def load_pipeline():
    device = 0 if USE_GPU else -1

    # Si un modèle local existe
    if MODEL_PATH and os.path.isdir(MODEL_PATH):
        try:
            tok = AutoTokenizer.from_pretrained(MODEL_PATH)
            model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
            return pipeline("sentiment-analysis", model=model, tokenizer=tok, device=device)
        except Exception as e:
            print("Erreur chargement modèle local :", e)

    # Modèle Roberta par défaut
    return pipeline(
        "sentiment-analysis",
        model=HF_MODEL_NAME,
        tokenizer=HF_MODEL_NAME,
        device=device
    )

nlp = load_pipeline()
# ----------------------------------------------------------------


# ---------------------- Normalisation label ---------------------
def normalize_result(res):
    mapping = {
        "LABEL_0": "negative",
        "LABEL_1": "neutral",
        "LABEL_2": "positive"
    }
    return mapping.get(res["label"], res["label"]), float(res["score"])

# ----------------------------------------------------------------


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict_single():
    data = request.get_json() or {}
    text = data.get("text")

    if not text or not text.strip():
        return jsonify({"error": "field 'text' required"}), 400

    # PAS DE CORRECTION
    corrected = smart_correct(text)

    # Analyse sentiment Roberta
    res = nlp(text[:512])[0]
    label, score = normalize_result(res)

    # Sauvegarde DB
    rec = Prediction(text=text, corrected_text=corrected, label=label, score=score)
    db.session.add(rec)
    db.session.commit()

    return jsonify({
        "id": rec.id,
        "original_text": text,
        "corrected_text": corrected,
        "label": label,
        "score": round(score, 4)
    })


@app.route("/stats")
def stats():
    total = Prediction.query.count()
    pos = Prediction.query.filter_by(label="positive").count()
    neg = Prediction.query.filter_by(label="negative").count()
    neu = Prediction.query.filter_by(label="neutral").count()

    return jsonify({
        "total": total,
        "positive": pos,
        "negative": neg,
        "neutral": neu
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
