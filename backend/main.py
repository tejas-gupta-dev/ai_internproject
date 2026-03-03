from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from rag import retrieve
from escalation import should_escalate


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


persona_model = AutoModelForSequenceClassification.from_pretrained("../models/persona_model")
persona_tokenizer = AutoTokenizer.from_pretrained("../models/persona_model")

sent_model = AutoModelForSequenceClassification.from_pretrained("../models/sentiment_model")
sent_tokenizer = AutoTokenizer.from_pretrained("../models/sentiment_model")

persona_map = {0: "technical_expert", 1: "frustrated_user", 2: "business_executive"}
sentiment_map = {0: "negative", 1: "neutral", 2: "positive"}



def predict(model, tokenizer, text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1)
    confidence, predicted = torch.max(probs, dim=1)
    return predicted.item(), confidence.item()

def generate_reply(persona, context):
    if persona == "frustrated_user":
        return f"I understand your frustration. {context}"
    elif persona == "technical_expert":
        return f"Technical solution: {context}"
    else:
        return f"Business perspective: {context}"

def generate_pdf(chat_history, filename="chat_report.pdf"):
    doc = SimpleDocTemplate(filename)
    elements = []
    styles = getSampleStyleSheet()

    for entry in chat_history:
        text = f"{entry['sender']}: {entry['text']}"
        elements.append(Paragraph(text, styles["Normal"]))
        elements.append(Spacer(1, 0.3 * inch))

    doc.build(elements)
    return filename



@app.get("/download-pdf")
def download_pdf():
    return FileResponse("chat_report.pdf", media_type="application/pdf", filename="chat_report.pdf")



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    chat_history = []

    try:
        while True:
            message = await websocket.receive_text()

            

            persona_label, persona_conf = predict(persona_model, persona_tokenizer, message)
            sentiment_label, sent_conf = predict(sent_model, sent_tokenizer, message)

            persona = persona_map[persona_label]
            sentiment = sentiment_map[sentiment_label]

            
            
            if sentiment == "neutral" and persona == "frustrated_user":
                persona = "technical_expert"

            
            if persona_conf < 0.40:
                persona = "technical_expert"

            
            if "clarification" in message.lower():
                persona = "technical_expert"

            

            context = retrieve(message)
            if "clarification" in message.lower():
                reply = "Sure, please tell me what you would like clarification about."
            else:
                reply = generate_reply(persona, context)

            

            escalate = should_escalate(persona, sentiment)

            
            chat_history.append({"sender": "User", "text": message})
            chat_history.append({"sender": "Bot", "text": reply})

            response_data = {
                "persona": persona,
                "sentiment": sentiment,
                "confidence": round(persona_conf, 2),
                "reply": reply,
                "escalate": escalate
            }

            if escalate:
                generate_pdf(chat_history)
                response_data["escalation_message"] = "Escalation triggered. Human agent will review your case."
                response_data["pdf_download"] = "http://127.0.0.1:8000/download-pdf"

            await websocket.send_json(response_data)

    except Exception as e:
        print("WebSocket closed:", e)
        await websocket.close()
