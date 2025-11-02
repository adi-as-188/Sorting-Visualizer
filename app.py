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
placeholder.plotly_chart(fig, use_container_width=True, key=st.session_state.num)

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
        for i in range(1, len(task), 3):
            st.session_state.color[task[i]] = task[i+1]
    elif task[0] == "o":
        for i in range(1, len(task), 5):
            st.session_state.y[task[i]] = task[i+1]
            st.session_state.color[task[i]] = task[i+3]
    else:
        st.session_state.y[task[1]], st.session_state.y[task[2]] = st.session_state.y[task[2]], st.session_state.y[task[1]]
        st.session_state.color[task[1]], st.session_state.color[task[2]] = st.session_state.color[task[2]], st.session_state.color[task[1]]
    fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y, marker_color = st.session_state.color)])
    st.session_state.num += 1
    placeholder.plotly_chart(fig, use_container_width=True, key=st.session_state.num)
# button for next
if right.button("Next") and st.session_state.i < len(st.session_state.updates):
    task = st.session_state.updates[st.session_state.i]
    if task[0] == "l":
        for i in range(1, len(task), 3):
            st.session_state.color[task[i]] = task[i+2]
    elif task[0] == "o":
        for i in range(1, len(task), 5):
            st.session_state.y[task[i]] = task[i+2]
            st.session_state.color[task[i]] = task[i+4]
    else:
        st.session_state.y[task[1]], st.session_state.y[task[2]] = st.session_state.y[task[2]], st.session_state.y[task[1]]
        st.session_state.color[task[1]], st.session_state.color[task[2]] = st.session_state.color[task[2]], st.session_state.color[task[1]]
    st.session_state.i += 1
    fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y, marker_color = st.session_state.color)])
    st.session_state.num += 1
    placeholder.plotly_chart(fig, use_container_width=True, key=st.session_state.num)
# button to automatically complete the rest
if auto.button("Sort"):
    while st.session_state.i < len(st.session_state.updates):
        task = st.session_state.updates[st.session_state.i]
        if task[0] == "l":
            for i in range(1, len(task), 3):
                st.session_state.color[task[i]] = task[i+2]
        elif task[0] == "o":
            for i in range(1, len(task), 5):
                st.session_state.y[task[i]] = task[i+2]
                st.session_state.color[task[i]] = task[i+4]
        else:
            st.session_state.y[task[1]], st.session_state.y[task[2]] = st.session_state.y[task[2]], st.session_state.y[task[1]]
            st.session_state.color[task[1]], st.session_state.color[task[2]] = st.session_state.color[task[2]], st.session_state.color[task[1]]
        st.session_state.i += 1
        fig = go.Figure(data=[go.Bar(x = st.session_state.x, y = st.session_state.y, marker_color = st.session_state.color)])
        st.session_state.num += 1
        placeholder.plotly_chart(fig, use_container_width=True, key=st.session_state.num)
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


# selection sort
def selection_sort():
    arr = [i for i in st.session_state.y]
    ret = []
    for i in range(len(arr)):
        ret.append(("l", i, "blue", "orange"))
        s = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[s]:
                if s == j-1:
                    ret.append(("l", j, "blue", "orange", s, "orange", "blue"))
                else:
                    ret.append(('l', j, "blue", "orange", j-1, "yellow", "blue", s, "orange", "blue"))
                s = j
            elif s == j-1:
                ret.append(("l", j, "blue", "yellow"))
            else:
                ret.append(('l', j, "blue", "yellow", j-1, "yellow", "blue"))
        if s != len(arr) - 1:
            ret.append(("l", len(arr) - 1, "yellow", "blue"))
        arr[i], arr[s] = arr[s], arr[i]
        ret.append(("s", i, s))
        ret.append(("l", i, "orange", "green"))
    st.session_state.updates = ret


# insertion sort
def insertion_sort():
    arr = [i for i in st.session_state.y]
    ret = []
    ret.append(("l", 0, "blue", "green"))
    for i in range(1, len(arr)):
        ret.append(("l", i, "blue", "yellow"))
        j = i
        while j > 0 and arr[j] < arr[j-1]:
            ret.append(("s", j, j-1))
            arr[j], arr[j-1] = arr[j-1], arr[j]
            j -= 1
        ret.append(("l", j, "yellow", "green"))
    st.session_state.updates = ret


# merge sort
def merge_sort():
    arr = [i for i in st.session_state.y]
    ret = []
    m_sort(arr, 0, len(arr)-1, ret)
    col = ["l"]
    for i in range(len(arr)):
        col.append(i)
        col.append("blue")
        col.append("green")
    ret.append(tuple(col))
    st.session_state.updates = ret

# helper function for merge sort
def m_sort(arr, l, r, ret):
    if l == r:
        return
    m = (l + r) // 2
    m_sort(arr, l, m, ret)
    m_sort(arr, m+1, r, ret)
    left = arr[l:m+1]
    right = arr[m+1:r+1]
    a = b = 0
    i = l
    while a < len(left) and b < len(right):
        if left[a] < right[b]:
            ret.append(("o", i, arr[i], left[a], "blue", "yellow"))
            ret.append(("l", i, "yellow", "blue"))
            arr[i] = left[a]
            a += 1
            i += 1
        else:
            ret.append(("o", i, arr[i], right[b], "blue", "yellow"))
            ret.append(("l", i, "yellow", "blue"))
            arr[i] = right[b]
            b += 1
            i += 1
    while a < len(left):
        ret.append(("o", i, arr[i], left[a], "blue", "yellow"))
        ret.append(("l", i, "yellow", "blue"))
        arr[i] = left[a]
        a += 1
        i += 1
    while b < len(right):
        ret.append(("o", i, arr[i], right[b], "blue", "yellow"))
        ret.append(("l", i, "yellow", "blue"))
        arr[i] = right[b]
        b += 1
        i += 1


# quick sort
def quick_sort():
    arr = [i for i in st.session_state.y]
    ret = []
    q_sort(arr, 0, len(arr)-1, ret)
    st.session_state.updates = ret

# helper function for quick sort
def q_sort(arr, l, r, ret):
    if l > r:
        return
    if l == r:
        ret.append(("l", l, "blue", "green"))
        return
    i = random.randint(l, r)
    ret.append(("l", i, "blue", "orange"))
    ret.append(("s", i, r))
    arr[i], arr[r] = arr[r], arr[i]
    left = l
    for j in range(l, r):
        ret.append(("l", j, "blue", "yellow"))
        if (arr[j] < arr[r]):
            ret.append(("s", j, left))
            arr[j], arr[left] = arr[left], arr[j]
            ret.append(("l", left, "yellow", "blue"))
            left += 1
        else:
            ret.append(("l", j, "yellow", "blue"))
    ret.append(("s", r, left))
    arr[r], arr[left] = arr[left], arr[r]
    ret.append(("l", left, "orange", "green"))
    q_sort(arr, l, left-1, ret)
    q_sort(arr, left+1, r, ret)


# dropdown to select algorithm
with algo:
    algorithm = st.selectbox("Choose algorithm:", ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"])
    match algorithm:
        case "Bubble Sort":
            if st.session_state.alg != "Bubble":
                st.session_state.alg = "Bubble"
                st.session_state.i = 0
                bubble_sort()
        case "Selection Sort":
            if st.session_state.alg != "Selection":
                st.session_state.alg = "Selection"
                st.session_state.i = 0
                selection_sort()
        case "Insertion Sort":
            if st.session_state.alg != "Insertion":
                st.session_state.alg = "Insertion"
                st.session_state.i = 0
                insertion_sort()
        case "Merge Sort":
            if st.session_state.alg != "Merge":
                st.session_state.alg = "Merge"
                st.session_state.i = 0
                merge_sort()
        case "Quick Sort":
            if st.session_state.alg != "Quick":
                st.session_state.alg = "Quick"
                st.session_state.i = 0
                quick_sort()