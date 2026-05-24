import streamlit as st
from google_auth_oauthlib.flow import Flow

st.set_page_config(page_title="Astro-Calendar", page_icon="🚀")
st.title("Astro-Calendar")
st.write("Dünya genelindeki fırlatmaları google takvim üzerinden erişin")

col1, col2, col3 = st.columns(3)
col1.metric("Fırlatma sayısı", "100+")
col2.metric("Güncelleme", "her gün")
col3.metric("Ajans sayısı", "23")
st.divider()


def create_flow():
    return Flow.from_client_secrets_file(
        '../../alistirmalar/credentials.json',
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri='http://localhost:8501'
    )


def google_link():
    flow = create_flow()
    auth_url, _ = flow.authorization_url(prompt='consent')
    return auth_url


query_params = st.query_params

if "code" in query_params:
    auth_code = query_params["code"]

    try:
        flow = create_flow()
        flow.fetch_token(code=auth_code)
        credentials = flow.credentials

        with open('../../alistirmalar/tkn.json', 'w') as token_file:
            token_file.write(credentials.to_json())

        st.success("✅ Google Takvim bağlantısı başarıyla kuruldu! Arka planda veriler eklenmeye başlayacak.")
        st.balloons()

        st.query_params.clear()

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
else:
    try:
        yonlendirme_linki = google_link()
        st.markdown(f'''
            <a href="{yonlendirme_linki}" target="_self" style="text-decoration:none;">
                <button style="background-color:#ff4b4b; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">
                    Takvimime Bağlan ve İzin Ver
                </button>
            </a>
        ''', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Link oluşturulamadı HATA → {e}")
