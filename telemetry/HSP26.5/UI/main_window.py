# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 11:35:07 2026

@author: oscar
"""


"""
Denna modulen hanterar flikarna och är huvudprogram i UI

Om det i framtiden blir fler sidor(inte fler flikar) ska denna vara ett underprogram
"""


# Kör denna modulen i kommandotolken
#     C:\Users\oscar\Documents\HUST\HSP26.5>python -m UI.main_window


from .lora_tab import *

# ============================================================
# MAIN WINDOW
# ============================================================

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("HUST Strategy")

        self.resize(1200,700)

        self.setup_ui()

    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):

        container = QWidget()

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(0)

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = QWidget()

        header_layout = QHBoxLayout()

        # Logo
        logo = QLabel()

        pixmap = QPixmap("Logo.png")

        if not pixmap.isNull():

            logo.setPixmap(pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio))

        header_layout.addWidget(logo)

        # Title
        title = QLabel("HUST Strategy Control Panel")

        title.setStyleSheet(
            """
            font-size: 20px;
            font-weight: bold;
            """
        )

        header_layout.addWidget(title)

        header_layout.addStretch()

        header.setLayout(header_layout)

        # ----------------------------------------------------
        # TABS
        # ----------------------------------------------------

        self.tabs = QTabWidget()

        self.graph_tab = GraphTab()

        self.example_tab = ExampleTab()
        
        self.lora_tab = LoraTab()

        self.tabs.addTab(
            self.graph_tab,
            "Graph"
        )

        self.tabs.addTab(
            self.example_tab,
            "Example"
        )
        
        self.tabs.addTab(
            self.lora_tab,
            "LoRa"
        )

        # ----------------------------------------------------
        # MAIN LAYOUT
        # ----------------------------------------------------

        layout.addWidget(
            header
        )

        layout.addWidget(
            self.tabs
        )

        container.setLayout(
            layout
        )

        self.setCentralWidget(
            container
        )


# ============================================================
# APPLICATION
# ============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )
