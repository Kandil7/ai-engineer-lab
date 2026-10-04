# 📋 AI Engineer Lab - Expansion Plan
**Projects: 00-core-foundations/python/**

---

## 📊 Current State Analysis (as of July 2026)

### Existing Structure (405+ files across 7 phases)

| Phase | Directory | Files | Status |
|-------|-----------|-------|--------|
| 1 | `01-core-python/` | 43 (.py + practice) | ✅ Complete |
| 2 | `02-advanced-python/` | 20 (.py + lectures) | ✅ Complete |
| 3 | `03-libraries/numpy/` | 28 files + lectures | ✅ Complete |
| 3 | `03-libraries/pandas/` | **0 files** | ❌ **MISSING** |
| 3 | `03-libraries/matplotlib/` | **0 files** | ❌ **MISSING** |
| 3 | `03-libraries/scipy/` | 12 files + lectures | ✅ Complete |
| 4 | `04-databases/mysql/` | 12 files + lectures | ✅ Complete |
| 4 | `04-databases/mongodb/` | 11 files + lectures | ✅ Complete |
| 5 | `05-web-frameworks/fastapi/` | 25 + exercises + lectures | ✅ Complete |
| 5 | `05-web-frameworks/django/` | 20 files | ✅ Complete |
| 5 | `05-web-frameworks/flask/` | **0 files** | ❌ **MISSING** |
| 6 | `06-data-structures-algorithms/` | 20 + lectures | ✅ Complete |
| 7 | `07-machine-learning/` | 23 + lectures | ⚠️ **Incomplete** (missing DL, MLOps, GenAI) |
| 📚 | `supplementary/lectures/` | 82+ files | ✅ Good |
| 📚 | `supplementary/quizzes/` | 29 files | ⚠️ **Incomplete** |
| 📚 | `supplementary/interviews/` | 16 files | ⚠️ **Incomplete** |
| 🏆 | `projects/` | 5 projects | ⚠️ **Need more capstones** |

---

## 🎯 Expansion Plan: 9 Phases Total (7 existing + 2 new)

### Phase 3 Completion: Data Science Libraries (HIGH PRIORITY)

#### 3a. Pandas (`03-libraries/pandas/`) — 24 Exercise Files + Lectures
| # | File | Topic | Key Concepts |
|---|------|-------|--------------|
| 1 | `01-introduction.py` | Series & DataFrame creation | `pd.Series`, `pd.DataFrame`, from dict/list/CSV |
| 2 | `02-inspecting-data.py` | `.head()`, `.info()`, `.describe()`, `.dtypes` | Data inspection basics |
| 3 | `03-indexing-selection.py` | `loc`, `iloc`, boolean indexing | Label vs positional indexing |
| 4 | `04-filtering.py` | Query, mask, `isin`, `between` | Advanced filtering |
| 5 | `05-missing-data.py` | `isna`, `fillna`, `dropna`, interpolation | Handling NaN |
| 6 | `06-data-types.py` | `astype`, `to_datetime`, `to_numeric`, categories | Type conversion |
| 7 | `07-string-methods.py` | `.str` accessor, regex, vectorized string ops | Text processing |
| 8 | `08-datetime.py` | `pd.Timestamp`, `pd.Timedelta`, resampling, time zones | Time series basics |
| 9 | `09-groupby-aggregation.py` | `groupby`, `agg`, `transform`, `filter` | Split-apply-combine |
| 10 | `10-pivot-tables.py` | `pivot_table`, `crosstab`, `melt`, `pivot` | Reshaping data |
| 11 | `11-merging-joining.py` | `merge`, `join`, `concat`, `combine_first` | SQL-style joins |
| 12 | `12-window-functions.py` | `rolling`, `expanding`, `ewm` | Moving averages, trends |
| 13 | `13-apply-map.py` | `apply`, `map`, `applymap`, `pipe` | Custom transformations |
| 14 | `14-categorical-data.py` | `Categorical`, `get_dummies`, `factorize` | Encoding |
| 15 | `15-io-csv-json.py` | `read_csv`, `read_json`, `read_parquet`, `to_*` | I/O formats |
| 16 | `16-io-excel-sql.py` | `read_excel`, `read_sql`, chunksize | Large datasets |
| 17 | `17-data-cleaning.py` | Duplicates, outliers, type fixing, validation | Real-world cleaning |
| 18 | `18-visualization.py` | `df.plot()`, integration with matplotlib/seaborn | Quick plotting |
| 19 | `19-multiindex.py` | Hierarchical indexing, `xs`, `swaplevel` | Advanced indexing |
| 20 | `20-performance.py` | `eval`, `query`, `numba`, memory optimization | Speed tips |
| 21 | `21-styling.py` | `Styler`, conditional formatting, export to Excel | Reporting |
| 22 | `22-case-study-eda.py` | End-to-end EDA on real dataset | Practice project |
| 23 | `23-case-study-timeseries.py` | Time series analysis project | Practice project |
| 24 | `24-case-study-ml-prep.py` | Feature engineering for ML pipeline | ML prep |

**Lectures:** `lectures/01-introduction-lecture.md` → `24-case-study-ml-prep-lecture.md` (24 files + glossaries)

#### 3b. Matplotlib (`03-libraries/matplotlib/`) — 20 Exercise Files + Lectures
| # | File | Topic |
|---|------|-------|
| 1 | `01-introduction.py` | Pyplot interface, figure/axes, basic plot |
| 2 | `02-line-plots.py` | Line styles, markers, multiple lines |
| 3 | `03-scatter-plots.py` | Scatter, bubble plots, color mapping |
| 4 | `04-bar-plots.py` | Bar, horizontal bar, grouped, stacked |
| 5 | `05-histograms.py` | Hist, density, cumulative, 2D hist |
| 6 | `06-pie-charts.py` | Pie, donut, explode, labels |
| 7 | `07-box-violin.py` | Boxplot, violin plot, statistical viz |
| 8 | `08-subplots.py` | `subplots`, `GridSpec`, `subplot_mosaic` |
| 9 | `09-3d-plots.py` | 3D scatter, surface, wireframe |
| 10 | `10-contour-heatmap.py` | Contour, heatmap, pcolormesh |
| 11 | `11-annotations.py` | Text, arrows, shapes, legends |
| 12 | `12-styling.py` | Stylesheets, rcParams, seaborn integration |
| 13 | `13-customizing-axes.py` | Ticks, scales (log, symlog), spines |
| 14 | `14-color-maps.py` | Colormaps, normalization, colorbars |
| 15 | `15-animation.py` | `FuncAnimation`, saving GIF/MP4 |
| 16 | `16-embedding.py` | Embedding in Tkinter, PyQt, web |
| 17 | `17-case-study-dashboard.py` | Multi-panel dashboard |
| 18 | `18-case-study-scientific.py` | Publication-quality figures |
| 19 | `19-case-study-ml-viz.py` | Learning curves, confusion matrices, ROC |
| 20 | `20-exporting.py` | Savefig, DPI, formats, vector vs raster |

**Lectures:** 20 lecture + glossary pairs

---

### Phase 5 Expansion: Flask + Advanced FastAPI (MEDIUM PRIORITY)

#### 5c. Flask (`05-web-frameworks/flask/`) — 15 Exercise Files
| # | File | Topic |
|---|------|-------|
| 1 | `01-introduction.py` | Minimal app, routing, `render_template` |
| 2 | `02-templates.py` | Jinja2, template inheritance, filters |
| 3 | `03-static-files.py` | CSS, JS, images, `url_for('static')` |
| 4 | `04-request-response.py` | Request object, form data, JSON, cookies |
| 5 | `05-forms-wtforms.py` | WTForms, validation, CSRF protection |
| 6 | `06-database-sqlalchemy.py` | Flask-SQLAlchemy, models, migrations |
| 7 | `07-auth-login.py` | Flask-Login, sessions, password hashing |
| 8 | `08-blueprints.py` | Modular apps, blueprints, URL prefixes |
| 9 | `09-rest-api.py` | RESTful design, `jsonify`, error handling |
| 10 | `10-testing.py` | Pytest fixtures, client, mocking |
| 11 | `11-deployment-gunicorn.py` | WSGI, Gunicorn, Nginx config |
| 12 | `12-docker.py` | Dockerfile, docker-compose |
| 13 | `13-logging-config.py` | Structured logging, config classes |
| 14 | `14-extensions.py` | Mail, caching, rate limiting, CORS |
| 15 | `15-case-study-blog.py` | Full blog app with auth, CRUD, API |

#### 5d. Advanced FastAPI Patterns (add to existing `fastapi/`)
| # | File | Topic |
|---|------|-------|
| 26 | `26-graphql.py` | Strawberry/GraphQL integration |
| 27 | `27-grpc.py` | gRPC with grpcio + protobuf |
| 28 | `28-rate-limiting.py` | SlowAPI, Redis-backed rate limiting |
| 29 | `29-api-versioning.py` | URL path, header, content negotiation versioning |
| 30 | `30-openapi-custom.py` | Custom OpenAPI, tags, security schemes |
| 31 | `31-background-jobs-celery.py` | Celery + Redis/RabbitMQ |
| 32 | `32-websockets-advanced.py` | Connection manager, rooms, broadcasting |
| 33 | `33-sse.py` | Server-Sent Events for streaming |
| 34 | `34-monitoring.py` | Prometheus metrics, health checks, structured logging |
| 35 | `35-deployment-docker.py` | Multi-stage Dockerfile, docker-compose.prod.yml |

---

### Phase 7 Expansion: Advanced ML (HIGH PRIORITY)

#### 7b. Advanced Classical ML (`07-machine-learning/advanced/`)
| # | File | Algorithm | Type |
|---|------|-----------|------|
| 24 | `24-gradient-boosting.py` | XGBoost / LightGBM / CatBoost | Supervised |
| 25 | `25-stacking-voting.py` | Ensemble: Stacking, Voting, Blending | Supervised |
| 26 | `26-calibration.py` | Platt scaling, isotonic regression | Supervised |
| 27 | `27-imbalanced-learning.py` | SMOTE, ADASYN, class weights, threshold moving | Supervised |
| 28 | `28-time-series-forecasting.py` | ARIMA, Prophet, statsmodels | Time Series |
| 29 | `29-feature-selection.py` | RFE, SelectKFromModel, SHAP values | Feature Eng |
| 30 | `30-model-explainability.py` | SHAP, LIME, permutation importance | Explainability |
| 31 | `31-hyperopt-optuna.py` | Optuna, Bayesian optimization | Tuning |
| 32 | `32-mlflow-tracking.py` | MLflow tracking, projects, models | MLOps |
| 33 | `33-pipeline-sklearn.py` | Pipeline, ColumnTransformer, FeatureUnion | Production |

#### 7c. Deep Learning Fundamentals (`07-machine-learning/deep-learning/`)
| # | File | Topic |
|---|------|-------|
| 1 | `01-pytorch-tensors.py` | Tensors, autograd, device management |
| 2 | `02-pytorch-nn.py` | `nn.Module`, layers, activations, loss |
| 3 | `03-pytorch-training.py` | Training loop, optimizer, scheduler, DataLoader |
| 4 | `04-cnn.py` | Conv2d, pooling, image classification (CIFAR-10) |
| 5 | `05-rnn-lstm.py` | RNN, LSTM, GRU, sequence modeling |
| 6 | `06-transformers.py` | Attention, transformer blocks, BERT/GPT basics |
| 7 | `07-transfer-learning.py` | Pretrained models, fine-tuning, feature extraction |
| 8 | `08-lightning.py` | PyTorch Lightning, Trainer, callbacks, loggers |
| 9 | `09-tensorflow-keras.py` | Keras Sequential/Functional API comparison |
| 10 | `10-case-study-nlp.py` | Text classification with transformers |
| 11 | `11-case-study-cv.py` | Object detection / segmentation |
| 12 | `12-case-study-tabular.py` | Tabular deep learning (TabNet, etc.) |

---

### Phase 8 (NEW): MLOps / Production ML (HIGH PRIORITY)
**Directory:** `08-mlops/`

| # | File | Topic |
|---|------|-------|
| 1 | `01-docker-ml.py` | Multi-stage Dockerfile, .dockerignore, build args |
| 2 | `02-docker-compose-ml.py` | Services: API, DB, Redis, monitoring, training |
| 3 | `03-fastapi-model-serving.py` | Model loading, batch inference, async endpoints |
| 4 | `04-model-registry.py` | MLflow Model Registry, versioning, stages |
| 5 | `05-ci-cd-github-actions.yml` | Workflow: test → build → deploy (staging → prod) |
| 6 | `06-prefect-airflow.py` | Orchestration: DAGs, tasks, retries, scheduling |
| 7 | `07-data-validation.py` | Great Expectations, Pandera, schema validation |
| 8 | `08-model-monitoring.py` | Drift detection (Evidently), data quality, performance |
| 9 | `09-a-b-testing.py` | Experiment framework, statistical significance |
| 10 | `10-feature-store.py` | Feast / custom feature store, offline/online |
| 11 | `11-kubernetes-ml.py` | K8s manifests, KServe, Kubeflow, scaling |
| 12 | `12-model-optimization.py` | ONNX, TensorRT, quantization, distillation |
| 13 | `13-case-study-e2e.py` | End-to-end: data → train → register → deploy → monitor |

**Lectures:** `lectures/01-docker-ml-lecture.md` → `13-case-study-e2e-lecture.md`

---

### Phase 9 (NEW): GenAI / LLM Engineering (HIGH PRIORITY)
**Directory:** `09-genai/`

| # | File | Topic |
|---|------|-------|
| 1 | `01-prompt-engineering.py` | Few-shot, CoT, ReAct, self-consistency, templates |
| 2 | `02-openai-api.py` | ChatCompletion, function calling, structured outputs |
| 3 | `03-langchain-basics.py` | Chains, prompts, memory, output parsers |
| 4 | `04-langgraph.py` | StateGraph, nodes, edges, conditional routing |
| 5 | `05-rag-basics.py` | Chunking, embeddings, vector store, retrieval |
| 6 | `06-rag-advanced.py` | HyDE, reranking, query expansion, multi-hop |
| 7 | `07-vector-dbs.py` | Chroma, Pinecone, Weaviate, Qdrant, Milvus |
| 8 | `08-agent-patterns.py` | ReAct, Plan-and-Execute, Reflexion, multi-agent |
| 9 | `09-fine-tuning.py` | LoRA/QLoRA, PEFT, SFT, DPO, Unsloth |
| 10 | `10-llm-eval.py` | LLM-as-judge, RAGAS, DeepEval, custom metrics |
| 11 | `11-guardrails.py` | NeMo Guardrails, Pydantic validation, jailbreak defense |
| 12 | `12-multimodal.py` | CLIP, BLIP, GPT-4V, LLaVA, image+text |
| 13 | `13-rag-production.py` | Incremental indexing, caching, hybrid search, observability |
| 14 | `14-agent-production.py` | LangGraph Platform, state persistence, human-in-loop |
| 15 | `15-case-study-chatbot.py` | RAG chatbot with citations, feedback, eval |
| 16 | `16-case-study-agent.py` | Code agent / research agent with tools |
| 17 | `17-case-study-multimodal.py` | Document QA with images/tables |

**Lectures:** 17 lecture + glossary pairs

---

### Supplementary Materials Expansion (MEDIUM PRIORITY)

#### Quizzes (`supplementary/quizzes/`) — Add 15 more
| Topic | File |
|-------|------|
| Pandas Basics | `pandas-basics-quiz.md` |
| Pandas Advanced | `pandas-advanced-quiz.md` |
| Matplotlib | `matplotlib-quiz.md` |
| Flask Basics | `flask-basics-quiz.md` |
| Flask Advanced | `flask-advanced-quiz.md` |
| Advanced ML | `ml-advanced-quiz.md` |
| Deep Learning | `deep-learning-quiz.md` |
| MLOps | `mlops-quiz.md` |
| GenAI / LLM Basics | `genai-basics-quiz.md` |
| RAG Systems | `rag-quiz.md` |
| Agents | `agents-quiz.md` |
| Prompt Engineering | `prompt-engineering-quiz.md` |
| Fine-tuning | `fine-tuning-quiz.md` |
| MLOps Kubernetes | `mlops-k8s-quiz.md` |
| System Design ML | `ml-system-design-quiz.md` |

#### Interview Prep (`supplementary/interviews/`) — Add 12 more
| Topic | File |
|-------|------|
| Pandas Interview | `pandas-interview.md` |
| MLOps Interview | `mlops-interview.md` |
| GenAI/LLM Interview | `genai-interview.md` |
| RAG Interview | `rag-interview.md` |
| ML System Design | `ml-system-design-interview.md` |
| Deep Learning Interview | `deep-learning-interview.md` |
| Feature Engineering Interview | `feature-engineering-interview.md` |
| Model Deployment Interview | `model-deployment-interview.md` |
| A/B Testing Interview | `ab-testing-interview.md` |
| LLM Fine-tuning Interview | `llm-finetuning-interview.md` |
| Vector Databases Interview | `vector-db-interview.md` |
| AI Safety/Ethics Interview | `ai-safety-interview.md` |

#### Cheat Sheets (NEW: `supplementary/cheatsheets/`)
| Topic | File |
|-------|------|
| Pandas | `pandas-cheatsheet.md` |
| NumPy | `numpy-cheatsheet.md` |
| Matplotlib | `matplotlib-cheatsheet.md` |
| Scikit-learn | `sklearn-cheatsheet.md` |
| FastAPI | `fastapi-cheatsheet.md` |
| Docker for ML | `docker-ml-cheatsheet.md` |
| SQL for Data Science | `sql-cheatsheet.md` |
| Git for ML | `git-ml-cheatsheet.md` |
| Prompt Engineering | `prompt-engineering-cheatsheet.md` |
| LangChain/LangGraph | `langchain-cheatsheet.md` |

---

### Capstone Projects Expansion (HIGH PRIORITY)
**Directory:** `projects/`

| # | Project | Directory | Phases Required | Description |
|---|---------|-----------|-----------------|-------------|
| 6 | **RAG Knowledge Base** | `06-rag-knowledge-base/` | 1,2,3,5,7,9 | Document QA with citations, hybrid search, eval |
| 7 | **ML Training Pipeline** | `07-ml-training-pipeline/` | 1,2,3,4,7,8 | Data validation → train → register → deploy → monitor |
| 8 | **Multi-Modal Document AI** | `08-multimodal-document-ai/` | 1,2,3,5,7,9 | PDF parsing, table extraction, vision+text QA |
| 9 | **LLM Fine-tuning Platform** | `09-llm-finetuning-platform/` | 1,2,3,7,8,9 | Dataset prep → LoRA training → eval → deploy |
| 10 | **AI Agent Marketplace** | `10-agent-marketplace/` | 1,2,3,5,8,9 | Multi-agent system with tool registry, human-in-loop |
| 11 | **Real-time ML Feature Store** | `11-feature-store/` | 1,2,3,4,7,8 | Online/offline store, materialization, point-in-time |
| 12 | **ML Model Monitoring Dashboard** | `12-model-monitoring/` | 1,3,4,5,8 | Drift detection, alerting, retraining triggers |

Each project includes:
- `README.md` - Architecture, setup, usage
- `main.py` / `app/` - Runnable application
- `tests/` - Unit + integration tests
- `docker-compose.yml` - Local dev environment
- `.github/workflows/` - CI/CD
- `docs/` - Architecture diagrams, API docs

---

## 📦 Updated Requirements

### Core Requirements (`requirements.txt`)
```
# Phase 1-2: Core Python (stdlib only)

# Phase 3: Data Science
numpy>=1.26.0
pandas>=2.1.0
matplotlib>=3.8.0
seaborn>=0.13.0
scipy>=1.11.0
scikit-learn>=1.3.0

# Phase 4: Databases
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
pymongo>=4.6.0
redis>=5.0.0

# Phase 5: Web Frameworks
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
jinja2>=3.1.0
httpx>=0.26.0
# Flask
flask>=3.0.0
flask-sqlalchemy>=3.1.0
flask-login>=0.6.0
flask-wtf>=1.2.0
wtforms>=3.1.0
flask-migrate>=4.0.0
gunicorn>=21.0.0

# Phase 6: DSA (stdlib)

# Phase 7: ML
xgboost>=2.0.0
lightgbm>=4.1.0
catboost>=1.2.0
optuna>=3.5.0
mlflow>=2.9.0
evidently>=0.4.0

# Phase 8: MLOps
docker>=7.0.0
prefect>=3.0.0
# kubernetes client (optional)
# kserve (optional)

# Phase 9: GenAI
openai>=1.12.0
anthropic>=0.18.0
langchain>=0.1.0
langchain-openai>=0.0.5
langgraph>=0.0.20
chromadb>=0.4.0
sentence-transformers>=2.2.0
tiktoken>=0.5.0
ragas>=0.0.20
deepeval>=0.20.0
```

### Dev Requirements (`requirements-dev.txt`)
```
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-asyncio>=0.23.0
pytest-mock>=3.12.0
black>=23.0.0
ruff>=0.1.0
mypy>=1.7.0
pre-commit>=3.6.0
jupyter>=1.0.0
ipykernel>=6.28.0
```

---

## 🗺️ Updated Learning Path (learning_path.md additions)

### Phase 3 Updated Order
```
NumPy (28) → Pandas (24) → Matplotlib (20) → SciPy (12)
     ↓           ↓            ↓             ↓
  Arrays      DataFrames    Visualization  Scientific
```

### Phase 5 Updated Order
```
FastAPI (25+10) → Flask (15) → Django (20)
     ↓               ↓            ↓
  Modern API    Traditional    Full-stack
```

### Phase 7 Updated Order
```
Classical ML (23) → Advanced ML (10) → Deep Learning (12)
       ↓                ↓                   ↓
   Sklearn         XGBoost/LightGBM    PyTorch/TensorFlow
```

### New Phase 8: MLOps (13)
```
Docker → Model Serving → CI/CD → Orchestration → Monitoring → K8s
```

### New Phase 9: GenAI (17)
```
Prompt Eng → APIs → LangChain → RAG → Agents → Fine-tuning → Production
```

---

## 📁 Final Directory Structure (Target)

```
python/
├── 01-core-python/                    # 43 files ✅
├── 02-advanced-python/                # 20 files ✅
├── 03-libraries/
│   ├── numpy/                         # 28 files ✅
│   ├── pandas/                        # 24 files 🆕
│   ├── matplotlib/                    # 20 files 🆕
│   └── scipy/                         # 12 files ✅
├── 04-databases/
│   ├── mysql/                         # 12 files ✅
│   └── mongodb/                       # 11 files ✅
├── 05-web-frameworks/
│   ├── fastapi/                       # 35 files 🆕 (+10 advanced)
│   ├── django/                        # 20 files ✅
│   └── flask/                         # 15 files 🆕
├── 06-data-structures-algorithms/     # 20 files ✅
├── 07-machine-learning/
│   ├── (existing 23)                  # ✅
│   ├── advanced/                      # 10 files 🆕
│   └── deep-learning/                 # 12 files 🆕
├── 08-mlops/                          # 13 files 🆕 (NEW PHASE)
├── 09-genai/                          # 17 files 🆕 (NEW PHASE)
├── supplementary/
│   ├── lectures/                      # 200+ files 🆕
│   ├── quizzes/                       # 44 files 🆕 (+15)
│   ├── interviews/                    # 28 files 🆕 (+12)
│   └── cheatsheets/                   # 10 files 🆕 (NEW)
├── projects/
│   ├── 01-calculator/                 # ✅
│   ├── 02-file-manager/               # ✅
│   ├── 03-api-server/                 # ✅
│   ├── 04-data-analyzer/              # ✅
│   ├── 05-ml-pipeline/                # ✅
│   ├── 06-rag-knowledge-base/         # 🆕
│   ├── 07-ml-training-pipeline/       # 🆕
│   ├── 08-multimodal-document-ai/     # 🆕
│   ├── 09-llm-finetuning-platform/    # 🆕
│   ├── 10-agent-marketplace/          # 🆕
│   ├── 11-feature-store/              # 🆕
│   └── 12-model-monitoring/           # 🆕
├── _dev/
├── requirements.txt                   # 🔄 UPDATED
├── requirements-dev.txt               # 🔄 UPDATED
├── learning_path.md                   # 🔄 UPDATED
├── run_smoke_tests.py                 # 🔄 UPDATED
└── README.md                          # 🔄 UPDATED
```

---

## 📅 Implementation Priority Order

| Priority | Phase | Effort | Dependencies |
|----------|-------|--------|--------------|
| 1 | Phase 3: Pandas + Matplotlib | High | Phase 1 |
| 2 | Phase 7: Advanced ML + Deep Learning | High | Phase 1, 3 |
| 3 | Phase 8: MLOps | High | Phase 1, 3, 5, 7 |
| 4 | Phase 9: GenAI | High | Phase 1, 2, 3, 7 |
| 5 | Phase 5: Flask + Advanced FastAPI | Medium | Phase 1, 2 |
| 6 | Supplementary: Quizzes/Interviews/Cheatsheets | Medium | All phases |
| 7 | Capstone Projects (6-12) | High | Phases 1-9 |

---

## ✅ Acceptance Criteria

- [ ] All 9 phases have complete exercise files with lectures
- [ ] Every `.py` file is runnable with `python file.py`
- [ ] Every FastAPI/Flask file runnable with `uvicorn`/`flask run`
- [ ] All projects have `README.md`, tests, Docker, CI/CD
- [ ] `run_smoke_tests.py` passes for all new files
- [ ] `requirements.txt` installs without conflicts
- [ ] `learning_path.md` reflects all 9 phases
- [ ] `README.md` updated with new structure
- [ ] Supplementary materials cover all phases

---

## 📝 Notes

1. **Pandas/Matplotlib**: Use the existing NumPy/SciPy lecture format (lecture + glossary pairs)
2. **Deep Learning**: Use PyTorch as primary, show TensorFlow/Keras equivalents
3. **MLOps**: Use local tools (Docker, Prefect, MLflow) — K8s optional/advanced
4. **GenAI**: Use OpenAI API + local models (Ollama/Llama.cpp) for cost control
5. **Projects**: Each should be portfolio-ready with documentation

---

*Plan created: July 2024 | Target: 405 → 800+ files*