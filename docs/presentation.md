# Serverless Cold Start & Cost Analysis — Final Presentation Notes

**Project**: Cloud Computing Lab Project — Group 50  
**Theme**: Theme 4: Serverless & Startups (Freshworks Case Study)  
**Deliverable File**: [Cloud_Computing_Group_50_Presentation.pptx](Cloud_Computing_Group_50_Presentation.pptx)  

---

## Slide 1: Title & Team Overview
- **Title**: Serverless Cold Start & Cost Analysis
- **Subtitle**: Theme 4: Serverless & Startups — Production Benchmarking & Cloud Economics
- **Group**: Project Group 50 | Partner Track: Freshworks Case Study
- **Team Members & Responsibilities**:
  - **Person A (Aalok Thakkar / A-K-0802)**: Backend Architecture, DynamoDB Schema, API Gateway Configuration, AWS SAM Template, CI/CD Pipeline.
  - **Person B (Bhagya Thakkar / BM1100)**: Benchmarking Suite, 500-Request Latency Matrix, CloudWatch Insights Analytics, Latency Plots.
  - **Person C (Farhan Ansari / FARHAN5826)**: Cost Analysis Spreadsheet, EC2 Break-Even Economics, Technical Documentation, Final Presentation & Report.

> **Speaker Notes**:  
> "Good morning everyone. We are Group 50 presenting our project on Serverless Cold Starts and Cost Analysis for startups, inspired by real-world engineering challenges at scale such as Freshworks and Shaadi.com. In this presentation, we will walk you through our live AWS deployment, our empirical 500-request benchmark, our CloudWatch internal telemetry breakdown, and our comprehensive cost model comparing serverless to always-on EC2 instances."

---

## Slide 2: Problem Statement: The Serverless Cold Start Dilemma
- **The Startup Promise**: Zero idle cost, automatic horizontal scaling, no OS/patch maintenance.
- **The Reality**: Cold starts introduce unpredictable latency penalties when containers boot up from scratch.
- **The Impact**: Degraded customer experience, higher bounce rates, and SLA breaches on user-facing endpoints.

> **Speaker Notes**:  
> "Serverless compute via AWS Lambda represents an ideal architecture for early-stage startups because you pay only for compute time used. However, serverless introduces cold starts: when an API receives traffic after an idle period or traffic spikes, AWS Firecracker microVMs must spin up, initialize runtimes, and import dependencies before serving the request. Our goal was to measure and explain this penalty precisely."

---

## Slide 3: Architecture Overview & Live Endpoint
- **Entrypoint**: Amazon API Gateway (HTTP API) in `ap-south-1` (Mumbai).
- **Compute**: AWS Lambda (Python 3.11, 128 MB RAM).
- **Storage**: Amazon DynamoDB (On-Demand billing).
- **Observability**: Amazon CloudWatch Logs Insights.
- **Live Endpoint**:  
  `POST https://w3obh27tnh.execute-api.ap-south-1.amazonaws.com/submit`
- **Sample Payload**: `{"name": "tester", "score": 9.5}`

> **Speaker Notes**:  
> "Our architecture is deployed live in AWS Asia Pacific Mumbai (ap-south-1). The API Gateway routes incoming POST requests to our Python 3.11 Lambda handler. The Lambda validates the payload and writes it directly to an On-Demand DynamoDB table. All invocations stream high-resolution metrics directly into CloudWatch."

---

## Slide 4: Infrastructure as Code & CI/CD Pipeline
- **AWS SAM (Serverless Application Model)**: Declarative `template.yaml` defining API routes, Lambda permissions, and DynamoDB tables.
- **GitHub Actions**: Automated CI/CD pipeline on push to `main` executing `sam build` and `sam deploy --no-confirm-changeset`.
- **Zero Configuration Drift**: Repeatable deployments across environments with IAM least privilege.

> **Speaker Notes**:  
> "To guarantee production reproducibility, 100% of our infrastructure is managed as code using AWS SAM. Whenever a commit lands on main, our GitHub Actions workflow validates the SAM template, builds the Lambda artifact, and deploys the stack to AWS without manual console intervention."

---

## Slide 5: Benchmarking Methodology
- **Matrix**: 5 independent rounds × 100 sequential requests = 500 total requests.
- **Cold Boot Forcing**: Altered dummy environment variables between rounds to force container eviction.
- **Dual Telemetry**: Client-perceived round-trip latency (`requests.elapsed`) coupled with internal AWS CloudWatch execution logs.

> **Speaker Notes**:  
> "To isolate cold starts from warm executions cleanly, we designed a forced cold-start benchmark. Lambda containers typically remain warm for 5 to 15 minutes. By updating an environment variable before each 100-request batch, we forced AWS to spin up a brand new microVM for request #1 of each round, allowing us to capture 5 distinct cold start baselines against 495 warm executions."

---

## Slide 6: Latency Results & Visual Chart
- **Cold Start Average (1st request)**: 1,270.01 ms
- **Warm Average (100th request)**: 504.98 ms
- **Warm Average (Overall warm)**: 547.59 ms
- **Warm 95th Percentile (p95)**: 792.55 ms
- **Cold-to-Warm Ratio**: **2.32x slower**
- *(Includes embedded chart from `results/latency_graph.png`)*

> **Speaker Notes**:  
> "Here are our empirical results. Across all 5 rounds, cold start latency averaged 1,270 ms, whereas subsequent warm executions stabilized at 548 ms. That represents a 2.32x latency penalty for the first user hitting the API. The graph clearly visualizes the massive spike on request 1, followed by immediate stabilization into a flat, predictable warm band."

---

## Slide 7: CloudWatch Telemetry & Latency Breakdown
- **Average Init Duration (Cold Boot)**: 455.87 ms (MicroVM boot & `boto3` loading)
- **Average Execution Duration**: 25.39 ms (Pure Python handler runtime)
- **Average Billed Duration**: 33.39 ms (Official billed duration tier)
- **Dissecting the Gap**:
  - CloudWatch Execution: ~25 ms
  - Container Init: ~456 ms
  - Local Client-to-Mumbai Round Trip: ~520 ms
  - Total Perceived: ~1,270 ms

> **Speaker Notes**:  
> "Looking inside AWS CloudWatch Logs Insights across 545 invocations, we discovered a vital insight. The Lambda code itself executes in just 25 milliseconds! The 456 ms Init Duration represents the AWS hypervisor initializing Python and loading the boto3 SDK. The remaining ~520 ms is physical network transit between the local client and the AWS Mumbai datacenter."

---

## Slide 8: Cost Model & EC2 Break-Even Analysis
- **Serverless Cost per 1,000 requests**: **$0.00252** (approx 1/4 of a cent)
  - API Gateway: $0.00100
  - DynamoDB write: $0.00125
  - Lambda invocations: $0.00020
  - Lambda compute (33.39 ms @ 128MB): $0.00007
- **Always-on EC2 (t3.micro)**: **$7.59 / month** ($0.0104/hr × 730 hrs)
- **Break-Even Traffic**: **~3,010,000 requests/month** (~3.01 million)

> **Speaker Notes**:  
> "On the economics front, our spreadsheet model reveals that 1,000 requests cost just $0.0025 on serverless. An always-on t3.micro EC2 instance costs $7.59 per month regardless of whether anyone uses it. The break-even point is approximately 3.01 million requests per month. For early-stage startups and fluctuating traffic, serverless provides immense financial savings with zero idle burn."

---

## Slide 9: Industry Best Practices & Mitigations
1. **Provisioned Concurrency**: Eliminates cold starts for mission-critical routes by keeping pre-warmed execution environments ready.
2. **Lean Dependency Trees**: Import only specific client submodules (e.g. `boto3.client('dynamodb')` rather than entire SDK) to cut initialization overhead.
3. **EventBridge Warming Pings**: Scheduled cron invocations every 5 minutes keep containers resident in memory.
4. **AWS Graviton (arm64)**: Up to 34% better price-performance with faster boot times compared to x86_64.

> **Speaker Notes**:  
> "How do engineering teams like Freshworks and Shaadi.com mitigate cold starts? In production, critical checkout or auth paths can use Provisioned Concurrency. Non-critical paths benefit from scheduled warming pings, trimming unnecessary packages from Lambda layers, and moving to ARM64 Graviton architecture."

---

## Slide 10: Conclusion & Deliverables Checklist
- **Summary**:
  - Cold start penalty is verified at 2.32x slower (~1,270 ms vs ~548 ms).
  - Serverless is radically cheaper (< $0.01/day) for startup workloads under 3M requests/mo.
  - Zero server maintenance allows small startup teams to focus 100% on product logic.
- **Checklist Complete**:
  - [x] Live Serverless API in AWS ap-south-1
  - [x] AWS SAM & GitHub Actions CI/CD
  - [x] 500-Request Production Benchmarking & CloudWatch telemetry
  - [x] Cost Model Spreadsheet (`results/cost.xlsx`)
  - [x] Comprehensive Documentation & Architecture Diagram (`README.md`)
  - [x] Final Presentation Deck (`Cloud_Computing_Group_50_Presentation.pptx`)

> **Speaker Notes**:  
> "In conclusion, serverless provides an unmatched economic advantage for startups, provided engineering teams design around the 2.32x cold start factor. All project deliverables—including code, benchmarks, cost models, and documentation—are complete and available in our repository. Thank you!"
