import math, random, itertools, json, sys
from data import NODES, EDGES
from layout import ellipse_arc_positions, A, B, CX, CY
ids=[n['id'] for n in NODES if n['id']!='odysseus']
N=len(ids)
pts=[(CX+x,CY+y) for x,y in ellipse_arc_positions(N,A,B)]
chords=[(a,b) for a,b,*_ in EDGES if 'odysseus' not in (a,b)]
region={n['id']:n['region'] for n in NODES}
cat={n['id']:n['cat'] for n in NODES}
def seg_cross(p1,p2,p3,p4):
    def ccw(a,b,c): return (c[1]-a[1])*(b[0]-a[0])>(b[1]-a[1])*(c[0]-a[0])
    return ccw(p1,p3,p4)!=ccw(p2,p3,p4) and ccw(p1,p2,p3)!=ccw(p1,p2,p4)
def cost(order):
    idx={v:i for i,v in enumerate(order)}
    c=0; cr=0
    segs=[]
    for a,b in chords:
        pa,pb=pts[idx[a]],pts[idx[b]]
        L=math.dist(pa,pb); c+=L**1.35
        segs.append((pa,pb,a,b))
    for (p1,p2,a1,b1),(p3,p4,a2,b2) in itertools.combinations(segs,2):
        if len({a1,b1,a2,b2})<4: continue
        if seg_cross(p1,p2,p3,p4): cr+=1
    c+=cr*1500
    # zeus pinned top
    c+= 0 if order[0]=='zeus' else 1e6
    # gods near top (y small)
    for v in order:
        y=pts[idx[v]][1]
        if cat[v]=='god' and region[v]=='olympus': c+=max(0,y-420)*30
        if region[v]=='hades': c+=max(0,760-y)*10
    return c,cr
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
best=None
for trial in range(6):
    order=ids[:]; random.shuffle(order); order.remove('zeus'); order=['zeus']+order
    cur=cost(order)[0]; T=20000
    for it in range(30000):
        i,j=random.sample(range(1,N),2)
        o2=order[:]
        if random.random()<0.5: o2[i],o2[j]=o2[j],o2[i]
        else:
            x=o2.pop(i); o2.insert(j,x)
        c2=cost(o2)[0]
        if c2<cur or random.random()<math.exp((cur-c2)/T):
            order,cur=o2,c2
        T*=0.9996
    r=cost(order)
    print(trial,[round(x) for x in r],order,flush=True)
    if best is None or r[0]<best[0]: best=(r[0],order)
from layout import ORDER
print('current',[round(x) for x in cost(ORDER)])
json.dump(best[1],open('order3.json','w'),ensure_ascii=False)
