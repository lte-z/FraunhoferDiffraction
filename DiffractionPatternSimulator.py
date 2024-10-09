import os
import sys
import ctypes
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QWidget, QGridLayout, QAction, QFileDialog, QVBoxLayout, QLabel, QFrame, QLineEdit, QSlider

# 设置plt绘图中文字体和负号正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置应用程序ID
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("DiffractionPatternSimulator")

# 日志窗口
class LogWindow(QWidget):
    # 窗口居中
    def center(self, ParentWindow):
        ParentWindowSize = ParentWindow.frameGeometry() # 获取主窗口大小
        ParentWindowCentre = ParentWindowSize.center() # 获取主窗口中心
        WindowsSize = self.frameGeometry() # 获取关于窗口大小
        WindowsSize.moveCenter(ParentWindowCentre) # 将关于窗口中心移动到主窗口中心
        self.move(WindowsSize.topLeft()) # 移动关于窗口

    # 初始化窗口
    def __init__(self, ParentWindow):
        # 调用父类的构造函数
        super().__init__()

        if hasattr(sys, '_MEIPASS'):
            # 如果存在 _MEIPASS 属性，说明是打包后的环境
            CurrentDir = sys._MEIPASS
        else:
            # 否则是开发环境
            CurrentDir = os.path.dirname(os.path.abspath(__file__))
        self.setWindowIcon(QIcon(os.path.join(CurrentDir, 'icon.ico'))) # 设置窗口图标

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建标签
        label1 = QLabel("\n    软件版本：v1.0\n    发布日期：2024.10.3\n\n    实现了程序的基本功能。\n")
        label1.setWordWrap(True) # 设置自动换行

        label2 = QLabel("\n    软件版本：v1.1（当前版本）\n    发布日期：2024.10.8\n\n    增加了输入限制，修复了输入纯数字方程导致软件崩溃的问题。\n    优化了界面UI和字体渲染，修复了图标显示的问题。\n    优化了变量命名和代码可读性。\n    增加了更新日志。\n")
        label2.setWordWrap(True) # 设置自动换行

        line = QFrame() # 创建分割线
        line.setFrameShape(QFrame.HLine) # 设置分割线形状
        line.setFrameShadow(QFrame.Sunken) # 设置分割线阴影

        # 添加标签到布局
        layout.addWidget(label2)
        layout.addWidget(line)
        layout.addWidget(label1)
        self.setLayout(layout)

        # 设置字体 & 字号
        font = QFont('SimHei')
        font.setPointSize(9)
        self.setFont(font)

# 关于窗口
class AboutWindow(QWidget):
    # 窗口居中
    def center(self, ParentWindow):
        ParentWindowSize = ParentWindow.frameGeometry() # 获取主窗口大小
        ParentWindowCentre = ParentWindowSize.center() # 获取主窗口中心
        WindowsSize = self.frameGeometry() # 获取关于窗口大小
        WindowsSize.moveCenter(ParentWindowCentre) # 将关于窗口中心移动到主窗口中心
        self.move(WindowsSize.topLeft()) # 移动关于窗口

    # 初始化窗口
    def __init__(self, ParentWindow):
        # 调用父类的构造函数
        super().__init__()

        if hasattr(sys, '_MEIPASS'):
            # 如果存在 _MEIPASS 属性，说明是打包后的环境
            CurrentDir = sys._MEIPASS
        else:
            # 否则是开发环境
            CurrentDir = os.path.dirname(os.path.abspath(__file__))
        self.setWindowIcon(QIcon(os.path.join(CurrentDir, 'icon.ico'))) # 设置窗口图标

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建标签
        label1 = QLabel("\n    本软件使用 Python 3 开发，使用 numpy 、 matplotlib 和 PyQt5 等库辅助开发，主要用于夫琅禾费衍射图像的模拟。\n    我们团队正在参加北京邮电大学2024年雏雁计划，本软件的源代码将在项目结束后开源，欢迎大家参与维护！\n")
        label1.setWordWrap(True) # 设置自动换行
        line = QFrame() # 创建分割线
        line.setFrameShape(QFrame.HLine) # 设置分割线形状
        line.setFrameShadow(QFrame.Sunken) # 设置分割线阴影
        label2 = QLabel("\n灵感来源 & 公式计算：takoyaki\n软件设计 & 代码实现：lte_z\n团队其他成员：Levent、Skorska、zm\n\n联系我们：ltezstudios@gmail.com\n")
        label3 = QLabel("小Z工作室#2024")
        label3.setAlignment(Qt.AlignRight)  # 设置标签居右

        # 添加标签到布局
        layout.addWidget(label1)
        layout.addWidget(line)
        layout.addWidget(label2)
        layout.addStretch() # 添加伸展项，将后面的控件推到布局底部
        layout.addWidget(label3)
        self.setLayout(layout)

        # 设置字体 & 字号
        font = QFont('SimHei')
        font.setPointSize(9)
        self.setFont(font)

# 主窗口
class MainWindow(QMainWindow):
    # 窗口居中
    def center(self):
        WindowSize = self.frameGeometry() # 获取窗口大小
        ScreenCentre = QDesktopWidget().availableGeometry().center() # 获取屏幕中心
        WindowSize.moveCenter(ScreenCentre) # 将窗口中心移动到屏幕中心
        self.move(WindowSize.topLeft()) # 移动窗口

    # 初始化窗口
    def __init__(self):
        # 调用父类的构造函数
        super().__init__()

        if hasattr(sys, '_MEIPASS'):
            # 如果存在 _MEIPASS 属性，说明是打包后的环境
            CurrentDir = sys._MEIPASS
        else:
            # 否则是开发环境
            CurrentDir = os.path.dirname(os.path.abspath(__file__))
        self.setWindowIcon(QIcon(os.path.join(CurrentDir, 'icon.ico'))) # 设置窗口图标

        # 创建网格布局
        layout = QGridLayout()

        # 创建菜单栏
        menubar = self.menuBar()

        # 创建菜单选项
        OptionMenu = menubar.addMenu('选项') # 添加菜单
        SaveAction = QAction('另存为', self) # 添加选项
        ClearAction = QAction('清空画布', self)
        QuitAction = QAction('退出', self)
        OptionMenu.addAction(SaveAction) # 添加选项到菜单
        OptionMenu.addAction(ClearAction)
        OptionMenu.addSeparator()
        OptionMenu.addAction(QuitAction)
        SaveAction.triggered.connect(self.save) # 连接选项到函数
        ClearAction.triggered.connect(self.clear)
        QuitAction.triggered.connect(self.quit)

        PresetMenu = menubar.addMenu('预设') # 添加菜单
        RoundHole = QAction('圆形孔', self) # 添加选项
        RectangularHole = QAction('矩形孔', self)
        RightTriangleHole = QAction('直角三角形孔', self)
        RoundPiece = QAction('圆形片', self)
        RectangularPiece = QAction('矩形片', self)
        RightTrianglePiece = QAction('直角三角形片', self)
        PresetMenu.addAction(RoundHole) # 添加选项到菜单
        PresetMenu.addAction(RectangularHole)
        PresetMenu.addAction(RightTriangleHole)
        PresetMenu.addSeparator()
        PresetMenu.addAction(RoundPiece)
        PresetMenu.addAction(RectangularPiece)
        PresetMenu.addAction(RightTrianglePiece)
        RoundHole.triggered.connect(self.CreateRoundHole) # 连接选项到函数
        RectangularHole.triggered.connect(self.CreateRectangularHole)
        RightTriangleHole.triggered.connect(self.CreateRightTriangleHole)
        RoundPiece.triggered.connect(self.CreateRoundPiece)
        RectangularPiece.triggered.connect(self.CreateRectangularPiece)
        RightTrianglePiece.triggered.connect(self.CreateRightTrianglePiece)

        MoreMenu = menubar.addMenu('更多') # 添加菜单
        LogAction = QAction('更新日志', self) # 添加选项
        AboutAction = QAction('关于我们', self)
        MoreMenu.addAction(LogAction) # 添加选项到菜单
        MoreMenu.addSeparator()
        MoreMenu.addAction(AboutAction)
        LogAction.triggered.connect(self.log) # 连接选项到函数
        AboutAction.triggered.connect(self.about)
        self.OpenLogWindow = None # 初始化日志窗口
        self.OpenAboutWindow = None # 初始化关于窗口

        # 创建输入框
        self.LineEdit = QLineEdit(self) # 创建输入框
        self.LineEdit.setPlaceholderText("例如 'np.sqrt(X**2 + Y**2) < 1' 来定义圆形孔") # 设置提示文本
        self.close() # 关闭输入框

        # 创建画布
        self.figure = Figure() # 创建画布
        self.canvas = FigureCanvas(self.figure) # 创建画布控件

        # 创建滑动条
        self.slider = QSlider() # 创建滑动条
        self.slider.setOrientation(Qt.Horizontal) # 设置滑动条方向
        self.slider.setRange(0, 500) # 设置滑动条范围
        self.slider.valueChanged.connect(self.generate) # 连接滑动条到函数
        self.ResultLabel = QLabel("拖动滑动条以生成图像/更改缩放。") # 描述滑动条

        # 添加控件到布局
        layout.addWidget(QLabel("请输入关于 x 和 y 的方程来描述光孔形状："), 0, 0, 1, 2)
        layout.addWidget(self.LineEdit, 1, 0, 1, 2)
        layout.addWidget(self.canvas, 2, 0, 1, 2)
        layout.addWidget(self.slider, 3, 0, 1, 2)
        layout.addWidget(self.ResultLabel, 4, 0, 1, 2)

        # 设置字体 & 字号
        font = QFont('SimHei')
        font.setPointSize(10)
        self.setFont(font)

        # 将QWidget对象作为窗口的中心部件
        CentralWidget = QWidget()
        CentralWidget.setLayout(layout)
        self.setCentralWidget(CentralWidget)

    # 生成衍射图像 & 窗口内绘图
    def generate(self):
        self.figure.clf() # 清空画布
        self.canvas.draw() # 重绘画布
        InputString = self.LineEdit.text() # 获取输入框内容

        # 原generate_diffraction_image()函数部分
        # 生成光孔形状
        try:
            aperture = CreateApertureFromEquation(InputString, GridSize = 800)
        except Exception:
            self.ResultLabel.setText("生成失败，请检查您的方程表达式。")
            return
    
        # 生成衍射图像
        try:
            intensity = GenerateDiffractionPattern(aperture)
        except Exception:
            self.ResultLabel.setText("生成失败，请检查您的方程表达式。")
            return
    
        # 裁剪衍射图像的中心区域
        CroppedIntensity = CropCenter(intensity, CropSize = self.slider.value())
    
        # 设置画布布局比例
        GridSpec = gridspec.GridSpec(1, 2, width_ratios=[1, 2]) # 设置宽度比例，右图为左图的两倍宽

        # 展示光孔形状
        SubgraphLeft = self.figure.add_subplot(GridSpec[0]) # 添加子图
        SubgraphLeft.imshow(aperture, extent=(-5, 5, -5, 5), cmap='gray') # 绘制图像
        SubgraphLeft.set_title("光孔形状") # 设置标题
    
        # 展示裁剪后的衍射图像中心区域
        SubgraphRight = self.figure.add_subplot(GridSpec[1]) # 添加子图
        CropExtent = (-5, 5, -5, 5) # 设定中心区域显示的坐标范围
        SubgraphRight.imshow(np.log(CroppedIntensity + 1), extent=CropExtent, cmap='inferno') # 绘制图像
        SubgraphRight.set_title("夫琅禾费衍射图像（中心部分）") # 设置标题
        self.figure.colorbar(SubgraphRight.imshow(np.log(CroppedIntensity + 1), extent=CropExtent, cmap='inferno'), ax=SubgraphRight, label="衍射强度") # 添加颜色条
    
        self.ResultLabel.setText("生成成功！") # 设置结果标签
        self.canvas.draw() # 重绘画布

    # 另存为函数
    def save(self):
        SaveOptions = QFileDialog.Options()
        FilePath, _ = QFileDialog.getSaveFileName(self, "保存衍射图像", "Result.png", "PNG 格式 (*.png);;所有格式 (*)", options = SaveOptions)
        if FilePath:
            self.figure.savefig(FilePath)
    
    # 清空画布函数
    def clear(self):
        self.figure.clf() # 清空画布
        self.canvas.draw() # 重绘画布
        self.LineEdit.clear() # 清空输入框
        self.slider.setValue(0) # 重置滑动条
        self.ResultLabel.setText("拖动滑动条以生成图像/更改缩放。") # 重置结果标签

    # 退出函数
    def quit(self):
        self.close()

    # 圆形孔预设函数
    def CreateRoundHole(self):
        self.LineEdit.setText("np.sqrt(X**2 + Y**2) < 1")
        self.generate()
        self.slider.setValue(100)

    # 矩形孔预设函数
    def CreateRectangularHole(self):
        self.LineEdit.setText("(np.abs(X) < 1) & (np.abs(Y) < 1)")
        self.generate()
        self.slider.setValue(100)

    # 直角三角形孔预设函数
    def CreateRightTriangleHole(self):
        self.LineEdit.setText("(X > 0) & (Y > 0) & (X + Y < 1)")
        self.generate()
        self.slider.setValue(100)

    # 圆形片预设函数
    def CreateRoundPiece(self):
        self.LineEdit.setText("np.sqrt(X**2 + Y**2) > 1")
        self.generate()
        self.slider.setValue(100)

    # 矩形片预设函数
    def CreateRectangularPiece(self):
        self.LineEdit.setText("(np.abs(X) > 1) | (np.abs(Y) > 1)")
        self.generate()
        self.slider.setValue(100)

    # 直角三角形片预设函数
    def CreateRightTrianglePiece(self):
        self.LineEdit.setText("(X < 0) | (Y < 0) | (X + Y > 1)")
        self.generate()
        self.slider.setValue(100)
    
    # 日志函数
    def log(self):
        if self.OpenLogWindow is None: # 如果关于窗口未打开
            self.OpenLogWindow = LogWindow(self) # 创建关于窗口
            self.OpenLogWindow.setWindowTitle('更新日志') # 设置窗口标题
        self.OpenLogWindow.setGeometry(100, 100, 480, 600) # 设置窗口大小
        self.OpenLogWindow.center(self) # 居中窗口
        self.OpenLogWindow.show() # 显示窗口

    # 关于函数
    def about(self):
        if self.OpenAboutWindow is None: # 如果关于窗口未打开
            self.OpenAboutWindow = AboutWindow(self) # 创建关于窗口
            self.OpenAboutWindow.setWindowTitle('关于我们') # 设置窗口标题
        self.OpenAboutWindow.setGeometry(100, 100, 480, 540) # 设置窗口大小
        self.OpenAboutWindow.center(self) # 居中窗口
        self.OpenAboutWindow.show() # 显示窗口

# 其余外部函数
# 将用户输入的字符串解析为方程
def CreateApertureFromEquation(InputString, GridSize):
    """
    根据用户输入的方程生成光孔形状
    InputString: 用户输入的关于x和y的方程（字符串格式）
    GridSize: 网格大小，用于定义衍射图的分辨率
    return: 光孔形状的二维numpy数组
    """
    # 创建x, y坐标网格
    x = np.linspace(-5, 5, GridSize)
    y = np.linspace(5, -5, GridSize)
    X, Y = np.meshgrid(x, y)
    
    # 将用户输入的方程转化为可执行代码
    try:
        aperture = eval(InputString)
    except Exception:
        return None

    # 将光孔形状限制在0和1之间
    aperture = np.where(aperture > 0, 1, 0)
    return aperture

# 生成衍射图像
def GenerateDiffractionPattern(aperture):
    """
    根据光孔形状生成夫琅禾费衍射图像
    aperture: 光孔的二维数组
    return: 衍射强度的二维数组
    """
    # 对光孔形状进行二维傅里叶变换
    field = np.fft.fftshift(np.fft.fft2(aperture))
    intensity = np.abs(field)**2
    return intensity

# 裁剪衍射图像中心区域
def CropCenter(intensity, CropSize):
    """
    从衍射图像中裁剪中心区域
    intensity: 衍射强度的二维数组
    CropSize: 裁剪的大小（裁剪出的中心区域的宽度和高度）
    return: 裁剪后的衍射强度
    """
    CenterX = intensity.shape[1] // 2
    CenterY = intensity.shape[0] // 2
    HalfCrop = CropSize // 2
    CroppedIntensity = intensity[CenterY - HalfCrop:CenterY + HalfCrop, CenterX - HalfCrop:CenterX + HalfCrop]
    return CroppedIntensity

# 主函数
if __name__ == '__main__':
    app = QApplication(sys.argv) # 创建应用程序
    window = MainWindow() # 创建主窗口
    window.setWindowTitle('夫琅禾费衍射图像模拟器 v1.1') # 设置窗口标题
    window.setGeometry(100, 100, 960, 720) # 设置窗口大小
    window.center() # 居中窗口
    window.show() # 显示窗口
    sys.exit(app.exec_()) # 运行应用程序