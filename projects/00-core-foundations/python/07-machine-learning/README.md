# 🤖 Phase 7: Machine Learning

51 self-contained topic directories organized into 3 levels covering ML from fundamentals through deep learning and model optimization.

## 📋 Directory Structure

Each topic directory contains:
- `NN-topic-name.py` — Exercise (runnable code, `--verify` self-checks)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation, 400+ lines)
- `NN-topic-name-glossary.md` — Glossary (key terms)
- `NN-topic-name-quiz.md` — Quiz (8 questions + scoring guide)

```
07-machine-learning/
├── fundamentals/                 # 23 topics: Basic ML concepts (01-23)
│   ├── 01-getting-started/
│   │   ├── 01-getting-started.py
│   │   ├── 01-getting-started-lecture.md
│   │   ├── 01-getting-started-glossary.md
│   │   └── 01-getting-started-quiz.md
│   └── ... (23 topics)
│
├── advanced/                     # 16 topics: pipelines, metrics, tuning, optimization (24-35, 48-51)
│   ├── 24-sklearn-pipelines/
│   └── ... (16 topics)
│
└── deep-learning/                # 12 topics: PyTorch, architectures, frameworks, training strategies (36-47)
    ├── 36-pytorch-tensors/
    └── ... (12 topics)
```

## 📚 Topics

### fundamentals/ (01-23): Basic ML Concepts
| # | Topic | Description |
|---|-------|-------------|
| 01 | Getting Started | ML overview, workflow |
| 02 | Data Mining | Data collection, exploration |
| 03 | Data Set | Dataset creation, loading |
| 04 | Clean Data | Preprocessing, handling missing values |
| 05 | Linear Regression | Simple linear regression |
| 06 | Polynomial Regression | Non-linear regression |
| 07 | R-Squared | Model evaluation metrics |
| 08 | Multiple Regression | Multiple features |
| 09 | Scale | Feature scaling, normalization |
| 10 | Train/Test Split | Data splitting strategies |
| 11 | Decision Tree | Tree-based classification |
| 12 | Confusion Matrix | Classification metrics |
| 13 | Correlation | Feature relationships |
| 14 | Linear Regression Example | Complete workflow |
| 15 | Logistic Regression | Binary classification |
| 16 | K-Means | Clustering |
| 17 | Hierarchical Clustering | Agglomerative clustering |
| 18 | PCA | Dimensionality reduction |
| 19 | Naive Bayes | Probabilistic classification |
| 20 | Random Forest | Ensemble methods |
| 21 | SVM | Support vector machines |
| 22 | Cross Validation | Model validation |
| 23 | K-Nearest Neighbors | Instance-based learning |

### advanced/ (24-35): Advanced Techniques
| # | Topic | Description |
|---|-------|-------------|
| 24 | Sklearn Pipelines | Pipeline API, chaining |
| 25 | Data Leakage | Preventing data leakage |
| 26 | Validation Strategies | Advanced validation |
| 27 | Metrics Deep Dive | Comprehensive metrics |
| 28 | Calibration | Probability calibration |
| 29 | Imbalanced Learning | Handling class imbalance |
| 30 | Gradient Boosting | XGBoost, LightGBM |
| 31 | Feature Engineering | Feature creation |
| 32 | Feature Selection | Feature importance |
| 33 | Hyperparameter Tuning | Grid/random search |
| 34 | Ensembling | Model ensembles |
| 35 | Explainability | SHAP, LIME |
| 48 | Hyperband and BOHB | Multi-fidelity tuning |
| 49 | Quantization | PTQ/QAT, INT8/INT4 |
| 50 | Pruning | Structured/unstructured sparsity |
| 51 | Distillation | Teacher-student compression |

### deep-learning/ (36-47): PyTorch, Architectures, Frameworks
| # | Topic | Description |
|---|-------|-------------|
| 36 | PyTorch Tensors | Tensor operations |
| 37 | PyTorch Training Loop | Training workflow |
| 38 | Neural Network Basics | NN architecture |
| 39 | Transfer Learning | Pre-trained models |
| 40 | Transformers from Scratch | Transformer architecture |
| 41 | CNNs | Convolutions, pooling, receptive field |
| 42 | RNNs | Recurrence, LSTM/GRU, sequences |
| 43 | TensorFlow and Keras | Declarative framework, SavedModel |
| 44 | JAX and Flax | Functional transforms, jit/grad/vmap |
| 45 | Data Augmentation | Label-preserving transforms |
| 46 | Few-Shot and Zero-Shot | Similarity, prototypes, in-context |
| 47 | Self-Supervised Learning | Pretext tasks, contrastive, masked |

## 🚀 Quick Start

```bash
# Install dependencies
pip install scikit-learn numpy pandas matplotlib torch

# Run any topic
python fundamentals/01-getting-started/01-getting-started.py

# Run all fundamentals
for d in fundamentals/[0-9]*/; do
    py=$(ls "$d"/*.py 2>/dev/null | head -1)
    [ -n "$py" ] && echo "=== $d ===" && python "$py"
done
```

## 📖 Recommended Learning Order

### Level 1: Fundamentals (01-23)
Start with the basics of ML algorithms and workflows.

### Level 2: Advanced (24-35)
Learn production ML techniques: pipelines, metrics, tuning.

### Level 3: Deep Learning (36-47)
PyTorch, architectures (CNN, RNN, Transformer), frameworks (Keras, JAX),
and training strategies (augmentation, few/zero-shot, self-supervised).

### Level 4: Model Optimization (48-51)
Compress and tune at scale: multi-fidelity tuning (Hyperband/BOHB),
quantization, pruning, and knowledge distillation.

---

*Last updated: October 2026*
