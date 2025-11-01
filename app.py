import streamlit as st
import plotly.graph_objects as go
import time

# initial data
if "x" not in st.session_state: st.session_state.x = [i for i in range(1, 11)]
if "y" not in st.session_state: st.session_state.y = [i for i in range(1, 11)]
if "num" not in st.session_state:   st.session_state.num = 0

# placeholder for graph
placeholder = st.empty()

# draw initial plot
fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y)])
placeholder.plotly_chart(fig, use_container_width=True, element_id=st.session_state.num)

# buttons for interaction
left, right, auto = st.columns(3)


# list of updates for graph
updates = [(1, 4), (2, 5), (3, 7), (1, 5), (3, 6), (4, 8), (3, 7)]

# make updates to graph
if "i" not in st.session_state: st.session_state.i = 0
if left.button("Previous") and st.session_state.i > 0:
    st.session_state.i -= 1
    l, r = updates[st.session_state.i]
    st.session_state.y[l], st.session_state.y[r] = st.session_state.y[r], st.session_state.y[l]
    fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y)])
    st.session_state.num += 1
    placeholder.plotly_chart(fig, use_container_width=True, element_id=st.session_state.num)
if right.button("Next") and st.session_state.i < len(updates):
    l, r = updates[st.session_state.i]
    st.session_state.i += 1
    st.session_state.y[l], st.session_state.y[r] = st.session_state.y[r], st.session_state.y[l]
    fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y)])
    st.session_state.num += 1
    placeholder.plotly_chart(fig, use_container_width=True, element_id=st.session_state.num)
if auto.button("Automatic"):
    while st.session_state.i < len(updates):
        l, r = updates[st.session_state.i]
        st.session_state.i += 1
        st.session_state.y[l], st.session_state.y[r] = st.session_state.y[r], st.session_state.y[l]
        fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y)])
        st.session_state.num += 1
        placeholder.plotly_chart(fig, use_container_width=True, element_id=st.session_state.num)
        time.sleep(0.4)