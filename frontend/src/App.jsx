import { useState, useEffect, useCallback, useRef } from "react";

const API = "http://localhost:8000/api";

// ─── helpers ──────────────────────────────────────────────────────────────────
const scoreColor = v => v >= 0.7 ? "#ef4444" : v >= 0.45 ? "#f59e0b" : "#10b981";
const scoreBg    = v => v >= 0.7 ? "rgba(239,68,68,0.12)" : v >= 0.45 ? "rgba(245,158,11,0.12)" : "rgba(16,185,129,0.1)";
const scoreLabel = v => v >= 0.7 ? "CRITICAL" : v >= 0.45 ? "ELEVATED" : "NORMAL";

function ScoreBar({ value, color }) {
  const bg = color || scoreColor(value);
  return (
    <div style={{ background:"#1e2a3a", borderRadius:3, height:6, width:"100%", overflow:"hidden" }}>
      <div style={{ width:`${Math.min(value*100,100)}%`, height:"100%", background:bg, borderRadius:3, transition:"width 0.6s" }} />
    </div>
  );
}

function Sparkline({ data=[], color="#10b981", width=80, height=28 }) {
  if (data.length < 2) return <svg width={width} height={height}/>;
  const min=Math.min(...data), max=Math.max(...data), range=max-min||1;
  const pts = data.map((v,i)=>`${(i/(data.length-1))*width},${height-((v-min)/range)*(height-4)-2}`).join(" ");
  return <svg width={width} height={height}><polyline points={pts} fill="none" stroke={color} strokeWidth="1.5" strokeLinejoin="round"/></svg>;
}

// ─── MAIN APP ─────────────────────────────────────────────────────────────────
export default function AI4MH() {
  const [tab, setTab]           = useState("dashboard");
  const [posts, setPosts]       = useState([]);
  const [scores, setScores]     = useState([]);
  const [alerts, setAlerts]     = useState([]);
  const [auditLog, setAuditLog] = useState([]);
  const [loading, setLoading]   = useState(false);
  const [live, setLive]         = useState(true);
  const [trendHistory, setTrendHistory] = useState({});
  const [apiError, setApiError] = useState(false);
  const pollRef = useRef(null);

  // ── API calls ──────────────────────────────────────────────────────────────
  const fetchAll = useCallback(async () => {
    try {
      const [postsRes, scoresRes, alertsRes, auditRes] = await Promise.all([
        fetch(`${API}/posts?limit=60`),
        fetch(`${API}/scores`),
        fetch(`${API}/alerts`),
        fetch(`${API}/audit`),
      ]);
      const [p, s, a, au] = await Promise.all([postsRes.json(), scoresRes.json(), alertsRes.json(), auditRes.json()]);
      setPosts(p.posts || []);
      setScores(s.scores || []);
      setAlerts(a.alerts || []);
      setAuditLog(au.log || []);
      setTrendHistory(prev => {
        const next = {...prev};
        (s.scores||[]).forEach(r => {
          next[r.region_id] = [...(prev[r.region_id]||[]).slice(-19), r.final_score||r.crisis_score];
        });
        return next;
      });
      setApiError(false);
    } catch {
      setApiError(true);
    }
  }, []);

  const triggerIngest = useCallback(async () => {
    setLoading(true);
    try { await fetch(`${API}/ingest?n=30`, {method:"POST"}); await fetchAll(); } catch { setApiError(true); }
    setLoading(false);
  }, [fetchAll]);

  const reviewAlert = useCallback(async (id, decision) => {
    await fetch(`${API}/alerts/${id}/review`, {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({decision, analyst:"analyst-01", note:""}),
    });
    await fetchAll();
  }, [fetchAll]);

  // ── Polling ────────────────────────────────────────────────────────────────
  useEffect(() => { fetchAll(); }, [fetchAll]);
  useEffect(() => {
    if (live) { pollRef.current = setInterval(triggerIngest, 5000); }
    else      { clearInterval(pollRef.current); }
    return () => clearInterval(pollRef.current);
  }, [live, triggerIngest]);

  // ── Derived ────────────────────────────────────────────────────────────────
  const pending      = alerts.filter(a=>a.status==="pending");
  const criticalCount= scores.filter(s=>(s.final_score||s.crisis_score)>=0.7).length;
  const avgScore     = scores.length ? (scores.reduce((s,r)=>s+(r.final_score||r.crisis_score),0)/scores.length).toFixed(3) : "—";
  const topRegions   = [...scores].sort((a,b)=>(b.final_score||b.crisis_score)-(a.final_score||a.crisis_score)).slice(0,5);

  const TABS = [
    {id:"dashboard", label:"Dashboard"},
    {id:"map",       label:"Signal Map"},
    {id:"feed",      label:"Post Feed"},
    {id:"scoring",   label:"Scoring Engine"},
    {id:"governance",label:"Governance"},
    {id:"review",    label:`Review Queue${pending.length>0?` (${pending.length})`:""}`},
    {id:"audit",     label:"Audit Log"},
  ];

  return (
    <div style={{fontFamily:"'IBM Plex Mono',monospace",background:"#060d16",color:"#c8d8e8",minHeight:"100vh",display:"flex",flexDirection:"column"}}>

      {/* HEADER */}
      <header style={{background:"#0a1628",borderBottom:"1px solid #1a3050",padding:"0 24px",display:"flex",alignItems:"center",gap:16,height:56,flexShrink:0}}>
        <div style={{display:"flex",alignItems:"center",gap:10}}>
          <div style={{width:32,height:32,borderRadius:8,background:"linear-gradient(135deg,#0ea5e9,#6366f1)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:16,color:"#fff"}}>✦</div>
          <div>
            <div style={{fontSize:13,fontWeight:700,color:"#e2f0ff",letterSpacing:"0.05em"}}>AI4MH</div>
            <div style={{fontSize:9,color:"#4a7090",letterSpacing:"0.1em",textTransform:"uppercase"}}>Mental Health Crisis Monitor</div>
          </div>
        </div>
        {apiError && (
          <div style={{marginLeft:16,fontSize:9,padding:"4px 10px",borderRadius:4,background:"rgba(239,68,68,0.15)",color:"#ef4444",border:"1px solid #ef444433"}}>
            ⚠ Backend offline — run: uvicorn main:app --reload
          </div>
        )}
        <div style={{marginLeft:"auto",display:"flex",alignItems:"center",gap:12}}>
          <div style={{display:"flex",alignItems:"center",gap:6}}>
            <div style={{width:7,height:7,borderRadius:"50%",background:live?"#10b981":"#4a7090",boxShadow:live?"0 0 8px #10b981":"none"}}/>
            <span style={{fontSize:10,color:"#4a7090"}}>{live?"LIVE":"PAUSED"}</span>
          </div>
          <button onClick={()=>setLive(l=>!l)} style={{background:live?"rgba(239,68,68,0.1)":"rgba(16,185,129,0.1)",border:`1px solid ${live?"#ef4444":"#10b981"}`,color:live?"#ef4444":"#10b981",padding:"4px 12px",borderRadius:4,cursor:"pointer",fontSize:10,fontFamily:"inherit"}}>
            {live?"⏸ PAUSE":"▶ LIVE"}
          </button>
          <button onClick={triggerIngest} disabled={loading} style={{background:"rgba(14,165,233,0.1)",border:"1px solid #0ea5e9",color:"#0ea5e9",padding:"4px 12px",borderRadius:4,cursor:"pointer",fontSize:10,fontFamily:"inherit"}}>
            {loading?"…":"⟳ INGEST"}
          </button>
          <span style={{fontSize:10,color:"#2a4060"}}>{posts.length} posts · {scores.length} regions</span>
        </div>
      </header>

      {/* NAV */}
      <nav style={{background:"#080f1a",borderBottom:"1px solid #0e1e30",display:"flex",padding:"0 24px",gap:2,flexShrink:0}}>
        {TABS.map(t=>(
          <button key={t.id} onClick={()=>setTab(t.id)} style={{background:tab===t.id?"rgba(14,165,233,0.12)":"transparent",border:"none",borderBottom:tab===t.id?"2px solid #0ea5e9":"2px solid transparent",color:tab===t.id?"#0ea5e9":"#3a5570",padding:"12px 14px",cursor:"pointer",fontSize:10,fontFamily:"inherit",letterSpacing:"0.06em",whiteSpace:"nowrap"}}>
            {t.label.toUpperCase()}
          </button>
        ))}
      </nav>

      {/* CONTENT */}
      <main style={{flex:1,overflow:"auto",padding:"20px 24px"}}>

        {/* ── DASHBOARD ── */}
        {tab==="dashboard" && (
          <div>
            <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:12,marginBottom:20}}>
              {[
                {label:"TOTAL POSTS",     value:posts.length,    sub:"last 500 ingested",    color:"#0ea5e9"},
                {label:"CRITICAL REGIONS",value:criticalCount,   sub:"score ≥ 0.70",         color:"#ef4444"},
                {label:"AVG CRISIS SCORE",value:avgScore,        sub:"across all regions",   color:"#f59e0b"},
                {label:"PENDING REVIEWS", value:pending.length,  sub:"awaiting analyst",     color:"#a78bfa"},
              ].map(k=>(
                <div key={k.label} style={{background:"#0a1628",border:"1px solid #0e2040",borderRadius:8,padding:"14px 16px"}}>
                  <div style={{fontSize:9,color:"#3a5570",letterSpacing:"0.1em",marginBottom:6}}>{k.label}</div>
                  <div style={{fontSize:28,fontWeight:700,color:k.color,lineHeight:1}}>{k.value}</div>
                  <div style={{fontSize:9,color:"#2a4060",marginTop:4}}>{k.sub}</div>
                </div>
              ))}
            </div>

            <div style={{display:"grid",gridTemplateColumns:"1.2fr 1fr",gap:16,marginBottom:16}}>
              <div style={{background:"#0a1628",border:"1px solid #0e2040",borderRadius:8,overflow:"hidden"}}>
                <div style={{padding:"12px 16px",borderBottom:"1px solid #0e2040",fontSize:10,color:"#4a7090",letterSpacing:"0.1em"}}>◈ TOP REGIONS BY CRISIS SCORE</div>
                <div style={{padding:"8px 0"}}>
                  {topRegions.map((r,i)=>{
                    const sc = r.final_score||r.crisis_score;
                    return (
                      <div key={r.region_id} style={{padding:"8px 16px",borderLeft:`3px solid ${scoreColor(sc)}`,marginLeft:-1}}>
                        <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:4}}>
                          <div style={{fontSize:11,color:"#c8d8e8"}}><span style={{color:"#2a4060",marginRight:8}}>#{i+1}</span>{r.region_id}</div>
                          <span style={{fontSize:9,padding:"2px 7px",borderRadius:3,background:scoreBg(sc),color:scoreColor(sc)}}>{scoreLabel(sc)}</span>
                        </div>
                        <div style={{display:"flex",gap:12,alignItems:"center"}}>
                          <ScoreBar value={sc}/>
                          <span style={{fontSize:10,color:scoreColor(sc),minWidth:36}}>{(sc*100).toFixed(0)}%</span>
                          <Sparkline data={trendHistory[r.region_id]||[sc]} color={scoreColor(sc)}/>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div style={{background:"#0a1628",border:"1px solid #0e2040",borderRadius:8,overflow:"hidden"}}>
                <div style={{padding:"12px 16px",borderBottom:"1px solid #0e2040",fontSize:10,color:"#4a7090",letterSpacing:"0.1em"}}>✦ RECENT ALERTS</div>
                <div style={{padding:"8px 0",maxHeight:260,overflowY:"auto"}}>
                  {alerts.slice(0,8).map(a=>(
                    <div key={a.id} style={{padding:"8px 16px",borderBottom:"1px solid #060d16"}}>
                      <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start"}}>
                        <div style={{fontSize:10,color:"#c8d8e8"}}>{a.region_id}</div>
                        <span style={{fontSize:8,padding:"2px 6px",borderRadius:3,background:a.status==="pending"?"rgba(245,158,11,0.15)":a.status==="confirmed"?"rgba(239,68,68,0.15)":"rgba(16,185,129,0.15)",color:a.status==="pending"?"#f59e0b":a.status==="confirmed"?"#ef4444":"#10b981"}}>{a.status.toUpperCase()}</span>
                      </div>
                      <div style={{fontSize:9,color:"#3a5570",marginTop:2}}>Score: <span style={{color:scoreColor(a.final_score)}}>{a.final_score}</span> · Conf: {a.confidence} · {new Date(a.created_at).toLocaleTimeString()}</div>
                    </div>
                  ))}
                  {alerts.length===0&&<div style={{padding:"20px 16px",fontSize:10,color:"#2a4060",textAlign:"center"}}>No alerts yet</div>}
                </div>
              </div>
            </div>

            {/* All regions table */}
            <div style={{background:"#0a1628",border:"1px solid #0e2040",borderRadius:8,overflow:"hidden"}}>
              <div style={{padding:"12px 16px",borderBottom:"1px solid #0e2040",fontSize:10,color:"#4a7090",letterSpacing:"0.1em"}}>▣ ALL REGIONS</div>
              <div style={{overflowX:"auto"}}>
                <table style={{width:"100%",borderCollapse:"collapse",fontSize:10}}>
                  <thead><tr style={{background:"#060d16"}}>
                    {["Region","Posts","Crisis Score","Norm.Score","Sentiment","Volume","Geo","Trend","Confidence","Tier","Status"].map(h=>(
                      <th key={h} style={{padding:"8px 10px",textAlign:"left",color:"#2a4060",fontWeight:700,fontSize:9,whiteSpace:"nowrap"}}>{h}</th>
                    ))}
                  </tr></thead>
                  <tbody>
                    {scores.map((r,i)=>{
                      const sc=r.final_score||r.crisis_score;
                      return (
                        <tr key={r.region_id} style={{background:i%2===0?"transparent":"rgba(10,22,40,0.5)",borderLeft:`2px solid ${scoreColor(sc)}`}}>
                          <td style={{padding:"7px 10px",color:"#c8d8e8"}}>{r.region_id}</td>
                          <td style={{padding:"7px 10px",color:"#4a7090"}}>{r.post_count}</td>
                          <td style={{padding:"7px 10px",color:scoreColor(r.crisis_score),fontWeight:700}}>{(r.crisis_score*100).toFixed(1)}%</td>
                          <td style={{padding:"7px 10px",color:scoreColor(sc),fontWeight:700}}>{(sc*100).toFixed(1)}%</td>
                          <td style={{padding:"7px 10px",color:r.sentiment_intensity>0.5?"#ef4444":"#4a7090"}}>{(r.sentiment_intensity*100).toFixed(0)}%</td>
                          <td style={{padding:"7px 10px",color:"#4a7090"}}>{(r.volume_spike*100).toFixed(0)}%</td>
                          <td style={{padding:"7px 10px",color:"#4a7090"}}>{(r.geo_cluster*100).toFixed(0)}%</td>
                          <td style={{padding:"7px 10px",color:"#4a7090"}}>{(r.trend_accel*100).toFixed(0)}%</td>
                          <td style={{padding:"7px 10px",color:r.confidence<0.6?"#ef4444":"#10b981"}}>{(r.confidence*100).toFixed(0)}%</td>
                          <td style={{padding:"7px 10px"}}><span style={{fontSize:8,padding:"2px 6px",borderRadius:3,background:"rgba(14,165,233,0.1)",color:"#0ea5e9"}}>{r.population_tier||"—"}</span></td>
                          <td style={{padding:"7px 10px"}}><span style={{fontSize:8,padding:"2px 7px",borderRadius:3,background:scoreBg(sc),color:scoreColor(sc)}}>{scoreLabel(sc)}</span></td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ── MAP ── */}
        {tab==="map" && (
          <div>
            <div style={{marginBottom:12,fontSize:10,color:"#3a5570"}}>◈ GEOSPATIAL SIGNAL MAP — circle size reflects crisis score intensity</div>
            <div style={{background:"#0a1628",border:"1px solid #0e2040",borderRadius:8,overflow:"hidden"}}>
              <svg viewBox="0 0 900 500" style={{width:"100%",background:"#060d16"}}>
                {[...Array(9)].map((_,i)=><line key={`v${i}`} x1={i*100+50} y1={0} x2={i*100+50} y2={500} stroke="#0e1e30" strokeWidth={0.5}/>)}
                {[...Array(5)].map((_,i)=><line key={`h${i}`} x1={0} y1={i*100+50} x2={900} y2={i*100+50} stroke="#0e1e30" strokeWidth={0.5}/>)}
                <path d="M80 80 L820 80 L820 400 L600 400 L600 420 L580 440 L460 440 L440 420 L440 400 L80 400 Z" fill="none" stroke="#1a3050" strokeWidth={1}/>
                <text x={450} y={50} fill="#1a3050" fontSize={11} textAnchor="middle" fontFamily="monospace">UNITED STATES — CRISIS SIGNAL HEATMAP</text>
                {/* Region lat/lng → SVG coords mapping */}
                {scores.map(r=>{
                  const COORDS = {
                    "CA-LA":{x:130,y:260},"TX-HOU":{x:390,y:330},"NY-NYC":{x:720,y:175},
                    "IL-CHI":{x:555,y:190},"AZ-PHX":{x:195,y:290},"PA-PHI":{x:690,y:195},
                    "WV-CHA":{x:640,y:230},"KY-HAZ":{x:610,y:245},"OH-CHI":{x:615,y:210},
                  };
                  const pos = COORDS[r.region_id];
                  if (!pos) return null;
                  const sc = r.final_score||r.crisis_score;
                  const col = scoreColor(sc);
                  const rad = 8 + sc*28;
                  return (
                    <g key={r.region_id}>
                      {sc>=0.7&&<circle cx={pos.x} cy={pos.y} r={rad+10} fill="none" stroke={col} strokeWidth={1} opacity={0.3}><animate attributeName="r" values={`${rad};${rad+18};${rad}`} dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.4;0;0.4" dur="2s" repeatCount="indefinite"/></circle>}
                      <circle cx={pos.x} cy={pos.y} r={rad} fill={col} fillOpacity={0.2} stroke={col} strokeWidth={1.5}/>
                      <circle cx={pos.x} cy={pos.y} r={3} fill={col}/>
                      <text x={pos.x} y={pos.y-rad-5} fill={col} fontSize={8} textAnchor="middle" fontFamily="monospace">{(sc*100).toFixed(0)}%</text>
                      <text x={pos.x} y={pos.y+rad+12} fill="#3a5570" fontSize={7} textAnchor="middle" fontFamily="monospace">{r.region_id}</text>
                    </g>
                  );
                })}
                <g transform="translate(660,420)">
                  <rect x={0} y={0} width={190} height={68} rx={4} fill="#0a1628" stroke="#0e2040"/>
                  <text x={10} y={16} fill="#3a5570" fontSize={8} fontFamily="monospace">LEGEND</text>
                  {[["#10b981","NORMAL (< 0.45)"],["#f59e0b","ELEVATED (0.45–0.70)"],["#ef4444","CRITICAL (≥ 0.70)"]].map(([c,l],i)=>(
                    <g key={l} transform={`translate(10,${28+i*14})`}>
                      <circle r={5} fill={c} fillOpacity={0.3} stroke={c} strokeWidth={1}/>
                      <text x={14} y={4} fill="#4a7090" fontSize={8} fontFamily="monospace">{l}</text>
                    </g>
                  ))}
                </g>
              </svg>
            </div>
          </div>
        )}

        {/* ── POST FEED ── */}
        {tab==="feed" && (
          <div>
            <div style={{marginBottom:12,fontSize:10,color:"#3a5570"}}>
              ≡ LIVE POST FEED — {posts.length} posts · {posts.filter(p=>p.is_bot).length} bots · {posts.filter(p=>p.nlp_crisis_flag).length} crisis-flagged
            </div>
            <div style={{display:"flex",flexDirection:"column",gap:8}}>
              {posts.slice(0,40).map(p=>(
                <div key={p.id} style={{background:"#0a1628",border:`1px solid ${p.is_bot?"#ef4444":p.nlp_crisis_flag?"#f59e0b":"#0e2040"}`,borderRadius:6,padding:"10px 14px",opacity:p.is_bot?0.6:1}}>
                  <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:6}}>
                    <div style={{display:"flex",gap:8,alignItems:"center"}}>
                      <span style={{fontSize:9,color:"#0ea5e9"}}>r/{p.subreddit}</span>
                      <span style={{fontSize:9,color:"#2a4060"}}>·</span>
                      <span style={{fontSize:9,color:"#2a4060"}}>{p.region_id}</span>
                      <span style={{fontSize:9,color:"#2a4060"}}>·</span>
                      <span style={{fontSize:9,color:"#2a4060"}}>{new Date(p.timestamp).toLocaleTimeString()}</span>
                    </div>
                    <div style={{display:"flex",gap:6}}>
                      {p.is_bot&&<span style={{fontSize:8,padding:"1px 6px",borderRadius:3,background:"rgba(239,68,68,0.15)",color:"#ef4444"}}>BOT</span>}
                      {p.nlp_crisis_flag&&<span style={{fontSize:8,padding:"1px 6px",borderRadius:3,background:"rgba(245,158,11,0.15)",color:"#f59e0b"}}>CRISIS</span>}
                      <span style={{fontSize:8,padding:"1px 6px",borderRadius:3,background:p.sentiment<-0.3?"rgba(239,68,68,0.1)":"rgba(16,185,129,0.1)",color:p.sentiment<-0.3?"#ef4444":"#10b981"}}>{p.sentiment>0?"+":""}{p.sentiment}</span>
                    </div>
                  </div>
                  <div style={{fontSize:11,color:p.nlp_crisis_flag?"#e2c87a":"#8a9ab0",lineHeight:1.5}}>{p.text}</div>
                  {p.keyword_terms?.length>0&&(
                    <div style={{marginTop:6,display:"flex",gap:4,flexWrap:"wrap"}}>
                      {p.keyword_terms.map(k=><span key={k} style={{fontSize:8,padding:"1px 6px",borderRadius:3,background:"rgba(239,68,68,0.1)",color:"#ef4444",border:"1px solid rgba(239,68,68,0.2)"}}>{k}</span>)}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── SCORING ── */}
        {tab==="scoring" && (
          <div>
            <div style={{background:"#060d16",border:"1px solid #0ea5e9",borderRadius:8,padding:16,marginBottom:20,fontFamily:"monospace"}}>
              <div style={{fontSize:9,color:"#0ea5e9",letterSpacing:"0.1em",marginBottom:8}}>COMPOSITE FORMULA</div>
              <div style={{fontSize:13,color:"#c8d8e8",lineHeight:1.8}}>
                crisis_score = <span style={{color:"#f59e0b"}}>0.35</span>·sentiment + <span style={{color:"#f59e0b"}}>0.30</span>·volume_spike + <span style={{color:"#f59e0b"}}>0.20</span>·geo_cluster + <span style={{color:"#f59e0b"}}>0.15</span>·trend_accel
              </div>
              <div style={{marginTop:10,fontSize:9,color:"#2a4060"}}>
                Escalate if: score ≥ 0.70 AND confidence ≥ 0.60 AND governance_ok AND bot_ratio &lt; 0.25
              </div>
            </div>
            <div style={{background:"#0a1628",border:"1px solid #0e2040",borderRadius:8,overflow:"hidden"}}>
              <div style={{padding:"12px 16px",borderBottom:"1px solid #0e2040",fontSize:10,color:"#4a7090",letterSpacing:"0.1em"}}>REGION EXPLAINABILITY</div>
              <div style={{overflowX:"auto"}}>
                <table style={{width:"100%",borderCollapse:"collapse",fontSize:10}}>
                  <thead><tr style={{background:"#060d16"}}>
                    {["Region","Score","Sentiment×.35","Volume×.30","Geo×.20","Trend×.15","BotRatio","Conf","Escalate"].map(h=>(
                      <th key={h} style={{padding:"8px 10px",textAlign:"left",color:"#2a4060",fontWeight:700,fontSize:9,whiteSpace:"nowrap"}}>{h}</th>
                    ))}
                  </tr></thead>
                  <tbody>
                    {scores.map((r,i)=>{
                      const sc=r.final_score||r.crisis_score;
                      return (
                        <tr key={r.region_id} style={{background:i%2===0?"transparent":"rgba(10,22,40,0.5)"}}>
                          <td style={{padding:"7px 10px",color:"#c8d8e8"}}>{r.region_id}</td>
                          <td style={{padding:"7px 10px",color:scoreColor(sc),fontWeight:700}}>{(sc*100).toFixed(1)}%</td>
                          <td style={{padding:"7px 10px"}}><div style={{display:"flex",gap:4,alignItems:"center"}}><ScoreBar value={r.sentiment_intensity} color="#ef4444"/><span style={{color:"#ef4444",fontSize:9,minWidth:28}}>{(r.sentiment_intensity*100).toFixed(0)}%</span></div></td>
                          <td style={{padding:"7px 10px"}}><div style={{display:"flex",gap:4,alignItems:"center"}}><ScoreBar value={r.volume_spike} color="#f59e0b"/><span style={{color:"#f59e0b",fontSize:9,minWidth:28}}>{(r.volume_spike*100).toFixed(0)}%</span></div></td>
                          <td style={{padding:"7px 10px"}}><div style={{display:"flex",gap:4,alignItems:"center"}}><ScoreBar value={r.geo_cluster} color="#a78bfa"/><span style={{color:"#a78bfa",fontSize:9,minWidth:28}}>{(r.geo_cluster*100).toFixed(0)}%</span></div></td>
                          <td style={{padding:"7px 10px"}}><div style={{display:"flex",gap:4,alignItems:"center"}}><ScoreBar value={r.trend_accel} color="#0ea5e9"/><span style={{color:"#0ea5e9",fontSize:9,minWidth:28}}>{(r.trend_accel*100).toFixed(0)}%</span></div></td>
                          <td style={{padding:"7px 10px",color:r.bot_ratio>0.25?"#ef4444":"#3a5570"}}>{(r.bot_ratio*100).toFixed(0)}%</td>
                          <td style={{padding:"7px 10px",color:r.confidence<0.6?"#ef4444":"#10b981"}}>{(r.confidence*100).toFixed(0)}%</td>
                          <td style={{padding:"7px 10px"}}>{r.should_escalate?<span style={{fontSize:8,padding:"2px 7px",borderRadius:3,background:"rgba(239,68,68,0.15)",color:"#ef4444"}}>YES</span>:<span style={{fontSize:8,padding:"2px 7px",borderRadius:3,background:"rgba(16,185,129,0.1)",color:"#10b981"}}>NO</span>}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ── GOVERNANCE ── */}
        {tab==="governance" && (
          <div>
            <div style={{marginBottom:16,fontSize:10,color:"#3a5570"}}>⚠ GOVERNANCE LAYER — Active filters applied to all incoming signals</div>
            <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:16,marginBottom:20}}>
              {[
                {title:"Bot Filter",color:"#ef4444",icon:"🤖",stat:`${posts.filter(p=>p.is_bot).length} bots removed`,rules:["post_rate > 20/hr → flagged","duplicate hash matching","removed before scoring","bot_ratio > 25% blocks alert"]},
                {title:"Media Spike Detection",color:"#f59e0b",icon:"📰",stat:"National event dampening active",rules:["topic overlap with news feed","national vs local ratio test","dampening factor: 0.6×","local posts weighted 2×"]},
                {title:"Rural Normalization",color:"#a78bfa",icon:"🌾",stat:`Population-adjusted for all ${scores.length} regions`,rules:["rural: ×1.30 boost","suburban: ×1.05","urban: ×1.00","tiered min_posts thresholds"]},
              ].map(g=>(
                <div key={g.title} style={{background:"#0a1628",border:`1px solid ${g.color}22`,borderRadius:8,padding:16}}>
                  <div style={{display:"flex",alignItems:"center",gap:8,marginBottom:10}}>
                    <span style={{fontSize:18}}>{g.icon}</span>
                    <div style={{fontSize:10,fontWeight:700,color:g.color}}>{g.title.toUpperCase()}</div>
                  </div>
                  <div style={{fontSize:9,color:g.color,marginBottom:10,padding:"4px 8px",background:`${g.color}11`,borderRadius:4}}>{g.stat}</div>
                  {g.rules.map(r=><div key={r} style={{fontSize:9,color:"#4a7090",display:"flex",gap:6,marginBottom:3}}><span style={{color:g.color}}>›</span>{r}</div>)}
                </div>
              ))}
            </div>

            {/* Normalized score comparison */}
            <div style={{background:"#0a1628",border:"1px solid #0e2040",borderRadius:8,overflow:"hidden"}}>
              <div style={{padding:"12px 16px",borderBottom:"1px solid #0e2040",fontSize:10,color:"#4a7090",letterSpacing:"0.1em"}}>POPULATION-NORMALIZED SCORES</div>
              <div style={{overflowX:"auto"}}>
                <table style={{width:"100%",borderCollapse:"collapse",fontSize:10}}>
                  <thead><tr style={{background:"#060d16"}}>
                    {["Region","Posts","Bot Ratio","Raw Score","Norm Score","Tier","Governance OK"].map(h=>(
                      <th key={h} style={{padding:"8px 12px",textAlign:"left",color:"#2a4060",fontWeight:700,fontSize:9}}>{h}</th>
                    ))}
                  </tr></thead>
                  <tbody>
                    {scores.map((r,i)=>(
                      <tr key={r.region_id} style={{background:i%2===0?"transparent":"rgba(10,22,40,0.5)"}}>
                        <td style={{padding:"7px 12px",color:"#c8d8e8"}}>{r.region_id}</td>
                        <td style={{padding:"7px 12px",color:"#4a7090"}}>{r.post_count}</td>
                        <td style={{padding:"7px 12px",color:r.bot_ratio>0.25?"#ef4444":"#10b981"}}>{(r.bot_ratio*100).toFixed(0)}%</td>
                        <td style={{padding:"7px 12px",color:scoreColor(r.crisis_score)}}>{(r.crisis_score*100).toFixed(1)}%</td>
                        <td style={{padding:"7px 12px",color:scoreColor(r.normalized_score||r.crisis_score),fontWeight:700}}>{((r.normalized_score||r.crisis_score)*100).toFixed(1)}%</td>
                        <td style={{padding:"7px 12px"}}><span style={{fontSize:8,padding:"2px 6px",borderRadius:3,background:"rgba(14,165,233,0.1)",color:"#0ea5e9"}}>{r.population_tier||"—"}</span></td>
                        <td style={{padding:"7px 12px"}}>{r.governance_ok?<span style={{color:"#10b981",fontSize:9}}>✓ YES</span>:<span style={{color:"#ef4444",fontSize:9}}>✗ NO</span>}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ── REVIEW QUEUE ── */}
        {tab==="review" && (
          <div>
            <div style={{marginBottom:12,fontSize:10,color:"#3a5570"}}>✦ HUMAN REVIEW QUEUE — No alert triggers intervention automatically</div>
            <div style={{background:"rgba(245,158,11,0.06)",border:"1px solid rgba(245,158,11,0.2)",borderRadius:8,padding:"10px 16px",marginBottom:20,fontSize:10,color:"#c8a060"}}>
              ⚠ All escalated alerts require analyst approval before any public health action.
            </div>
            {alerts.length===0
              ?<div style={{background:"#0a1628",border:"1px solid #0e2040",borderRadius:8,padding:40,textAlign:"center",color:"#2a4060",fontSize:12}}>No alerts yet — system monitoring...</div>
              :<div style={{display:"flex",flexDirection:"column",gap:12}}>
                {alerts.map(a=>(
                  <div key={a.id} style={{background:"#0a1628",border:`1px solid ${a.status==="pending"?scoreColor(a.final_score):a.status==="confirmed"?"#ef4444":"#10b981"}`,borderRadius:8,padding:16,opacity:a.status!=="pending"?0.7:1}}>
                    <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:12}}>
                      <div>
                        <div style={{fontSize:13,fontWeight:700,color:"#c8d8e8",marginBottom:2}}>{a.region_id}</div>
                        <div style={{fontSize:9,color:"#3a5570"}}>ID: {a.id} · {new Date(a.created_at).toLocaleString()}</div>
                      </div>
                      <span style={{fontSize:10,padding:"4px 12px",borderRadius:4,fontWeight:700,background:a.status==="pending"?"rgba(245,158,11,0.15)":a.status==="confirmed"?"rgba(239,68,68,0.15)":"rgba(16,185,129,0.15)",color:a.status==="pending"?"#f59e0b":a.status==="confirmed"?"#ef4444":"#10b981"}}>{a.status.toUpperCase()}</span>
                    </div>
                    <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:10,marginBottom:12}}>
                      {[
                        {label:"Final Score",value:`${(a.final_score*100).toFixed(1)}%`,color:scoreColor(a.final_score)},
                        {label:"Confidence", value:`${(a.confidence*100).toFixed(1)}%`, color:a.confidence>=0.6?"#10b981":"#ef4444"},
                        {label:"Post Count", value:a.post_count, color:"#0ea5e9"},
                        {label:"Bot Ratio",  value:`${(a.bot_ratio*100).toFixed(0)}%`,  color:a.bot_ratio>0.25?"#ef4444":"#10b981"},
                      ].map(s=>(
                        <div key={s.label} style={{background:"#060d16",borderRadius:6,padding:"8px 10px"}}>
                          <div style={{fontSize:8,color:"#2a4060",marginBottom:4}}>{s.label}</div>
                          <div style={{fontSize:16,fontWeight:700,color:s.color}}>{s.value}</div>
                        </div>
                      ))}
                    </div>
                    {a.status==="pending"&&(
                      <div style={{display:"flex",gap:10,flexWrap:"wrap"}}>
                        <button onClick={()=>reviewAlert(a.id,"confirmed")} style={{background:"rgba(239,68,68,0.15)",border:"1px solid #ef4444",color:"#ef4444",padding:"6px 14px",borderRadius:4,cursor:"pointer",fontSize:10,fontFamily:"inherit"}}>✦ CONFIRM — Escalate to Agency</button>
                        <button onClick={()=>reviewAlert(a.id,"dismissed")} style={{background:"rgba(16,185,129,0.1)",border:"1px solid #10b981",color:"#10b981",padding:"6px 14px",borderRadius:4,cursor:"pointer",fontSize:10,fontFamily:"inherit"}}>✓ DISMISS — False Positive</button>
                        <button onClick={()=>reviewAlert(a.id,"monitoring")} style={{background:"rgba(14,165,233,0.1)",border:"1px solid #0ea5e9",color:"#0ea5e9",padding:"6px 14px",borderRadius:4,cursor:"pointer",fontSize:10,fontFamily:"inherit"}}>◈ MONITOR — Watch 24h</button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            }
          </div>
        )}

        {/* ── AUDIT LOG ── */}
        {tab==="audit" && (
          <div>
            <div style={{marginBottom:12,fontSize:10,color:"#3a5570"}}>▣ AUDIT LOG — Every scoring event and analyst decision, immutably recorded</div>
            <div style={{background:"#0a1628",border:"1px solid #0e2040",borderRadius:8,overflow:"hidden"}}>
              <div style={{overflowX:"auto"}}>
                <table style={{width:"100%",borderCollapse:"collapse",fontSize:9}}>
                  <thead><tr style={{background:"#060d16"}}>
                    {["Timestamp","Event","Region","Score","Confidence","Alert Generated"].map(h=>(
                      <th key={h} style={{padding:"10px 12px",textAlign:"left",color:"#2a4060",fontWeight:700,letterSpacing:"0.08em",whiteSpace:"nowrap"}}>{h}</th>
                    ))}
                  </tr></thead>
                  <tbody>
                    {auditLog.slice(0,50).map((l,i)=>(
                      <tr key={i} style={{background:i%2===0?"transparent":"rgba(10,22,40,0.5)"}}>
                        <td style={{padding:"8px 12px",color:"#2a4060"}}>{new Date(l.logged_at||l.timestamp||Date.now()).toLocaleString()}</td>
                        <td style={{padding:"8px 12px"}}><span style={{fontSize:8,padding:"2px 6px",borderRadius:3,background:"rgba(14,165,233,0.1)",color:"#0ea5e9"}}>{l.event}</span></td>
                        <td style={{padding:"8px 12px",color:"#c8d8e8"}}>{l.region_id||"—"}</td>
                        <td style={{padding:"8px 12px",color:l.final_score>=0.7?"#ef4444":l.final_score>=0.45?"#f59e0b":"#10b981"}}>{l.final_score!=null?(l.final_score*100).toFixed(1)+"%":"—"}</td>
                        <td style={{padding:"8px 12px",color:l.confidence>=0.6?"#10b981":"#4a7090"}}>{l.confidence!=null?(l.confidence*100).toFixed(1)+"%":"—"}</td>
                        <td style={{padding:"8px 12px"}}>{l.alert_generated!=null?(l.alert_generated?<span style={{color:"#ef4444"}}>YES</span>:<span style={{color:"#3a5570"}}>no</span>):"—"}</td>
                      </tr>
                    ))}
                    {auditLog.length===0&&<tr><td colSpan={6} style={{padding:24,textAlign:"center",color:"#2a4060"}}>No audit events yet</td></tr>}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

      </main>
      <style>{`@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-track{background:#060d16}::-webkit-scrollbar-thumb{background:#1a3050;border-radius:3px}`}</style>
    </div>
  );
}
