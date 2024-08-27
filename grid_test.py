import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自动生成表格和折线图示例")
        self.setGeometry(100, 100, 800, 400)

        # 创建一个QTableWidget
        self.table_widget = QTableWidget()

        # 创建一个按钮
        self.button = QPushButton("更新表格")
        self.button.clicked.connect(self.update_table)

        # 创建一个布局并添加表格和按钮
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.button)

        # 创建一个中央窗口部件并设置布局
        central_widget = QWidget()
        central_layout = QHBoxLayout()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # 添加表格布局到中央布局
        central_layout.addLayout(layout)

        # 创建一个FigureCanvas来显示图表
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        central_layout.addWidget(self.canvas)

        # 示例数据
        self.data = [
            {"uid": "12345", "name": "Alice", "score": 95},
            {"uid": "67890", "name": "Bob", "score": 88},
            {"uid": "54321", "name": "Charlie", "score": 92},
        ]

        # 根据数据生成表格和图表
        self.generate_table(self.data)
        self.plot_graph(self.data)

    def generate_table(self, data):
        # 设置表格行数和列数
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(data[0]))

        # 设置表头
        self.table_widget.setHorizontalHeaderLabels(data[0].keys())

        # 填充表格数据
        for row_index, row_data in enumerate(data):
            for col_index, (key, value) in enumerate(row_data.items()):
                self.table_widget.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    def plot_graph(self, data):
        # 清除之前的图表
        self.figure.clear()

        # 创建一个新的子图
        ax = self.figure.add_subplot(111)

        # 提取数据
        names = [row["name"] for row in data]
        scores = [row["score"] for row in data]

        # 绘制折线图
        ax.plot(names, scores, marker='o')

        # 设置图表标题和标签
        ax.set_title("Scores by Name")
        ax.set_xlabel("Name")
        ax.set_ylabel("Score")

        # 刷新图表
        self.canvas.draw()

    def update_table(self):
        # 更新数据
        self.data = [
            {"uid": "12345", "name": "Alice", "score": 95, "other": "o1"},
            {"uid": "67890", "name": "Bob", "score": 88, "other": "o1"},
            {"uid": "54321", "name": "Charlie", "score": 92},
            {"uid": "98765", "name": "David", "score": 85, "other": "o1"},  # 新增数据
        ]
        # 重新生成表格和图表
        self.generate_table(self.data)
        self.plot_graph(self.data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())