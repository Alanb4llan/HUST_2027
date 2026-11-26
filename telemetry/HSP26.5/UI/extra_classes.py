# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 17:13:27 2026

@author: oscar
"""

from PyQt6.QtWidgets import QListWidget

class ToggleListWidget(QListWidget):
    def mousePressEvent(self, event):
        item = self.itemAt(event.position().toPoint())

        if item and item.isSelected():
            self.clearSelection()
            self.setCurrentItem(None)
        else:
            super().mousePressEvent(event)