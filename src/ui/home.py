import json
import streamlit as st
from constants import bg_css
from src.pipeline.ingestion import STATIONS, get_weather_data
from src.pipeline.storage_manager import createDataFrame
from src.expert_system.decision_engine import data_cleaning
from datetime import datetime

def create_logs():
    """
    Creates logs message from "src/data/gold/audit_logs.json"
    """
    with open("src/data/gold/audit_logs.json", 'r') as f:
        data = json.load(f)

    if not data:
        return "No anomaly found."
    else:
        log = ""
        for row in data:
            clean_ts = datetime.fromisoformat(row['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            log += f"On {clean_ts}, station {row['station_id']} detected an anomaly in {row['feature']} (original value: {row['original_value']}). Via {row['action']}, this measurement was successfully corrected to {row['new_value']}. \n\n"
        return log

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.markdown(bg_css, unsafe_allow_html=True)

    if 'raw_data' not in st.session_state: st.session_state.raw_data = None
    if 'processed_data' not in st.session_state: st.session_state.processed_data = None
    if 'logs' not in st.session_state: st.session_state.process_logs = None

    st.title("Automated data cleaning system")

    st.header("Data download")
    col1, col2 = st.columns([1, 2])

    with col1:
        num_of_data = st.number_input("Number of samples per each station", min_value=1, value=100, step=10)
    with col2:
        chosen_stations = st.pills("Choose weather stations", options=STATIONS, selection_mode="multi")

    if st.button("Download", type="primary"):
        if not chosen_stations:
            st.error("Choose at least one weather station.")
        else:
            try:
                with st.spinner("Downloading data..."):
                    get_weather_data(chosen_stations, num_of_data)
                    st.session_state.raw_data = createDataFrame()
                st.success("Data successfully downloaded.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    if st.session_state.raw_data is not None:
        st.subheader("Raw data preview")
        st.dataframe(st.session_state.raw_data)
        st.divider()

        st.header("Data cleaning")
        if st.button("Clean data"):
            with st.spinner("Cleaning data..."):
                data_to_clean = st.session_state.raw_data.copy()
                st.session_state.processed_data = data_cleaning(data_to_clean)
                st.session_state.process_logs = create_logs()

        if st.session_state.processed_data is not None:
            st.subheader("Cleaned data preview")
            col_data, col_info = st.columns([2, 1])

            with col_data:
                st.dataframe(st.session_state.processed_data, use_container_width=True)
            with col_info:
                st.info("Logs:")
                st.info(st.session_state.process_logs)