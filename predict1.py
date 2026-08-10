import numpy as np
import matplotlib.pyplot as plt
import win32ui
from PIL import Image, ImageWin
from sklearn.linear_model import LinearRegression


file_path = r"C:\Users\Lenovo\OneDrive\Documents\work\Ai\yodnam1\picture\AI_prediction.jpg"


def print_file(file_path):
    printer_name = "Brother HL-L2370DN series Printer"

    image = Image.open(file_path).convert("RGB")

    print("Image loaded:", image.size)

    dc = win32ui.CreateDC()
    dc.CreatePrinterDC(printer_name)

    page_width = dc.GetDeviceCaps(8)
    page_height = dc.GetDeviceCaps(10)

    img_width, img_height = image.size

    scale = min(
        page_width / img_width,
        page_height / img_height
    )

    new_width = int(img_width * scale)
    new_height = int(img_height * scale)

    image = image.resize(
        (new_width, new_height)
    )

    x = (page_width - new_width) // 2
    y = (page_height - new_height) // 2

    dc.StartDoc("AI Prediction")
    dc.StartPage()

    dib = ImageWin.Dib(image)

    dib.draw(
        dc.GetHandleOutput(),
        (x, y, x + new_width, y + new_height)
    )

    dc.EndPage()
    dc.EndDoc()
    dc.DeleteDC()

    print("Print job sent!")


class AIModel:

    def __init__(self):
        self.model = LinearRegression()
        self.X = []
        self.Y = []

    def add_point(self, x, y):
        self.X.append([x])
        self.Y.append(y)

    def fit(self):
        if len(self.X) >= 2:
            self.model.fit(self.X, self.Y)

    def predict(self, x):
        if len(self.X) < 2:
            return None

        self.fit()

        return float(
            self.model.predict([[x]])[0]
        )

    def plot(self, pred_x, pred_y):

        x = np.array([p[0] for p in self.X])
        y = np.array(self.Y)

        line_x = np.linspace(
            min(x),
            pred_x,
            100
        )

        line_y = self.model.predict(
            line_x.reshape(-1, 1)
        )

        plt.figure(figsize=(9, 6))

        plt.scatter(
            x,
            y,
            s=80,
            label="Data"
        )

        plt.plot(
            line_x,
            line_y,
            linewidth=2,
            label="AI Regression"
        )

        plt.scatter(
            pred_x,
            pred_y,
            marker="X",
            s=200,
            label="AI Prediction"
        )

        plt.xlabel("X")
        plt.ylabel("Y")

        plt.title(
            "AI Linear Regression Prediction Results"
        )

        plt.grid(True)
        plt.legend()

        plt.text(
            1,
            0,
            f"Prediction: x = {pred_x}, y = {pred_y:.2f}",
            transform=plt.gca().transAxes,
            ha="right",
            va="bottom"
        )

        plt.savefig(
            file_path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.show()
        plt.close()

        return file_path


# Main program

numx = int(
    input("How many x length do you need: ")
)

ai = AIModel()

for i in range(numx):

    y = float(
        input(
            f"Enter y value in position {i + 1}: "
        )
    )

    ai.add_point(
        i + 1,
        y
    )


next_x = numx + 1

predicted_y = ai.predict(
    next_x
)


if predicted_y is None:

    print(
        "You need at least 2 data points."
    )

else:

    print(
        f"\nAI predict when "
        f"x={next_x}, "
        f"y={predicted_y:.2f}"
    )

    # Open a graph window to show the result

    file_path = ai.plot(
        next_x,
        predicted_y
    )

    print(
        "Saved:",
        file_path
    )

    print_file(
        file_path
    )

