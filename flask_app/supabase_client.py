
import requests

from datetime import datetime

SUPABASE_URL ="https://gxihhetiihlwfoocvxtu.supabase.co"

SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd4aWhoZXRpaWhsd2Zvb2N2eHR1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODMzNTQ5NTcsImV4cCI6MjA5ODkzMDk1N30.IqDAC8ROCIA26znp2TebzXZXl7IggpS95SLQ1Laj_gc"
def registrar_evento(dispositivo: str, evento: str) -> bool:

    url = f"{SUPABASE_URL}/rest/v1/eventos"

    headers = {

        "apikey": SUPABASE_KEY,

        "Authorization": f"Bearer {SUPABASE_KEY}",

        "Content-Type": "application/json",

        "Prefer": "return=minimal",

    }

    data = {

        "dispositivo": dispositivo,

        "evento": evento,

        "fecha_hora": datetime.now().isoformat(),

    }

    try:

        r = requests.post(url, json=data, headers=headers, timeout=5)

        return r.status_code in (200, 201)

    except Exception as e:

        print("Error registrando en Supabase:", e)

        return False



                                                                                   
