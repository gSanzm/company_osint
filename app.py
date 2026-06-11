import streamlit as st

from agents.source_ranker import rank_sources
from agents.query_builder import build_company_queries
from services.search import run_company_search


st.set_page_config(
    page_title="Company OSINT Agent",
    page_icon="🕵️",
    layout="wide",
)


st.title("Company OSINT Agent")
st.caption("Mini investigación pública de empresas con un flujo multiagente en Python.")


with st.sidebar:
    st.header("Configuración")

    max_results_per_query = st.slider(
        "Resultados por búsqueda",
        min_value=1,
        max_value=10,
        value=3,
        step=1,
    )

    show_debug = st.toggle(
        "Mostrar detalles técnicos",
        value=True,
    )


company_name = st.text_input(
    "Nombre de la empresa",
    placeholder="Ejemplo: Movistar Prosegur Alarmas",
)

company_website = st.text_input(
    "Web oficial, opcional",
    placeholder="Ejemplo: https://www.movistarproseguralarmas.es",
)

country = st.text_input(
    "País o mercado, opcional",
    placeholder="Ejemplo: España",
)


if st.button("Ejecutar búsqueda inicial", type="primary"):
    if not company_name.strip():
        st.warning("Introduce al menos el nombre de la empresa.")
        st.stop()

    with st.status("Ejecutando flujo inicial...", expanded=True) as status:
        st.write("Agente Query Builder: generando búsquedas.")
        queries = build_company_queries(
            company_name=company_name,
            company_website=company_website,
            country=country,
        )

        st.write("Search Agent: consultando Tavily.")
        results = run_company_search(
            queries=queries,
            max_results_per_query=max_results_per_query,
        )

        st.write("Source Ranker Agent: clasificando fuentes.")
        ranked_sources = rank_sources(
            results=results,
            company_website=company_website,
        )

        status.update(
            label="Búsqueda inicial completada",
            state="complete",
            expanded=False,
        )

    tab_ranked, tab_results, tab_queries, tab_raw = st.tabs(
        ["Fuentes clasificadas", "Resultados brutos", "Queries generadas", "Debug"]
    )


    with tab_ranked:
        st.subheader("Fuentes clasificadas")

        if not ranked_sources:
            st.warning("No se han encontrado fuentes para clasificar.")
        else:
            source_groups = {
                "official": "Fuentes oficiales",
                "reviews": "Opiniones y reputación",
                "news": "Noticias y medios",
                "business_directory": "Directorios empresariales",
                "social": "Redes sociales / perfiles",
                "competitor": "Competidores / alternativas",
                "seo_aggregator": "Agregadores SEO",
                "unknown": "Sin clasificar",
            }

            for source_type, label in source_groups.items():
                group = [
                    source for source in ranked_sources
                    if source.source_type == source_type
                ]

                if not group:
                    continue

                st.markdown(f"## {label}")
                st.caption(f"{len(group)} fuente(s)")

                for source in group:
                    with st.container(border=True):
                        st.markdown(f"### [{source.title}]({source.url})")

                        col1, col2, col3 = st.columns([1, 1, 2])

                        with col1:
                            st.metric("Prioridad", source.priority)

                        with col2:
                            st.metric(
                                "Score Tavily",
                                round(source.score, 3) if source.score is not None else "N/A",
                            )

                        with col3:
                            st.caption(source.reason)

                        if source.content:
                            st.write(source.content)

                        st.caption(f"Query origen: {source.query}")



    with tab_results:
        st.subheader("Fuentes encontradas")

        if not results:
            st.warning("No se han encontrado resultados.")
        else:
            st.caption(f"Total de URLs únicas encontradas: {len(results)}")

            for i, result in enumerate(results, start=1):
                with st.container(border=True):
                    st.markdown(f"### {i}. [{result.title}]({result.url})")

                    if result.content:
                        st.write(result.content)

                    col1, col2 = st.columns([1, 3])

                    with col1:
                        st.metric(
                            "Score",
                            round(result.score, 3) if result.score is not None else "N/A",
                        )

                    with col2:
                        st.caption(f"Query origen: {result.query}")
                        st.caption(f"Objetivo: {result.purpose}")

    with tab_queries:
        st.subheader("Queries generadas")

        for query in queries:
            with st.container(border=True):
                st.code(query.query)
                st.caption(query.purpose)


    with tab_raw:
        if show_debug:
            st.subheader("Resultados normalizados")
            st.json([result.model_dump(mode="json") for result in results])

            st.subheader("Fuentes clasificadas")
            st.json([source.model_dump(mode="json") for source in ranked_sources])

            st.subheader("Queries")
            st.json([query.model_dump() for query in queries])
        else:
            st.info("Activa 'Mostrar detalles técnicos' en la barra lateral.")