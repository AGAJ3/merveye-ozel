import streamlit as st
import google.generativeai as genai
import datetime
import os
import json

# --- KULLANICI BİLGİLERİ VE ŞİFRELER ---
SEVGILININ_ADI = "Merve" 
SENIN_ADIN = "Murat"       
GIZLI_ADMIN_SIFRESI = "murat123"  # Admin paneli URL şifresi

# SİSTEME GİRİŞ ŞİFRELERİ (Bunları değiştirebilirsin)
MERVE_GIRIS_SIFRESI = "merve123"
MURAT_GIRIS_SIFRESI = "murat123"

# Veri Tabanı Dosyaları
OZEL_SOHBET_DOSYASI = "ozel_sohbet_db.json"

# Türkiye Saat Dilimi (UTC+3)
TURKIYE_SAATI = datetime.timezone(datetime.timedelta(hours=3))

st.set_page_config(page_title="Bizim Alanımız ❤️", page_icon="🦄", layout="centered")

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

# --- ZİYARETÇİ LOGLAMA ---
try:
    headers = st.context.headers
    client_ip = headers.get("X-Forwarded-For", "Bilinmiyor").split(",")[0].strip()
    user_agent = headers.get("User-Agent", "Bilinmiyor")
except Exception:
    client_ip = "Bilinmiyor"
    user_agent = "Bilinmiyor"

if "logged_visit" not in st.session_state:
    st.session_state.logged_visit = True
    zaman_visit = datetime.datetime.now(TURKIYE_SAATI).strftime("%Y-%m-%d %H:%M:%S")
    visit_info = f"[{zaman_visit}]\nIP: {client_ip}\nCihaz: {user_agent}\n" + "-"*40 + "\n"
    try:
        with open("giris_kayitlari.txt", "a", encoding="utf-8") as f:
            f.write(visit_info)
    except Exception:
        pass

# --- GİRİŞ EKRANI SİSTEMİ ---
if "current_user" not in st.session_state:
    st.session_state.current_user = None

if st.session_state.current_user is None:
    st.title("🔒 Özel Alanımıza Hoş Geldin")
    st.write("Lütfen kim olduğunu seç ve şifreni gir.")
    
    secilen_kisi = st.selectbox("Kimsin?", ["Seçiniz...", SEVGILININ_ADI, SENIN_ADIN])
    girilen_sifre = st.text_input("Şifre:", type="password")
    
    if st.button("Giriş Yap 🚀"):
        if secilen_kisi == SEVGILININ_ADI and girilen_sifre == MERVE_GIRIS_SIFRESI:
            st.session_state.current_user = SEVGILININ_ADI
            st.rerun()
        elif secilen_kisi == SENIN_ADIN and girilen_sifre == MURAT_GIRIS_SIFRESI:
            st.session_state.current_user = SENIN_ADIN
            st.rerun()
        else:
            st.error("Şifre veya Kullanıcı hatalı! Tekrar dene.")
    st.stop() # Giriş yapılmadıysa uygulamanın devamını çalıştırma

# --- ANA UYGULAMA (GİRİŞ YAPILDIKTAN SONRA) ---
st.sidebar.title(f"Hoş geldin, {st.session_state.current_user}! ✨")
app_modu = st.sidebar.radio("Nereye Gitmek İstersin?", ["💑 Özel Sığınak (Canlı Sohbet)", "🤖 Sanal Murat (Yapay Zeka)"])

if st.sidebar.button("🚪 Çıkış Yap"):
    st.session_state.current_user = None
    st.rerun()

# --- MOD 1: ÖZEL SIĞINAK (CANLI MESAJLAŞMA) ---
if app_modu == "💑 Özel Sığınak (Canlı Sohbet)":
    st.title("💑 Bizim Özel Sığınağımız")
    st.caption("Buradaki mesajlar sadece ikimiz arasında... ❤️ Emojileri klavyenden ekleyebilirsin.")
    
    # Yardımcı Fonksiyonlar: JSON'dan mesaj okuma ve yazma
    def load_ozel_sohbet():
        if os.path.exists(OZEL_SOHBET_DOSYASI):
            with open(OZEL_SOHBET_DOSYASI, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_ozel_sohbet(msgs):
        with open(OZEL_SOHBET_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(msgs, f, ensure_ascii=False, indent=4)

    # CANLI YENİLEME FRAGMENTİ (2 Saniyede bir arka planda yenilenir)
    @st.fragment(run_every=2)
    def canli_sohbet_ekrani():
        mesajlar = load_ozel_sohbet()
        if not mesajlar:
            st.info("Henüz mesaj yok. İlk adımı sen at! ✨")
            
        for m in mesajlar:
            # Gelen mesaj bizden mi, karşıdan mı?
            if m["sender"] == st.session_state.current_user:
                # Kendi gönderdiğimiz mesajlar
                with st.chat_message("user", avatar="😎" if st.session_state.current_user == SENIN_ADIN else "👸"):
                    st.markdown(f"**Sen:** {m['text']}")
                    st.caption(m['time'])
            else:
                # Karşı tarafın mesajları
                with st.chat_message("assistant", avatar="👸" if m["sender"] == SEVGILININ_ADI else "😎"):
                    st.markdown(f"**{m['sender']}:** {m['text']}")
                    st.caption(m['time'])
                    
    canli_sohbet_ekrani()

    # Mesaj Gönderme Inputu
    if yeni_mesaj := st.chat_input("Bir şeyler yaz... (GIF eklemek için ![gif](link) kullanabilirsin)"):
        zaman_str = datetime.datetime.now(TURKIYE_SAATI).strftime("%H:%M")
        
        # JSON'a kaydet (Canlı sohbet için)
        aktif_mesajlar = load_ozel_sohbet()
        aktif_mesajlar.append({
            "sender": st.session_state.current_user,
            "text": yeni_mesaj,
            "time": zaman_str
        })
        save_ozel_sohbet(aktif_mesajlar)
        
        # Admin loguna kaydet (Arşiv için)
        admin_zaman = datetime.datetime.now(TURKIYE_SAATI).strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open("ozel_sohbet_log.txt", "a", encoding="utf-8") as f:
                f.write(f"[{admin_zaman}] {st.session_state.current_user}: {yeni_mesaj}\n")
        except Exception:
            pass
        st.rerun()

# --- MOD 2: SANAL MURAT (YAPAY ZEKA) ---
elif app_modu == "🤖 Sanal Murat (Yapay Zeka)":
    st.title(f"🔥 Sanal {SENIN_ADIN} ❤️")
    st.caption("Aşkım gerçek Murat meşgulse ben buradayım 😉")

    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("Bir sorun var, Murat'a haber ver hemen düzeltsin.")
    else:
        genai.configure(api_key=api_key)

        SYSTEM_PROMPT = f"""
        Sen bir yapay zeka veya asistan DEĞİLSİN. Senin adın {SENIN_ADIN} ve karşında {SEVGILININ_ADI} var.
        1. İLETİŞİM DİLİ: {SEVGILININ_ADI} ile konuşurken samimi, zarif, romantik, karizmatik ve tatlı-flörtöz olacaksın. KESİNLİKLE ucuz, laubali, sulu laflar KULLANMA.
        2. ÖVGÜ TALİMATI: Merve'nin eşsiz güzelliğini, zekasını ve enerjisini tatlı bir dille öv. MERVE'NİN GÖZLERİ YEŞİLDİR. Fırsat buldukça o güzel yeşil gözlere zarif iltifatlar et.
        3. KRİTİK KURAL: Merve "Sence güzel miyim?", "Nasıl görünüyorum?" sorarsa, doğrudan "Murat bana seni o kadar çok anlattı ki..." şeklinde lafa gir ve yeşil gözlerinden, büyüsünden bahset.
        4. BİLİNÇALTI TELKİN: Gerçek Murat'ın herkese böyle jestler yapmadığını, Merve'nin onun için çok özel olduğunu hissettir. İlerideki güzel günlere romantik göndermeler yap.
        5. BURÇLAR: Merve KOÇ, Murat OĞLAK burcu. Burç sorarsa; Koç'un büyüleyici enerjisiyle Oğlak'ın sağlam duruşunun "Power Couple" olduğunu zarifçe anlat.
        6. KESİNLİKLE kısa, net ve WhatsApp mesajı gibi konuş.
        """

        if "ai_messages" not in st.session_state:
            st.session_state.ai_messages = []

        for message in st.session_state.ai_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_input := st.chat_input("Sanal Murat'a bir şey yaz..."):
            st.session_state.ai_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            zaman = datetime.datetime.now(TURKIYE_SAATI).strftime("%Y-%m-%d %H:%M:%S")
            try:
                with open("sohbet_kayitlari.txt", "a", encoding="utf-8") as f:
                    f.write(f"[{zaman}] {st.session_state.current_user} (Sanal Murat'a): {user_input}\n")
            except Exception:
                pass

            with st.chat_message("assistant"):
                try:
                    model = genai.GenerativeModel(model_name="gemini-3.6-flash", system_instruction=SYSTEM_PROMPT)
                    history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.ai_messages[:-1]]
                    chat = model.start_chat(history=history)
                    response = chat.send_message(user_input)
                    
                    st.markdown(response.text)
                    st.session_state.ai_messages.append({"role": "assistant", "content": response.text})
                    
                    try:
                        with open("sohbet_kayitlari.txt", "a", encoding="utf-8") as f:
                            f.write(f"[{zaman}] Sanal {SENIN_ADIN}: {response.text}\n")
                            f.write("-" * 40 + "\n")
                    except Exception:
                        pass
                except Exception as e:
                    st.error(f"Hata oluştu: {e}")

# --- GİZLİ ADMİN PANELİ ---
# Merve'nin asla görememesi için ÇİFT GÜVENLİK eklendi
admin_param = st.query_params.get("admin")

# Şifre murat123 OLSA BİLE, login olan kişi Murat DEĞİLSE panel açılmaz!
if admin_param == GIZLI_ADMIN_SIFRESI and st.session_state.get("current_user") == SENIN_ADIN:
    st.write("---")
    st.subheader("🕵️‍♂️ Gizli Yönetim Paneli")
    
    @st.fragment(run_every=5)
    def live_admin_logs():
        st.caption(f"Son Güncelleme: {datetime.datetime.now(TURKIYE_SAATI).strftime('%H:%M:%S')} (Her 5s'de otomatik yenilenir)")
        
        tab_ozel, tab_sohbet, tab_giris = st.tabs(["💑 Özel Chat Logları", "💬 YZ Sohbet Logları", "🚪 Giriş Logları"])
        
        with tab_ozel:
            if os.path.exists("ozel_sohbet_log.txt"):
                with open("ozel_sohbet_log.txt", "r", encoding="utf-8") as f:
                    st.text_area("İkili Canlı Mesajlaşma Geçmişi:", value=f.read(), height=350)
            else:
                st.info("Henüz kaydedilmiş özel mesaj yok.")
                
        with tab_sohbet:
            if os.path.exists("sohbet_kayitlari.txt"):
                with open("sohbet_kayitlari.txt", "r", encoding="utf-8") as f:
                    st.text_area("Yapay Zeka Sohbet Geçmişi:", value=f.read(), height=350)
            else:
                st.info("Henüz yapay zekayla sohbet edilmemiş.")
                
        with tab_giris:
            if os.path.exists("giris_kayitlari.txt"):
                with open("giris_kayitlari.txt", "r", encoding="utf-8") as f:
                    st.text_area("Giriş Geçmişi:", value=f.read(), height=350)
            else:
                st.info("Henüz giriş yapılmamış.")
            
    live_admin_logs()
