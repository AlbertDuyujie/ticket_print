import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QSpinBox, QPushButton, QDateTimeEdit, QFormLayout, QScrollArea, QLineEdit, QDateEdit
from PyQt5.QtCore import QDateTime, Qt, QDate
import numpy as np
import random
import win32print
import win32ui
from wcwidth import wcswidth
from datetime import datetime, timedelta
import time

base_interval = 16
store_name = "喜湘湘特色菜"


def get_weekdays(start_date, end_date):
    # 转换字符串日期为 datetime 对象
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # 获取当前年份并更新日期的年份（假设同一年）
    current_year = datetime.now().year
    start_date = start_date.replace(year=current_year)
    end_date = end_date.replace(year=current_year)

    # 检查如果开始日期大于结束日期，交换它们
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    # 生成日期范围
    current_date = start_date
    weekdays = []

    while current_date <= end_date:
        # 如果不是周末(周一到周五)
        if current_date.weekday() < 5:
            weekdays.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    return weekdays

def get_random_time():
    # 定义时间段
    now = datetime.now()
    today_midnight = datetime.combine(now.date(), datetime.min.time())  # 使用 datetime.min.time()

    # 上午11点到下午1点半
    start_morning = today_midnight + timedelta(hours=11)
    end_morning = today_midnight + timedelta(hours=13, minutes=30)

    # 下午5点半到晚上9点半
    start_evening = today_midnight + timedelta(hours=17, minutes=30)
    end_evening = today_midnight + timedelta(hours=21, minutes=30)

    # 随机选择一个时间段
    if random.choice([True, False]):
        selected_time = random_time(start_morning, end_morning)  # 使用不同的变量名
        random_timestamp = selected_time.strftime("%H:%M:%S")
        return selected_time, random_timestamp
    else:
        selected_time = random_time(start_evening, end_evening)  # 使用不同的变量名
        random_timestamp = selected_time.strftime("%H:%M:%S")
        return selected_time, random_timestamp

def random_time(start, end):
    # 返回在 start 和 end 时间之间的随机时间
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

def generate_receipt(order):
    # 准备小票标题和日期时间
    receipt_lines = [
        f"               {store_name}              ",
        "",
        "******************************************",
        "",
        f"日期:{order['date']}",
        "",
        f"时间:{order['timestamp']}",
        "",
        "------------------------------------------",
        "",
        "{:<12}{:<8}{:<8}{:<8}".format("商品", "数量", "单价", "总价"),
        "",
        "------------------------------------------"
    ]

    # 添加每个菜品的信息
    total_amount = 0.0
    for dish, (quantity, unit_price) in order["meal_info"].items():
        total_price = quantity * unit_price
        total_amount += total_price
        a = base_interval - (wcswidth(dish)//2)
        receipt_lines.append(f"{dish:<{a}}{quantity:<9}{unit_price:>6.2f}{total_price:>12.2f}")
    
    # 添加分隔线和总计
    receipt_lines.append("------------------------------------------")
    receipt_lines.append("------------------------------------------")
    receipt_lines.append(f"总计:{total_amount:.2f}")
    receipt_lines.append("")
    receipt_lines.append("谢谢惠顾，欢迎下次光临!")
    receipt_lines.append("------------------------------------------")
    receipt_lines.append("******************************************")

    # 将列表转换为字符串
    receipt_content = "\n".join(receipt_lines)
    return receipt_content

def print_receipt(menu_info):
    # 获取默认打印机
    printer_name = win32print.GetDefaultPrinter()
    # print(receipt_text)
    # 打开打印机
    hprinter = win32print.OpenPrinter(printer_name)


    # try:
    #     hjob = win32print.StartDocPrinter(hprinter, 1, ("Receipt", None, "RAW"))
    #     try:
    #         win32print.StartPagePrinter(hprinter)
    #         # 打印内容
    #         receipt_text = generate_receipt(menu_info)
    #         print(receipt_text)
    #         # ESC/POS指令
    #         ESC = b'\x1b'
    #         GS = b'\x1d'
    #         cut_paper = GS + b'V' + b'\x01'  # 半切纸指令

    #         # 打印文本
    #         # win32print.WritePrinter(hprinter, receipt_text.encode('gb18030'))  # 使用GB18030编码避免中文乱码

    #         # 发送切纸指令
    #         # win32print.WritePrinter(hprinter, cut_paper)

    #         # 结束打印页面
    #         # win32print.EndPagePrinter(hprinter)
    #     finally:
    #         # 结束打印作业
    #         win32print.EndDocPrinter(hprinter)
    # finally:
    #     # 关闭打印机
    #     win32print.ClosePrinter(hprinter)

    try:
        hjob = win32print.StartDocPrinter(hprinter, 1, ("Receipt", None, "RAW"))
        try:
            win32print.StartPagePrinter(hprinter)
            # 打印内容
            receipt_text = generate_receipt(menu_info)
            # ESC/POS指令
            ESC = b'\x1b'
            GS = b'\x1d'
            cut_paper = GS + b'V' + b'\x01'  # 半切纸指令

            # 打印文本
            win32print.WritePrinter(hprinter, receipt_text.encode('gb18030'))  # 使用GB18030编码避免中文乱码

            # 发送切纸指令
            win32print.WritePrinter(hprinter, cut_paper)

            # 结束打印页面
            win32print.EndPagePrinter(hprinter)
        finally:
            # 结束打印作业
            win32print.EndDocPrinter(hprinter)
    finally:
        # 关闭打印机
        win32print.ClosePrinter(hprinter)


def random_menu():
    selected_dishes = {}
    order_meal_number = random.choice([1, 2])
    for i in range(order_meal_number):
        dish_meal = random.choice(list(menu["中式炒菜"].keys()))
        if dish_meal in selected_dishes:
            selected_dishes[dish_meal][0] += 1
        else:
            selected_dishes[dish_meal] = [1, menu["中式炒菜"][dish_meal]]
    order_drinks_number = random.choice([0, 1, 2])
    for i in range(order_drinks_number):
        dish_drinks = random.choice(list(menu["饮料"].keys()))
        if dish_drinks in selected_dishes:
            selected_dishes[dish_drinks][0] += 1
        else:
            selected_dishes[dish_drinks] = [1, menu["饮料"][dish_drinks]]
    order_rice = random.choice([1])
    for i in range(order_rice):
        dish_staple = random.choice(list(menu["主食"].keys()))
        if dish_staple in selected_dishes:
            selected_dishes[dish_staple][0] += 1
        else:
            selected_dishes[dish_staple] = [1, menu["主食"][dish_staple]]
    return selected_dishes

def print_order(order, check_random, timestamp, start_time, end_time):
    selected_dishes = random_menu()
    print_info = {}
    if check_random:
        # 将 QDate 对象转换为字符串格式
        start_time_str = start_time.toString("yyyy-MM-dd")
        end_time_str = end_time.toString("yyyy-MM-dd")
        time_period = get_weekdays(start_time_str, end_time_str)
        random_period = random.sample(time_period, 2)
        print(time_period, random_period)
        if time_period != []:
            print(time_period)
            for i in random_period:
                print_info["date"] = i
                print_info["meal_info"] = selected_dishes
                print_info["timestamp"] = get_random_time()[1]
                print(print_info["meal_info"])
                print_receipt(print_info)
    else:
        for item, quantity in order.items():
            print(f"{item}: {quantity}")
            if item in menu["中式炒菜"]:
                selected_dishes[item] = [quantity, menu["中式炒菜"][item]]
            elif item in menu["饮料"]:
                selected_dishes[item] = [quantity, menu["饮料"][item]]
            elif item in menu["主食"]:
                selected_dishes[item] = [quantity, menu["主食"][item]]
        print_info["meal_info"] = selected_dishes
        # 将 QDate 对象转换为字符串格式
        print_info["date"] = timestamp.toString("yyyy-MM-dd")
        print_info["timestamp"] = get_random_time()[1]
        print_receipt(print_info)

# 菜单和价格
menu = {
    "中式炒菜": {
        "宫保鸡丁": 30,
        "鱼香肉丝": 25,
        "麻婆豆腐": 20,
        "回锅肉": 22,
        "蒜蓉生菜": 18,
        "红烧肉": 35,
        "糖醋里脊": 30,
        "清蒸鲈鱼": 43,
        "酸辣土豆丝": 15,
        "辣子鸡丁": 32,
        "干煸四季豆": 20,
        "红烧茄子": 18,
        "黑椒牛柳": 42,
        "孜然羊肉": 38,
        "荷叶粉蒸排骨": 36,
        "香菇鸡片": 28,
        "西红柿炒蛋": 16,
        "酸菜鱼": 38,
        "水煮牛肉": 41,
        "韭菜炒鸡蛋": 22,
        "油焖大虾": 38,
        "京酱肉丝": 30,
        "虎皮青椒": 18,
        "香菇滑鸡": 30,
        "黄焖豆腐": 35,
        "蚝油生菜": 18,
        "蒜苗炒肉": 22,
        "剁椒鱼头": 42,
        "凉拌鸡丝": 20,
        "魔芋空心菜": 18,
        "豆角炒土豆": 28,
        "东坡肉": 39,
        "叫花鸭": 32,
        "孜然羊肉": 38,
        "香辣烤鱼": 48,
        "清炒时蔬": 10,
        "招牌凉粉": 10,
    },
    "饮料": {
        "可乐": 48,
        "雪碧": 10,
        "果汁": 10,
    },
    "主食": {
        "米饭": 48,
        "面条": 10,
        "玉米面": 10,
    }
}

def calculate_total(order):
    total = 0
    for item, quantity in order.items():
        for category in menu.values():
            if item in category:
                total += category[item] * quantity
    return total

class RestaurantOrderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Fake Ordering')
        self.setGeometry(100, 100, 600, 400)

        mainLayout = QVBoxLayout()

        # 时间选择
        self.dateTimeEdit = QDateTimeEdit(QDateTime.currentDateTime(), self)
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        mainLayout.addWidget(QLabel("Select time:"))
        mainLayout.addWidget(self.dateTimeEdit)

        self.shopNameEdit = QLineEdit(self)
        self.shopNameEdit.setPlaceholderText("Please enter store name")
        mainLayout.addWidget(QLabel("Store name:"))
        mainLayout.addWidget(self.shopNameEdit)

        # 菜单选择
        self.order = {}
        formLayout = QFormLayout()
        for category, items in menu.items():
            for item, price in items.items():
                hbox = QHBoxLayout()
                label = QLabel(f"{item} ({price}元)")
                label.setFixedWidth(200)
                spinBox = QSpinBox()
                spinBox.setRange(0, 50)
                spinBox.valueChanged.connect(lambda value, i=item: self.update_order(i, value))
                hbox.addWidget(label)
                hbox.addWidget(spinBox)
                formLayout.addRow(hbox)

        # 滚动区域
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollContent = QWidget()
        scrollContent.setLayout(formLayout)
        scrollArea.setWidget(scrollContent)

        # 总价显示
        self.totalLabel = QLabel("Total Price: 0元")

        # 是否随机生成菜单的复选框
        check_vbox = QVBoxLayout()
        self.checkbox = QCheckBox("Generate random")
        self.checkbox.setStyleSheet("QCheckBox;;indicator { background-color: white; } QCheckBox:;indicator:checked { background-color: black; }")
        check_vbox.addWidget(self.checkbox) 
        check_vbox.addStretch()

       # 创建时间选择器的容器
        self.time_range_widget = QWidget()
        time_layout = QHBoxLayout()

        # 前后两个时间段的选择器(QDateEdit)
        self.start_time = QDateEdit(QDate.currentDate(), self)
        self.start_time.setDisplayFormat("yyyy-MM-dd")
        self.end_time = QDateEdit(QDate.currentDate(), self)
        self.end_time.setDisplayFormat("yyyy-MM-dd")

        # 为时间选择器添加标签
        time_layout.addWidget(QLabel("Start Time:"))
        time_layout.addWidget(self.start_time)
        time_layout.addWidget(QLabel("End Time:"))
        time_layout.addWidget(self.end_time)

        # 将时间选择器的布局添加到时间区域容器中
        self.time_range_widget.setLayout(time_layout)

        # 初始时隐藏时间段选择插件
        self.time_range_widget.setVisible(False)

        # 将时间段选择器添加到生布局中
        check_vbox.addWidget(self.time_range_widget)

        # 信号槽连接，当复选框状态改变时调用
        self.checkbox.toggled.connect(self.toggle_time_range)

        # 打印按钮
        self.printButton = QPushButton("打印订单")
        self.printButton.clicked.connect(self.print_order)

        # 布局调整
        menuLayout = QVBoxLayout()
        menuLayout.addWidget(scrollArea)
        menuLayout.addWidget(self.totalLabel)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.printButton)
        buttonLayout.addStretch()

        hboxLayout = QHBoxLayout()
        hboxLayout.addLayout(menuLayout)
        hboxLayout.addLayout(check_vbox)
        hboxLayout.addLayout(buttonLayout)

        mainLayout.addLayout(hboxLayout)
        self.setLayout(mainLayout)


    def toggle_time_range(self, checked):
        """根据复选框的状态，显示或隐藏时间段选择插件"""
        self.time_range_widget.setVisible(checked)

    def update_order(self, item, quantity):
        if quantity == 0:
            if item in self.order:
                del self.order[item]
        else:
            self.order[item] = quantity
        self.update_total()

    def update_total(self):
        total = calculate_total(self.order)
        self.totalLabel.setText(f"总价: {total}元")

    def get_time_range(self):
        "获取用户选择的时间段"
        start_time = self.start_time.date().toString("yyyy-MM-dd")
        end_time = self.end_time.date().toString("yyyy-MM-dd")
        return start_time, end_time

    def print_order(self):
        global store_name
        if self.shopNameEdit.text().strip():
            store_name = self.shopNameEdit.text().strip()
        print(self.start_time.date(), self.end_time.date())
        # 直接传 self.checkbox.isChecked() 而不是 self.checkbox
        print_order(self.order, self.checkbox.isChecked(), self.dateTimeEdit.date(), self.start_time.date(), self.end_time.date())
# 假设的 calculate_total 函数
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RestaurantOrderApp()
    ex.show()
    sys.exit(app.exec_())