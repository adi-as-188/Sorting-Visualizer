import streamlit as st
import plotly.graph_objects as go
import time
import random


# initial data
if "x" not in st.session_state: st.session_state.x = [i for i in range(1, 31)]
if "y" not in st.session_state: st.session_state.y = [random.randint(1, 1000) for i in range(1, 31)]
if "num" not in st.session_state:   st.session_state.num = 0

# placeholder for graph
placeholder = st.empty()

# draw initial plot
fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y)])
placeholder.plotly_chart(fig, use_container_width=True, element_id=st.session_state.num)

# buttons for interaction
algo, left, right, auto = st.columns(4)

# list of updates for graph
if "updates" not in st.session_state:   st.session_state.updates = []

# make updates to graph
if "i" not in st.session_state: st.session_state.i = 0
# button for previous
if right.button("Previous") and st.session_state.i > 0:
    st.session_state.i -= 1
    l, r = st.session_state.updates[st.session_state.i]
    st.session_state.y[l], st.session_state.y[r] = st.session_state.y[r], st.session_state.y[l]
    fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y)])
    st.session_state.num += 1
    placeholder.plotly_chart(fig, use_container_width=True, element_id=st.session_state.num)
# button for next
if right.button("Next") and st.session_state.i < len(st.session_state.updates):
    l, r = st.session_state.updates[st.session_state.i]
    st.session_state.i += 1
    st.session_state.y[l], st.session_state.y[r] = st.session_state.y[r], st.session_state.y[l]
    fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y)])
    st.session_state.num += 1
    placeholder.plotly_chart(fig, use_container_width=True, element_id=st.session_state.num)
# button to automatically complete the rest
if auto.button("Automatic"):
    while st.session_state.i < len(st.session_state.updates):
        l, r = st.session_state.updates[st.session_state.i]
        st.session_state.i += 1
        st.session_state.y[l], st.session_state.y[r] = st.session_state.y[r], st.session_state.y[l]
        fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y)])
        st.session_state.num += 1
        placeholder.plotly_chart(fig, use_container_width=True, element_id=st.session_state.num)
        time.sleep(0.2)

# dropdown to select algorithm
with algo:
    algorithm = st.selectbox("Choose algorithm: ", ["Bubble Sort"])


# bubble sort
def bubble_sort():
    arr = [i for i in st.session_state.y]
    ret = []
    for i in range(len(arr)):
        changed = False
        for j in range(len(arr) - i - 1):
            if (arr[j] > arr[j+1]):
                ret.append((j, j+1))
                arr[j], arr[j+1] = arr[j+1], arr[j]
                changed = True
        if not changed: break
    st.session_state.updates = ret

# start the sort
if left.button("Sort"):
    st.session_state.i = 0
    match algorithm:
        case "Bubble Sort":
            bubble_sort()