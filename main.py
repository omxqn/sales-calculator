import threading
from PyQt5.Qt import QDialog,QPushButton,QLineEdit,QLabel,QMessageBox,QComboBox,QCheckBox,QFormLayout,QApplication,QDir,QFont,QFontDatabase,Qt,QIcon
import sys
import os
import logging
from cachetools import cached, TTLCache

APP_AUTHOR = "عزام"
APP_VERSION = "1.0"

global ready_now
global error
global connection_error
ready_now = False
ready = False
connection_error = False
cache = TTLCache(maxsize=100, ttl=86400)

@cached(cache)
def connect_database(item_name1,item_price1,sell_type1,item_quantity1):
    global connection_error
    global ready_now

    try:
        from database import add_new

        ready_now = True
        connection_error = False

    except Exception as ex:
        logger.debug("Error in database connection")
        connection_error = True

    if ready_now and item_name1 != '' and item_price1 != '' and sell_type1 != '' and item_quantity1 != '':
        add_new(table='sale_log', item_name=str(item_name1), price=str(item_price1), sale_type=str(sell_type1), quantity = str(item_quantity1))
        logger.debug("Database connected successfully")


thread = threading.Thread(target=connect_database,args=['','','',''])
thread.start()

logging.basicConfig(filename="logs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = QApplication(sys.argv)
dir_ = QDir("Cairo")
_id = QFontDatabase.addApplicationFont("Fonts\Cairo-Bold.ttf")
dir_ = QDir("Cairo-light")
_id = QFontDatabase.addApplicationFont("Fonts\Cairo-Light.ttf")

@cached(cache)
class Downloader(QDialog):
    global ready
    global ready_now
    global connection_error

    def __init__(self):
        global btn_download
        global reset_btn
        global connection_error
        global layout
        current_dir = os.path.dirname(os.path.realpath(__file__))
        QDialog.__init__(self)
        layout = QFormLayout()
        self.show_sale = False
        self.i = 0
        self.folder = ""
        self.item_name = QLineEdit()
        self.item_price = QLineEdit()
        self.item_quantity = QLineEdit()
        self.save_location = QLineEdit()
        self.sell_type = QComboBox()
        self.check_box = QCheckBox("View sale report/ اظهار تقرير")
        self.line = QLabel("The copyrights © for Azzam / Sojjadah Store ")
        self.line.setAlignment(Qt.AlignCenter)

        font = QFont("Cairo")
        font1 = QFont("Cairo-light")
        btn_download = QPushButton("إدخال المنتج")
        btn_info = QPushButton("معلومات", self)
        btn_info.move(100,140)

        reset_btn = QPushButton("تهيئة قاعدة البيانات", self)
        reset_btn.move(450,300)
        btn_info.unsetLayoutDirection()
        reset_btn.hide()


        self.item_name.setPlaceholderText("اسم المنتج")
        self.item_price.setPlaceholderText("سعر المنتج")
        self.item_quantity.setPlaceholderText("الكمية")
        self.sell_type.setPlaceholderText(" ")

        #combo boxes
        self.sell_type.addItems(["Buy","Sell"])

        # FONTS
        self.line.setFont(font)
        self.item_price.setFont(font)
        self.item_quantity.setFont(font)
        self.sell_type.setFont(font)
        self.item_name.setFont(font)
        btn_download.setFont(font)
        btn_info.setFont(font1)


        #layout.addWidget(self.playlist)
        layout.addWidget(self.item_name)
        layout.addWidget(self.check_box)
        layout.addWidget(self.item_price)
        layout.addWidget(self.item_quantity)
        layout.addWidget(self.sell_type)
        layout.addWidget(btn_download)
        layout.addWidget(self.line)
        btn_info.setGeometry(10, 280, 10, 10)
        self.sell_type.currentTextChanged.connect(self.check_formats)


        #system settings
        self.setLayout(layout)
        self.setWindowTitle("برنامج سُجادة للحسابات")

        self.setFocus()
        #self.setMaximumSize(500,500)
        self.hight = 350
        self.width = 600
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.hight)
        self.setAutoFillBackground(10)
        self.setWindowIcon(QIcon(os.path.join(current_dir, 'icon.ico')))

        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        #layouts settings
        btn_download.setFixedWidth(573)
        btn_download.setFixedHeight(45)

        self.item_name.setFixedWidth(573)
        self.item_name.setFixedHeight(35)
        layout.removeWidget(self.item_price)
        layout.removeWidget(self.item_quantity)
        self.item_price.setFixedWidth(100)
        self.item_price.setFixedHeight(35)
        self.item_price.setAlignment(Qt.AlignRight)
        self.item_price.move(490, 50)


        self.item_quantity.setFixedWidth(70)
        self.item_quantity.setFixedHeight(35)
        self.item_quantity.setAlignment(Qt.AlignRight)
        self.item_quantity.move(415, 50)

        self.sell_type.setFixedWidth(90)
        self.sell_type.setFixedHeight(30)
        btn_info.unsetLayoutDirection()
        btn_info.setFixedWidth(45)
        btn_info.setFixedHeight(45)
        btn_info.setFocus()

        #hide all this things when start the program



        #self.cb.setFixedHeight(35)
        btn_download.clicked.connect(self.submit)
        reset_btn.clicked.connect(self.reset_function)
        btn_info.clicked.connect(self.info)
        self.check_box.clicked.connect(self.check_box_clicked)


        logger.debug("Checking for internet connection")
        while True:

            if ready_now and not connection_error:
                QMessageBox.information(self, "معلومات", "تم الاتصال بقاعدة البيانات")
                self.setFocus()
                logger.debug("Database connected successfully")
                break
            if connection_error:
                try:
                    QMessageBox.warning(self, "تحذير", "No internet connection")
                    logger.debug("No internet connection - Checking internet again")

                    connect_database('','','')
                    if not connection_error:
                        QMessageBox.information(self, "معلومات", "تم الاتصال بقاعدة البيانات")
                        logger.debug("Connection successed after failing")
                        break
                except:
                    QMessageBox.warning(self, "تحذير", "Check your internet connection then click OK")


    def check_formats(self):
        if self.sell_type.currentText() == "Buy":
            logger.debug("Sale type 'Buy' has been chosen")
        if self.sell_type.currentText() == "Sell":
            logger.debug("Sale type 'Sell' has been chosen")


    def reset_function(self):
        from database import delete_all
        delete_all("sale_log")
        logger.debug("All data in database has been deleted")


    def check_box_clicked(self):
        global btn_download
        global buy_price
        global sell_price
        global reset_btn
        buy_price = 0
        sell_price = 0

        self.i += 1
        if self.i % 2 == 0:
            logger.debug("Check box has been Unchecked")
            self.show_sale = False
            self.sell_type.show()
            self.item_price.show()
            self.item_quantity.show()
            self.item_name.show()
            btn_download.show()
            reset_btn.hide()
            self.items_sale.hide()
            logger.debug("All widgets has been shown")

        if self.i % 2 != 0:

            from database import get_table_info
            logger.debug("Check box has been checked")

            self.show_sale = True
            self.sell_type.hide()
            self.item_price.hide()
            self.item_quantity.hide()
            self.item_name.hide()
            btn_download.hide()
            reset_btn.show()
            logger.debug("All widgets has been hidden")

            logger.debug("Getting table:'sale_log' info from database")
            test = get_table_info('sale_log',False)
            logger.debug("Gathered successfully")

            for i in test:
                i = list(i)
                print(i[3])

                if str(i[3]) == "Buy":

                    buy_price += int(i[2])
                    logger.debug(f"Item:{i[1]} with price {i[2]} Has been added to Buy")

                elif str(i[3]) == "Sell":
                    sell_price += int(i[2])
                    logger.debug(f"Item:{i[1]} with price {i[2]} Has been added to Sell")
                else:
                    logger.debug("Error while adding sale profit report")

            self.items_sale = QLabel(f"Buy price is: {buy_price}\nSell price is: {sell_price}\nProfit is: {sell_price-buy_price}")
            layout.addWidget(self.items_sale)
            font = QFont("Cairo",25)
            self.items_sale.setFont(font)
            logger.debug("Sale profit report has been printed")

    def submit(self):#دالة التحميل
        logger.debug("Submission button has been clicked")
        global ready
        #الصيغ مال التحميل
        item_name = self.item_name.text()
        item_price = self.item_price.text()
        item_quantity = self.item_quantity.text()
        sell_type = self.sell_type.currentText()
        logger.debug(f"Item name: {item_name}")
        logger.debug(f"Item Price: {item_price}")
        logger.debug(f"Sell Type: {sell_type}")

        try:
            if ready_now and not connection_error:
                logger.debug("Trying to submit data")

                if item_name == '' or item_price == '' or sell_type == '' or item_quantity == '':
                    QMessageBox.warning(self, "تحذير", "أحد الحقول فارغة يرجى التأكد منها")
                else:
                    connect_database(item_name, item_price, sell_type,item_quantity)
                    QMessageBox.information(self, "معلومات", "تم اضافة المنتج في قاعدة البيانات")
                    logger.debug("Data has been submitted successfully")
            else:
                try:
                    QMessageBox.warning(self, "تحذير", "No internet connection ")
                    logger.debug("No internet connection - Checking internet again - when click submit")
                    connect_database('', '', '')
                    if not connection_error:
                        QMessageBox.information(self, "معلومات", "تم الاتصال بقاعدة البيانات")
                        logger.debug("Connection successes after failing")
                except:
                    QMessageBox.warning(self, "تحذير", "Check your internet connection then click OK")

        except Exception as ex:
            QMessageBox.warning(self,"تحذير","حدث خطأ ما يرجى المحاولة من جديد")
            logger.debug("Something went wrong")

    def info(self):
        QMessageBox.information(self,"معلومات عن البرنامج ",f"تم انشاء هذا البرنامج بواسطة {APP_AUTHOR} لمتجر سُجادة\n\n  إصدار البرنامج: {APP_VERSION} \n\n انستا: 2zmx")
        logger.debug("Info button has been clicked")



dialog = Downloader()
dialog.show()
app.exec_()
logger.debug("App has been closed")