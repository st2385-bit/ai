import numpy as np
from sklearn.linear_model import LinearRegression

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
        return float(self.model.predict([[x]])[0])
    def plot_ascii(self, pred_x, pred_y, height=10, width=35):
        """วาดกราฟใน Terminal ด้วยตัวอักษร ASCII"""
        all_x = [pt[0] for pt in self.X] + [pred_x]
        all_y = self.Y + [pred_y]

        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        range_x = max_x - min_x if max_x != min_x else 1
        range_y = max_y - min_y if max_y != min_y else 1

        canvas = [[" " for _ in range(width)] for _ in range(height)]

        for x, y in zip(self.X, self.Y):
            c = int((x[0] - min_x) / range_x * (width - 1))
            r = height - 1 - int((y - min_y) / range_y * (height - 1))
            canvas[r][c] = "O"

        c_p = int((pred_x - min_x) / range_x * (width - 1))
        r_p = height - 1 - int((pred_y - min_y) / range_y * (height - 1))
        canvas[r_p][c_p] = "X"

        print("\n" + "=" * 45)
        print("  Terminal Graph  (O = Data, X = Prediction)")
        print("=" * 45)
        for i, row in enumerate(canvas):
            val_y = max_y - i * (range_y / (height - 1))
            print(f"{val_y:6.1f} | " + "".join(row))
        print(" " * 8 + "-" * width)
        print(" " * 8 + f"x={min_x:<{width-8}}x={max_x}")

numx = int(input("How many x length do you need: "))
ai = AIModel()

for i in range(numx):
    y = float(input(f"Enter y value in position {i+1}: "))
    ai.add_point(i + 1, y)

next_x = numx + 1
predicted_y = ai.predict(next_x)

print(f"\nAI predict when x={next_x}, y={predicted_y:.2f}")

ai.plot_ascii(next_x, predicted_y)