import time

import streamlit as st
import pandas as pd

from dataclasses import asdict
from streamlit_keycloak import login

from utils.config import KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT, KEYCLOAK_ROLES
from utils.logging import set_logging_configuration
from utils.styling import set_df_time_style, highlight_state, style_dataframe
from calls import get_calls_df, get_ended_calls_df, update_calls_df


set_logging_configuration()

st.set_page_config(page_title="IT Support", page_icon="assets/favicon.ico", layout="wide")

st.title("Streamlit Keycloak example")

keycloak = login(
    url=KEYCLOAK_URL,
    realm=KEYCLOAK_REALM,
    client_id=KEYCLOAK_CLIENT
)

old_calls_df = pd.DataFrame()
ended_calls_df = pd.DataFrame()

if keycloak.authenticated:
    user = asdict(keycloak)
    roles = user.get('user_info', {}).get('resource_access', {}).get('it-support', {}).get('roles', [])
    if any(item in roles for item in KEYCLOAK_ROLES):

        st.write(f"Welcome {keycloak.user_info['preferred_username']}!")
        placeholder = st.empty()

        while True:
            new_calls_df = get_calls_df()
            if not new_calls_df.empty:
                updated_calls_df = update_calls_df(old_calls_df, new_calls_df)
                ended_calls_df = get_ended_calls_df(old_calls_df, updated_calls_df, ended_calls_df)

                old_calls_df = updated_calls_df.copy()

                incoming_calls = updated_calls_df[updated_calls_df['direction'] == 'Incoming'].copy()
                incoming_calls = set_df_time_style(incoming_calls)
            else:
                incoming_calls = old_calls_df[old_calls_df['direction'] == 'Incoming'].copy()
                incoming_calls = set_df_time_style(incoming_calls)

            placeholder.empty()
            with placeholder.container():
                st.write("Incoming calls")
                st.write(style_dataframe(incoming_calls[['start', 'state', 'agent_name', 'wait_time', 'duration']].style.apply(highlight_state, axis=1), 'lightblue').to_html(), unsafe_allow_html=True)

                st.write("Ended calls")
                if not ended_calls_df.empty:
                    tmp_df = ended_calls_df.head(10).copy()
                    tmp_df = set_df_time_style(tmp_df)
                    tmp_df['state'] = tmp_df.apply(lambda row: 'Missed' if row['state'] not in ['Connected', 'Transferred'] else row['state'], axis=1)
                    st.write(style_dataframe(tmp_df[['start', 'state', 'agent_name', 'wait_time', 'duration']].style.apply(highlight_state, axis=1), 'lightblue').to_html(), unsafe_allow_html=True)
            time.sleep(1)

    else:
        st.write("You are not authorized to view this page")
