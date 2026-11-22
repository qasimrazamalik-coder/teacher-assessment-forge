#!/usr/bin/env python3
import argparse, collections, json, re
CONFIG={"name": "teacher-assessment-forge", "kind": "schedule", "root": "items", "fields": ["id", "priority", "effort", "channel"]}

def num(v, default=0.0):
    try: return float(v)
    except (TypeError,ValueError): return default

def audit(d):
    out=[]
    weights={"critical":1.0,"high":.8,"medium":.5,"low":.2}
    for i,x in enumerate(d.get(CONFIG["root"],[])):
        sev=str(x.get("severity","medium")).lower(); reach=min(1,num(x.get("users_affected"))/1000); conf=num(x.get("confidence"),.5)
        score=round(100*(weights.get(sev,.5)*.55+reach*.25+conf*.2),1)
        out.append({"id":x.get("id") or x.get("tool") or x.get("claim") or x.get("screen") or x.get("cell") or x.get("animation") or i,"priority_score":score,"severity":sev,"requires_human_review":sev in {"critical","high"}})
    return {"skill":CONFIG["name"],"prioritized_findings":sorted(out,key=lambda x:-x["priority_score"]),"decision":"review" if out else "no-findings"}

def rank(d):
    rows=[]
    for i,x in enumerate(d.get(CONFIG["root"],[])):
        score=round(100*(num(x.get("impact"))*.45+num(x.get("confidence"))*.3+num(x.get("urgency"))*.25),1)
        rows.append({"id":x.get("id",i),"score":score,"evidence":x.get("evidence"),"qualified":bool(x.get("evidence"))})
    return {"skill":CONFIG["name"],"ranked":sorted(rows,key=lambda x:-x["score"]),"excluded":[x["id"] for x in rows if not x["qualified"]]}

def compare(d):
    baseline={x["key"]:x.get("value") for x in d.get("baseline",[])}; changes=[]
    for x in d.get(CONFIG["root"],[]):
        old=baseline.get(x.get("key")); new=x.get("value")
        if old!=new: changes.append({"key":x.get("key"),"before":old,"after":new,"classification":"added" if old is None else "changed"})
    return {"skill":CONFIG["name"],"changes":changes,"change_count":len(changes)}

def schema(d):
    dims=[]; measures=[]
    for c in d.get(CONFIG["root"],[]):
        typ=str(c.get("type","")).lower(); item={"name":c.get("name"),"description":c.get("description")}
        (measures if any(t in typ for t in ["int","decimal","float","numeric"]) else dims).append(item)
    return {"skill":CONFIG["name"],"dimensions":dims,"measures":measures,"questions":["Confirm business grain","Confirm additive behavior","Confirm ownership"]}

def contract(d):
    req=CONFIG["fields"]; results=[]
    for i,x in enumerate(d.get(CONFIG["root"],[])):
        missing=[k for k in req if x.get(k) in (None,"",[])]; results.append({"id":x.get("name",i),"valid":not missing,"missing":missing})
    return {"skill":CONFIG["name"],"contracts":results,"valid":all(x["valid"] for x in results)}

def schedule(d):
    rows=sorted(d.get(CONFIG["root"],[]),key=lambda x:(-num(x.get("priority")),num(x.get("effort"))))
    return {"skill":CONFIG["name"],"plan":[{"order":i+1,"id":x.get("id"),"effort":x.get("effort"),"channel":x.get("channel"),"review_gate":True} for i,x in enumerate(rows)]}

def graph(d):
    edges=[]; nodes=set()
    for x in d.get(CONFIG["root"],[]):
        a=x.get("source") or x.get("id"); b=x.get("target")
        if a: nodes.add(a)
        if b: nodes.add(b); edges.append({"source":a,"target":b,"kind":x.get("kind","related")})
    return {"skill":CONFIG["name"],"nodes":sorted(nodes),"edges":edges,"orphan_count":sum(1 for n in nodes if not any(n in (e["source"],e["target"]) for e in edges))}

def design(d):
    groups=collections.defaultdict(list)
    for x in d.get(CONFIG["root"],[]): groups[str(x.get("property","unknown"))].append(x.get("value"))
    return {"skill":CONFIG["name"],"tokens":{k:[{"value":v,"uses":vals.count(v)} for v in sorted(set(vals),key=str)] for k,vals in groups.items()},"source_count":len(d.get(CONFIG["root"],[]))}

def redact(d):
    text=str(d.get("text","")); rules={"email":r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',"phone":r'(?<!\w)(?:\+?\d[\d -]{7,}\d)(?!\w)',"ip":r'\b(?:\d{1,3}\.){3}\d{1,3}\b'}; manifest=[]
    for label,pat in rules.items():
        found=re.findall(pat,text); manifest.append({"type":label,"count":len(found)}); text=re.sub(pat,f'[REDACTED_{label.upper()}]',text)
    return {"skill":CONFIG["name"],"redacted_text":text,"manifest":manifest}

ENGINES={"audit":audit,"rank":rank,"score":rank,"compare":compare,"schema":schema,"contract":contract,"schedule":schedule,"plan":schedule,"graph":graph,"design":design,"redact":redact}
def main():
    p=argparse.ArgumentParser(); p.add_argument("input"); p.add_argument("--output"); a=p.parse_args(); d=json.load(open(a.input,encoding="utf-8")); result=ENGINES[CONFIG["kind"]](d); txt=json.dumps(result,indent=2)
    if a.output: open(a.output,"w",encoding="utf-8").write(txt+'\n')
    else: print(txt)
if __name__=='__main__': main()
