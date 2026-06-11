import streamlit as st


st.set_page_config(
    page_title="Company OSINT Agent",
    page_icon="🕵️",
    layout="wide",
)

st.title("Company OSINT Agent")
st.caption("Mini investigación pública de empresas con un flujo multiagente.")

company_name = st.text_input("Nombre de la empresa")
company_website = st.text_input("Web oficial, opcional")
country = st.text_input("País o mercado, opcional")

if st.button("Ejecutar investigación"):
    if not company_name.strip():
        st.warning("Introduce al menos el nombre de la empresa.")
        st.stop()

    st.success(f"Proyecto inicial funcionando para: {company_name}")

    st.subheader("Datos introducidos")
    st.write(
        {
            "company_name": company_name,
            "company_website": company_website,
            "country": country,
        }
    )