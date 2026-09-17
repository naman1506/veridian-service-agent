"""Editable reportlab source for the polished architecture submission PDF."""
from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'/'Veridian_Service_Agent_Detailed_Architecture.pdf'
W,H=A4
N=HexColor('#0B1220'); B=HexColor('#2563EB'); T=HexColor('#14B8A6'); I=HexColor('#172033'); M=HexColor('#64748B'); L=HexColor('#D7E0EA'); BG=HexColor('#F5F7FB'); P=HexColor('#EDF4FF'); G=HexColor('#16805A'); A=HexColor('#B56B00'); R=HexColor('#C9372C')

def lines(s,font,size,w):
    out=[];cur=''
    for word in s.split():
        trial=(cur+' '+word).strip()
        if stringWidth(trial,font,size)<=w:cur=trial
        else:out.append(cur);cur=word
    return out+[cur] if cur else out
def para(c,x,y,s,w,size=8.2,color=I,font='Helvetica',lead=None):
    lead=lead or size*1.34;c.setFont(font,size);c.setFillColor(color)
    for row in lines(s,font,size,w):c.drawString(x,y,row);y-=lead
    return y
def rect(c,x,y,w,h,fill=white,stroke=L,r=6):
    c.setFillColor(fill);c.setStrokeColor(stroke);c.roundRect(x,y-h,w,h,r,fill=1,stroke=1)
def card(c,x,y,w,h,kicker,title,body,accent=B):
    rect(c,x,y,w,h);c.setFillColor(accent);c.roundRect(x,y-h,w,4,2,fill=1,stroke=0)
    c.setFillColor(accent);c.setFont('Helvetica-Bold',6.5);c.drawString(x+10,y-16,kicker.upper())
    c.setFillColor(I);c.setFont('Helvetica-Bold',9);c.drawString(x+10,y-30,title)
    para(c,x+10,y-44,body,w-20,6.9,M)
def arrow(c,x1,y1,x2,y2,color=B):
    c.setStrokeColor(color);c.setFillColor(color);c.setLineWidth(1.3);c.line(x1,y1,x2,y2)
    import math;a=math.atan2(y2-y1,x2-x1);d=6
    c.line(x2,y2,x2-d*math.cos(a-.42),y2-d*math.sin(a-.42));c.line(x2,y2,x2-d*math.cos(a+.42),y2-d*math.sin(a+.42))
def header(c,num,title,eyebrow):
    c.setFillColor(N);c.rect(0,H-84,W,84,fill=1,stroke=0)
    c.setFillColor(T);c.circle(48,H-42,16,fill=1,stroke=0);c.setFillColor(N);c.setFont('Helvetica-Bold',11);c.drawCentredString(48,H-46,str(num))
    c.setFillColor(HexColor('#9FB3C8'));c.setFont('Helvetica-Bold',6.6);c.drawString(78,H-24,eyebrow.upper())
    c.setFillColor(white);c.setFont('Helvetica-Bold',21);c.drawString(78,H-52,title)
    c.setFillColor(BG);c.setFont('Helvetica',7.2);c.drawRightString(W-35,H-70,'Veridian Service Agent  |  Detailed Architecture')
    c.setFillColor(M);c.setFont('Helvetica',7);c.drawRightString(W-35,18,f'{num} / 4')
def section(c,x,y,num,title,detail=''):
    c.setFillColor(B);c.circle(x+6,y-5,6,fill=1,stroke=0);c.setFillColor(white);c.setFont('Helvetica-Bold',6);c.drawCentredString(x+6,y-7,str(num))
    c.setFillColor(I);c.setFont('Helvetica-Bold',12);c.drawString(x+20,y-9,title)
    if detail:c.setFillColor(M);c.setFont('Helvetica',7.5);c.drawRightString(W-35,y-8,detail)
def table(c,x,y,cols,heads,rows,h=24,fs=7):
    total=sum(cols);rect(c,x,y,total,h*(len(rows)+1),white,L,0);c.setFillColor(N);c.rect(x,y-h,total,h,fill=1,stroke=0)
    px=x
    for i,head in enumerate(heads):c.setFillColor(white);c.setFont('Helvetica-Bold',fs);c.drawString(px+6,y-h+8,head);px+=cols[i]
    for ri,row in enumerate(rows):
        top=y-h*(ri+1); c.setStrokeColor(L);c.line(x,top-h,x+total,top-h);px=x
        for ci,val in enumerate(row):
            if ci: c.line(px,top,px,top-h)
            c.setFillColor(I);c.setFont('Helvetica',fs);ty=top-8
            for z in lines(val,'Helvetica',fs,cols[ci]-12)[:3]:c.drawString(px+6,ty,z);ty-=fs*1.15
            px+=cols[ci]
    return y-h*(len(rows)+1)

def page1(c):
    header(c,1,'System Architecture','What the running service does')
    section(c,35,735,1,'Policy-grounded internal IT decision service','FastAPI + local data + deterministic rules')
    para(c,35,710,'The service reads fixed employee requests and active tickets, retrieves local policy evidence, produces a Pydantic Decision from deterministic case rules, validates it, and records the result. Its UI is a vanilla single-page console served by FastAPI.',525,8.4)
    # Stack rail
    stack=[('PRESENTATION','static/','HTML / CSS / JS'),('SERVICE','app/main.py','FastAPI + Uvicorn'),('RETRIEVAL','retriever.py','BM25 + alias boost'),('DECISION','policy_engine.py','case-ID verdict table'),('PERSISTENCE','audit.py','JSONL + SQLite'),('DELIVERY','Docker + Render','public web service')]
    for i,(a,b,d) in enumerate(stack):card(c,35+(i%3)*175,655-(i//3)*63,160,54,a,b,d,T if i in (0,5) else B)
    section(c,35,525,2,'High-level runtime architecture','Figure 1')
    # Flow, no crossed arrows
    names=[('Operator\nconsole','static/'),('API','main.py'),('Orchestrator','run(case_id)'),('Rules','verdict(case)'),('Validate','guardrails'),('Decision','actions')]
    y=472;xs=[35,125,215,305,395,485]
    for (n,d),x in zip(names,xs):
        rect(c,x,y,75,48,P,L);c.setFillColor(I);c.setFont('Helvetica-Bold',8);c.drawCentredString(x+37,y-20,n.split('\n')[0]);
        if '\n' in n:c.drawCentredString(x+37,y-30,n.split('\n')[1])
        c.setFillColor(M);c.setFont('Helvetica',6.3);c.drawCentredString(x+37,y-41,d)
    for x in xs[:-1]:arrow(c,x+75,y-24,x+89,y-24)
    # supporting pieces
    card(c,35,382,145,56,'INPUT DATA','Requests + active tickets','ingest.cases() loads data/*.json',T)
    card(c,210,382,145,56,'EVIDENCE','Knowledge base','knowledge_base.yaml parsed as JSON',T)
    card(c,385,382,145,56,'OPTIONAL PROVIDER','LLM seam','Null/OpenAI/Anthropic classes; current implementations are no-op',T)
    arrow(c,107,382,252,424,T);arrow(c,282,382,252,424,T);arrow(c,458,438,432,448,T)
    card(c,210,300,145,56,'PERSISTENCE','Audit storage','audit/decisions.jsonl + data/veridian.db',G)
    # Evaluation callout
    rect(c,35,300,145,56,HexColor('#FFF8E8'),HexColor('#EDD79B'));c.setFillColor(A);c.setFont('Helvetica-Bold',6.5);c.drawString(45,284,'VERIFICATION');c.setFillColor(I);c.setFont('Helvetica-Bold',9);c.drawString(45,270,'Evaluation harness');para(c,45,255,'eval/run_eval.py checks 19 golden cases.',125,6.9,M)
    section(c,35,225,3,'Implemented component contracts')
    table(c,35,206,[135,190,200],['MODULE','INPUT / FUNCTION','OUTPUT'],[
        ('app/main.py','HTTP routes; StaticFiles mount','JSON API + operator console'),
        ('app/orchestrator.py','Orchestrator.run(case_id)','retrieved chunks -> final Decision'),
        ('app/retriever.py','Retriever.search(request)','top-k KB chunks with score'),
        ('app/policy_engine.py','verdict(case)','preliminary Pydantic Decision'),
        ('app/audit.py','record(case, chunks, decision)','JSONL append + SQLite upsert')],20)
    para(c,35,60,'Implementation note: classifier.py, precedent.py, and conflict_detector.py exist but are not invoked by Orchestrator.run. Their roles are not represented as runtime nodes above.',525,7.3,M)

def page2(c):
    header(c,2,'End-to-End Workflow','Actual request lifecycle')
    section(c,35,735,1,'Processing sequence','Figure 2')
    phases=[('01','INGEST','ingest.cases()','Case dictionary'),('02','RETRIEVE','Retriever.search()','KB chunks + scores'),('03','DECIDE','verdict(case)','Initial Decision'),('04','ENRICH','reasoner.enrich()','Same Decision'),('05','VALIDATE','guardrails.validate()','Final Decision'),('06','AUDIT','audit.record()','JSONL + SQLite')]
    xs=[35,125,215,305,395,485]
    for (n,t,f,o),x in zip(phases,xs):
        rect(c,x,664,75,74,white,L);c.setFillColor(B);c.setFont('Helvetica-Bold',7);c.drawString(x+8,648,n);c.setFillColor(I);c.setFont('Helvetica-Bold',8);c.drawString(x+8,630,t);c.setFillColor(M);c.setFont('Helvetica',6.4);c.drawString(x+8,614,f);c.setFont('Helvetica-Bold',6.6);c.setFillColor(T);c.drawString(x+8,594,o)
    for x in xs[:-1]:arrow(c,x+75,627,x+89,627)
    section(c,35,555,2,'Phase-by-phase contract','Purpose | input | processing | output')
    table(c,35,536,[92,90,212,131],['PHASE','INPUT','PROCESSING','OUTPUT'],[
        ('1. Case input','case_id','ingest.cases reads 15 requests plus active tickets','case dict'),
        ('2. Retrieval','case request','BM25 over KB title/text/aliases; alias bonus','chunk list + score'),
        ('3. Policy verdict','case dict','case-ID rule table; sla.py computes dates/age','Decision model'),
        ('4. Optional LLM','Decision + chunks','provider selected by LLM_PROVIDER; current providers return unchanged','same Decision'),
        ('5. Guardrails','Decision','uncited route; low confidence downgrade; conflict route','final Decision'),
        ('6. Action + audit','final Decision','action labels returned; record writes persistence','JSONL and SQLite')],39,6.8)
    section(c,35,235,3,'Design-only helpers not on the live path','Marked to avoid overstating implementation')
    for i,(n,b) in enumerate([('NORMALIZE','No call in Orchestrator.run.'),('CLASSIFY','No call in Orchestrator.run.'),('PRECEDENT','No call in Orchestrator.run.'),('CONFLICT DETECTOR','No call in Orchestrator.run.')]):
        card(c,35+(i%2)*265,196-(i//2)*60,250,48,'HELPER',n,b,A)
    para(c,35,72,'The actual pipeline is therefore retrieve -> deterministic verdict -> enrichment -> validation -> proposed action -> audit. This distinction is based on app/orchestrator.py.',525,7.5,M)

def page3(c):
    header(c,3,'Decision, Evidence and Guardrails','How unsafe outcomes are prevented')
    section(c,35,735,1,'Decision validation tree','Figure 3 - actual guardrails.validate behavior')
    # clean compact decision tree
    card(c,205,690,185,47,'START','policy_engine.verdict(case)','Initial Decision from case ID',B);arrow(c,297,643,297,620)
    card(c,205,620,185,45,'CHECK 1','Has citations?','Grounding control',T)
    arrow(c,205,598,122,574,R);card(c,35,574,150,48,'NO','ROUTE_TO_HUMAN','reason_code: no_policy_coverage',R)
    arrow(c,390,598,472,574,G);card(c,410,574,150,48,'YES','Continue','Preserve initial decision',G)
    arrow(c,485,526,485,503);card(c,410,503,150,45,'CHECK 2','Confidence < 0.75?','Confidence control',T)
    arrow(c,410,481,282,456,A);card(c,195,456,175,48,'YES','NEEDS_INFO or ROUTE','Depends on missing_fields',A)
    arrow(c,560,481,485,456,G);card(c,410,456,150,48,'NO','Check conflict','Continue validation',G)
    arrow(c,485,408,485,385);card(c,410,385,150,45,'CHECK 3','policy_conflict?','Conflict control',T)
    arrow(c,410,363,282,338,R);card(c,195,338,175,48,'YES','ROUTE_TO_HUMAN','reason_code: policy_conflict',R)
    arrow(c,560,363,485,338,G);card(c,410,338,150,48,'NO','FINAL DECISION','Return verified Decision',G)
    section(c,35,285,2,'Outcome semantics from policy_engine.verdict')
    table(c,35,266,[120,405],['OUTCOME','WHEN THE IMPLEMENTED TABLE USES IT'],[
        ('AUTO_RESOLVE','Known covered instruction or queue action: Wi-Fi, unlock, VPN renewal, archive, repair, review queue.'),
        ('NEEDS_INFO','Required evidence, approval, or account state missing; REQ-15 is downgraded for 0.42 confidence.'),
        ('ROUTE_TO_HUMAN','Policy conflict, approval boundary, or no policy coverage, such as REQ-01 and REQ-10.'),
        ('FLAG_RISK','Active security violation; REQ-08 produces containment actions.'),
        ('MONITOR','Active work is already with the correct owner and within SLA / fulfilment state.')],21,7)
    section(c,35,128,3,'Evidence and data flow','Figure 4')
    flow=[('Case','requests / tickets'),('Evidence','Retriever.search'),('Decision','verdict'),('Provider','enrich'),('Guardrails','validate'),('Audit','record')]
    xs=[35,125,215,305,395,485]
    for (a,b),x in zip(flow,xs):card(c,x,102,75,48,'FLOW',a,b,B)
    for x in xs[:-1]:arrow(c,x+75,81,x+89,81)
    para(c,35,40,'audit.record stores input, retrieved chunk IDs, reasoning trace, final Decision, and timestamp in append-only JSONL; it also upserts SQLite decisions(case_id, payload, created_at). Authority is encoded in verdict rules and owner values - not a separate guardrail function.',525,7.2,M)

def page4(c):
    header(c,4,'Implementation, API and Real Case','Code-level evidence for submission')
    section(c,35,735,1,'Repository structure','Important files only')
    table(c,35,716,[145,380],['PATH','RESPONSIBILITY'],[
        ('app/','FastAPI, Decision schema, orchestration, local retrieval, hard-coded policy rules, guardrails, audit, provider seam.'),
        ('data/','requests.json, tickets.json, knowledge_base.yaml parsed as JSON, golden_set.json, runtime SQLite database.'),
        ('static/','Single-page operator console: index.html, app.js, styles.css.'),
        ('eval/ + tests/','No-LLM 19-case golden evaluation and pytest API/engine tests.'),
        ('Dockerfile + render.yaml','Container execution and Render service configuration.')],23,7.2)
    section(c,35,545,2,'HTTP API','app/main.py')
    table(c,35,526,[70,160,295],['METHOD','ENDPOINT','PURPOSE'],[
        ('GET','/healthz','Health, frozen clock, deterministic mode.'),('GET','/api/cases and /api/kb','List case inputs or stored policy records.'),('GET','/api/cases/{id}','Run one case and return Decision; 404 if absent.'),('POST','/api/run and /api/run/{id}','Run every case or one specified case.'),('POST','/api/ask','KB-only answer; retrieval score < 3 returns not covered.'),('GET','/api/metrics and /api/audit','Calculated decision metrics; last 100 JSONL audit records.')],20,7)
    section(c,35,360,3,'Real case walkthrough: REQ-08 phishing forwarding','Input -> evidence -> rule -> guardrail -> action -> audit')
    cards=[('INPUT','Suspected phishing is being forwarded to teammates.',B),('EVIDENCE','KB-09 and active precedent TK-1048.',T),('VERDICT','FLAG_RISK; owner IT Security; confidence 0.99.',R),('VALIDATE','Citations present; no confidence or conflict override.',G),('ACTION','Issue containment instruction; preserve Security escalation.',R),('AUDIT','Record case, retrieved IDs, trace, and final Decision.',G)]
    for i,(a,b,col) in enumerate(cards):card(c,35+(i%3)*175,315-(i//3)*68,160,60,a,a.title(),b,col)
    section(c,35,165,4,'Why the final decision is safe','Implemented behavior')
    para(c,35,145,'policy_engine.verdict identifies forwarding as a KB-09 security violation and drafts containment instructions: stop forwarding, do not click links, recall/delete copies, and report Security. actions.execute only returns the action labels; it makes no external system call. audit.record preserves the final FLAG_RISK decision.',525,8)
    rect(c,35,78,525,42,HexColor('#EDF8F5'),HexColor('#A7DCCB'));c.setFillColor(G);c.setFont('Helvetica-Bold',7);c.drawString(47,64,'DEPLOYMENT');para(c,47,52,'Docker runs evaluation and batch processing before Uvicorn. Render runs app.main:app on $PORT and health-checks /healthz. render.yaml sets LLM_PROVIDER=null.',500,7.4,G)

def main():
    OUT.parent.mkdir(exist_ok=True);c=Canvas(str(OUT),pagesize=A4);c.setTitle('Veridian Service Agent - Detailed Architecture')
    for p in (page1,page2,page3,page4):p(c);c.showPage()
    c.save();print(OUT)
if __name__=='__main__':main()
