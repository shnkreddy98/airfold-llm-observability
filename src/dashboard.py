from file_manipulation import read_file
from io import StringIO

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

af_config = ".airfold/config.yaml"

filter_mapping = {
    "5m": "fiveminutes", 
    "30m": "thirtyminutes", 
    "1hr": "onehour", 
    "3h": "threehours", 
    "12h": "twelvehours", 
    "1d": "oneday", 
    "7d": "sevendays", 
    "30d": "thirtydays", 
    "90d": "nintydays", 
    "1y": "oneyear"
}

def add_params(param_dict):
    params = "?"
    for key, val in param_dict.items():
        params += f"{key}={val}&"
    return params

def api_call(endpoint_name, params):
    url = 'https://api.us.airfold.co/v1/pipes/{}.csv'
    auth_bearer = 'Bearer {}'

    auth_code = read_file(af_config)['key']
    params = add_params(params)
    url_with_params = url+params

    response = requests.get(url_with_params.format(endpoint_name), 
                            headers={
                                'Authorization': auth_bearer.format(auth_code)
                                })
    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Error: {response.status_code}, {response.text}")

def display_card(container, label, value):
    container.markdown(
        f"""
        <div style="background-color:#11111; padding:10px 15px; border-radius:10px; margin-bottom:10px; box-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
            <p style="color:#aaaaaa; text-align:center; font-size:14px; margin:4px 0;">{label}</p>
            <p style="color:#ffffff; text-align:center; font-size:20px; font-weight:bold; margin:4px 0;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def component_tokens(container, token_type, component_name, params):
    params = {"interval": filter_mapping[timeframe],
                "col_type": token_type}
    avg_prompt_tokens = api_call("total_values",
                                    params)
    avg_prompt_tokens = pd.read_csv(StringIO(avg_prompt_tokens))
    disp_val = round(avg_prompt_tokens.values[0][0], 2)
    display_card(container, component_name, disp_val)

if __name__=="__main__":
    st.set_page_config(layout="wide")
    dr_col, gran_col = st.columns(2)
    with dr_col:
        with st.popover("Date Range"):
            st.write("Quick Select")
            dr_options = ["5m", "30m", "1hr", "3h", "12h", "1d", "7d", "30d", "90d", "1y"]
            timeframe = st.segmented_control(
                "TimeFrame",
                dr_options,
                selection_mode="single",
                default= "5m"
            )

            st.write("Custom Date Range")
            start_col, end_col = st.columns(2)
            with start_col:
                start_date = st.date_input(label="Start Date",                                                                                                          
                                value="2024-01-04",                                                                                                                            
                                format="YYYY/MM/DD",                                                                                                                           
                                min_value="2024-01-04",                                                                                                                        
                                max_value="today")                                                                                                                             
            with end_col:
                end_date = st.date_input(label="End Date",                                                                                                            
                                value=start_date,                                                                                                                              
                                format="YYYY/MM/DD",                                                                                                                           
                                min_value=start_date,                                                                                                                          
                                max_value="today")                                                                                                                             

    with gran_col:
        with st.popover("Granularity"):
            gran_options = ["minute", "hour", "day", "month"]
            granularity = st.segmented_control(
                "Granularity",
                gran_options,
                selection_mode="single",
                default= "hour"
            )

    timeline_chart, avg_stats = st.columns([2, 1], 
                                           vertical_alignment="bottom")
    with timeline_chart:
        # Requests vs Errors Chart
        params = {"interval": filter_mapping[timeframe]}
        gran_params = params

        gran_params["granularity"] = granularity
        req_err_data = api_call("requests_timeline",
                                params)
        req_err_data = pd.read_csv(StringIO(req_err_data))
        fig = px.line(req_err_data, 
                      x="timeseries", 
                      y=["requests", "errors"])
                    #   line_shape='spline') # Visually aesthetic but rounds off peak?
        st.plotly_chart(fig)

    with avg_stats:
        # Avg Input/Output/Total Tokens
        component_name_fmt = "Avg {} Tokens/Req"

        prompt_contianer = st.container(border=True)
        component_tokens(prompt_contianer, 
                         "prompt", 
                         component_name_fmt.format("Prompt"),
                         params)

        compl_contianer = st.container(border=True)
        component_tokens(compl_contianer, 
                         "completion", 
                         component_name_fmt.format("Completition"),
                         params)

        total_contianer = st.container(border=True)
        component_tokens(total_contianer, 
                         "total", 
                         component_name_fmt.format("Total"),
                         params)
        
        errors_container = st.container(border=True)
        component_tokens(errors_container,
                         "total_error",
                         "Total Errors",
                         params)
    
    # Top Models
    top_models_data = api_call("top_models",
                                params)
    top_models_data = pd.read_csv(StringIO(top_models_data))
    fig = px.bar(
        top_models_data,
        x='use_count',
        y='model',
        orientation='h',
        title='Top Models',
        labels= {
            'use_count': 'No of Requests',
            'model': 'Models'
        }
    )

    st.plotly_chart(fig, use_container_width=True)
                
    user_count_col, quantiles_col = st.columns(2,
                                               vertical_alignment="bottom")
    with user_count_col:
        # Users
        user_count_data = api_call("user_count",
                                gran_params)
        user_count_data = pd.read_csv(StringIO(user_count_data))
        fig = px.line(user_count_data, 
                    title="No of Active Users",
                    x="timeseries", 
                    y="users",
                    labels= {
                        'users': 'No of Users',
                        'timeseries': 'Dates'
                    },
                    line_shape='spline') # Visually aesthetic but rounds off peak?
        st.plotly_chart(fig)
    
    with quantiles_col:
        # Quantiles
        quant_param = gran_params
        col_select = st.selectbox("Select Column",
                                  ["Latency", "Prompt", "Completion", "Total"])
        col_select = col_select.lower()
        quant_param['col_val'] = col_select
        quants = ['p75', 'p90', 'p95', 'p99']
        display_cols = [quant+col_select for quant in quants]

        quantiles_data = api_call("quantiles",
                                  quant_param)
        quantiles_data = pd.read_csv(StringIO(quantiles_data))

        fig = px.line(quantiles_data, 
                      title="Quantiles",
                      x="timeseries", 
                      y=display_cols,
                      labels= {
                          'users': 'No of Users',
                          'timeseries': 'Dates'
                          },
                      line_shape='spline') # Visually aesthetic but rounds off peak?
        st.plotly_chart(fig)       

    top_errors_col, latency_col= st.columns(2,
                                             vertical_alignment='bottom')

    with top_errors_col:
        error_types = api_call("top_errors",
                               params)
        error_types = pd.read_csv(StringIO(error_types))
        fig = px.pie(error_types, 
                     title='Error Types',
                     values='error_instances',
                     names='error_type',
                     hole=0.4)
        st.plotly_chart(fig)

    with latency_col:
        # Latency
        latency_data = api_call("latency_timeline",
                                gran_params)
        latency_data = pd.read_csv(StringIO(latency_data))
        fig = px.line(latency_data, 
                    title= "Latency over time",
                    x="timeseries", 
                    y="latency",
                    labels= {
                        'users': 'Latency'
                    },
                    line_shape='spline') # Visually aesthetic but rounds off peak?
        st.plotly_chart(fig)

    # Tokens/Minute
    tokens_pm_data = api_call("tokens_pm",
                              gran_params)
    tokens_pm_data = pd.read_csv(StringIO(tokens_pm_data))
    fig = px.line(
        tokens_pm_data,
        x='timeseries',
        y='tokens_per_minute',
        title='Tokens Per Minutes'
    )
    st.plotly_chart(fig)