# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 13:04:55 2026

@author: oscar
"""

"""
Denna modulen är en utveckling av GraphTab

Anpassning till Lora görs i:
    __init__
    start_updates
    stop_updates
    data !!!
"""

from .UI2 import *

from LORA.Receiver import *

from .extra_classes import *

from Strategi.FORB import get_consumption
from Strategi.SOLBIL import *

"""

Fortsätt runt rad 460 för att lägga till funktioner

2026-10-14 Nu borde funktioner fungera, 
    nästa steg är att göra det möjligt att byta namn på respektive dataindex
    det visar sig att en del av värdena har fått fel index.
    Detta är i dataset_names, innehållet kanske ska finnas i en .txt fil så
    att när du ändrar namnen sparas de tills vidare.
    
    Det behöver också bli mer flexibelt vilken typ av funktioner som går att 
    skapa.
    
2026-11-04 Nu har problemet med mer flexibla funktioner lösts
    förutsatt att du följer "mönstret" för hur man programerar de andra 
    delarna.
    Mönstret är:
        1. Lägg till i complex names
        2. Gå till funktionen add_graph_button_clicked och lägg till ett 
            fall som uppfyller den nya funktionens vilkor. 
            Inkludera funktionen i steg 3
        3. Definiera en datahämtningsfunktion anpassad för din funktion 
            använd get_data_mult som referens för hur man ska göra
        4. Lägg till i update_live_data så att datan uppdateras
        
Nästa steg är att lägga till en graf där det går att se data relativt till distansen
    2026-11-11 Fixat, nu går det att lägga till distans på all data 
"""

# ============================================================
# LORA TAB
# ============================================================

class LoraTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # De enkla standard värdena
        self.dataset_names = ["hastighet",
        "distans",
        "batteri spänning",
        "batteri ström",
        "batteri_cell låg",
        "batteri cell hög spänninf",
        "batteri cell snitt volt",
        "batteri cell låg temp",
        "batteri cell hög temp",
        "batteri cell snitt temp",
        "batteri cell id låg",
        "BMS temp",
        "motor temp",
        "motor ström",
        "motor controller temp",
        "MPPT input power 1",
        "MPPT input power 2",
        "MPPT input power 3",
        "MPPT input power tot"]
        
        # Värdena som är funktioner av flera av värdena ovan
        
        self.complex_names = [
            {"name" : "Motor förbrukning", "method": "mult", "name1": "motor ström", "name2": "batteri spänning"}, # motor ström * batteri spänning
            {"name" : "MPPT Total", "method": "add", "selections": ["MPPT input power 1", # Hämtar summan av alla MPPT:er
                                                                    "MPPT input power 2",
                                                                    "MPPT input power 3",
                                                                    "MPPT input power tot"]},
            {"name" : "Estimerad förbrukning", "method": "cons", "solar_car": henry},
            {"name" : "Estimerad lutning", "method": "angle", "solar_car": henry}
            ]

        self.curves = []
        self.color_index = 0
        self.graph_counter = 0
        self.t = 0.0
        self.distance = False
        self.index = False

        self.colors = [
            "r",
            "g",
            "b",
            "m",
            "c",
            "y"
        ]
        
        self.lora = read_lora(False, False)

        self.setup_ui()
        self.setup_timer()

    # ========================================================
    # UI
    # Om man gör om tabs till en abstrct typ eller liknande kommer denna setup_ui att bestämma
    # utseendet för varje specifik tab i programmet.
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

        #self.amp_box, self.omg_box, self.m_box = (self.add_options_section(left_panel))

        # ====================================================
        # GRAPH BUTTONS
        # ====================================================

        self.btn_add = self.add_button("Add Graph", self.add_graph_button_clicked, left_panel)

        #self.btn_random = self.add_button("Randomize Data",self.randomize_data,left_panel)

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
        
        # ====
        # Indexera värdena så att de går att jämföra
        # ====
        
        self.index_checkbox = QCheckBox(
            "Indexera värden"
        )

        self.index_checkbox.setChecked(True)

        self.index_checkbox.stateChanged.connect(
            self.index_values
        )

        left_panel.addWidget(
            self.index_checkbox
        )
        
        # =====================
        # Visa värdena mot distans
        # ===============================
        
        self.distance_checkbox = QCheckBox(
            "Värden mot distans"
        )

        self.distance_checkbox.setChecked(True)

        self.distance_checkbox.stateChanged.connect(
            self.distance_setter
        )

        left_panel.addWidget(
            self.distance_checkbox
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
        
        
        # =========================
        # Middle Panel
        # ==========================
        
        mid_panel = QVBoxLayout()

        # ====================================================
        # CONTROL SECTION
        # ====================================================

        mid_panel.addWidget(QLabel("<b>Controls</b>"))

        #self.btn_start = self.add_button("Start", self.start_updates, left_panel)
        
        #self.btn_stop = self.add_button("Stop", self.stop_updates, left_panel)

        # ====================================================
        # DATASET SECTION
        # ====================================================

        self.dataset_list_2 = self.add_dataset_section_adv(mid_panel, [n["name"] for n in self.complex_names])

        

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
            padding: 18px;
            """
        )

        right_panel.addWidget(
            self.info_label
        )

        # ====================================================
        # MAIN LAYOUT
        # ====================================================

        main_layout.addLayout(left_panel, 1)
        
        main_layout.addLayout(mid_panel, 1)

        main_layout.addLayout(right_panel, 4)

        self.setLayout(main_layout)

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
    
        #dataset_list = QListWidget()
        dataset_list = ToggleListWidget()
    
        for name in datasets:
            dataset_list.addItem(QListWidgetItem(name))
    
        #dataset_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        dataset_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
    
        #dataset_list.itemClicked.connect(self.toggle_selection)
    
        layout.addWidget(dataset_list)

        return dataset_list
    
    # Denna ska kunna ha funktioner av input
    def add_dataset_section_adv(self, layout, datasets):
        layout.addWidget(QLabel("<b>Datasets</b>"))
    
        dataset_list = ToggleListWidget()
        dataset_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
    
    
        for dataset in datasets:
            item = QListWidgetItem(dataset)
            item.setData(Qt.ItemDataRole.UserRole, dataset)
            dataset_list.addItem(item)

        layout.addWidget(dataset_list)
        

        return dataset_list
    
    
    def toggle_selection(self, item):
        if item.isSelected():
            list_widget = item.listWidget()
            list_widget.clearSelection()

        
    # Options
    
    """
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
    """
    
    # ========================================================
    # TIMER
    # ========================================================

    def setup_timer(self):

        self.timer = QTimer()

        self.timer.timeout.connect(self.update_live_data)

        self.timer.start(200)

    def start_updates(self):

        self.lora.read = True

    def stop_updates(self):

        self.lora.read = False

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
    
    def index_normalize(self, y):
        if self.index:
            avg = sum(y)/len(y)
            y = [y[i] / avg for i in range(len(y))]
        return y
    
    def get_x(self, data):
        x = []
        if self.distance:
            x = [float(d[self.dataset_names.index("distans")]) for d in data]
        else:
            x = np.linspace(0, len(data), len(data))
        return x
    
    def get_x_and_y(self, data, y):
        y = self.index_normalize(y)

        x = self.get_x(data)
        
        if y == []:
            y = [0, 1]
            x = [0, 1]
            
        return x, y

    def get_data(self, selection):
        """
        Detta är för att hämta enkel data som förekommer direkt
        """
        
        data = self.lora.points
        #print("Data: "+str(data))
        
        y = [float(d[self.dataset_names.index(selection)]) for d in data]
        
        """
        # Om vi ska indexera värdena så att de går att jämföra med varandra
        y = self.index_normalize(y)
        
        #print("y: "+str(y))

        x = self.get_x()
        
        if y == []:
            y = [0, 1]
            x = [0, 1]
        """
        
        x, y = self.get_x_and_y(data, y)
        
        return x, y
    
    
    def get_data_mult(self, selection1, selection2):
        """
        Denna modulen används för att ta fram data som är en multiplikation 
        av flera datainputs.
        """
        
        data = self.lora.points
        #print("Data: "+str(data))
        
        y1 = [float(d[self.dataset_names.index(selection1)]) for d in data]
        y2 = [float(d[self.dataset_names.index(selection2)]) for d in data]
        
        #print("y: "+str(y))
        
        y = [y1[i] * y2[i] for i in range(len(y1))]
        
        """
        # Om vi ska indexera värdena så att de går att jämföra med varandra
        y = self.index_normalize(y)

        x = self.get_x(data)
        
        if y == []:
            y = [0, 1]
            x = [0, 1]
        """
        x, y = self.get_x_and_y(data, y)
        
        return x, y
    
    
    def get_data_add(self, selections):
        """
        Lägger ihop alla värden i listan 
        ex om [a, b, c] och a = [1,2,3], b = [1,1,1], c = [6,3,1]
        ger x = a + b + c = [8, 6, 5]
        Dvs summeringen sker separat på varje index
        """
        
        data = self.lora.points
        #print("Data: "+str(data))
        ys = []
        ya = []
        
        for selection in selections:
            ya = [float(d[self.dataset_names.index(selection)]) for d in data]
            ys.append(ya)
        
        #print("y: "+str(y))
        
        y = [sum(values) for values in zip(*ys)]
        
        """
        # Om vi ska indexera värdena så att de går att jämföra med varandra
        y = self.index_normalize(y)
        
        #y = [ for i in range(len(ya))]

        x = self.get_x(data)
        
        if y == []:
            y = [0, 1]
            x = [0, 1]
        """
        x, y = self.get_x_and_y(data, y)
        
        return x, y
    
    
    def get_data_cons(self, solar_car):
        """
        Denna modulen används för att ta fram den estimerade konsumtionen utifrån hastigheten
        """
        
        data = self.lora.points
        #print("Data: "+str(data))
        yv = [float(d[self.dataset_names.index("hastighet")]) for d in data]
        yl = [float(d[self.dataset_names.index("distans")]) for d in data]
        
        y = [0] + [get_consumption(yv[i], yl[i-1]/1000, yl[i]/1000, solar_car) + solar_car.weight * (yv[i]-yv[i-1])**2 for i in range(1, len(yv))]
        #print(y)
        
        """
        # Om vi ska indexera värdena så att de går att jämföra med varandra
        y = self.index_normalize(y)
        
        x = np.linspace(0, len(y), len(y))
        
        if y == []:
            y = [0, 1]
            x = [0, 1]
        """
        x, y = self.get_x_and_y(data, y)
        
        return x, y
    
    
    def get_data_angle(self, solar_car):
        """
        Denna funktionen används för att ta fram den estimerade vinklen utifrån
        differensen mellan den estimerade och den faktiska förbrukningen
        
        Denna kan eventuellt förkortas genom att använda get_data_cons och get_data_mult
        Dock bör man isåfall betänka om indexeringen kommer att påverka resultatet
        """
        
        data = self.lora.points
        
        # Räkna ut den estimerade förbrukningen
        #print("Data: "+str(data))
        yv = [float(d[self.dataset_names.index("hastighet")]) for d in data]
        yl = [float(d[self.dataset_names.index("distans")]) for d in data]
        
        y1 = [0] + [get_consumption(yv[i], yl[i-1]/1000, yl[i]/1000, solar_car) + solar_car.weight * (yv[i]-yv[i-1])**2 for i in range(1, len(yv))]
        #print(y)
        
        # Räknar ut den faktiska förbrukningen
        name1 = "motor ström" 
        name2 = "batteri spänning"
        
        ym1 = [float(d[self.dataset_names.index(name1)]) for d in data]
        ym2 = [float(d[self.dataset_names.index(name2)]) for d in data]

        ym = [ym1[i] * ym2[i] for i in range(len(ym1))]
        
        # Vi tar fram differensen
        yd = [ym[i] - y1[i] for i in range(len(ym))]
        
        # Sedan använder vi funktionen för gradientmotstånd och inverterar funktionen
        # resistance = mass*g * m.sin(alpha) 
        # angle = m.asin(res/(mass*g))
        y = [m.asin(yd[i] / (solar_car.weight*g))*180/3.14159 for i in range(len(yd))]
        
        """
        # Om vi ska indexera värdena så att de går att jämföra med varandra
        y = self.index_normalize(y)
        
        x = np.linspace(0, len(y), len(y))
        
        if y == []:
            y = [0, 1]
            x = [0, 1]
        """
        x, y = self.get_x_and_y(data, y)
        
        return x, y
    

    # ========================================================
    # ADD GRAPH
    # ========================================================
    
    def add_graph_button_clicked(self):

        selected_items = self.dataset_list.selectedItems()
        items2 = self.dataset_list_2.selectedItems()
        
        #for obj in items2:
        #    print(obj)
        
        selected_data = [
            item.data(Qt.ItemDataRole.UserRole)
            for item in items2
        ]
        
        if len(selected_data) >= 2:
            result = selected_data[0] * selected_data[1]
            selected_items.append(result)
    
        if not selected_items and not items2:
            print("No selected items")
            return
    
        #k, omega, m = self.get_options()
    
        for item in selected_items:
    
            name = item.text()
            #print(name)
    
            # Get the data from wherever you want
            x, y = self.get_data(name)
    
            #self.add_graph(name, x, y, k, omega, m)
            self.add_graph(name, x, y)
            
        for com in self.complex_names:
            name = com["name"]
            #print(items2)
            found = name in [n.text() for n in items2]
            #print(items2[0].text())
    
            if found and com["method"] == "mult":
                name1 = com["name1"]
                name2 = com["name2"]
                
                # Get the data from wherever you want
                x, y = self.get_data_mult(name1, name2)
        
                self.add_graph(name, x, y)
                
            elif found and com["method"] == "add":
                selections = com["selections"]
        
                # Get the data from wherever you want
                x, y = self.get_data_add(selections)
        
                self.add_graph(name, x, y)
                
            elif found and com["method"] == "cons":
                solar_car = com["solar_car"]
        
                # Get the data from wherever you want
                x, y = self.get_data_cons(solar_car)
        
                self.add_graph(name, x, y)
                
            elif found and com["method"] == "angle":
                solar_car = com["solar_car"]
        
                # Get the data from wherever you want
                x, y = self.get_data_angle(solar_car)
        
                self.add_graph(name, x, y)
    
    
    def add_graph(self, name, x, y, k=1.0, omega=1.0, m=0.0):

        color = self.colors[self.color_index % len(self.colors)]
        self.color_index += 1
    
        curve = self.plot_widget.plot(x, y, pen=pg.mkPen(color=color, width=2), name=name)
    
        self.graph_counter += 1
        graph_name = f"{name} #{self.graph_counter}"
    
        self.graph_list.addItem(graph_name)
    
        entry = GraphData(curve=curve, graph_type=name, name=graph_name, x=np.asarray(x), y=np.asarray(y), k=k, omega=omega, m=m)
    
        self.curves.append(entry)
    
        self.update_limits()
        
    
    # ========================================================
    # LIVE UPDATE
    # ========================================================

    def update_live_data(self):

        self.lora.read_data()
        
        for entry in self.curves:
            if entry.graph_type in self.dataset_names:
                x, y = self.get_data(entry.graph_type)
            else:
                name = entry.graph_type
                print(name)
                my_dict = {}
                for n in self.complex_names:
                    if n["name"] == name:
                        my_dict = n
                        
                idx = self.complex_names.index(my_dict)
                
                if self.complex_names[idx]["method"] == "mult":
                    name1 = self.complex_names[idx]["name1"]
                    name2 = self.complex_names[idx]["name2"]
                    x, y = self.get_data_mult(name1, name2)
                elif self.complex_names[idx]["method"] == "add":
                    selects = self.complex_names[idx]["selections"]
                    x, y = self.get_data_add(selects)
                elif self.complex_names[idx]["method"] == "cons":
                    solar_car = self.complex_names[idx]["solar_car"]
                    x, y = self.get_data_cons(solar_car)
                elif self.complex_names[idx]["method"] == "angle":
                    solar_car = self.complex_names[idx]["solar_car"]
                    x, y = self.get_data_angle(solar_car)
            self.update_graph_data(entry, x, y)
        
        self.update_selected_graph_info()
        self.update_limits()
        
    # Update
    
    def update_graph_data(self, entry, x, y):
        entry.x = np.asarray(x)
        entry.y = np.asarray(y)
    
        entry.curve.setData(entry.x, entry.y)
    
        self.update_selected_graph_info()
        self.update_limits()

    # ========================================================
    # ANALYZE DATA
    # ========================================================

    def analyze_data(self, x, y):

        amplitude = (np.max(y) - np.min(y))

        mean_val = np.mean(y)

        zero_crossings = np.where(np.diff(np.sign(y)))[0]

        if len(zero_crossings) > 1:

            periods = np.diff(x[zero_crossings])

            avg_period = (np.mean(periods) * 2)

        last = y[-1]

        peak_index = np.argmax(y)

        phase = x[peak_index]

        return (amplitude, mean_val, last, phase)

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

                amp, mean_val, last, phase = (
                    self.analyze_data(
                        entry.x,
                        entry.y
                    )
                )

                self.info_label.setText(
                    f"Dataset: {selected_name}\n"
                    f"Amplitude: {amp:.3f}\n"
                    f"Mean: {mean_val:.3f}\n"
                    f"Senaste: {last:.3f}\n"
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
        
    # =====
    # Indexera värdena
    # =====
    
    def index_values(self):

        state = (
            self.index_checkbox.isChecked()
        )

        self.index = state
        
    # ===========
    # Visa distans på X axeln
    # ============
    
    def distance_setter(self):

        state = (
            self.distance_checkbox.isChecked()
        )

        self.distance = state
    
