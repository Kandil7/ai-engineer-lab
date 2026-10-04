# Matplotlib Quiz

## Topic Overview
Matplotlib is the most widely used Python library for creating static, animated, and interactive visualizations. It provides a MATLAB-like interface for creating publication-quality plots. This quiz covers plotting basics, customization, and common chart types.

**Difficulty:** Beginner to Intermediate
**Questions:** 20
**Time:** ~25 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**What is Matplotlib primarily used for?**

A) Data manipulation
B) Creating visualizations and plots
C) Machine learning
D) Web development

**Correct Answer:** B
**Explanation:** Matplotlib is a plotting library for creating static, animated, and interactive visualizations in Python. It's the foundation for most other Python visualization libraries.

---

### Question 2 [Easy]
**How do you import Matplotlib's pyplot module?**

A) `import matplotlib.pyplot as plt`
B) `from matplotlib import pyplot`
C) `import pyplot as plt`
D) Both A and B

**Correct Answer:** D
**Explanation:** Both import styles work. The convention `import matplotlib.pyplot as plt` is the most common and recommended.

---

### Question 3 [Easy]
**What function creates a line plot?**

A) `plt.plot()`
B) `plt.line()`
C) `plt.draw()`
D) `plt.show()`

**Correct Answer:** A
**Explanation:** `plt.plot()` creates line plots. It accepts x and y data, color, markers, labels, and other styling options.

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
plt.show()
```

---

### Question 4 [Easy]
**What does `plt.show()` do?**

A) Creates a plot
B) Displays the plot
C) Saves the plot
D) Clears the plot

**Correct Answer:** B
**Explanation:** `plt.show()` renders and displays the plot. In Jupyter notebooks, you may not need it if using `%matplotlib inline`. It's required in standard Python scripts.

---

### Question 5 [Medium]
**How do you add a title to a plot?**

A) `plt.title()`
B) `plt.set_title()`
C) `plt.name()`
D) `plt.add_title()`

**Correct Answer:** A
**Explanation:** `plt.title('My Plot')` adds a title to the current plot. You can customize font size, weight, and position with additional parameters.

---

### Question 6 [Medium]
**Which function creates a bar chart?**

A) `plt.bar()`
B) `plt.barplot()`
C) `plt.barchart()`
D) `plt.column()`

**Correct Answer:** A
**Explanation:** `plt.bar()` creates vertical bar charts. Use `plt.barh()` for horizontal bars. `sns.barplot()` exists in Seaborn but not in Matplotlib.

---

### Question 7 [Easy]
**How do you add axis labels?**

A) `plt.xlabel()` and `plt.ylabel()`
B) `plt.x_label()` and `plt.y_label()`
C) `plt.set_xlabel()` and `plt.set_ylabel()`
D) `plt.label()`

**Correct Answer:** A
**Explanation:** `plt.xlabel('X Axis')` and `plt.ylabel('Y Axis')` set the axis labels for the current plot.

---

### Question 8 [Medium]
**What does `plt.subplot()` do?**

A) Creates a sub-plot within a figure
B) Divides the plot area
C) Adds a secondary axis
D) Creates multiple figures

**Correct Answer:** A
**Explanation:** `plt.subplot(nrows, ncols, index)` creates a subplot grid and activates the specified position. For example, `plt.subplot(2, 2, 1)` creates a 2x2 grid and selects the first position.

---

### Question 9 [Medium]
**How do you create a scatter plot?**

A) `plt.scatter()`
B) `plt.scatterplot()`
C) `plt.dot()`
D) `plt.points()`

**Correct Answer:** A
**Explanation:** `plt.scatter()` creates scatter plots. It accepts x, y coordinates, color (`c`), size (`s`), and other styling options.

```python
plt.scatter([1, 2, 3, 4], [1, 4, 9, 16], c="red", s=100)
```

---

### Question 10 [Medium]
**What does `plt.legend()` do?**

A) Adds a legend to the plot
B) Reads legend data
C) Creates a legend file
D) Removes the legend

**Correct Answer:** A
**Explanation:** `plt.legend()` displays a legend box identifying each plotted line or marker. You provide labels via the `label` parameter in plot functions or directly in `legend()`.

---

### Question 11 [Easy]
**How do you save a plot to a file?**

A) `plt.savefig()`
B) `plt.save()`
C) `plt.export()`
D) `plt.write()`

**Correct Answer:** A
**Explanation:** `plt.savefig('filename.png')` saves the current figure to a file. Supports PNG, PDF, SVG, and other formats. Call `savefig()` before `show()`.

---

### Question 12 [Medium]
**What does `fig, ax = plt.subplots()` do?**

A) Creates a figure and axes object
B) Creates two plots
C) Creates a subplot grid
D) Both A and C

**Correct Answer:** D
**Explanation:** `plt.subplots()` creates a Figure and Axes object(s). It's the object-oriented approach to Matplotlib. You specify rows and columns, e.g., `plt.subplots(2, 3)` creates a 2x3 grid.

---

### Question 13 [Medium]
**How do you change the plot style?**

A) `plt.style.use('style_name')`
B) `plt.set_style('style_name')`
C) `plt.style = 'style_name'`
D) `plt.apply_style('style_name')`

**Correct Answer:** A
**Explanation:** `plt.style.use('ggplot')` applies a predefined style. Available styles include 'ggplot', 'seaborn', 'dark_background', 'fivethirtyeight', etc.

---

### Question 14 [Easy]
**What is `plt.figure()` used for?**

A) Creates a new figure
B) Adds data
C) Removes a figure
D) Changes the figure

**Correct Answer:** A
**Explanation:** `plt.figure()` creates a new figure with optional parameters like `figsize`, `dpi`, and `facecolor`. It's useful for creating multiple independent plots.

---

### Question 15 [Medium]
**How do you create a histogram?**

A) `plt.hist()`
B) `plt.histogram()`
C) `plt.bar()` with special parameters
D) `plt.distribution()`

**Correct Answer:** A
**Explanation:** `plt.hist(data, bins=10)` creates a histogram showing the distribution of data. The `bins` parameter controls the number of bins.

---

### Question 16 [Hard]
**What does `plt.tight_layout()` do?**

A) Makes the plot larger
B) Automatically adjusts subplot parameters for fit
C) Tightens the axes
D) Reduces plot size

**Correct Answer:** B
**Explanation:** `tight_layout()` automatically adjusts subplot parameters to fit all elements (titles, labels, legends) without overlap. Call it before `show()` or `savefig()`.

---

### Question 17 [Medium]
**How do you create a pie chart?**

A) `plt.pie()`
B) `plt.circle()`
C) `plt.piechart()`
D) `plt.donut()`

**Correct Answer:** A
**Explanation:** `plt.pie()` creates a pie chart. It accepts sizes, labels, colors, and options like `autopct` for percentage display and `startangle` for rotation.

---

### Question 18 [Hard]
**What does the object-oriented API (`fig, ax = plt.subplots()`) offer over the pyplot interface?**

A) Better performance
B) More control and flexibility for complex plots
C) Simpler syntax
D) No difference

**Correct Answer:** B
**Explanation:** The object-oriented approach (`ax.plot()`, `ax.set_title()`) gives you explicit control over each Axes object. It's more Pythonic and better for complex, multi-panel figures.

---

### Question 19 [Medium]
**How do you create a heatmap?**

A) `plt.imshow()` or `plt.pcolormesh()`
B) `plt.heatmap()`
C) `plt.color()`
D) `plt.map()`

**Correct Answer:** A
**Explanation:** `plt.imshow()` displays data as an image (heatmap). `plt.pcolormesh()` is better for irregular grids. Seaborn's `sns.heatmap()` provides a higher-level interface.

---

### Question 20 [Medium]
**What does `plt.xticks()` and `plt.yticks()` do?**

A) Set tick locations and labels for axes
B) Create tick marks
C) Remove ticks
D) Rotate the plot

**Correct Answer:** A
**Explanation:** `plt.xticks()` and `plt.yticks()` control tick locations and labels. You can customize positions, labels, rotation, and font properties.

```python
plt.xticks(rotation=45, ha="right")
plt.yticks([0, 25, 50, 75, 100])
```

---

## Answer Key

| Question | Answer |
|----------|--------|
| 1 | B |
| 2 | D |
| 3 | A |
| 4 | B |
| 5 | A |
| 6 | A |
| 7 | A |
| 8 | A |
| 9 | A |
| 10 | A |
| 11 | A |
| 12 | D |
| 13 | A |
| 14 | A |
| 15 | A |
| 16 | B |
| 17 | A |
| 18 | B |
| 19 | A |
| 20 | A |

---

## Score Tracking

| Score Range | Level |
|-------------|-------|
| 18-20 | Expert - You've mastered Matplotlib! |
| 14-17 | Proficient - Strong visualization skills |
| 10-13 | Developing - Good foundation, explore more chart types |
| 6-9 | Beginner - Review plotting fundamentals |
| 0-5 | Novice - Start with Matplotlib tutorial |

---

*Quiz created for AI Engineer Lab - Python Foundations*
