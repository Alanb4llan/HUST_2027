# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 12:07:28 2026

@author: oscar
"""

"""
Denna behöver göras om genom att man tar bort de båda tabs som finns här.

Istället bör det göras en modul(alt att denna modulen görs om och har den abstrakta typen tab)
"""


import sys
import numpy as np
import pyqtgraph as pg

from dataclasses import dataclass

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QDoubleValidator, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


# ============================================================
# GRAPH DATA
# ============================================================

@dataclass
class GraphData:
    curve: object
    graph_type: str
    name: str
    x: np.ndarray
    y: np.ndarray
    k: float = 1.0
    omega: float = 1.0
    m: float = 0.0


# ============================================================
# EXAMPLE TAB
# ============================================================

class ExampleTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()

        layout.addWidget(QLabel("This is an example tab."))

        layout.addWidget(QLabel("You can put other functionality here later."))

        layout.addStretch()

        self.setLayout(layout)


# ============================================================
# GRAPH TAB
# ============================================================

class GraphTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.dataset_names = ["Sine Wave", "Cosine Wave", "Linear", "Quad"]

        self.curves = []
        self.color_index = 0
        self.graph_counter = 0
        self.t = 0.0

        self.colors = [
            "r",
            "g",
            "b",
            "m",
            "c",
            "y"
        ]

        self.setup_ui()
        self.setup_timer()

    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):

        main_layout = QHBoxLayout()

        # ----------------------------------------------------
        # LEFT PANEL
        # ----------------------------------------------------

        left_panel = QVBoxLayout()

        # ====================================================
        # CONTROL SECTION
        # ====================================================

        left_panel.addWidget(QLabel("<b>Controls</b>"))

        self.btn_start = self.add_button("Start", self.start_updates, left_panel)
        
        self.btn_stop = self.add_button("Stop", self.stop_updates, left_panel)

        # ====================================================
        # DATASET SECTION
        # ====================================================

        self.dataset_list = self.add_dataset_section(left_panel, self.dataset_names)

        # ====================================================
        # OPTIONS SECTION
        # ====================================================

        self.amp_box, self.omg_box, self.m_box = (self.add_options_section(left_panel))

        # ====================================================
        # GRAPH BUTTONS
        # ====================================================

        self.btn_add = self.add_button("Add Graph", self.add_graph, left_panel)

        self.btn_random = self.add_button("Randomize Data",self.randomize_data,left_panel)

        self.btn_clear = self.add_button("Clear Graph",self.clear_graph,left_panel)

        # ====================================================
        # GRID
        # ====================================================

        self.grid_checkbox = QCheckBox(
            "Show Grid"
        )

        self.grid_checkbox.setChecked(True)

        self.grid_checkbox.stateChanged.connect(
            self.toggle_grid
        )

        left_panel.addWidget(
            self.grid_checkbox
        )

        # ====================================================
        # PLOTTED GRAPHS
        # ====================================================

        left_panel.addWidget(
            QLabel("<b>Plotted Graphs</b>")
        )

        self.graph_list = QListWidget()

        self.graph_list.itemSelectionChanged.connect(
            self.update_selected_graph_info
        )

        left_panel.addWidget(
            self.graph_list
        )

        # ====================================================
        # RIGHT PANEL
        # ====================================================

        right_panel = QVBoxLayout()

        self.plot_widget = pg.PlotWidget()

        self.plot_widget.setBackground(
            "w"
        )

        self.plot_widget.showGrid(
            x=True,
            y=True
        )

        self.plot_widget.addLegend()

        right_panel.addWidget(
            self.plot_widget
        )

        # ====================================================
        # INFO
        # ====================================================

        self.info_label = QLabel(
            "No data yet"
        )

        self.info_label.setStyleSheet(
            """
            background-color: #111;
            color: white;
            padding: 15px;
            """
        )

        right_panel.addWidget(
            self.info_label
        )

        # ====================================================
        # MAIN LAYOUT
        # ====================================================

        main_layout.addLayout(
            left_panel,
            1
        )

        main_layout.addLayout(
            right_panel,
            4
        )

        self.setLayout(
            main_layout
        )

    # ==============
    # Add Buttons
    # ==============
    
    def add_button(self, text, callback, layout=None):
        button = QPushButton(text)
        button.clicked.connect(callback)
    
        if layout is None:
            layout = self.layout()
    
        layout.addWidget(button)
    
        return button

    # ==================
    # Dataset
    # =====================
    
    def add_dataset_section(self, layout, datasets):
        layout.addWidget(QLabel("<b>Datasets</b>"))
    
        dataset_list = QListWidget()
    
        for name in datasets:
            dataset_list.addItem(QListWidgetItem(name))
    
        dataset_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
    
        layout.addWidget(dataset_list)

        return dataset_list

    # Options
    
    def add_options_section(self, layout):
        layout.addWidget(QLabel("<b>Options</b>"))
    
        # Amplitude
        layout.addWidget(QLabel("Amplitude"))
    
        amp_box = QLineEdit()
        amp_box.setValidator(QDoubleValidator())
        amp_box.setPlaceholderText("Amplitude")
    
        layout.addWidget(amp_box)
    
        # Frequency
        layout.addWidget(QLabel("Frequency"))
    
        omg_box = QLineEdit()
        omg_box.setValidator(QDoubleValidator())
        omg_box.setPlaceholderText("Frequency")
    
        layout.addWidget(omg_box)
    
        # Baseline
        layout.addWidget(QLabel("Baseline") )
    
        m_box = QLineEdit()
        m_box.setValidator(QDoubleValidator())
        m_box.setPlaceholderText("Baseline")
    
        layout.addWidget(m_box)

        return amp_box, omg_box, m_box

    # ========================================================
    # TIMER
    # ========================================================

    def setup_timer(self):

        self.timer = QTimer()

        self.timer.timeout.connect(self.update_live_data)

        self.timer.start(1000)

    def start_updates(self):

        self.timer.start(1000)

    def stop_updates(self):

        self.timer.stop()

    # ========================================================
    # OPTIONS
    # ========================================================

    def get_options(self):

        k = 1.0
        omega = 1.0
        m = 0.0

        if self.amp_box.text():
            k = float(self.amp_box.text() )

        if self.omg_box.text():
            omega = float(self.omg_box.text() )

        if self.m_box.text():
            m = float(self.m_box.text() )

        return k, omega, m

    # ========================================================
    # DATA
    # ========================================================

    def get_data(self, selection):

        x = np.linspace(0, 10, 200)

        if selection == "Sine Wave":
            y = np.sin(x)

        elif selection == "Cosine Wave":
            y = np.cos(x)

        elif selection == "Quad":
            y = x ** 2

        else:
            y = x

        return x, y

    # ========================================================
    # ADD GRAPH
    # ========================================================

    def add_graph(self):

        selected_items = (
            self.dataset_list.selectedItems()
        )

        if not selected_items:
            return

        # Read options once
        k, omega, m = self.get_options()

        for item in selected_items:

            selection = item.text()

            x, y = self.get_data(
                selection
            )

            color = self.colors[
                self.color_index
                % len(self.colors)
            ]

            self.color_index += 1

            curve = self.plot_widget.plot(
                x,
                y,
                pen=pg.mkPen(
                    color=color,
                    width=2
                ),
                name=selection
            )

            self.graph_counter += 1

            name = (
                f"{selection} "
                f"#{self.graph_counter}"
            )

            self.graph_list.addItem(
                name
            )

            entry = GraphData(
                curve=curve,
                graph_type=selection,
                name=name,
                x=x,
                y=y,
                k=k,
                omega=omega,
                m=m
            )

            self.curves.append(
                entry
            )

        self.update_limits()

    # ========================================================
    # LIVE UPDATE
    # ========================================================

    def update_live_data(self):

        self.t += 0.2

        t = self.t

        for entry in self.curves:

            x = entry.x

            k = entry.k
            omega = entry.omega
            m = entry.m

            graph_type = entry.graph_type

            if graph_type == "Sine Wave":

                y = (
                    k
                    * np.sin(
                        omega * (x + t)
                    )
                    + m
                )

            elif graph_type == "Cosine Wave":

                y = (
                    k
                    * np.cos(
                        omega * (x + t)
                    )
                    + m
                )

            elif graph_type == "Linear":

                y = (
                    k
                    * (x + (t % 5))
                    + m
                )

            elif graph_type == "Quad":

                y = (
                    k
                    * (x + t) ** 2
                ) % 100 + m

            else:

                y = entry.y

            entry.y = y

            entry.curve.setData(
                x,
                y
            )

        self.update_selected_graph_info()
        self.update_limits()

    # ========================================================
    # ANALYZE DATA
    # ========================================================

    def analyze_data(self, x, y):

        amplitude = (
            np.max(y) -
            np.min(y)
        ) / 2

        mean_val = np.mean(y)

        zero_crossings = np.where(
            np.diff(np.sign(y))
        )[0]

        if len(zero_crossings) > 1:

            periods = np.diff(
                x[zero_crossings]
            )

            avg_period = (
                np.mean(periods) * 2
            )

            frequency = (
                1 / avg_period
                if avg_period != 0
                else 0
            )

        else:

            frequency = 0

        peak_index = np.argmax(y)

        phase = x[peak_index]

        return (
            amplitude,
            mean_val,
            frequency,
            phase
        )

    # ========================================================
    # SELECTED GRAPH INFO
    # ========================================================

    def update_selected_graph_info(self):

        selected_items = (
            self.graph_list.selectedItems()
        )

        if not selected_items:
            return

        selected_name = (
            selected_items[0].text()
        )

        for entry in self.curves:

            if entry.name == selected_name:

                amp, mean_val, freq, phase = (
                    self.analyze_data(
                        entry.x,
                        entry.y
                    )
                )

                self.info_label.setText(
                    f"Dataset: {selected_name}\n"
                    f"Amplitude: {amp:.3f}\n"
                    f"Mean: {mean_val:.3f}\n"
                    f"Frequency: {freq:.3f}\n"
                    f"Phase: {phase:.3f}"
                )

                return

    # ========================================================
    # LIMITS
    # ========================================================

    def update_limits(self):

        if not self.curves:
            return

        all_x = np.concatenate(
            [
                entry.x
                for entry in self.curves
            ]
        )

        all_y = np.concatenate(
            [
                entry.y
                for entry in self.curves
            ]
        )

        x_min = np.min(all_x)
        x_max = np.max(all_x)

        y_min = np.min(all_y)
        y_max = np.max(all_y)

        x_range = x_max - x_min
        y_range = y_max - y_min

        if x_range == 0:
            x_range = 1

        if y_range == 0:
            y_range = 1

        x_pad = x_range * 0.1
        y_pad = y_range * 0.1

        self.plot_widget.setLimits(
            xMin=x_min - x_pad,
            xMax=x_max + x_pad,
            yMin=y_min - y_pad,
            yMax=y_max + y_pad,
            minXRange=0.5,
            maxXRange=x_range * 2,
            minYRange=0.5,
            maxYRange=y_range * 2
        )

    # ========================================================
    # RANDOMIZE
    # ========================================================

    def randomize_data(self):

        for entry in self.curves:

            y = np.random.random(
                len(entry.x)
            )

            entry.y = y

            entry.curve.setData(
                entry.x,
                y
            )

        self.update_selected_graph_info()
        self.update_limits()

    # ========================================================
    # CLEAR
    # ========================================================

    def clear_graph(self):

        self.plot_widget.clear()

        self.plot_widget.addLegend()

        self.curves.clear()

        self.graph_list.clear()

        self.color_index = 0
        self.graph_counter = 0

        self.info_label.setText(
            "No data yet"
        )

    # ========================================================
    # GRID
    # ========================================================

    def toggle_grid(self):

        state = (
            self.grid_checkbox.isChecked()
        )

        self.plot_widget.showGrid(
            x=state,
            y=state
        )

