"""Editable source for Veridian_Service_Agent_Detailed_Architecture.pdf.
Content is derived from the current repository implementation, not README claims.
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "Veridian_Service_Agent_Detailed_Architecture.pdf"
W, H = A4
NAVY, BLUE, CYAN, INK, MUTED, LINE, PALE, GREEN, AMBER, RED = map(HexColor, ["#0B0D10", "#4C8DFF", "#25B7C8", "#15202B", "#667688", "#CBD5DF", "#F3F7FA", "#18794E", "#A86600", "#B42318"])

def wrap(text, font, size, width):
    words=text.split(); lines=[]; current=""
    for word in words:
        test=(current+" "+word).strip()
        if stringWidth(test,font,size)<=width: current=test
        else: lines.append(current); current=word
    if current: lines.append(current)
    return lines

def text(c, x, y, s, size=8.3, color=INK, font="Helvetica", width=None, leading=None):
    c.setFillColor(color); c.setFont(font,size); leading=leading or size*1.32
    lines=wrap(s,font,size,width) if width else s.split("\n")
    for line in lines: c.drawString(x,y,line); y-=leading
    return y

def box(c,x,y,w,h,title,body="",fill=white,accent=BLUE,small=7.1):
    c.setFillColor(fill);c.setStrokeColor(LINE);c.roundRect(x,y-h,w,h,5,fill=1,stroke=1)
    c.setFillColor(accent);c.roundRect(x,y-h,w,4,2,fill=1,stroke=0)
    c.setFillColor(INK);c.setFont("Helvetica-Bold",8);c.drawCentredString(x+w/2,y-15,title)
    if body:
        yy=y-28;c.setFont("Helvetica",small);c.setFillColor(MUTED)
        for ln in wrap(body,"Helvetica",small,w-12): c.drawCentredString(x+w/2,yy,ln);yy-=small*1.25

def arrow(c,x1,y1,x2,y2,color=BLUE):
    c.setStrokeColor(color);c.setFillColor(color);c.setLineWidth(1);c.line(x1,y1,x2,y2)
    import math
    a=math.atan2(y2-y1,x2-x1);d=6
    c.line(x2,y2,x2-d*math.cos(a-.45),y2-d*math.sin(a-.45));c.line(x2,y2,x2-d*math.cos(a+.45),y2-d*math.sin(a+.45))

def header(c,num,title,subtitle):
    c.setFillColor(NAVY);c.rect(0,H-48,W,48,fill=1,stroke=0)
    c.setFillColor(white);c.setFont("Helvetica-Bold",16);c.drawString(35,H-29,title)
    c.setFillColor(HexColor("#B8C8D8"));c.setFont("Helvetica",7.7);c.drawRightString(W-35,H-27,subtitle)
    c.setFillColor(BLUE);c.rect(35,H-55,62,3,fill=1,stroke=0)
    c.setFillColor(MUTED);c.setFont("Helvetica",7);c.drawRightString(W-35,20,f"Veridian Service Agent | Architecture Design | Page {num} of 4")

def section(c,x,y,label):
    c.setFillColor(BLUE);c.rect(x,y-3,3,14,fill=1,stroke=0);c.setFillColor(INK);c.setFont("Helvetica-Bold",11);c.drawString(x+8,y,label)

def table(c,x,y,widths,headers,rows,rowh=20,font=7.2):
    h=rowh*(len(rows)+1); full=sum(widths);c.setStrokeColor(LINE);c.setFillColor(white);c.rect(x,y-h,full,h,fill=1,stroke=1)
    c.setFillColor(NAVY);c.rect(x,y-rowh,full,rowh,fill=1,stroke=0);xx=x
    for i,hd in enumerate(headers):
        c.setFillColor(white);c.setFont("Helvetica-Bold",font);c.drawString(xx+4,y-rowh+7,hd);xx+=widths[i]
    for r,row in enumerate(rows):
        yy=y-rowh*(r+1);c.setStrokeColor(LINE);c.line(x,yy-rowh,x+full,yy-rowh);xx=x
        for i,val in enumerate(row):
            c.line(xx,yy,xx,yy-rowh); c.setFillColor(INK);c.setFont("Helvetica",font)
            lines=wrap(val,"Helvetica",font,widths[i]-8);ty=yy-7
            for ln in lines[:2]:c.drawString(xx+4,ty,ln);ty-=font*1.18
            xx+=widths[i]
    c.line(x+full,y,x+full,y-h); return y-h

def page1(c):
    header(c,1,"System Architecture","Actual implementation | FastAPI 1.0.0")
    section(c,35,760,"Purpose and stack")
    text(c,35,742,"Internal IT service desk that returns a structured, policy-grounded Decision for each fixed request or active ticket. The operator UI is static HTML/JS; FastAPI exposes processing, evidence, metrics, and audit routes.",8.2,width=525)
    y=700
    tech=[("UI","static/index.html, app.js, styles.css"),("API","FastAPI, Pydantic v2, Uvicorn"),("Retrieval","rank_bm25 BM25Okapi + alias score boost"),("Storage","SQLite stdlib + append-only JSONL"),("Quality","pytest + eval/run_eval.py"),("Deploy","Dockerfile; Render web service")]
    for i,(a,b) in enumerate(tech):
        x=35+(i%3)*175; yy=y-(i//3)*38;box(c,x,yy,160,30,a,b,PALE,CYAN,6.7)
    section(c,35,610,"Figure 1. High-level architecture")
    # top main path
    labels=[("Operator UI","static/"),("FastAPI API","app/main.py"),("Orchestrator","run(case_id)"),("Deterministic verdict","policy_engine.py"),("Guardrails","guardrails.py"),("Decision + action","models/actions")]
    xs=[35,126,217,308,399,490]
    for (a,b),x in zip(labels,xs): box(c,x,565,78,45,a,b,white,BLUE,6.2)
    for x in xs[:-1]: arrow(c,x+78,542,x+89,542)
    # dependencies
    box(c,112,480,115,44,"Knowledge base","data/knowledge_base.yaml\nrequests + tickets",PALE,CYAN,6.5);arrow(c,170,524,255,565)
    box(c,247,480,115,44,"Retriever","Retriever.search\nBM25 + aliases",PALE,CYAN,6.5);arrow(c,304,524,256,565)
    box(c,382,480,115,44,"LLM provider seam","Null/OpenAI/Anthropic\ncurrently no-op",PALE,CYAN,6.5);arrow(c,440,524,438,565)
    box(c,430,405,130,44,"Audit storage","audit/decisions.jsonl\ndata/veridian.db",PALE,GREEN,6.5);arrow(c,528,519,495,449,GREEN)
    box(c,40,405,135,44,"Evaluation","eval/run_eval.py\n19-case golden set",PALE,AMBER,6.5);arrow(c,107,449,260,480,AMBER)
    text(c,35,365,"Actual orchestration order: retrieve -> verdict -> enrich -> validate -> execute -> record. The code does not call normalize, classify, precedent.lookup, or conflict_detector.hardware_conflict in this path.",7.6,color=MUTED,width=520)
    section(c,35,325,"Component responsibilities")
    table(c,35,307,[130,205,190],["Component", "Actual function / input", "Output / dependency"],[
        ("app/main.py","HTTP routes; StaticFiles mount","JSON Decision / HTML UI"),("app/orchestrator.py","Orchestrator.run(case_id)","retrieved chunks, final Decision"),("app/policy_engine.py","verdict(case) lookup table","preliminary Pydantic Decision"),("app/reasoner.py","enrich(decision, chunks)","retains deterministic outcome"),("app/audit.py","record(case, chunks, decision)","JSONL entry + SQLite upsert")],22)

def page2(c):
    header(c,2,"End-to-End Workflow","Actual runtime path and unused helper boundaries")
    section(c,35,760,"Figure 2. Processing pipeline")
    steps=[("1 Ingest","ingest.cases"),("2 Retrieve","Retriever.search"),("3 Verdict","policy_engine.verdict"),("4 Enrich","reasoner.enrich"),("5 Validate","guardrails.validate"),("6 Execute + audit","actions / audit")]
    xs=[35,124,213,302,391,480]
    for (a,b),x in zip(steps,xs):box(c,x,715,76,42,a,b,white,BLUE,6); 
    for x in xs[:-1]:arrow(c,x+76,694,x+88,694)
    text(c,35,648,"Sequence: POST /api/run/{id} or GET /api/cases/{id} -> Orchestrator.run -> evidence retrieval -> deterministic decision -> optional no-op enrichment -> validation -> proposed actions -> audit persistence.",7.7,color=MUTED,width=520)
    section(c,35,615,"Implemented phases")
    rows=[
      ("1. Case input","case_id","ingest.cases() reads 15 requests plus active tickets","dict with request text and status"),
      ("2. Retrieve","case['request']","BM25 top-k against KB text/title/aliases; alias bonus","list[dict] chunks + score"),
      ("3. Deterministic verdict","case dict","policy_engine.verdict selects a hard-coded case rule; SLA helpers calculate date/age","Decision model"),
      ("4. Optional LLM","Decision + chunks","reasoner calls selected provider. NullProvider returns unchanged; OpenAI/Anthropic inherit it","same Decision"),
      ("5. Guardrails","Decision","uncited -> route; confidence < .75 -> downgrade; conflict -> route","final Decision"),
      ("6. Proposed action + audit","final Decision","actions.execute returns action labels; audit.record appends and upserts","JSONL + SQLite")]
    table(c,35,597,[75,84,245,121],["Phase", "Input", "Processing", "Output"],rows,38,6.6)
    section(c,35,298,"Important code-vs-design distinction")
    text(c,35,280,"The repository includes classifier.py (classify), precedent.py (lookup), and conflict_detector.py (hardware_conflict). None is called by Orchestrator.run. Normalization is also not implemented as a function. Their stated pipeline roles are therefore proposed/design-only rather than runtime phases.",8,width=520)
    section(c,35,225,"Relevant dependencies")
    table(c,35,207,[145,190,190],["Dependency", "Used by", "Role"],[
      ("fastapi / uvicorn","main.py","API and static UI serving"),("pydantic","models.py","validated Decision schema"),("rank-bm25","retriever.py","local evidence ranking"),("sqlite3 (stdlib)","audit.py","decision persistence"),("pytest / httpx","tests/","API and logic verification")],21,7)

def page3(c):
    header(c,3,"Decision, Data and Guardrails","What produces and constrains a final Decision")
    section(c,35,760,"Figure 3. Decision tree - actual final validation behavior")
    box(c,212,720,170,38,"policy_engine.verdict(case)","Initial Decision from case-ID rule table",white,BLUE,7)
    arrow(c,297,682,297,654);box(c,212,654,170,38,"Has citations?","guardrails.validate",PALE,CYAN,7)
    arrow(c,212,635,120,610,RED);box(c,35,610,150,38,"No","ROUTE_TO_HUMAN\nno_policy_coverage",PALE,RED,7)
    arrow(c,382,635,470,610,GREEN);box(c,410,610,150,38,"Yes","Continue validation",PALE,GREEN,7)
    arrow(c,485,572,485,544);box(c,410,544,150,38,"confidence < 0.75?","needs fields decides target",PALE,CYAN,7)
    arrow(c,410,525,285,500,AMBER);box(c,195,500,180,38,"Yes","NEEDS_INFO if fields;\notherwise ROUTE_TO_HUMAN",PALE,AMBER,7)
    arrow(c,560,525,485,500,GREEN);box(c,410,500,150,38,"No","preserve decision",PALE,GREEN,7)
    arrow(c,485,462,485,434);box(c,410,434,150,38,"policy_conflict?","Conflict override",PALE,CYAN,7)
    arrow(c,410,415,290,390,RED);box(c,195,390,180,38,"Yes","ROUTE_TO_HUMAN\npolicy_conflict",PALE,RED,7)
    arrow(c,560,415,485,390,GREEN);box(c,410,390,150,38,"No","final Decision",PALE,GREEN,7)
    section(c,35,345,"Implemented outcome values")
    table(c,35,327,[105,420],["Outcome", "Actual use in policy_engine.verdict"],[
      ("AUTO_RESOLVE","Known covered instruction or queue action, e.g. guest Wi-Fi, manual unlock, VPN renewal, archive, repair, or Security review queue."),
      ("NEEDS_INFO","Required field/approval/account evidence missing; low confidence case REQ-15 remains NEEDS_INFO after guardrail."),
      ("ROUTE_TO_HUMAN","Policy conflict, missing authority, or no policy coverage; REQ-01 and REQ-10 are examples."),
      ("FLAG_RISK","Active security violation; REQ-08 produces immediate phishing containment instructions."),
      ("MONITOR","Active case already with appropriate owner and within defined SLA / fulfilment status.")],25,7)
    section(c,35,181,"Figure 4. Data flow and guardrail controls")
    labels=["Case", "Retrieved evidence", "Policy Decision", "Optional LLM", "Guardrails", "Final Decision", "Audit"]
    xs=[35,108,192,276,360,444,528]
    for lab,x in zip(labels,xs): box(c,x,140,64,32,lab,"",white,BLUE,6.3)
    for x in xs[:-1]:arrow(c,x+64,124,x+72,124)
    text(c,35,91,"Storage: audit.record writes JSONL (append-only) and SQLite decisions(case_id PRIMARY KEY, payload, created_at). Guardrails implemented in code: grounding, confidence, conflict, and audit. There is no separate authority guard function; authority is encoded in verdict rules and owner values.",7.5,color=MUTED,width=520)

def page4(c):
    header(c,4,"Implementation, API and Case Example","Repository evidence: REQ-08 phishing containment")
    section(c,35,760,"A. Important project structure")
    table(c,35,742,[135,390],["Path", "Actual responsibility"],[
      ("app/","FastAPI app, models, orchestration, rule engine, retrieval, audit, LLM provider seam."),("data/","knowledge_base.yaml stored as JSON; requests/tickets; golden_set; SQLite created at runtime."),("static/","Single-page operator console: HTML, CSS, JavaScript."),("eval/ and tests/","No-LLM golden-set evaluation; pytest engine and API checks."),("scripts/ and docs/","Asset/deck/PDF generators and submitted images/deck."),("Dockerfile, render.yaml","Container startup and Render web-service configuration.")],21,7.1)
    section(c,35,588,"B. Actual API")
    table(c,35,570,[88,142,295],["Method", "Path", "Purpose"],[
      ("GET","/healthz","Returns ok, frozen clock, deterministic mode."),("GET","/api/cases","Returns active case inputs."),("GET","/api/kb","Returns locally stored policy records."),("GET","/api/cases/{id}","Processes one case and returns Decision; 404 if absent."),("POST","/api/run and /api/run/{id}","Processes all cases or a specified case."),("POST","/api/ask","KB-only answer; score < 3 returns not covered by policy."),("GET","/api/metrics and /api/audit","Runs metric decisions; returns last 100 audit JSONL rows.")],21,7)
    section(c,35,388,"C. Real walkthrough: REQ-08")
    text(c,35,369,"Input: Ananya Reddy reports a suspected phishing email and says it is being forwarded to teammates. The case is read from data/requests.json; actual runtime classification is embedded as category='security' in policy_engine.verdict, not produced by classifier.py.",8,width=520)
    stages=[("Evidence","KB-09, TK-1048"),("Rule logic","Forwarding violates KB-09"),("Initial decision","FLAG_RISK, owner IT Security"),("Guardrails","Citations exist; 0.99 confidence; no conflict override"),("Action","Issue containment instruction; preserve Security escalation"),("Audit","Case + retrieved IDs + trace + Decision to JSONL/SQLite")]
    for i,(a,b) in enumerate(stages):
        x=35+(i%3)*175;yy=315-(i//3)*58;box(c,x,yy,160,47,a,b,PALE,RED if i in (1,2) else BLUE,6.8)
    section(c,35,181,"Why this final decision is safe")
    text(c,35,163,"The deterministic table selects the incident response. The draft reply tells the employee to stop forwarding, do not click links, recall/delete copies, and report Security. The action remains proposed only: actions.execute returns labels and does not call external systems. The final audited decision is FLAG_RISK.",8,width=520)
    text(c,35,101,"Deployment verification: Docker runs evaluation and batch processing before Uvicorn. Render is configured to run uvicorn app.main:app on $PORT with /healthz as the health endpoint. LLM_PROVIDER is configured as null in render.yaml.",7.6,color=MUTED,width=520)

def main():
    OUT.parent.mkdir(exist_ok=True); c=canvas.Canvas(str(OUT),pagesize=A4)
    c.setTitle("Veridian Service Agent - Detailed Architecture")
    for render in (page1,page2,page3,page4): render(c);c.showPage()
    c.save();print(OUT)
if __name__ == "__main__": main()
