import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QTabWidget, QScrollArea, QGridLayout, QCheckBox, QLineEdit, QPushButton,
    QSizePolicy
)
from PyQt5.QtGui import QTextCursor
from framework.database import Settings

settings = Settings()

class HomeTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.counters = {
            'Blocked': 0,
            'Deleted': 0
        }
        self.counter_labels = {}
        self.terminal_lines = []
        self.max_lines = 15000
        
        self.init_ui()

    def init_ui(self) -> None:
        main_layout = QVBoxLayout()
        top_layout = self.create_top_layout()

        main_layout.addLayout(top_layout)
        self.create_terminal_area(main_layout)

        self.setLayout(main_layout)

    def set_label_style(self, *labels, font_size: int = 16) -> None:
        for label in labels:
            label.setStyleSheet(f'font-size: {font_size}pt; font-family: "Cascadia Code", "Courier New", monospace;')

    def create_top_layout(self) -> QHBoxLayout:
        top_layout = QHBoxLayout()
        left_layout = self.create_counter_layout()
        top_layout.addLayout(left_layout)
        return top_layout

    def create_counter_layout(self) -> QVBoxLayout:
        left_layout = QVBoxLayout()
        grid = QGridLayout()
        row = 0

        for key, value in self.counters.items():
            name_label = QLabel(key + ':')
            value_label = QLabel(str(value))
            self.counter_labels[key] = value_label
            self.set_label_style(name_label, value_label, font_size = 13)

            grid.addWidget(name_label, row, 0)
            grid.setAlignment(name_label, Qt.AlignLeft)

            grid.addWidget(value_label, row, 1)
            grid.setAlignment(value_label, Qt.AlignRight)

            row += 1

        counter_widget = QWidget()
        counter_widget.setLayout(grid)
        left_layout.addWidget(counter_widget)

        return left_layout

    def create_terminal_area(self, main_layout: QVBoxLayout) -> None:
        terminal_label = QLabel('')
        terminal_label.setStyleSheet('font-size: 14pt;')
        main_layout.addWidget(terminal_label)

        self.terminal_text = QTextEdit()
        self.terminal_text.setReadOnly(True)
        self.set_terminal_style()
        main_layout.addWidget(self.terminal_text)

    def set_terminal_style(self) -> None:
        self.terminal_text.setStyleSheet('''
            font-family: 'Courier New', monospace;
            font-size: 12pt;
            background-color: #1E1E1E;
            color: #D4D4D4;
            border: none;
        ''')

        self.terminal_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.terminal_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def increment_counter(self, key: str) -> None:
        if key in self.counters:
            self.counters[key] += 1
            self.counter_labels[key].setText(str(self.counters[key]))

    def add_to_terminal(self, text: str) -> None:
        if text:
            self.terminal_lines.append(text)
            if len(self.terminal_lines) > self.max_lines:
                self.terminal_lines = self.terminal_lines[-self.max_lines:]

            self.terminal_text.setHtml('<br>'.join(self.terminal_lines))
            self.terminal_text.moveCursor(QTextCursor.End)

class SettingsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.country_buttons = {}
        self.checkboxes = {}
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        block_button = QPushButton('BLOCK NON-US')
        block_button.clicked.connect(self.handle_country_toggle)

        block_button_undo = QPushButton('UNBLOCK ALL')
        block_button_undo.clicked.connect(self.handle_country_unblock_toggle)
        for btn in (block_button, block_button_undo):
            btn.setStyleSheet('''
                QPushButton {
                    font-size: 12pt;
                    font-family: 'Cascadia Code', 'Courier New', monospace;
                    background-color: #DDDDDD;
                    color: black;
                    border: 1px solid #AAAAAA;
                    border-radius: 6px;
                    padding: 8px 12px;
                }
                QPushButton:hover {
                    background-color: #CFCFCF;
                }
                QPushButton:pressed {
                    background-color: #BBBBBB;
                }
            ''')

            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            left_layout.addWidget(btn)

        country_label = QLabel('Countries:')
        country_label.setStyleSheet('margin-top: 8px; font-size: 11pt; font-family: "Cascadia Code", "Courier New", monospace;')
        left_layout.addWidget(country_label)

        country_scroll = QScrollArea()
        country_scroll.setWidgetResizable(True)
        country_widget = QWidget()
        country_layout = QGridLayout(country_widget)
        country_scroll.setWidget(country_widget)
        left_layout.addWidget(country_scroll)

        countries = [
            'AF', 'AL', 'DZ', 'AD', 'AO', 
            'AG', 'AR', 'AM', 'AU', 'AT',
            'AZ', 'BS', 'BH', 'BD', 'BB', 
            'BY', 'BE', 'BZ', 'BJ', 'BT',
            'BO', 'BA', 'BW', 'BR', 'BN', 
            'BG', 'BF', 'BI', 'CV', 'KH',
            'CM', 'CA', 'CF', 'TD', 'CL', 
            'CN', 'CO', 'KM', 'CD', 'CG',
            'CR', 'CI', 'HR', 'CU', 'CY', 
            'CZ', 'DK', 'DJ', 'DM', 'DO',
            'EC', 'EG', 'SV', 'GQ', 'ER', 
            'EE', 'SZ', 'ET', 'FJ', 'FI',
            'FR', 'GA', 'GM', 'GE', 'DE', 
            'GH', 'GR', 'GD', 'GT', 'GN',
            'GW', 'GY', 'HT', 'HN', 'HU', 
            'IS', 'IN', 'ID', 'IR', 'IQ',
            'IE', 'IL', 'IT', 'JM', 'JP', 
            'JO', 'KZ', 'KE', 'KI', 'KP',
            'KR', 'KW', 'KG', 'LA', 'LV', 
            'LB', 'LS', 'LR', 'LY', 'LI',
            'LT', 'LU', 'MG', 'MW', 'MY', 
            'MV', 'ML', 'MT', 'MH', 'MR',
            'MU', 'MX', 'FM', 'MD', 'MC', 
            'MN', 'ME', 'MA', 'MZ', 'MM',
            'NA', 'NR', 'NP', 'NL', 'NZ', 
            'NI', 'NE', 'NG', 'MK', 'NO',
            'OM', 'PK', 'PW', 'PA', 'PG', 
            'PY', 'PE', 'PH', 'PL', 'PT',
            'QA', 'RO', 'RU', 'RW', 'KN', 
            'LC', 'VC', 'WS', 'SM', 'ST',
            'SA', 'SN', 'RS', 'SC', 'SL', 
            'SG', 'SK', 'SI', 'SB', 'SO',
            'ZA', 'SS', 'ES', 'LK', 'SD', 
            'SR', 'SE', 'CH', 'SY', 'TW',
            'TJ', 'TZ', 'TH', 'TL', 'TG', 
            'TO', 'TT', 'TN', 'TR', 'TM',
            'TV', 'UG', 'UA', 'AE', 'GB', 
            'US', 'UY', 'UZ', 'VU', 'VA',
            'VE', 'VN', 'YE', 'ZM', 'ZW',
            'PS', 'PR', 'RE', 'YT', 'SH', 'EH'
        ]
        
        for i, code in enumerate(countries):
            btn = QPushButton(code)
            btn.setCheckable(True)
            btn.setFixedSize(50, 40)
            btn.setStyleSheet('''
                QPushButton {
                    font-size: 11pt;
                    font-weight: bold;
                    background-color: #F1F1F1;
                    color: black;
                    border: 1px solid #AAAAAA;
                    border-radius: 6px;
                }
                              
                QPushButton:hover {
                    background-color: #E0E0E0;
                }
                              
                QPushButton:pressed {
                    background-color: #CCCCCC;
                }
                              
                QPushButton:checked {
                    background-color: #4A90E2;
                    color: white;
                }
            ''')

            self.country_buttons[code] = btn

            btn.setChecked(code in settings.get_countries())
            btn.toggled.connect(lambda checked, c = code: self.toggle_country(c, checked)) 

            country_layout.addWidget(btn, i // 5, i % 5)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)

        for label in ['Delete Chat', 'Block User', 'Log User Info', 'Log Successful Block', 'Log Successful Delete', 'Log Errors']:
            box = QCheckBox(label)
            box.setStyleSheet('''
                QCheckBox {
                    font-size: 13pt;
                    font-family: 'Cascadia Code', 'Courier New', monospace;
                    spacing: 10px;
                    margin-bottom: 6px;
                }

                QCheckBox::indicator {
                    width: 14px;
                    height: 14px;
                    border: 2px solid #888;
                    border-radius: 4px;
                    background-color: transparent;
                }

                QCheckBox::indicator:checked {
                    background-color: #BBBBBB;
                    border: 2px solid #BBBBBB;
                }

                QCheckBox::indicator:hover {
                    border: 2px solid #CFCFCF;
                }
            ''')
            self.checkboxes[label] = box
            initial = {
                'Delete Chat': settings.get_delete_chat,
                'Block User': settings.get_block_user,
                'Log User Info': settings.get_log_user_info,
                'Log Successful Block': settings.get_log_block,
                'Log Successful Delete': settings.get_log_delete,
                'Log Errors': settings.get_log_errors
            }[label]

            box.setChecked(initial())

            box.stateChanged.connect(lambda state, l=label: self.handle_settings_toggle(l, state))
            right_layout.addWidget(box)

        right_layout.addStretch()

        token_label = QLabel('Bot Token:')
        token_label.setStyleSheet('font-size: 11pt; font-family: "Cascadia Code", "Courier New", monospace;')
        
        right_layout.addWidget(token_label)

        self.token_input = QLineEdit()
        self.token_input.setStyleSheet('''
            QLineEdit {
                font-size: 12pt;
                font-family: 'Cascadia Code', 'Courier New', monospace;
                padding: 8px;
                background-color: #FAFAFA;
                color: #222;
                border: 1px solid #BBBBBB;
                border-radius: 6px;
            }
            QLineEdit:focus {
                border: 1px solid #4A90E2;
                background-color: #FFFFFF;
            }
        ''')
        self.token_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        right_layout.addWidget(self.token_input)

        save_btn = QPushButton('SAVE')
        save_btn.setFixedHeight(32)
        save_btn.setStyleSheet('''
            QPushButton {
                font-size: 12pt;
                font-family: 'Cascadia Code', 'Courier New', monospace;
                background-color: #CCCCCC;
                color: black;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #CFCFCF;
            }
            QPushButton:pressed {
                background-color: #BBBBBB;
            }
        ''')

        save_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        right_layout.addWidget(save_btn)

        layout.addWidget(left_panel, stretch=1)
        layout.addWidget(right_panel, stretch=0)
        self.setLayout(layout)

    def toggle_country(self, code, checked):
        if not checked:
            settings.remove_countries([code])
            self.main_window.log_to_terminal(f"""[<span style="color: lightblue;">REGION</span>] Removed '{code}' from Blocked Countries """)
            return
        
        self.main_window.log_to_terminal(f"""[<span style="color: lightblue;">REGION</span>] Added '{code}' to Blocked Countries""")
        settings.add_countries([code])

    def handle_country_toggle(self):
        disabled = []

        for code, button in self.country_buttons.items():
            if code == 'US':
                button.setChecked(False)
                continue

            button.setChecked(True)
            disabled.append(code)

        self.main_window.log_to_terminal(f'[<span style="color: lightblue;">REGION</span>] Blocked {len(self.country_buttons.items())} Countries (Excluding: US)')
        settings.add_countries(disabled)

    def handle_country_unblock_toggle(self):
        enabled = []

        for code, button in self.country_buttons.items():
            button.setChecked(False)
            enabled.append(code)
        
        self.main_window.log_to_terminal(f'[<span style="color: lightblue;">REGION</span>] Unblocked {len(self.country_buttons.items())} Countries')
        settings.remove_countries(enabled)

    def handle_settings_toggle(self, label, state):
        labels = {
            'Delete Chat': settings.configure_delete_chat,
            'Block User': settings.configure_block_user,
            'Log User Info': settings.configure_log_user_info,
            'Log Successful Block': settings.configure_log_block,
            'Log Successful Delete': settings.configure_log_delete,
            'Log Errors': settings.configure_log_errors
        }

        for _label, function in labels.items():
            if _label == label:
                function(state)
                self.main_window.log_to_terminal(f"""[<span style="color: lightblue;">CONFIG</span>] {'Enabled' if state else 'Disabled'} '{label}' """)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('JB')
        self.setFixedSize(800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.home_tab = HomeTab()
        self.settings_tab = SettingsTab(self)

        self.tabs.addTab(self.home_tab, 'Home')
        self.tabs.addTab(self.settings_tab, 'Settings')

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def log_to_terminal(self, message: str):
        self.home_tab.add_to_terminal(message)

    def increment_counter(self, key: str):
        self.home_tab.increment_counter(key)

app = QApplication(sys.argv)
