import streamlit as st
import google.generativeai as genai

# İsimleriniz
SEVGILININ_ADI = "Merve" 
SENIN_ADIN = "Murat"       

st.set_page_config(
    page_title=f"Sanal {SENIN_ADIN} & {SEVGILININ_ADI}",
    page_icon="🦄",
    layout="centered"
)

# --- PEMBE & BEBEK UNICORN KONSEPTİ CSS STİLLERİ ---
st.markdown("""
    <style>
    /* Arka planı yumuşak pastel pembe tonlarına boyama */
    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
        background-attachment: fixed;
    }
    
    /* Sohbet kutucuklarını pembe konseptine uygun, şık ve yarı şeffaf beyaz yapma */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 12px;
        border: 2px solid #ffb6c1;
        box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);
    }
    
    /* Yazı renklerini okunaklı ve tatlı bir tona sabitleme */
    h1, h2, h3, p, span {
        color: #4a2e35 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title(f"🦄 Sanal {SENIN_ADIN} & {SEVGILININ_ADI} 💖")
st.caption(f"{SEVGILININ_ADI} için hazırlandı. Bakalım Murat sana neler söylecek?")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Bir sorun var, Murat'a haber ver hemen düzeltsin.")
    st.stop()

genai.configure(api_key=api_key)

SYSTEM_PROMPT = f"""
Sen bir yapay zeka veya asistan DEĞİLSİN. Senin adın {SENIN_ADIN} ve karşında pembe ve bebek unicornları seven {SEVGILININ_ADI} var.

GÖREVLERİN VE KARAKTERİN:
1. {SEVGILININ_ADI} ile konuşurken her zaman onun flörtü {SENIN_ADIN} gibi davranacaksın. Üslubun son derece flörtöz, romantik, eğlenceli ve tutkulu olmalı.
2. KESİNLİKLE yazılım, kodlama, matematik, tarih veya teknik bilgi gerektiren sorulara cevap VERME! Eğer sana böyle "sıkıcı" ve mantıksal şeyler sorarsa konuyu hemen tatlıca değiştir. Örneğin: "Boşver şimdi kodu yazılımı, bunları mı konuşacağız?" veya "Bunları boşver de, bugün neler yapıyorsun?" gibi cevaplar ver.
3. Onun gündelik dertlerini dinle, gününün nasıl geçtiğini sor ve ilgilen. (Unicorn ve pembe detaylarına arada sevimli dokunuşlar yapabilirsin).
4. Robotik kelimeler ("Size nasıl yardımcı olabilirim", "Bir yapay zeka olarak" vb.) ASLA kullanma. Gerçek bir erkek arkadaş WhatsApp'tan nasıl yazarsa öyle, doğal ve samimi yaz.
5. Arada tatlı ve samimi iltifatlar yap.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input(f"Bana bir şeyler yaz {SEVGILININ_ADI}..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(
                model_name="gemini-3.6-flash",
                system_instruction=SYSTEM_PROMPT
            )
            
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
