import streamlit as st
import psutil
import platform
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

st.title("Cloud Monitoring Dashboard")
st.subheader("System Function")
st.set_page_config(layout="wide")

cpu=psutil.cpu_percent()

ram=psutil.virtual_memory()

disk=psutil.disk_usage("/")

col1,col2,col3=st.columns(3)
with col1:
    st.metric("CPU Usage" , f"{cpu}%")

with col2:
    st.metric("RAM Usage",f"{ram.percent}%")

with col3:
    st.metric("Disk Usage",f"{disk.percent}%")

#OVERLOADD#
st.subheader("System Status")
if(cpu>80 or ram.percent>80):
    st.error("System Overload")
elif(cpu>60):
    st.warning("System Moderate load")
else:
    st.success("System Healthy")

#History#
if "cpu" not in st.session_state:
    st.session_state.cpu = []
    st.session_state.ram = []
    st.session_state.disk = []

his=pd.DataFrame({
    "CPU":st.session_state.cpu,
    "RAM":st.session_state.ram,
    "DISK":st.session_state.disk
})

st.subheader("Usage History")
st.dataframe(his)

#visual#
st.subheader("System Performance")

if "cpu" not in st.session_state:
    st.session_state.cpu = []
    st.session_state.ram = []
    st.session_state.disk = []

st.session_state.cpu.append(cpu)
st.session_state.ram.append(ram.percent)
st.session_state.disk.append(disk.percent)

st.session_state.cpu = st.session_state.cpu[-20:]
st.session_state.ram = st.session_state.ram[-20:]
st.session_state.disk = st.session_state.disk[-20:]

st.line_chart({"CPU":st.session_state.cpu,
               "RAM":st.session_state.ram,
               "DISK":st.session_state.disk})

#platform#
st.subheader("System Information ")
system=platform.system()

processor=platform.processor()

machine=platform.machine()

computer_name=platform.node()

col4,col5,col6,col7=st.columns(4)

with col4:
    st.write("Operating System : ",system)

with col5:
    st.write("Processor : ",processor)

with col6:
    st.write("Machine : ",machine)

with col7:
    st.write("Computer Name : ",computer_name)

#autorefresh#
st_autorefresh(interval=2000,key="cloud_refresh")

#datetime#
timiing=st.write("Last Updated : ",datetime.now().strftime("%Y-%m-%D-%H:%M:%S"))