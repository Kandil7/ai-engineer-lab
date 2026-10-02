# MLOps Production AI Systems Engineer Quiz

**Instructions:** Answer these 16 questions to test your knowledge of Production AI Systems Engineering concepts.

---

## Section 1: Data Engineering Fundamentals

### Question 1
**Topic: Batch vs Streaming Processing**

A production recommendation system processes user clickstream data arriving at 10,000 events/second. The features need to be available for real-time inference with sub-50ms latency. Which architecture pattern would you choose and why?

A) Lambda Architecture - Process batch data nightly for training, stream data for online features
B) Kappa Architecture - Use Kafka Streams/Flink CDC to maintain up-to-date feature store from a single streaming stream
C) Simple Batch - Aggregate data in Spark daily and serve pre-computed features
D) Data Lakehouse - Use Delta Lake with ACID transactions on batch updates

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

### Question 2
**Topic: Feature Stores**

You're implementing an online feature store using Feast. The system has the following requirements:
- 10M features needed at inference time
- Features must be consistent between training and serving
- Latency requirement: <5ms per feature access

Which of these is a critical best practice for this scenario?

A) Use Redis for offline storage with Parquet files for caching
B) Implement feature retrieval with proper keying (user_id, context_id) and use online store (Redis/Bigtable) with appropriate TTL
C) Store all features in S3 and load them on-demand at inference time
D) Use only memory caching without persistence

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

### Question 3
**Topic: Data Quality**

Your production model's performance degraded after a week. Investigation shows the input data distribution has shifted significantly. Which tool would help you detect this drift BEFORE it impacts production?

A) Apache Airflow - for scheduling
B) Great Expectations with anomaly detection on incoming streams
C) MLflow experiments only
D) Simple data visualization in Grafana

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

## Section 2: Machine Learning Development

### Question 4
**Topic: Model Optimization for Production**

You've trained a ResNet-50 model (123MB, takes 87ms inference) and need to deploy it on edge devices with 4GB RAM constraint. Which optimization technique would give the best performance/accuracy trade-off?

A) Post-training quantization to INT8 using TensorRT
B) Model pruning only
C) Knowledge distillation to a smaller student model
D) All of the above combined

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

### Question 5
**Topic: Hyperparameter Optimization**

You have a complex model with ~50 hyperparameters and need to optimize within a budget of 100 training runs. Which strategy provides the best balance of exploration and exploitation?

A) Grid Search over all parameters
B) Random Search with limited trials
C) Bayesian Optimization using Optuna with PrunedSearchSpace
D) Manual tuning based on intuition

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

### Question 6
**Topic: Transfer Learning**

You're applying a pre-trained BERT model to a domain-specific task (legal document classification). The pre-trained model has 350M parameters. Your dataset is only 10K labeled documents. What's the recommended fine-tuning strategy?

A) Fine-tune all layers including embeddings
B) Freeze embedding and lower layers, only train classification head
C) Use adapter modules (LoRA) to inject trainable weights into frozen model
D) Pre-train from scratch on domain data

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

## Section 3: MLOps Core Concepts

### Question 7
**Topic: Experiment Tracking**

You're comparing 100 different model configurations. Which experiment tracking setup would give you the best view of results?

A) Console logs only
B) MLflow with custom metrics logged to registry, versioned artifacts, and comparison dashboard
C) Email summaries at end of training
D) Manual spreadsheet tracking

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

### Question 8
**Topic: Model Registry & Governance**

Your team needs a model approval workflow before promotion to production. Which governance pattern ensures this while maintaining efficiency?

A) Auto-deploy to production after any training success
B) MLflow Model Registry with Stage transitions (Staging → Production) requiring approval at each gate
C) Manual review by one person per model
D) Deploy to staging and hope it works

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

### Question 9
**Topic: CI/CD for ML**

Set up automated retraining for a credit scoring model. Data drift triggers occur when PSI > 0.25 on key features. Which pipeline design handles this correctly?

A) Fixed schedule (e.g., daily retrain regardless of data quality)
B) Event-driven: Airflow sensor triggers on Kafka topic indicating drift detection, then retrains and deploys to shadow for validation
C) Manual trigger from dashboard button
D) Retrain only when error rate exceeds threshold

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

## Section 4: Cloud Infrastructure

### Question 10
**Topic: Kubernetes for ML**

You're deploying a model serving service on EKS. The model requires GPU acceleration and must handle variable traffic (2 requests/sec to 5000 requests/sec). Which HPA configuration is correct?

A) Only CPU-based metrics
B) Custom metrics API with request queue length OR GPU utilization thresholds
C) Fixed number of replicas regardless of load
D) No scaling, use Lambda instead

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

### Question 11
**Topic: Docker & Containerization**

Creating a Docker image for a PyTorch model serving container. Which steps optimize the image size and security?

A) Use python:3.9-slim, multi-stage build with base tools removed, non-root user, pinned dependencies
B) Use full Python image without cleanup
C) Copy all dev packages to production image
D) Use only system containers without Docker

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

### Question 12
**Topic: Serverless ML**

For a fraud detection model that processes payments, you want serverless deployment with sub-second cold starts and automatic scaling. Which pattern works best?

A) AWS Lambda invoking SageMaker Endpoint via InvokeEndpoint API with VPC
B) EC2 instance without auto-scaling
C) Bare metal servers with manual scaling
D) Only use container instances

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

## Section 5: Model Serving & APIs

### Question 13
**Topic: Inference Server Selection**

You're serving multiple models (PyTorch, TensorFlow, ONNX) from a single endpoint with dynamic batching. Which serving solution provides the best flexibility and performance?

A) Flask app calling model directly
B) Triton Inference Server with ensemble support and dynamic batch size scheduling
C) Custom gRPC server only
D) REST API with synchronous inference calls

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

### Question 14
**Topic: Request Caching**

A recommendation model produces identical recommendations for same user context. You want to reduce inference costs by caching results. Which caching strategy is appropriate?

A) Cache all requests indefinitely
B) Redis with TTL based on content freshness, cache key = hash(user_id + context_features), invalidation rules for schema changes
C) No caching - always recompute
D) Only cache error responses

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

## Section 6: Monitoring & Observability

### Question 15
**Topic: Drift Detection Implementation**

You need to implement data drift detection for a production model. The input features are numeric and you want to detect when distribution shifts beyond acceptable bounds. What metrics and tests would you use?

A) Only check if errors increase
B) PSI (Population Stability Index) with threshold of 0.1-0.25, Kolmogorov-Smirnov test for continuous distributions, correlation matrix drift
C) Visual inspection only
D) Check model accuracy once per month

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

### Question 16
**Topic: Latency Monitoring**

Your API shows p95 latency of 200ms (SLA requirement is <300ms). However, users complain about slow responses. What additional metrics should you track to identify root causes?

A) Only response time
B) p50/p95/p99 percentiles, request queue depth, GPU utilization, model load times, cache hit rate, error breakdown by type
C) Just CPU usage
D) Database connection count only

**Answer:** \_\_\_\_\_\_\_\_\_\_

---

## Answers and Explanations

### Answer Key:
1. **A (Lambda)** - Batch training + streaming features for real-time requirements
2. **B** - Feature stores need proper online store with consistent retrieval patterns
3. **B** - Data quality tools provide automated drift detection before issues occur
4. **D** - Combined approaches (quantization + pruning + distillation) give best results
5. **C** - Bayesian optimization balances exploration/exploitation efficiently
6. **C** - LoRA is ideal for small datasets with large pre-trained models
7. **B** - MLflow provides comprehensive experiment tracking and comparison
8. **B** - Stage transitions with approvals balance governance and workflow
9. **B** - Event-driven pipelines react to actual triggers, not just schedules
10. **B** - Custom metrics allow queue-length-based scaling for latency SLAs
11. **A** - Multi-stage builds with slim base images are security best practices
12. **A** - Lambda + SageMaker Runtime enables serverless ML with cold start mitigation
13. **B** - Triton supports multiple frameworks, dynamic batching, and model ensembles
14. **B** - Redis caching with proper TTL prevents stale data issues
15. **B** - Multiple statistical tests provide comprehensive drift detection
16. **B** - Full observability requires monitoring at multiple layers

---

## Scoring Guide

- **13-16 correct**: 🌟 Production AI Systems Engineer Ready!
- **9-12 correct**: 👍 Solid Foundation, review weak areas
- **5-8 correct**: 📚 Continue studying the roadmap sections
- **0-4 correct**: 🔨 Start with fundamentals and practice projects

---

## Next Steps After Quiz

Based on your score:

- **High Score (13+)**: Move to specialization tracks (LLM Engineering, Edge AI, etc.)
- **Medium Score (5-12)**: Review quiz explanations, revisit roadmap sections
- **Low Score (0-4)**: Complete Phase 1 of learning path, build foundational projects

---

*Part of the Production AI Systems Engineer Roadmap*  
*Last updated: October 2026*
