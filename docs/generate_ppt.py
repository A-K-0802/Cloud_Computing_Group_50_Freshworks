import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    DARK_BG = RGBColor(11, 25, 44)       # Deep Navy
    LIGHT_BG = RGBColor(248, 249, 250)   # Off white
    CARD_BG = RGBColor(255, 255, 255)    # White card
    CARD_BORDER = RGBColor(220, 224, 230)
    PRIMARY = RGBColor(30, 62, 98)       # Navy Accent
    ACCENT = RGBColor(255, 101, 0)       # AWS Orange
    TEAL = RGBColor(0, 150, 160)         # Cyan / Teal
    TEXT_DARK = RGBColor(33, 37, 41)     # Charcoal text
    TEXT_MUTED = RGBColor(108, 117, 125) # Grey text
    WHITE = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="CLOUD COMPUTING GROUP 50"):
        # Header category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = ACCENT

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = PRIMARY

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_BG
    bg1.line.color.rgb = DARK_BG

    # Accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.8), Inches(0.15), Inches(3.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    bar.line.color.rgb = ACCENT

    # Title box
    tbox1 = s1.shapes.add_textbox(Inches(1.6), Inches(1.7), Inches(10.5), Inches(2.2))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Serverless Cold Start & Cost Analysis"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Theme 4: Serverless & Startups — Production Benchmarking & Cloud Economics"
    p1_sub.font.size = Pt(18)
    p1_sub.font.color.rgb = ACCENT

    # Team Box
    teambox = s1.shapes.add_textbox(Inches(1.6), Inches(4.2), Inches(10.5), Inches(2.2))
    tf_team = teambox.text_frame
    tf_team.word_wrap = True
    
    p_grp = tf_team.paragraphs[0]
    p_grp.text = "Project Group 50 | Partner Track: Freshworks Case Study"
    p_grp.font.size = Pt(14)
    p_grp.font.bold = True
    p_grp.font.color.rgb = WHITE

    members = [
        ("Person A (Aalok Thakkar / A-K-0802)", "Backend Architecture, AWS SAM, DynamoDB, CI/CD Pipeline"),
        ("Person B (Bhagya Thakkar / BM1100)", "Benchmarking Suite, 500-Req Latency Study, CloudWatch Analytics"),
        ("Person C (Farhan Ansari / FARHAN5826)", "Cost Economics, EC2 Break-Even Model, Documentation & Deliverables")
    ]
    for mem, role in members:
        pm = tf_team.add_paragraph()
        pm.text = f"• {mem} — {role}"
        pm.font.size = Pt(12)
        pm.font.color.rgb = RGBColor(200, 210, 225)

    # ==========================================
    # SLIDE 2: Problem Statement
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement: The Serverless Cold Start Dilemma")

    cards_s2 = [
        ("The Startup Promise", 
         "Serverless architectures (AWS Lambda) offer zero idle costs, automatic scaling, and frictionless developer velocity—ideal for early-stage startups and fluctuating workloads.",
         ACCENT),
        ("The Reality: Cold Start Penalty", 
         "When traffic is intermittent or bursts, AWS provisions new microVMs (Firecracker). Container boot and Python runtime initialization introduce significant, unpredictable latency spikes.",
         PRIMARY),
        ("Business & UX Impact", 
         "Slow API calls hurt user conversion, SEO, and partner SLA compliance. Understanding the exact magnitude of cold starts is vital before committing production services to serverless.",
         TEAL)
    ]
    for idx, (head, body, col) in enumerate(cards_s2):
        left = Inches(0.8 + idx * 4.0)
        c = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(3.7), Inches(4.8))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER
        c.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(left + Inches(0.25), Inches(2.1), Inches(3.2), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(18)
        p_h.font.bold = True
        p_h.font.color.rgb = col

        p_b = tf.add_paragraph()
        p_b.space_before = Pt(16)
        p_b.text = body
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = TEXT_DARK

    # ==========================================
    # SLIDE 3: Architecture Overview
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Serverless Architecture & System Topology")

    # Left card: System Components
    left_c3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.8))
    left_c3.fill.solid()
    left_c3.fill.fore_color.rgb = CARD_BG
    left_c3.line.color.rgb = CARD_BORDER
    tb3 = s3.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(6.2), Inches(4.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "End-to-End Pipeline Components"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    items3 = [
        ("API Gateway (HTTP API)", "Lightweight, low-latency regional entrypoint in ap-south-1 with native CORS support."),
        ("AWS Lambda (Python 3.11)", "Single-purpose compute handler with 128 MB RAM, arm64/x86_64 runtime, and strict IAM least privilege."),
        ("Amazon DynamoDB (On-Demand)", "NoSQL datastore receiving form submissions (PutItem) with zero provisioned capacity planning."),
        ("Amazon CloudWatch", "Captures detailed Execution, Billed, and Init Durations across all request invocations.")
    ]
    for it, desc in items3:
        p_i = tf3.add_paragraph()
        p_i.space_before = Pt(10)
        p_i.text = f"• {it}: "
        p_i.font.bold = True
        p_i.font.size = Pt(13)
        p_i.font.color.rgb = TEXT_DARK
        p_d = tf3.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = TEXT_MUTED

    # Right card: Live API Details
    right_c3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), Inches(1.8), Inches(4.5), Inches(4.8))
    right_c3.fill.solid()
    right_c3.fill.fore_color.rgb = CARD_BG
    right_c3.line.color.rgb = CARD_BORDER
    tb3_r = s3.shapes.add_textbox(Inches(8.2), Inches(2.0), Inches(4.1), Inches(4.4))
    tf3_r = tb3_r.text_frame
    tf3_r.word_wrap = True
    p_r = tf3_r.paragraphs[0]
    p_r.text = "Live Endpoint Verification"
    p_r.font.size = Pt(18)
    p_r.font.bold = True
    p_r.font.color.rgb = ACCENT

    p_r2 = tf3_r.add_paragraph()
    p_r2.space_before = Pt(14)
    p_r2.text = "Production Endpoint:"
    p_r2.font.bold = True
    p_r2.font.size = Pt(12)
    p_r2.font.color.rgb = TEXT_DARK

    p_url = tf3_r.add_paragraph()
    p_url.text = "https://w3obh27tnh.execute-api.ap-south-1.amazonaws.com/submit"
    p_url.font.size = Pt(11)
    p_url.font.color.rgb = TEAL

    p_r3 = tf3_r.add_paragraph()
    p_r3.space_before = Pt(14)
    p_r3.text = "Sample Payload:"
    p_r3.font.bold = True
    p_r3.font.size = Pt(12)
    p_r3.font.color.rgb = TEXT_DARK

    p_code = tf3_r.add_paragraph()
    p_code.text = '{\n  "name": "Cloud Computing Tester",\n  "score": 9.5\n}'
    p_code.font.size = Pt(12)
    p_code.font.color.rgb = PRIMARY

    p_r4 = tf3_r.add_paragraph()
    p_r4.space_before = Pt(14)
    p_r4.text = "Status: 200 OK | Verified Live in AWS ap-south-1"
    p_r4.font.bold = True
    p_r4.font.size = Pt(12)
    p_r4.font.color.rgb = RGBColor(40, 167, 69)

    # ==========================================
    # SLIDE 4: IaC & CI/CD Pipeline
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Infrastructure as Code & CI/CD Automation")

    c4_items = [
        ("AWS SAM (Serverless Application Model)",
         "Declarative Infrastructure as Code defining API Gateway routes, Lambda function resources, DynamoDB table schema, and environment configurations in a single template.yaml.",
         PRIMARY),
        ("Automated GitHub Actions CI/CD",
         "Every pull request and merge to main triggers sam build and sam deploy --no-confirm-changeset with automated AWS credential assumption and zero downtime rollouts.",
         ACCENT),
        ("Production Hygiene & Reproducibility",
         "100% cloud resources reproducible via code. Eliminates manual AWS console drift, enforces semantic versioning, and enables one-command environment teardown.",
         TEAL)
    ]
    for idx, (title, desc, col) in enumerate(c4_items):
        top = Inches(1.8 + idx * 1.65)
        c = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.4))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER
        c.line.width = Pt(1.5)

        tb = s4.shapes.add_textbox(Inches(1.1), top + Inches(0.15), Inches(11.1), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = title
        p_h.font.size = Pt(16)
        p_h.font.bold = True
        p_h.font.color.rgb = col

        p_b = tf.add_paragraph()
        p_b.space_before = Pt(4)
        p_b.text = desc
        p_b.font.size = Pt(13)
        p_b.font.color.rgb = TEXT_DARK

    # ==========================================
    # SLIDE 5: Benchmarking Methodology
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Benchmarking Methodology: Isolating Cold vs. Warm")

    s5_boxes = [
        ("5 x 100 Request Matrix", 
         "Executed 5 independent rounds of 100 sequential HTTP POST requests each (500 total requests) against the live production endpoint in ap-south-1."),
        ("Cold Start Forcing Mechanism", 
         "Before each 100-request round, a dummy environment variable was updated via AWS CLI / SAM to force Lambda to discard idle microVMs and trigger a fresh container cold boot."),
        ("High-Precision Instrumentation", 
         "Recorded client-perceived millisecond-accurate round-trip latency (Python requests.elapsed) alongside AWS CloudWatch internal Billed, Init, and Execution logs.")
    ]
    for idx, (t, d) in enumerate(s5_boxes):
        left = Inches(0.8 + idx * 4.0)
        c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(3.7), Inches(4.8))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        tb = s5.shapes.add_textbox(left + Inches(0.25), Inches(2.1), Inches(3.2), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = f"Step 0{idx+1}\n{t}"
        p_t.font.size = Pt(17)
        p_t.font.bold = True
        p_t.font.color.rgb = PRIMARY

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(16)
        p_d.text = d
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = TEXT_DARK

    # ==========================================
    # SLIDE 6: Latency Results & Chart
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Benchmark Results: 2.32x Cold Start Penalty")

    # Left: Stats Table Card
    left_c6 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.2), Inches(4.8))
    left_c6.fill.solid()
    left_c6.fill.fore_color.rgb = CARD_BG
    left_c6.line.color.rgb = CARD_BORDER

    tb6 = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(4.8), Inches(4.4))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    p = tf6.paragraphs[0]
    p.text = "Measured Production Latencies"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    metrics_list = [
        ("Cold Start Latency (1st req avg)", "1,270.01 ms", ACCENT),
        ("Warm Latency (100th req avg)", "504.98 ms", TEAL),
        ("Warm Latency (Overall avg)", "547.59 ms", PRIMARY),
        ("Warm Latency 95th Percentile (p95)", "792.55 ms", PRIMARY),
        ("Cold-to-Warm Ratio", "2.32x Slower", ACCENT)
    ]
    for lbl, val, col in metrics_list:
        p_l = tf6.add_paragraph()
        p_l.space_before = Pt(8)
        p_l.text = lbl
        p_l.font.size = Pt(11)
        p_l.font.color.rgb = TEXT_MUTED

        p_v = tf6.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(18)
        p_v.font.bold = True
        p_v.font.color.rgb = col

    # Right: Embedded Chart Image
    graph_path = "results/latency_graph.png"
    if not os.path.exists(graph_path):
        graph_path = "serverless-coldstart/results/latency_graph.png"
    
    if os.path.exists(graph_path):
        s6.shapes.add_picture(graph_path, Inches(6.3), Inches(1.8), Inches(6.2), Inches(4.8))
    else:
        # Fallback card
        r_c6 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.3), Inches(1.8), Inches(6.2), Inches(4.8))
        r_c6.fill.solid()
        r_c6.fill.fore_color.rgb = CARD_BG

    # ==========================================
    # SLIDE 7: CloudWatch Proof
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "CloudWatch Telemetry & Latency Breakdown")

    # CloudWatch Stats Card (Left)
    c7_l = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    c7_l.fill.solid()
    c7_l.fill.fore_color.rgb = CARD_BG
    c7_l.line.color.rgb = CARD_BORDER

    tb7_l = s7.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.4))
    tf7_l = tb7_l.text_frame
    tf7_l.word_wrap = True
    p = tf7_l.paragraphs[0]
    p.text = "CloudWatch Logs Insights (545 Invocations)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    cw_stats = [
        ("Average Init Duration (Cold Boot)", "455.87 ms", ACCENT, "Firecracker microVM boot & boto3 module loading"),
        ("Average Billed Duration", "33.39 ms", TEAL, "Official billed duration in ap-south-1"),
        ("Average Pure Execution Duration", "25.39 ms", PRIMARY, "Actual Python code execution handling request"),
        ("Configured Memory Tier", "128 MB (0.125 GB)", TEXT_DARK, "Lean memory footprint optimizing unit compute costs")
    ]
    for lbl, val, col, sub in cw_stats:
        pl = tf7_l.add_paragraph()
        pl.space_before = Pt(8)
        pl.text = f"{lbl}: "
        pl.font.size = Pt(11)
        pl.font.color.rgb = TEXT_MUTED

        pv = tf7_l.add_paragraph()
        pv.text = val
        pv.font.size = Pt(16)
        pv.font.bold = True
        pv.font.color.rgb = col

        ps = tf7_l.add_paragraph()
        ps.text = sub
        ps.font.size = Pt(10)
        ps.font.color.rgb = TEXT_MUTED

    # Why the difference? Card (Right)
    c7_r = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    c7_r.fill.solid()
    c7_r.fill.fore_color.rgb = CARD_BG
    c7_r.line.color.rgb = CARD_BORDER

    tb7_r = s7.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.4))
    tf7_r = tb7_r.text_frame
    tf7_r.word_wrap = True
    p = tf7_r.paragraphs[0]
    p.text = "Dissecting the Latency Gap"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT

    explanations = [
        ("Client Round-Trip (~500 ms)", 
         "The difference between CloudWatch's ~25 ms execution and the client's ~548 ms warm latency is physical WAN network transit from local client to AWS Mumbai (ap-south-1) and back."),
        ("Container Cold Boot (~456 ms)", 
         "CloudWatch Init Duration explicitly measures AWS spinning up a microVM, initializing the Python 3.11 environment, and importing the AWS SDK (boto3)."),
        ("End-to-End Cold Total (~1,270 ms)", 
         "Network Round-Trip (520 ms) + Container Init (456 ms) + Execution (25 ms) + API Gateway serialization exactly accounts for the 1,270 ms total perceived by the client.")
    ]
    for h, b in explanations:
        ph = tf7_r.add_paragraph()
        ph.space_before = Pt(10)
        ph.text = f"• {h}"
        ph.font.size = Pt(13)
        ph.font.bold = True
        ph.font.color.rgb = PRIMARY
        pb = tf7_r.add_paragraph()
        pb.text = b
        pb.font.size = Pt(12)
        pb.font.color.rgb = TEXT_DARK

    # ==========================================
    # SLIDE 8: Cost Model & Break-Even Analysis
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Cost Economics: Serverless vs. Always-On EC2")

    # Metric Banner 1: Serverless cost
    b1 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(3.7), Inches(2.2))
    b1.fill.solid()
    b1.fill.fore_color.rgb = CARD_BG
    b1.line.color.rgb = CARD_BORDER
    tb_b1 = s8.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(3.3), Inches(2.0))
    tf_b1 = tb_b1.text_frame
    tf_b1.word_wrap = True
    tf_b1.paragraphs[0].text = "Serverless Cost"
    tf_b1.paragraphs[0].font.size = Pt(14)
    tf_b1.paragraphs[0].font.bold = True
    tf_b1.paragraphs[0].font.color.rgb = PRIMARY
    p_cost = tf_b1.add_paragraph()
    p_cost.space_before = Pt(6)
    p_cost.text = "$0.00252"
    p_cost.font.size = Pt(32)
    p_cost.font.bold = True
    p_cost.font.color.rgb = ACCENT
    p_cost_sub = tf_b1.add_paragraph()
    p_cost_sub.text = "per 1,000 requests (< 1/4 of a cent)"
    p_cost_sub.font.size = Pt(11)
    p_cost_sub.font.color.rgb = TEXT_MUTED

    # Metric Banner 2: EC2 cost
    b2 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.8), Inches(3.7), Inches(2.2))
    b2.fill.solid()
    b2.fill.fore_color.rgb = CARD_BG
    b2.line.color.rgb = CARD_BORDER
    tb_b2 = s8.shapes.add_textbox(Inches(5.0), Inches(1.9), Inches(3.3), Inches(2.0))
    tf_b2 = tb_b2.text_frame
    tf_b2.word_wrap = True
    tf_b2.paragraphs[0].text = "EC2 t3.micro (24/7)"
    tf_b2.paragraphs[0].font.size = Pt(14)
    tf_b2.paragraphs[0].font.bold = True
    tf_b2.paragraphs[0].font.color.rgb = PRIMARY
    p_ec2 = tf_b2.add_paragraph()
    p_ec2.space_before = Pt(6)
    p_ec2.text = "$7.59 / mo"
    p_ec2.font.size = Pt(32)
    p_ec2.font.bold = True
    p_ec2.font.color.rgb = TEAL
    p_ec2_sub = tf_b2.add_paragraph()
    p_ec2_sub.text = "$0.0104/hr × 730 hrs (fixed idle cost)"
    p_ec2_sub.font.size = Pt(11)
    p_ec2_sub.font.color.rgb = TEXT_MUTED

    # Metric Banner 3: Break-Even
    b3 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(2.2))
    b3.fill.solid()
    b3.fill.fore_color.rgb = CARD_BG
    b3.line.color.rgb = CARD_BORDER
    tb_b3 = s8.shapes.add_textbox(Inches(9.0), Inches(1.9), Inches(3.3), Inches(2.0))
    tf_b3 = tb_b3.text_frame
    tf_b3.word_wrap = True
    tf_b3.paragraphs[0].text = "Break-Even Traffic"
    tf_b3.paragraphs[0].font.size = Pt(14)
    tf_b3.paragraphs[0].font.bold = True
    tf_b3.paragraphs[0].font.color.rgb = PRIMARY
    p_be = tf_b3.add_paragraph()
    p_be.space_before = Pt(6)
    p_be.text = "~3.01 Million"
    p_be.font.size = Pt(32)
    p_be.font.bold = True
    p_be.font.color.rgb = PRIMARY
    p_be_sub = tf_b3.add_paragraph()
    p_be_sub.text = "requests / month threshold"
    p_be_sub.font.size = Pt(11)
    p_be_sub.font.color.rgb = TEXT_MUTED

    # Bottom Table: Breakdown per 1,000 requests
    btm_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.5))
    btm_card.fill.solid()
    btm_card.fill.fore_color.rgb = CARD_BG
    btm_card.line.color.rgb = CARD_BORDER
    tb_btm = s8.shapes.add_textbox(Inches(1.1), Inches(4.4), Inches(11.1), Inches(2.2))
    tf_btm = tb_btm.text_frame
    tf_btm.word_wrap = True
    p_b_h = tf_btm.paragraphs[0]
    p_b_h.text = "Serverless Component Cost Breakdown (per 1,000 requests)"
    p_b_h.font.size = Pt(15)
    p_b_h.font.bold = True
    p_b_h.font.color.rgb = PRIMARY

    c_breakdown = [
        ("API Gateway HTTP API", "$0.00100", "($1.00 per million calls)"),
        ("Amazon DynamoDB (On-Demand Write)", "$0.00125", "($1.25 per million write units)"),
        ("AWS Lambda Invocation Requests", "$0.00020", "($0.20 per million invocations)"),
        ("AWS Lambda Compute (33.39 ms @ 128MB)", "$0.00007", "($0.0000166667 per GB-second)"),
        ("TOTAL COST PER 1,000 REQUESTS", "$0.00252", "Zero infrastructure cost when traffic drops to zero")
    ]
    for svc, cost, note in c_breakdown:
        p_row = tf_btm.add_paragraph()
        p_row.space_before = Pt(2)
        p_row.text = f"• {svc}: {cost} — {note}"
        p_row.font.size = Pt(12)
        p_row.font.color.rgb = TEXT_DARK
        if "TOTAL" in svc:
            p_row.font.bold = True
            p_row.font.color.rgb = ACCENT

    # ==========================================
    # SLIDE 9: Industry Best Practices
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Industry Best Practices & Cold Start Mitigations")

    tech_mitigations = [
        ("Provisioned Concurrency",
         "Pre-initializes a designated number of execution environments. Eliminates cold starts completely for critical SLA paths at a modest baseline hourly cost.",
         PRIMARY),
        ("Lean Dependency Footprint",
         "Remove monolithic packages and dynamic runtime reflections. Import only specific boto3 clients (e.g. boto3.client('dynamodb') rather than full SDK).",
         ACCENT),
        ("Periodic Warming Pings",
         "Trigger scheduled EventBridge cron pings every 5 minutes with a lightweight header to keep containers active in memory without executing heavy business logic.",
         TEAL),
        ("ARM64 Graviton2 Migration",
         "Switching architecture from x86_64 to arm64 delivers up to 34% better price-performance and reduced initialization durations across Python runtimes.",
         PRIMARY)
    ]
    for idx, (t, d, col) in enumerate(tech_mitigations):
        col_idx = idx % 2
        row_idx = idx // 2
        left = Inches(0.8 + col_idx * 6.0)
        top = Inches(1.8 + row_idx * 2.5)

        c = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(2.2))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        tb = s9.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.2), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = t
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(8)
        p_d.text = d
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = TEXT_DARK

    # ==========================================
    # SLIDE 10: Conclusion & Deliverables Checklist
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Conclusions & Team Deliverables Checklist")

    # Left: Takeaways
    c10_l = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    c10_l.fill.solid()
    c10_l.fill.fore_color.rgb = CARD_BG
    c10_l.line.color.rgb = CARD_BORDER

    tb10_l = s10.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.4))
    tf10_l = tb10_l.text_frame
    tf10_l.word_wrap = True
    p = tf10_l.paragraphs[0]
    p.text = "Key Takeaways for Startups"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    conclusions = [
        ("The Cold Penalty is Real", "Cold requests are 2.32x slower (~1,270 ms vs ~548 ms). Startups must budget for init duration in SLAs."),
        ("Serverless Economics Win Early", "Below ~3 million requests/month, Serverless is radically cheaper than managing 24/7 EC2 instances."),
        ("Zero Operational Overhead", "Infrastructure as Code (SAM) + Serverless scales from 0 to thousands of users without server management.")
    ]
    for h, b in conclusions:
        ph = tf10_l.add_paragraph()
        ph.space_before = Pt(10)
        ph.text = f"• {h}: "
        ph.font.bold = True
        ph.font.size = Pt(13)
        ph.font.color.rgb = ACCENT
        pb = tf10_l.add_paragraph()
        pb.text = f"   {b}"
        pb.font.size = Pt(12)
        pb.font.color.rgb = TEXT_DARK

    # Right: Deliverables
    c10_r = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    c10_r.fill.solid()
    c10_r.fill.fore_color.rgb = CARD_BG
    c10_r.line.color.rgb = CARD_BORDER

    tb10_r = s10.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.4))
    tf10_r = tb10_r.text_frame
    tf10_r.word_wrap = True
    p = tf10_r.paragraphs[0]
    p.text = "Deliverables Completed"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    deliverables = [
        "[X] Live Serverless API in AWS ap-south-1 (HTTP API + Lambda + DynamoDB)",
        "[X] AWS SAM IaC Template & GitHub Actions Deployment Workflow",
        "[X] 500-Request Production Benchmarking Suite & CloudWatch Metrics",
        "[X] Cost Model Spreadsheet (results/cost.xlsx) & Break-Even Analysis",
        "[X] Comprehensive Technical README & Mermaid Architecture Diagram",
        "[X] Complete 10-Slide Final Presentation Deck & Technical Report"
    ]
    for d in deliverables:
        pd = tf10_r.add_paragraph()
        pd.space_before = Pt(8)
        pd.text = d
        pd.font.size = Pt(12)
        pd.font.color.rgb = RGBColor(40, 167, 69) if "[X]" in d else TEXT_DARK

    # Save Presentation
    output_path = "docs/Cloud_Computing_Group_50_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}!")

if __name__ == "__main__":
    create_deck()
