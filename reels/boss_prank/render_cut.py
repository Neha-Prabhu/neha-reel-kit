import subprocess
L="/home/claude/neha-reel-kit/assets/luts/"; FPS=24
# B-roll is always MUTED — only her voice; music goes on top later.
YT=[(3.0,7.5,1.6),(7.5,9.6,1.0)]   # explaining (sped) -> YouTube at 7.6 -> ~2 s playing
KK=[(0.0,4.3,1.5),(4.3,7.5,1.0)]   # unchanged from draft 2
VY=[(13.15,15.10),(15.40,17.62)]   # "I played music…meeting" + "Opened his YouTube…screen" (pause between removed)
VK=(18.09,20.17); kk_react=4.3/1.5+0.3
def dur(p): return sum((o-i)/s for i,o,s in p)
fc=[]
def vid(inp,parts,tag):
    vs=[]
    for k,(i,o,s) in enumerate(parts):
        fc.append(f"[{inp}:v]trim={i}:{o},setpts=(PTS-STARTPTS)/{s},fps={FPS},scale=1080:1920,setsar=1,lut3d={L}warm_pop_light.cube[{tag}v{k}]"); vs.append(f"[{tag}v{k}]")
    fc.append("".join(vs)+f"concat=n={len(vs)}:v=1:a=0[{tag}v]")
def fade(a,b): return f"afade=t=in:d=0.03,afade=t=out:st={b-a-0.04:.3f}:d=0.04"
# 1) A-roll to just before "I played music", boggled cutaway (muted)
fc.append(f"[0:v]trim=0:13.15,setpts=PTS-STARTPTS,lut3d={L}warm_pop.cube,scale=1080:1920,setsar=1[a1v0]")
fc.append(f"[1:v]trim=2.6:4.5,setpts=(PTS-STARTPTS)/{1.9/1.91}+11.0/TB,fps={FPS},scale=1080:1920,setsar=1,lut3d={L}warm_pop_light.cube[bog]")
fc.append("[a1v0][bog]overlay=eof_action=pass:enable='between(t,11.0,12.909)'[a1v]")
fc.append("[0:a]atrim=0:13.15,asetpts=PTS-STARTPTS[a1a]")
# 2) YouTube under both lines
vid(2,YT,"y"); dy=dur(YT)
for k,(a,b) in enumerate(VY): fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,{fade(a,b)}[yv{k}a]")
fc.append(f"[yv0a][yv1a]concat=n=2:v=0:a=1,apad,atrim=0:{dy:.4f}[ya]")
# 3) kicked out — unchanged timing
vid(3,KK,"k"); dk=dur(KK); at=kk_react-(VK[1]-VK[0])
fc.append(f"[0:a]atrim={VK[0]}:{VK[1]},asetpts=PTS-STARTPTS,{fade(*VK)},adelay={int(at*1000)}:all=1,apad,atrim=0:{dk:.4f}[ka]")
# 4) back to A-roll
fc.append(f"[0:v]trim=20.22:30.55,setpts=PTS-STARTPTS,lut3d={L}warm_pop.cube,scale=1080:1920,setsar=1[a2v]")
fc.append("[0:a]atrim=20.22:30.55,asetpts=PTS-STARTPTS[a2a]")
fc.append("[a1v][a1a][yv][ya][kv][ka][a2v][a2a]concat=n=4:v=1:a=1[v][araw];[araw]alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg","-v","error","-y","-i","../src/aroll.mp4","-i","../src/far_boss_boggled.MOV","-i","../src/youtube_play.MOV","-i","../src/kicked_him_out.mov",
  "-filter_complex",";".join(fc),"-map","[v]","-map","[a]","-r",str(FPS),"-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p",
  "-c:a","aac","-b:a","192k","-movflags","+faststart","boss_prank_graded_v3.mp4"],check=True)
y0=13.15; print(f"YT {y0:.2f}-{y0+dy:.2f} switch {y0+4.5/1.6+0.1:.2f} voice ends {y0+1.95+2.22:.2f} | KK {y0+dy:.2f}-{y0+dy+dk:.2f} | total {y0+dy+dk+10.33:.2f}")
