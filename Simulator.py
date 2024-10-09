import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# 设置中文字体和负号正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 用于将用户输入的字符串解析为方程的函数
def create_aperture_from_equation(eq_str, grid_size=500):
    """
    根据用户输入的方程生成光孔形状
    :param eq_str: 用户输入的关于x和y的方程（字符串格式）
    :param grid_size: 网格大小，用于定义衍射图的分辨率
    :return: 光孔形状的二维numpy数组
    """
    # 创建x, y坐标网格
    x = np.linspace(-5, 5, grid_size)
    y = np.linspace(5, -5, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # 将用户输入的方程转化为可执行代码
    try:
        aperture = eval(eq_str)
    except Exception as e:
        print(f"方程解析错误: {e}")
        return None
    
    # 将光孔形状限制在0和1之间
    aperture = np.where(aperture > 0, 1, 0)
    return aperture

# 生成衍射图像
def generate_diffraction_pattern(aperture):
    """
    根据光孔形状生成夫琅禾费衍射图像
    :param aperture: 光孔的二维数组
    :return: 衍射强度的二维数组
    """
    # 对光孔形状进行二维傅里叶变换
    field = np.fft.fftshift(np.fft.fft2(aperture))
    intensity = np.abs(field)**2
    return intensity

# 裁剪衍射图像中心区域
def crop_center(intensity, crop_size=100):
    """
    从衍射图像中裁剪中心区域
    :param intensity: 衍射强度的二维数组
    :param crop_size: 裁剪的大小（裁剪出的中心区域的宽度和高度）
    :return: 裁剪后的衍射强度
    """
    center_x = intensity.shape[1] // 2
    center_y = intensity.shape[0] // 2
    half_crop = crop_size // 2
    cropped_intensity = intensity[center_y - half_crop:center_y + half_crop, center_x - half_crop:center_x + half_crop]
    return cropped_intensity

# 主函数：接受用户输入方程并生成衍射图像
def generate_diffraction_image():
    print("请输入光孔的方程（关于 x 和 y，例如 'np.sqrt(X**2 + Y**2) < 1' 定义圆形孔）：")
    eq_str = input("方程: ")

    aperture = create_aperture_from_equation(eq_str)
    
    if aperture is None:
        print("光孔形状无效，无法生成衍射图像。")
        return
    
    # 生成并展示衍射图像
    intensity = generate_diffraction_pattern(aperture)
    
    # 裁剪衍射图像的中心区域（比如100x100的区域）
    cropped_intensity = crop_center(intensity, crop_size=100)
    
    # 设置画布大小和布局比例
    fig = plt.figure(figsize=(12, 6))  # 增大图像整体尺寸
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 2])  # 设置宽度比例，右图为左图的两倍宽

    # 展示光孔形状
    ax0 = plt.subplot(gs[0])
    ax0.imshow(aperture, extent=(-5, 5, -5, 5), cmap='gray')
    ax0.set_title("光孔形状")
    
    # 展示裁剪后的衍射图像中心区域
    ax1 = plt.subplot(gs[1])
    crop_extent = (-5, 5, -5, 5)  # 设定中心区域显示的坐标范围
    ax1.imshow(np.log(cropped_intensity + 1), extent=crop_extent, cmap='inferno')
    ax1.set_title("夫琅禾费衍射图像（中心部分）")
    plt.colorbar(ax1.imshow(np.log(cropped_intensity + 1), extent=crop_extent, cmap='inferno'), ax=ax1, label="衍射强度")
    
    plt.show()

# 调用主函数
generate_diffraction_image()