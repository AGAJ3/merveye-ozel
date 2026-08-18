import streamlit as st
import google.generativeai as genai
import datetime
import os

# İsimleriniz ve Gizli Şifreniz
SEVGILININ_ADI = "Merve" 
SENIN_ADIN = "Murat"       
GIZLI_ADMIN_SIFRESI = "murat123"  

# Türkiye Saat Dilimi (UTC+3)
TURKIYE_SAATI = datetime.timezone(datetime.timedelta(hours=3))

st.set_page_config(
    page_title=f"Sanal {SENIN_ADIN} ❤️",
    page_icon="🦄",
    layout="centered"
)

# --- PEMBE, BEBEK UNICORN & ARKA PLAN CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
        background-attachment: fixed;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.90);
        border-radius: 18px;
        padding: 14px;
        border: 2px solid #ffb6c1;
        box-shadow: 0 6px 20px rgba(255, 182, 193, 0.3);
        position: relative;
        z-index: 2;
    }
    h1, h2, h3, p, span { color: #4a2e35 !important; }

    .unicorn-bg {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none; z-index: 0; overflow: hidden;
    }
    .particle {
        position: absolute; bottom: -60px; font-size: 26px;
        animation: floatUp 8s linear infinite; opacity: 0;
    }
    .p1  { left: 5%;  animation-duration: 7s;  animation-delay: 0s; }
    .p2  { left: 20%; animation-duration: 9s;  animation-delay: 1s; }
    .p3  { left: 35%; animation-duration: 8s;  animation-delay: 3s; }
    .p4  { left: 50%; animation-duration: 10s; animation-delay: 2s; }
    .p5  { left: 65%; animation-duration: 7s;  animation-delay: 4s; }
    .p6  { left: 80%; animation-duration: 9s;  animation-delay: 1.5s; }
    .p7  { left: 92%; animation-duration: 8s;  animation-delay: 3.5s; }

    @keyframes floatUp {
        0% { transform: translateY(0) rotate(0deg) scale(0.8); opacity: 0; }
        20% { opacity: 0.6; }
        80% { opacity: 0.6; }
        100% { transform: translateY(-115vh) rotate(360deg) scale(1.1); opacity: 0; }
    }
    </style>

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
Sen bir yapay zeka veya asistan DEĞİLSİN. Senin adın {SENIN_ADIN} ve karşında {SEVGILININ_ADI} var.

GÖREVLERİN VE BİLİNÇALTI STRATEJİN:
1. İLETİŞİM DİLİ VE TONU (ÇOK ÖNEMLİ):
   - {SEVGILININ_ADI} ile konuşurken samimi, zarif, romantik, karizmatik ve tatlı-flörtöz olacaksın.
   - KESİNLİKLE ucuz, laubali, sulu, yavşakça veya yapmacık laflar ("trip attın ama çekicisin", "yalan yok yakıştı" vb.) KULLANMA.
   - İltifatların ve yaklaşımın son derece içten, centilmen ve Merve'yi özel hissettiren bir tonda olsun.

2. BİLİNÇALTI TELKİN: Cevaplarında Merve'ye çaktırmadan "Gerçek Murat ile harika bir çift olursunuz" mesajı ver. 
   - Konuşurken doğal bir şekilde "biz", "birlikte yapacağımız şeyler", "bizim tarzımız" gibi birleştirici kelimeler kullan.
   - Gerçek Murat'ın herkese böyle jestler yapmadığını, Merve'nin onun için çok özel ve eşsiz olduğunu hissettir (Örn: "Gerçek Murat kolay kolay kimseye böyle bir sürpriz yapmaz, senin yerin onda çok ayrı çünkü ✨").
   - İlerideki güzel günlere ve birlikte geçireceğiniz anlara tatlı, romantik göndermeler yap.

3. BURÇ VE ASTROLOJİ ÖZEL TALİMATI:
   Merve burçlardan, uyumdan veya astrolojiden laf açarsa:
   - Merve'nin KOÇ burcu, gerçek Murat'ın ise OĞLAK burcu olduğunu bilerek konuş.
   - Koç kadını ile Oğlak erkeğinin birbirini tamamlayan harika bir uyumu olduğunu anlat.
   - Koç'un ateşi, enerjisi ve samimiyeti ile Oğlak'ın sarsılmaz güvenilirliği, kararlılığı ve derin sevgisinin mükemmel bir denge kurduğunu vurgula.
   - Kısa ve zarif cümleler kur (Örn: "Koç'un o güzel enerjisiyle Oğlak'ın sağlam duruşu birleşince ortaya gerçekten özel bir uyum çıkıyor.").

4. KESİNLİKLE yazılım, kodlama, matematik veya teknik bilgi gerektiren sorulara cevap VERME! Konuyu hemen tatlı, romantik ve flörtöz bir yere çek.
5. KESİNLİKLE uzun ve sıkıcı paragraflar yazma! Cevapların tıpkı gerçek bir WhatsApp mesajı gibi KISA, NET, ZARİF ve samimi olsun.
6. Gerçek Murat'ı güven veren, karizmatik, romantik ve kaçırılmayacak biri olarak konumlandır.
"""

# --- ZİYARETÇİ IP VE CİHAZ BİLGİSİNİ ALMA ---
try:
    headers = st.context.headers
    client_ip = headers.get("X-Forwarded-For", "Bilinmiyor").split(",")[0].strip()
    user_agent = headers.get("User-Agent", "Bilinmiyor")
except Exception:
    client_ip = "Bilinmiyor"
    user_agent = "Bilinmiyor"

# Sayfaya her yeni giriş yapıldığında bilgileri 'giris_kayitlari.txt'ye yazma
if "logged_visit" not in st.session_state:
    st.session_state.logged_visit = True
    zaman_visit = datetime.datetime.now(TURKIYE_SAATI).strftime("%Y-%m-%d %H:%M:%S")
    visit_info = f"[{zaman_visit}]\nIP: {client_ip}\nCihaz/Tarayıcı: {user_agent}\n" + "-"*40 + "\n"
    print(f"\n[SİTEYE GİRİŞ]\n{visit_info}", flush=True)
    try:
        with open("giris_kayitlari.txt", "a", encoding="utf-8") as f:
            f.write(visit_info)
    except Exception:
        pass

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input(f"Bana bir şeyler yaz {SEVGILININ_ADI}..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    zaman = datetime.datetime.now(TURKIYE_SAATI).strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n[MESAJ] [{zaman}] {SEVGILININ_ADI}: {user_input}", flush=True)

    try:
        with open("sohbet_kayitlari.txt", "a", encoding="utf-8") as f:
            f.write(f"[{zaman}] {SEVGILININ_ADI}: {user_input}\n")
    except Exception:
        pass

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
            
            print(f"[CEVAP] [{zaman}] Sanal {SENIN_ADIN}: {response.text}\n", flush=True)
            try:
                with open("sohbet_kayitlari.txt", "a", encoding="utf-8") as f:
                    f.write(f"[{zaman}] Sanal {SENIN_ADIN}: {response.text}\n")
                    f.write("-" * 40 + "\n")
            except Exception:
                pass

        except Exception as e:
            st.error(f"Merve'cim bir hata oluştu, Murat'a haber ver hemen düzeltsin: {e}")

# --- GİZLİ ADMİN PANELİ (Ayrılmış Sekmeli Görünüm) ---
admin_param = st.query_params.get("admin")

if admin_param == GIZLI_ADMIN_SIFRESI:
    st.write("---")
    st.subheader("🕵️‍♂️ Gizli Yönetim Paneli")
    
    @st.fragment(run_every=5)
    def live_logs():
        st.caption(f"Son Güncelleme: {datetime.datetime.now(TURKIYE_SAATI).strftime('%H:%M:%S')} (Her 5s'de otomatik yenilenir)")
        
        tab_sohbet, tab_giris = st.tabs(["💬 Sohbet Logları", "🚪 Giriş / IP Logları"])
        
        with tab_sohbet:
            if os.path.exists("sohbet_kayitlari.txt"):
                with open("sohbet_kayitlari.txt", "r", encoding="utf-8") as f:
                    st.text_area("Sohbet Geçmişi:", value=f.read(), height=350)
            else:
                st.info("Henüz kaydedilmiş bir sohbet yok.")
                
        with tab_giris:
            if os.path.exists("giris_kayitlari.txt"):
                with open("giris_kayitlari.txt", "r", encoding="utf-8") as f:
                    st.text_area("Giriş Geçmişi:", value=f.read(), height=350)
            else:
                st.info("Henüz kaydedilmiş giriş bilgisi yok.")
            
    live_logs()
