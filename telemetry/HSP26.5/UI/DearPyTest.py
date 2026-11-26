# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 12:03:03 2026

@author: oscar
"""
import dearpygui.dearpygui as dpg
import numpy as np
import time

# ===== STATE =====
curves = []
graph_counter = 0
t = 0.0

colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 0, 255), (0, 255, 255), (255, 255, 0)
]

# ===== DATA =====
def get_data(selection):
    x = np.linspace(0, 10, 200)

    if selection == "Sine Wave":
        y = np.sin(x)
    elif selection == "Cosine Wave":
        y = np.cos(x)
    elif selection == "Quad":
        y = x**2
    else:
        y = x

    return x, y


def analyze_data(x, y):
    amplitude = (np.max(y) - np.min(y)) / 2
    mean_val = np.mean(y)

    zero_crossings = np.where(np.diff(np.sign(y)))[0]
    if len(zero_crossings) > 1:
        periods = np.diff(x[zero_crossings])
        avg_period = np.mean(periods) * 2
        frequency = 1 / avg_period if avg_period != 0 else 0
    else:
        frequency = 0

    peak_index = np.argmax(y)
    phase = x[peak_index]

    return amplitude, mean_val, frequency, phase


# ===== CALLBACKS =====
def add_graph():
    global graph_counter

    selections = dpg.get_value("dataset_list")
    if not selections:
        return

    k = dpg.get_value("amp") or 1
    omega = dpg.get_value("omega") or 1
    m = dpg.get_value("m") or 0

    for selection in selections:
        x, y = get_data(selection)

        color = colors[graph_counter % len(colors)]

        name = f"{selection} #{graph_counter}"
        graph_counter += 1

        tag = f"series_{name}"

        dpg.add_line_series(
            x, y,
            label=name,
            parent="y_axis",
            tag=tag
        )

        curves.append({
            "tag": tag,
            "name": name,
            "type": selection,
            "x": x,
            "y": y,
            "k": float(k),
            "omega": float(omega),
            "m": float(m)
        })

        dpg.configure_item(tag, color=color)

        dpg.add_selectable(label=name, parent="graph_list", callback=select_graph)


def select_graph(sender, app_data):
    selected_name = app_data

    for entry in curves:
        if entry["name"] == selected_name:
            x, y = entry["x"], entry["y"]
            amp, mean_val, freq, phase = analyze_data(x, y)

            dpg.set_value(
                "info",
                f"{selected_name}\n"
                f"Amp: {amp:.3f}\n"
                f"Mean: {mean_val:.3f}\n"
                f"Freq: {freq:.3f}\n"
                f"Phase: {phase:.3f}"
            )
            break


def clear_graph():
    global curves
    curves = []
    dpg.delete_item("y_axis", children_only=True)
    dpg.delete_item("graph_list", children_only=True)


def randomize_data():
    for entry in curves:
        x = entry["x"]
        y = np.random.random(len(x))
        entry["y"] = y
        dpg.set_value(entry["tag"], [x, y])


def update():
    global t
    t += 0.2

    for entry in curves:
        x = entry["x"]
        k = entry["k"]
        omega = entry["omega"]
        m = entry["m"]

        if entry["type"] == "Sine Wave":
            y = k * np.sin(omega * (x + t)) + m
        elif entry["type"] == "Cosine Wave":
            y = k * np.cos(omega * (x + t)) + m
        elif entry["type"] == "Linear":
            y = k * (x + (t % 5)) + m
        elif entry["type"] == "Quad":
            y = k * (x + t)**2 % 100 + m
        else:
            y = entry["y"]

        entry["y"] = y
        dpg.set_value(entry["tag"], [x, y])


# ===== UI =====
dpg.create_context()

with dpg.window(label="Interactive Graph Control Panel", width=1000, height=600):

    with dpg.group(horizontal=True):

        # LEFT PANEL
        with dpg.child_window(width=250):

            dpg.add_button(label="Add Graph", callback=add_graph)
            dpg.add_button(label="Randomize", callback=randomize_data)
            dpg.add_button(label="Clear", callback=clear_graph)

            dpg.add_separator()
            dpg.add_text("Datasets")

            dpg.add_listbox(
                items=["Sine Wave", "Cosine Wave", "Linear", "Quad"],
                tag="dataset_list",
                num_items=4,
                #multi_select=True
            )

            dpg.add_separator()
            dpg.add_text("Parameters")

            dpg.add_input_float(label="Amplitude", tag="amp", default_value=1)
            dpg.add_input_float(label="Omega", tag="omega", default_value=1)
            dpg.add_input_float(label="Offset", tag="m", default_value=0)

            dpg.add_separator()
            dpg.add_text("Graphs")
            dpg.add_child_window(tag="graph_list", height=150)

        # RIGHT PANEL
        with dpg.child_window():

            with dpg.plot(label="Plot", height=400, width=-1):

                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="X")
                dpg.add_plot_axis(dpg.mvYAxis, label="Y", tag="y_axis")

            dpg.add_text("No data", tag="info")


# ===== MAIN LOOP =====
dpg.create_viewport(title="Dear PyGui Graph", width=1000, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    update()
    dpg.render_dearpygui_frame()

dpg.destroy_context()