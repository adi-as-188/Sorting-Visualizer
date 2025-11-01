import streamlit as st
import plotly.graph_objects as go
import time
import random


# initial data
if "x" not in st.session_state: st.session_state.x = [i for i in range(1, 31)]
if "y" not in st.session_state: st.session_state.y = [random.randint(1, 1000) for i in range(30)]
if "color" not in st.session_state: st.session_state.color = ["blue"] * 30
if "num" not in st.session_state:   st.session_state.num = 0
if "alg" not in st.session_state:  st.session_state.alg = None

# placeholder for graph
placeholder = st.empty()

# draw initial plot
fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y, marker_color = st.session_state.color)])
placeholder.plotly_chart(fig, use_container_width=True, element_id=st.session_state.num)

# buttons for interaction
algo, left, right, auto = st.columns(4)

# list of updates for graph
if "updates" not in st.session_state:   st.session_state.updates = []

# make updates to graph
if "i" not in st.session_state: st.session_state.i = 0
# button for previous
if left.button("Previous") and st.session_state.i > 0:
    st.session_state.i -= 1
    task = st.session_state.updates[st.session_state.i]
    if task[0] == "l":
        st.session_state.color[task[1]] = task[2]
        if len(task) > 4:
            st.session_state.color[task[4]] = task[5]
    else:
        st.session_state.y[task[1]], st.session_state.y[task[2]] = st.session_state.y[task[2]], st.session_state.y[task[1]]
        st.session_state.color[task[1]], st.session_state.color[task[2]] = st.session_state.color[task[2]], st.session_state.color[task[1]]
    fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y, marker_color = st.session_state.color)])
    st.session_state.num += 1
    placeholder.plotly_chart(fig, use_container_width=True, element_id=st.session_state.num)
# button for next
if right.button("Next") and st.session_state.i < len(st.session_state.updates):
    task = st.session_state.updates[st.session_state.i]
    if task[0] == "l":
        st.session_state.color[task[1]] = task[3]
        if len(task) > 4:
            st.session_state.color[task[4]] = task[6]
    else:
        st.session_state.y[task[1]], st.session_state.y[task[2]] = st.session_state.y[task[2]], st.session_state.y[task[1]]
        st.session_state.color[task[1]], st.session_state.color[task[2]] = st.session_state.color[task[2]], st.session_state.color[task[1]]
    st.session_state.i += 1
    fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y, marker_color = st.session_state.color)])
    st.session_state.num += 1
    placeholder.plotly_chart(fig, use_container_width=True, element_id=st.session_state.num)
# button to automatically complete the rest
if auto.button("Sort"):
    while st.session_state.i < len(st.session_state.updates):
        task = st.session_state.updates[st.session_state.i]
        if task[0] == "l":
            st.session_state.color[task[1]] = task[3]
            if len(task) > 4:
                st.session_state.color[task[4]] = task[6]
        else:
            st.session_state.y[task[1]], st.session_state.y[task[2]] = st.session_state.y[task[2]], st.session_state.y[task[1]]
            st.session_state.color[task[1]], st.session_state.color[task[2]] = st.session_state.color[task[2]], st.session_state.color[task[1]]
        st.session_state.i += 1
        fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y, marker_color = st.session_state.color)])
        st.session_state.num += 1
        placeholder.plotly_chart(fig, use_container_width=True, element_id=st.session_state.num)
        time.sleep(0.1)


# bubble sort
def bubble_sort():
    arr = [i for i in st.session_state.y]
    ret = []
    for i in range(len(arr) - 1):
        ret.append(("l", 0, "blue", "yellow"))
        for j in range(len(arr) - i - 1):
            if (arr[j] > arr[j+1]):
                ret.append(("s", j, j+1))
                arr[j], arr[j+1] = arr[j+1], arr[j]
            else:
                ret.append(("l", j, "yellow", "blue", j+1, "blue", "yellow"))
        ret.append(("l", len(arr) - i - 1, "yellow", "green"))
    ret.append(("l", 0, "blue", "yellow"))
    ret.append(("l", 0, "yellow", "green"))
    st.session_state.updates = ret


# dropdown to select algorithm
with algo:
    algorithm = st.selectbox("Choose algorithm:", ["Bubble Sort"])
    match algorithm:
        case "Bubble Sort":
            if st.session_state.alg != "Bubble":
                st.session_state.alg = "Bubble"
                st.session_state.i = 0
                bubble_sort()