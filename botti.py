python


import feedparser
import smtplib
import os
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
SOURCES = {
    "🌍 Globaali (Google News)": "[news.google.com](https://news.google.com/rss/search?q=maritime+cyber+security+when:24h&hl=en-US&gl=US&ceid=US:en)",
    "🇫🇮 Suomi (Kyberturvallisuuskeskus)": "[kyberturvallisuuskeskus.fi](https://www.kyberturvallisuuskeskus.fi/fi/rss.xml)",
    "🇪🇺 EU (ENISA)": "[enisa.europa.eu](https://www.enisa.europa.eu/publications/RSS)"
}
KRIITTISET_SANAT = ["satama", "merenkulku", "laiva", "väylä", "logistiikka", "maritime", "port", "vessel", "shipping"]
def laheta_sahkoposti(aihe, html_viesti):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = aihe
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.attach(MIMEText(html_viesti, "html"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("Sähköposti lähetetty onnistuneesti.")
    except Exception as e:
        print(f"Virhe sähköpostin lähetyksessä: {e}")
def keraa_uutiset():
    tanaan = datetime.datetime.now().strftime("%d.%m.%Y")
    otsikko = f"Merenkulun kyberkatsaus | {tanaan}"
    
    html_viesti = f'<div style="font-family: Arial, sans-serif; color: #333;"><h2 style="color: #004481;">🚢 Merenkulun kyberkatsaus | {tanaan}</h2>'
    uutisia_loytyi = False
    for kategoria, url in SOURCES.items():
        feed = feedparser.parse(url)
        suodatetut_uutiset = []
        for entry in feed.entries:
            if kategoria.startswith("🌍") or any(s in entry.title.lower() or s in entry.get('summary', '').lower() for s in KRIITTISET_SANAT):
                suodatetut_uutiset.append(f'<li><a href="{entry.link}" style="text-decoration: none; color: #1a0dab;">{entry.title}</a></li>')
        if suodatetut_uutiset:
            uutisia_loytyi = True
            html_viesti += f'<h3 style="border-bottom: 1px solid #ddd; padding-bottom: 5px;">{kategoria}</h3><ul style="line-height: 1.6;">' + "".join(suodatetut_uutiset[:7]) + "</ul>"
    if not uutisia_loytyi:
        html_viesti += "<p>Ei uusia merkittäviä havaintoja viimeisen 24 tunnin ajalta.</p>"
        
    return otsikko, html_viesti + "</div>"
if __name__ == "__main__":
    aihe, sisalto = keraa_uutiset()
    laheta_sahkoposti(aihe, sisalto)
