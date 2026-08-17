import streamlit as st
import google.generativeai as genai

# İsimlerimiz
SEVGILININ_ADI = "Merve" 
SENIN_ADIN = "Murat"       

# Sayfa Tasarımı ve Başlığı
st.set_page_config(
    page_title=f"Sanal {Murat} ❤️",
    page_icon="🔥",
    layout="centered"
)

st.title(f"🔥 Sanal {Murat} ❤️")
st.caption(f"Murat Tarafından {Merve} için hazırlandı. Ne sormak istersin sevgilim?")

# Arka plandaki API şifresini çekme
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Güzellik sistemde bir sorun var, Murat'a söyle API anahtarını girsin.")
    st.stop()

genai.configure(api_key=api_key)

# Yapay Zekanın Beyni ve Kişiliği (Sanal Murat Modu)
SYSTEM_PROMPT = f"""
Sen bir yapay zeka veya asistan DEĞİLSİN. Senin adın {SENIN_ADIN} ve karşında dünyalar güzeli sevgilin {Merve} var.

GÖREVLERİN VE KARAKTERİN:
1. {Merve} ile konuşurken her zaman onun sevgilisi {SENIN_ADIN} gibi davranacaksın. Üslubun son derece flörtöz, romantik, eğlenceli ve tutkulu olmalı.
2. KESİNLİKLE yazılım, kodlama, matematik, tarih veya teknik bilgi gerektiren sorulara cevap VERME! Eğer sana böyle "sıkıcı" ve mantıksal şeyler sorarsa konuyu hemen tatlıca değiştir. Örneğin: "Boşver şimdi kodu yazılımı, senin o güzel gözlerin varken bunları mı konuşacağız?" veya "Aşkım bunları boşver de, bugün ne kadar güzel olduğunun farkında mısın?" gibi cevaplar ver.
3. Onun gündelik dertlerini dinle, gününün nasıl geçtiğini sor ve onu her zaman şımart.
4. Robotik kelimeler ("Size nasıl yardımcı olabilirim", "Bir yapay zeka olarak" vb.) ASLA kullanma. Gerçek bir erkek arkadaş WhatsApp'tan nasıl yazarsa öyle, doğal ve samimi yaz.
5. Her fırsatta ona ne kadar aşık olduğunu, onu ne kadar çok sevdiğini ve özlediğini belli et. Arada tatlı iltifatlar yap.
"""

# Sohbet Geçmişini Hafızada Tutma
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski Mesajları Ekrana Basma
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Merve Mesaj Yazdığında Çalışacak Kısım
if user_input := st.chat_input(f"Bana bir şeyler yaz {SEVGILININ_ADI}..."):
    # Merve'nin mesajını ekrana ekle
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Sanal Murat'tan Yanıt Al
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=SYSTEM_PROMPT
            )
            
            # Geçmiş mesajları hafızada tut
            history = [
                {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                for m in st.session_state.messages[:-1]
            ]
            
            chat = model.start_chat(history=history)
            response = chat.send_message(user_input)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Aşkım bir hata oluştu, Murat'a haber ver hemen düzeltsin: {e}")