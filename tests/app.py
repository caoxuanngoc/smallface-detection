import tkinter as tk
from tkinter import filedialog
import cv2
import sys
import matplotlib.pyplot as plt
from mtcnn import MTCNN
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from retinaface_mtcnn import RetinaFace
import time

def detect_faces(file_path, algorithm):
    # Đọc ảnh từ tệp
    img = cv2.imread(file_path)

    # Tiến hành xử lý ảnh và phát hiện khuôn mặt
    start_time = time.time()

    if algorithm == "MTCNN":
        detector = MTCNN(min_face_size=5)
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = detector.detect_faces(rgb_image)
    elif algorithm == "RetinaFace":
        faces = RetinaFace.detect_faces(file_path, threshold=0.1)
    else:
        print("Thuật toán không hợp lệ.")
        return

    end_time = time.time()

    # Kiểm tra xem khuôn mặt có được phát hiện hay không
    if not faces:
        print("Không có khuôn mặt được phát hiện.")
        return

    # Vẽ hình bao quanh khuôn mặt phát hiện được
    i=1
    for face in faces:
        if algorithm == "MTCNN":
            x, y, width, height = face['box']
        elif algorithm == "RetinaFace":
            x1, y1, x2, y2 = faces['face_{}'.format(i)]['facial_area']
            x, y, width, height = int(x1), int(y1), int(x2 - x1), int(y2 - y1)
        cv2.rectangle(img, (x, y), (x + width, y + height), (0, 0, 255), 2)

        i=i+1


    print("Thuat toan :", algorithm)
    num_faces = len(faces)

    print("Số lượng khuôn mặt phát hiện được:", num_faces)

    # Tính thời gian hoạt động của thuật toán
    execution_time = end_time - start_time
    print("Thời gian hoạt động của thuật toán:", execution_time, "giây")

    # Hiển thị ảnh trong cửa sổ Matplotlib
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
    if algorithm == "MTCNN":
        output_file_path = 'output_mtcnn/' + file_path.split('/')[-1]
        cv2.imwrite(output_file_path, img)
    elif algorithm == "RetinaFace":
        output_file_path = 'output_retinaface/' + file_path.split('/')[-1]
        cv2.imwrite(output_file_path, img)
def open_image():
    # Hiển thị hộp thoại chọn tệp
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    if file_path:
        algorithm = algorithm_var.get()
        detect_faces(file_path, algorithm)



def on_enter(e):
    button.config(bg="#45a049")  # Màu nền khi di chuột vào

def on_leave(e):
    button.config(bg="#4CAF50")  # Màu nền khi rời chuột
# Tạo cửa sổ giao diện
window = tk.Tk()

# Thiết lập kích thước cửa sổ và vị trí hiển thị giữa màn hình
window_width = 400
window_height = 250
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Thiết lập tiêu đề cửa sổ
window.title("Face Detection")

# Tạo frame chứa các thành phần giao diện
frame = tk.Frame(window, padx=20, pady=20)
frame.pack()

# Tạo label tiêu đề
title_label = tk.Label(frame, text="Chương trình Phát hiện khuôn mặt", font=("Arial", 25, "bold"))
title_label.pack()

# Tạo radio button
algorithm_var = tk.StringVar()
algorithm_var.set("MTCNN")

rb_frame = tk.Frame(frame)
rb_frame.pack(pady=10)

rb_mtcnn = tk.Radiobutton(rb_frame, text="MTCNN", variable=algorithm_var, value="MTCNN", font=("Arial", 20), fg="blue", height=3)
rb_mtcnn.pack(side="left", padx=10)

rb_retinaface = tk.Radiobutton(rb_frame, text="RetinaFace", variable=algorithm_var, value="RetinaFace", font=("Arial", 20), fg="blue", height=3)
rb_retinaface.pack(side="left", padx=10)

# Tạo nút bấm
button = tk.Button(frame, text="Chọn ảnh", command=open_image, bg="#4CAF50", fg="white", font=("Arial", 20), padx=20, pady=10)
button.pack(pady=10)

# Gắn sự kiện khi di chuột vào và rời khỏi nút
button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)

# Chạy vòng lặp hiển thị cửa sổ giao diện
window.mainloop()