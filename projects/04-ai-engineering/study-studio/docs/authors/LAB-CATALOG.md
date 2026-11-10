# Lab Catalog

This catalog documents all supported lab kinds in the Study Studio. Each kind specifies the data shape, rendering pattern, and examples for creating your own labs.

---

## Lab Structure Overview

Every lab shares this structure:

```json
{
  "id": "l01",                           // Unique lab identifier
  "title": "Lab Title",                  // Display title
  "goal": "What learners will understand.", // Learning objective
  "kind": "<lab-kind>",                  // See valid kinds below
  "controls": [...],                     // Input controls for the simulation
  "tasks": [                             // Exactly 3 guided tasks
    {
      "prompt": "Instruction text",
      "check": "Expected outcome text"
    }
  ],
  "takeawayEn": "One-line takeaway in English",
  "takeawayAr": "One-line takeaway in Arabic",
  "simulationNote": "Illustrative simulation, not real model output." // Required exact string
}
```

### Controls Structure

Each control defines an input widget:

```json
{
  "id": "<control-id>",          // Unique within this lab
  "label": "Display label",      // Shown in the control UI
  "kind": "<control-type>",      // slider | toggle | select | text
  "min": <number>,              // For sliders
  "max": <number>,              // For sliders
  "step": <number>,             // Slider step size (optional)
  "options": ["A", "B", "C"],   // For selects
  "default": <value>,           // Initial value
  "unit": "<unit>"              // Optional unit label (e.g., "x", "tokens")
}
```

### Tasks Structure

Each task has:
- `prompt`: Instruction text for the learner
- `check`: Expected outcome that validates success

---

## Valid Lab Kinds

| Kind | Description | Best For |
|------|-------------|----------|
| **tokenizer** | Tokenize text and show token IDs | Teaching tokenization basics |
| **embedding** | Vector space visualization | Showing semantic similarity |
| **attention** | Attention weight distribution | Demonstrating attention mechanics |
| **sampling** | Temperature/k-top sampling | Explaining sampling strategies |
| **rag-pipeline** | Multi-step RAG simulation | End-to-end retrieval generation |
| **training** | SGD/Adam optimizer visualization | Teaching training dynamics |
| **quantization** | Weight precision impact | Discussing model efficiency |
| **metrics** | Evaluation metric calculation | Showing metric computations |
| **cost-latency** | Cost and latency estimation | Budget planning discussions |
| **generic** | Custom lab runner template | Any simulation not covered above |

---

## 1. tokenizer Lab Kind

Tokenizes text into subword units and displays token IDs.

### Data Shape

```json
{
  "id": "l01",
  "title": "Tokenizer Playground",
  "goal": "See how text becomes tokens with IDs.",
  "kind": "tokenizer",
  "controls": [
    {
      "id": "text",
      "label": "Input Text",
      "kind": "text",
      "default": "hello world"
    },
    {
      "id": "tokenizer-type",
      "label": "Tokenizer",
      "kind": "select",
      "options": ["gpt2", "sentencepiece", "bpe"],
      "default": "gpt2"
    }
  ],
  "tasks": [
    {
      "prompt": "Type 'hello world' and read the token count.",
      "check": "The token count updates as you type."
    },
    {
      "prompt": "Switch to a different tokenizer and compare.",
      "check": "Different tokenizers produce different token counts."
    },
    {
      "prompt": "Find the longest token in your text.",
      "check": "The longest token is highlighted with its ID."
    }
  ],
  "takeawayEn": "Tokenization splits text into subword units that are more efficient than whole words.",
  "takeawayAr": "التokenization تقسم النص إلى وحدات جزئية تكون أكثر كفاءة من الكلمات الكاملة."
}
```

### Controls Typically Used

- **text**: Free text input (limited to short strings)
- **select**: Tokenizer type choice
- **slider**: Vocabulary size or context window

---

## 2. embedding Lab Kind

Visualizes embeddings in a 2D/3D space showing semantic similarity.

### Data Shape

```json
{
  "id": "l02",
  "title": "Embedding Space Explorer",
  "goal": "See how similar words cluster together.",
  "kind": "embedding",
  "controls": [
    {
      "id": "dimension-1",
      "label": "Dimension 1",
      "kind": "slider",
      "min": -3,
      "max": 3,
      "step": 0.5,
      "default": 0,
      "unit": ""
    },
    {
      "id": "dimension-2",
      "label": "Dimension 2",
      "kind": "slider",
      "min": -3,
      "max": 3,
      "step": 0.5,
      "default": 0,
      "unit": ""
    }
  ],
  "tasks": [
    {
      "prompt": "Move Dimension 1 and find similar words.",
      "check": "Similar concepts cluster together in the embedding space."
    },
    {
      "prompt": "Find words that are far apart semantically.",
      "check": "Dissimilar words appear on opposite sides of the plot."
    },
    {
      "prompt": "Identify an antonym pair.",
      "check": "Antonyms typically appear on opposite sides of axes."
    }
  ],
  "takeawayEn": "Embeddings place semantically similar words nearby in vector space.",
  "takeawayAr": "المضمّنات تضع كلمات متشابهة معانيها قريبًا في فضاء المتجهات."
}
```

### Rendering Considerations

- Use scatter plots with word labels
- Color-code by part of speech or category
- Allow hovering to see exact vector values
- Distance metric: cosine similarity preferred over Euclidean

---

## 3. attention Lab Kind

Demonstrates attention weight computation and distribution.

### Data Shape (Example from existing chapter)

```json
{
  "id": "l01",
  "title": "Attention heatmap",
  "goal": "See which tokens a query attends to.",
  "kind": "attention",
  "controls": [
    {
      "id": "sentence",
      "label": "Sentence",
      "kind": "text",
      "default": "the bank approved the river loan"
    },
    {
      "id": "query",
      "label": "Query token",
      "kind": "select",
      "options": ["bank", "approved", "river", "loan"],
      "default": "bank"
    },
    {
      "id": "sharpness",
      "label": "Sharpness",
      "kind": "slider",
      "min": 0.5,
      "max": 4,
      "step": 0.1,
      "default": 1.5,
      "unit": "x"
    }
  ],
  "tasks": [
    {
      "prompt": "Hover the query token 'bank' and read the weight on 'river'.",
      "check": "The river weight is high because bank and river belong to the same phrase."
    },
    {
      "prompt": "Switch the query to 'approved' and compare.",
      "check": "The river weight drops because approved is about the loan, not account."
    },
    {
      "prompt": "Raise sharpness to 4.0 and look at the weight spread.",
      "check": "Weights concentrate onto the top token and the rest collapse toward zero."
    }
  ],
  "takeawayEn": "Attention weights follow meaning, and sharper weighting concentrates mass.",
  "takeawayAr": "أوزان الانتباه تتبع المعنى، وكلما زادت الحدة تمركز التوزيع."
}
```

### Rendering Considerations

- Heatmap grid showing attention weights
- Hover to see exact weight values (0.0 - 1.0)
- Normalize weights so they sum to 1 across context
- Visualize softmax temperature effect

---

## 4. sampling Lab Kind

Demonstrates different text sampling strategies (temperature, k-top).

### Data Shape

```json
{
  "id": "l03",
  "title": "Sampling Strategy Simulator",
  "goal": "See how temperature affects output diversity.",
  "kind": "sampling",
  "controls": [
    {
      "id": "temperature",
      "label": "Temperature",
      "kind": "slider",
      "min": 0.1,
      "max": 2.0,
      "step": 0.1,
      "default": 1.0,
      "unit": "x"
    },
    {
      "id": "k-top",
      "label": "Top-K",
      "kind": "slider",
      "min": 1,
      "max": 50,
      "step": 1,
      "default": 40,
      "unit": "candidates"
    },
    {
      "id": "top-p",
      "label": "Top-P (Nucleus)",
      "kind": "toggle",
      "default": false
    }
  ],
  "tasks": [
    {
      "prompt": "Set temperature to 0.1 and generate a sample.",
      "check": "Low temperature produces deterministic, likely outputs."
    },
    {
      "prompt": "Raise temperature to 1.5 and compare samples.",
      "check": "Higher temperature increases diversity in outputs."
    },
    {
      "prompt": "Enable top-p=0.9 with temperature=0.8.",
      "check": "Nucleus sampling keeps tokens until cumulative probability reaches 0.9."
    }
  ],
  "takeawayEn": "Temperature controls creativity; top-K/top-P limit the candidate set.",
  "takeawayAr": "الدرجة تتحكم بالإبداع، بينما top-K/top-P تحدّ من مجموعة المرشحين."
}
```

---

## 5. rag-pipeline Lab Kind

Multi-step RAG simulation with retriever, reranker, and generator stages.

### Data Shape

```json
{
  "id": "l04",
  "title": "RAG Pipeline Simulator",
  "goal": "Trace a question through retrieval and generation.",
  "kind": "rag-pipeline",
  "controls": [
    {
      "id": "question",
      "label": "Question",
      "kind": "text",
      "default": "What is attention?"
    },
    {
      "id": "chunk-size",
      "label": "Chunk Size",
      "kind": "slider",
      "min": 100,
      "max": 1000,
      "step": 50,
      "default": 400,
      "unit": "tokens"
    },
    {
      "id": "top-k",
      "label": "Chunks to Retrieve",
      "kind": "slider",
      "min": 1,
      "max": 10,
      "step": 1,
      "default": 4,
      "unit": "chunks"
    }
  ],
  "tasks": [
    {
      "prompt": "Ask about 'attention' and read the retrieved chunks.",
      "check": "Retrieval returns chunks containing the concept."
    },
    {
      "prompt": "Reduce chunk size and rerun.",
      "check": "Smaller chunks are more precise but may split concepts."
    },
    {
      "prompt": "Increase top-K and observe context growth.",
      "check": "More chunks provide broader context but increase cost."
    }
  ],
  "takeawayEn": "RAG balances retrieval precision with context coverage.",
  "takeawayAr": "RAG توازن بين دقة الاسترجاع وتغطية السياق."
}
```

### Rendering Considerations

- Show retrieval scores before and after reranking
- Display chunk boundaries and overlap
- Visualize how retrieved chunks feed the generator
- Show token budget calculations

---

## 6. training Lab Kind

Visualizes training dynamics including loss curves and optimizer behavior.

### Data Shape

```json
{
  "id": "l05",
  "title": "Training Dynamics Viewer",
  "goal": "See how loss decreases during training.",
  "kind": "training",
  "controls": [
    {
      "id": "optimizer",
      "label": "Optimizer",
      "kind": "select",
      "options": ["sgd", "adam", "adamw"],
      "default": "adam"
    },
    {
      "id": "learning-rate",
      "label": "Learning Rate",
      "kind": "slider",
      "min": 0.0001,
      "max": 0.1,
      "step": 0.01,
      "default": 0.01,
      "unit": ""
    },
    {
      "id": "epochs",
      "label": "Epochs",
      "kind": "slider",
      "min": 1,
      "max": 50,
      "step": 1,
      "default": 10,
      "unit": ""
    }
  ],
  "tasks": [
    {
      "prompt": "Train with SGD and observe the loss curve.",
      "check": "SGD converges more slowly but can escape local minima."
    },
    {
      "prompt": "Switch to Adam and compare convergence speed.",
      "check": "Adam typically converges faster with adaptive learning rates."
    },
    {
      "prompt": "Increase the learning rate and watch for divergence.",
      "check": "Too high a learning rate causes oscillation or divergence."
    }
  ],
  "takeawayEn": "Optimizers balance speed of convergence with stability.",
  "takeawayAr": "المحسّنات توازن بين سرعة التقارب والاستقرار."
}
```

---

## 7. quantization Lab Kind

Demonstrates the impact of weight precision on model performance.

### Data Shape

```json
{
  "id": "l06",
  "title": "Quantization Impact Viewer",
  "goal": "See how precision affects accuracy and memory.",
  "kind": "quantization",
  "controls": [
    {
      "id": "bits",
      "label": "Precision",
      "kind": "select",
      "options": ["32-bit float", "16-bit float", "8-bit int", "4-bit int"],
      "default": "32-bit float"
    },
    {
      "id": "model-size",
      "label": "Model Size",
      "kind": "slider",
      "min": 0.1,
      "max": 70,
      "step": 2,
      "default": 7,
      "unit": "billion params"
    }
  ],
  "tasks": [
    {
      "prompt": "Start with 32-bit and note memory usage.",
      "check": "Float32 weights use 4 bytes per parameter."
    },
    {
      "prompt": "Switch to 8-bit and compare memory.",
      "check": "Int8 uses half the memory of float32 with minimal accuracy loss."
    },
    {
      "prompt": "Go to 4-bit and observe accuracy drop.",
      "check": "Quantization error accumulates, affecting performance."
    }
  ],
  "takeawayEn": "Lower precision saves memory but may reduce accuracy.",
  "takeawayAr": "الدقة المنخفضة توفر ذاكرة ولكن قد تقلل الدقة."
}
```

---

## 8. metrics Lab Kind

Calculates and displays evaluation metrics like P@K, MRR, F1.

### Data Shape

```json
{
  "id": "l07",
  "title": "Evaluation Metrics Calculator",
  "goal": "Compute retrieval and generation metrics.",
  "kind": "metrics",
  "controls": [
    {
      "id": "metric-type",
      "label": "Metric Type",
      "kind": "select",
      "options": ["P@1", "P@3", "MRR", "F1", "BLEU"],
      "default": "P@3"
    },
    {
      "id": "predictions-json",
      "label": "Predictions",
      "kind": "text",
      "default": '[{"pred":"Paris","gold":"Paris"},{"pred":"London","gold":"Paris"}]'
    }
  ],
  "tasks": [
    {
      "prompt": "Set P@1 with one correct match and read the score.",
      "check": "P@1 is 1.0 when the first prediction matches."
    },
    {
      "prompt": "Change predictions so only the second rank matches.",
      "check": "P@1 drops to 0.0 while P@2 stays at 1.0."
    },
    {
      "prompt": "Switch to MRR and compute mean reciprocal rank.",
      "check": "MRR considers how early the first match appears."
    }
  ],
  "takeawayEn": "Different metrics measure different aspects of retrieval quality.",
  "takeawayAr": "المقاييس المختلفة تقيس جوانب مختلفة من جودة الاسترجاع."
}
```

---

## 9. cost-latency Lab Kind

Estimates LLM call costs and latencies for budget planning.

### Data Shape

```json
{
  "id": "l08",
  "title": "Cost and Latency Calculator",
  "goal": "Estimate inference cost per request.",
  "kind": "cost-latency",
  "controls": [
    {
      "id": "input-tokens",
      "label": "Input Tokens",
      "kind": "slider",
      "min": 1,
      "max": 8000,
      "step": 256,
      "default": 512,
      "unit": "tokens"
    },
    {
      "id": "output-tokens",
      "label": "Output Tokens",
      "kind": "slider",
      "min": 1,
      "max": 4096,
      "step": 128,
      "default": 128,
      "unit": "tokens"
    },
    {
      "id": "model-tier",
      "label": "Model Tier",
      "kind": "select",
      "options": ["small", "medium", "large"],
      "default": "medium"
    }
  ],
  "tasks": [
    {
      "prompt": "Set input to 1,000 and output to 128 tokens.",
      "check": "The cost calculator shows dollars per request."
    },
    {
      "prompt": "Increase output to 2,000 tokens.",
      "check": "Cost increases linearly with output tokens."
    },
    {
      "prompt": "Compare small versus large model tiers.",
      "check": "Larger models cost more per token but may be more accurate."
    }
  ],
  "takeawayEn": "Cost scales linearly with total token count, not model accuracy alone.",
  "takeawayAr": "تكلفة تتدرج خطيًا مع عدد الرموز الكلي، وليس الدقة وحدها."
}
```

---

## 10. generic Lab Kind

Custom lab template for simulations not covered by the other kinds.

### Data Shape

```json
{
  "id": "l09",
  "title": "Custom Simulation",
  "goal": "Your custom learning objective.",
  "kind": "generic",
  "controls": [
    {
      "id": "<your-control>",
      "label": "<display label>",
      "kind": "<type>",
      "default": <value>
    }
  ],
  "tasks": [
    {
      "prompt": "Your first instruction.",
      "check": "Expected outcome."
    },
    {
      "prompt": "Your second instruction.",
      "check": "Expected outcome."
    },
    {
      "prompt": "Your third instruction.",
      "check": "Expected outcome."
    }
  ],
  "takeawayEn": "Your one-line takeaway in English.",
  "takeawayAr": "ملخصك باللغة العربية."
}
```

### Rendering Considerations for Generic Kinds

- The engine provides a placeholder container
- You control the HTML/JS via inline script blocks (if you extend the engine)
- Or use existing generic rendering pattern with your custom SVG/DOM updates
- Always document what your lab expects in the chapter JSON

---

## Control Type Details

### slider

Range input with numeric value:

```json
{
  "id": "my-slider",
  "label": "My Slider",
  "kind": "slider",
  "min": 0,
  "max": 100,
  "step": 1,
  "default": 50,
  "unit": "%",
  "onChange": "<function-that-runs-when-value-changes>" // Optional callback
}
```

### toggle

Boolean on/off switch:

```json
{
  "id": "my-toggle",
  "label": "Enable Feature",
  "kind": "toggle",
  "default": false,
  "onChange": "<function-that-runs-when-toggled>" // Optional callback
}
```

### select

Dropdown or radio buttons:

```json
{
  "id": "my-select",
  "label": "Choose Mode",
  "kind": "select",
  "options": ["Mode A", "Mode B", "Mode C"],
  "default": "Mode A",
  "onChange": "<function-that-runs-when-selected>" // Optional callback
}
```

### text

Short text input (use sparingly):

```json
{
  "id": "my-text",
  "label": "Enter Value",
  "kind": "text",
  "default": "0.5",
  "maxLength": 10, // Optional limit
  "onChange": "<function-that-runs-when-changed>" // Optional callback
}
```

---

## Best Practices for Lab Writing

### Do's

- ✅ Keep each lab focused on one concept
- ✅ Use all three tasks to guide learners through key insights
- ✅ Provide Arabic takeaways that capture the essence in a single sentence
- ✅ Test your lab controls with edge values (min, max)
- ✅ Describe mistakes learners commonly make in task checks

### Don'ts

- ❌ Don't make labs longer than 3 tasks (keep it focused)
- ❌ Don't forget the exact `simulationNote` string
- ❌ Don't rely on learner guessing; be explicit about expected values
- ❌ Don't use controls that have no visible effect

### Testing Your Labs

Before adding to your chapter, verify:

- All controls initialize with their default values
- Changing a control produces observable changes
- All tasks have realistic expected outcomes
- The Arabic takeaway accurately summarizes the learning point

---

## Summary Table

| Lab Kind | Key Controls | Typical Use Case |
|----------|--------------|------------------|
| tokenizer | text, select | Tokenization mechanics |
| embedding | sliders (2D/3D) | Vector space visualization |
| attention | text, select, slider | Attention weight distributions |
| sampling | slider, toggle | Temperature/k-top effects |
| rag-pipeline | text, sliders | Retrieval generation pipeline |
| training | select, slider | Optimizer behavior visualization |
| quantization | select, slider | Precision vs. accuracy tradeoff |
| metrics | select, text | Metric computation and interpretation |
| cost-latency | sliders, select | Budget planning discussions |
| generic | custom | Any custom simulation |
