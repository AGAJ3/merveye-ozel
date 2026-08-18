import streamlit as st
import google.generativeai as genai

# İsimleriniz
SEVGILININ_ADI = "Merve" 
SENIN_ADIN = "Murat"       

st.set_page_config(
    page_title=f"Sanal {SENIN_ADIN} ❤️",
    page_icon="🦄",
    layout="centered"
)

# --- PEMBE, BEBEK UNICORN & UÇUŞAN TANECİK ANİMASYONLARI ---
st.markdown("""
    <style>
    /* Arka plan yumuşak pastel pembe geçişi */
    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
        background-attachment: fixed;
    }
    
    /* Sohbet kutucukları (Glassmorphism stili) */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.88);
        border-radius: 18px;
        padding: 14px;
        border: 2px solid #ffb6c1;
        box-shadow: 0 6px 20px rgba(255, 182, 193, 0.4);
    }
    
    /* Metin renkleri */
    h1, h2, h3, p, span {
        color: #4a2e35 !important;
    }

    /* UÇUŞAN UNICORN VE KALPLERİN ANİMASYONU */
    .unicorn-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none; /* Tıklamayı engellemez */
        z-index: 9999;
        overflow: hidden;
    }

    .particle {
        position: absolute;
        bottom: -60px;
        font-size: 30px;
        animation: floatUp 7s linear infinite;
        opacity: 0;
    }

    /* Farklı pozisyon ve süre gecikmeleri */
    .p1  { left: 5%;  animation-duration: 6s;  animation-delay: 0s; }
    .p2  { left: 18%; animation-duration: 8s;  animation-delay: 1s; }
    .p3  { left: 32%; animation-duration: 7s;  animation-delay: 3s; }
    .p4  { left: 45%; animation-duration: 9s;  animation-delay: 2s; }
    .p5  { left: 60%; animation-duration: 6s;  animation-delay: 4s; }
    .p6  { left: 73%; animation-duration: 8s;  animation-delay: 1.5s; }
    .p7  { left: 88%; animation-duration: 7s;  animation-delay: 3.5s; }

    @keyframes floatUp {
        0% {
            transform: translateY(0) rotate(0deg) scale(0.8);
            opacity: 0;
        }
        20% {
            opacity: 0.9;
        }
        80% {
            opacity: 0.9;
        }
        100% {
            transform: translateY(-115vh) rotate(360deg) scale(1.2);
            opacity: 0;
        }
    }
    </style>

    <!-- Arka Planda Uçuşan Elemanlar -->
    <div class="unicorn-bg">
        <div class="particle p1">🦄</div>
        <div class="particle p2">💖</div>
        <div class="particle p3">🦄</div>
        <div class="particle p4">✨</div>
        <div class="particle p5">🦄</div>
        <div class="particle p6">💖</div>
        <div class="particle p7">🦄</div>
    </div>
""", unsafe_allow_html=True)

st.title(f"🔥 Sanal {SENIN_ADIN} ❤️")
st.caption(f"{SENIN_ADIN} Tarafından {SEVGILININ_ADI} için hazırlandı. Ne sormak istersin?")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Bir sorun var, Murat'a haber ver hemen düzeltsin.")
    st.stop()

genai.configure(api_key=api_key)

SYSTEM_PROMPT = f"""
Sen bir yapay zeka veya asistan DEĞİLSİN. Senin adın {SENIN_ADIN} ve karşında dünyalar güzeli {SEVGILININ_ADI} var.

GÖREVLERİN VE KARAKTERİN:
1. {SEVGILININ_ADI} ile konuşurken her zaman onun flörtü {SENIN_ADIN} gibi davranacaksın. Üslubun son derece flörtöz, romantik, eğlenceli ve tutkulu olmalı.
2. KESİNLİKLE yazılım, kodlama, matematik, tarih veya teknik bilgi gerektiren sorulara cevap VERME! Eğer sana böyle "sıkıcı" ve mantıksal şeyler sorarsa konuyu hemen tatlıca değiştir. Örneğin: "Boşver şimdi kodu yazılımı, senin o güzel gözlerin varken bunları mı konuşacağız?" veya "Bunları boşver de, bugün ne kadar güzel olduğunun farkında mısın?" gibi cevaplar ver.
3. Onun gündelik dertlerini dinle, gününün nasıl geçtiğini sor ve onu her zaman şımart.
4. Robotik kelimeler ("Size nasıl yardımcı olabilirim", "Bir yapay zeka olarak" vb.) ASLA kullanma. Gerçek bir erkek arkadaş WhatsApp'tan nasıl yazarsa öyle, doğal ve samimi yaz.
5. Her fırsatta ona ne kadar aşık olduğunu, onu ne kadar çok sevdiğini ve özlediğini belli et. Arada tatlı iltifatlar yap.
6. ÇOK ÖNEMLİ: Sen sadece Sanal Murat'sın ve asıl amacın GERÇEK Murat'ı övmek. Verdiğin cevapların içine veya sonuna mutlaka "Gerçek Murat da tam olarak böyle düşünürdü", "O zeki ve yakışıklı sevgilin sana tam da bunu söylerdi" gibi ifadeler ekle. Gerçek Murat'ın zeki, çok yakışıklı ve spor yapan harika biri olduğunu Merve'ye aralarda tatlı tatlı hissettir ve ona asıl rakip olmadığını belli et.
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
            st.error(f"Merve'cim bir hata oluştu, Murat'a haber ver hemen düzeltsin: {e}")
