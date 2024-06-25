import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import itertools as it
import numpy as np
g=9.8
# TODO: brečení
def anim(balls,pattern,t0s=None,hands=None,delay=0,hand_shift=3,happy_state=1):
    global frame,pause,incr,direction,t0,cycind
    print("ahoj",balls)
    radius=0.6
    direction=1
    pattern=[int(h) for h in pattern]
    incr=10
    head_posx,head_posy=np.array([0,9])
    head_radius=1.5
    

    fig,ax=plt.subplots()
    mh=0.5*g*max(pattern)**2/4
    m3=0.5*g*3**2/4
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    
    colors="r","b","g","y","pink"
    patches = [plt.Circle((0,0), radius, fc=c) for c,_ in zip(it.cycle(colors),range(balls))]
    
    hand_x,hand_y=3,0
    trunkx=[-hand_x*0.9,hand_x*0.9,hand_x*0.7,-hand_x*0.7]
    trunky=[head_posy-head_radius*1.5,head_posy-head_radius*1.5,0,0]#head_posy-head_radius-5,head_posy-head_radius-5]
    p0s=[]
    duration=100
    frame=0
    pause=False
    x0=hand_x
    if hands==None:
        hands=[h for h,_ in zip(it.cycle((-1,1)),range(balls))]
    frames=100*incr*duration
    thands=list(hands)
    durs=[0 for _ in range(balls)]
    llim=-5
    heights=[]
    ax.set_xlim(-hand_x*2,hand_x*2)
    ax.set_ylim(llim,mh*1.2)
    if t0s==None:
        t0s=list(range(balls))
    
    orig_t0s=list(t0s)
    
    #cycpat=it.cycle(pattern)
    t0=-1
    #print(durs,heights)
    
    for i,patch in enumerate(patches):
            ang=-np.pi/4+(i//2)*np.pi/2
     #       print(ang)
            p0s.append((x0*hands[i]+(0 if i<2 else 2*radius*np.cos(ang)),0 if i<2 else 2*radius*np.sin(ang)))
            ax.add_patch(patch)
    orig_p0s=list(p0s)
    ps=list(p0s)
    pat_texts = [ax.text(0.1+0.1*(i%9), 0.9-0.1*(i//9), '', fontsize=15,transform=ax.transAxes) for i,p in enumerate(pattern)]
    hand_lines=[ax.plot([],[])[0],ax.plot([],[])[0],ax.plot([],[])[0],ax.plot([],[])[0]]    
    head_lines=[ax.plot([],[])[0],ax.plot([],[])[0],ax.plot([],[],".",ms=4*m3/mh)[0],ax.plot([],[])[0],ax.plot([],[])[0],ax.plot([],[])[0],ax.plot([],[])[0],ax.plot([],[])[0]]
    trunk_lines=[ax.plot([],[])[0],ax.plot([],[])[0],ax.plot([],[])[0],ax.plot([],[])[0]]    
    def init():
        global frame,cycind,t0
        print("init!")
        frame=0
        #print("init!",orig_t0s)
        #input()
        t0s[:]=orig_t0s
        p0s[:]=orig_p0s
        ps[:]=orig_p0s
        thands[:]=list(hands)
        t0=-1
        cycind=0
        heights[:]=[0 for _ in range(balls)]
        durs[:]=[0 for _ in range(balls)]
        for i,pat_text in enumerate(pat_texts):
            pat_text.set_text(pattern[i])

        for i,patch in enumerate(patches):
            patch.center=p0s[i]
            ax.add_patch(patch)
        for line in hand_lines:
            line.set_data([],[])
            line.set_color("black")
            line.set_lw(0.8)
        head_lines[0].set_data(head_posx+head_radius*np.cos(np.linspace(0,2*np.pi,100)),head_posy+head_radius*np.sin(np.linspace(0,2*np.pi,100)))
        if happy_state==0:
            head_lines[1].set_data(head_posx-head_radius*0.35*np.cos(np.linspace(0,np.pi,100)),head_posy-head_radius/2+head_radius*0.35*np.sin(np.linspace(0,np.pi,100)))
        elif happy_state==1:
            head_lines[1].set_data(head_posx-head_radius*0.45*np.cos(np.linspace(np.pi,2*np.pi ,100)),head_posy-head_radius/6+head_radius*0.45*np.sin(np.linspace(np.pi,2*np.pi,100)))
        else:
            head_lines[1].set_data([head_posx-head_radius*0.4,head_posx+head_radius*0.4],[head_posy-head_radius/6,head_posy-head_radius/6])
        head_lines[2].set_data([head_posx-head_radius*0.3,head_posx+head_radius*0.3],[head_posy+head_radius*0.3,head_posy+head_radius*0.3])
        for head_line,ang,length in zip(head_lines[3:],(13/10*np.pi/2,np.pi/2,7/10*np.pi/2,2.8*np.pi/2,3.2*np.pi/2),(1.3,1.3,1.3,1.5,1.5)):
            head_line.set_data([head_posx+head_radius*np.cos(ang),head_posx+head_radius*length*np.cos(ang)],[head_posy+head_radius*np.sin(ang),head_posy+head_radius*length*np.sin(ang)])
        for head_line in head_lines:
            head_line.set_color("black")
            head_line.set_zorder(0)
            head_line.set_lw(0.8)
        for i in range(-1,3):
            trunk_lines[i].set_data([trunkx[i],trunkx[i+1]],[trunky[i],trunky[i+1]])
            trunk_lines[i].set_color("black")
            trunk_lines[i].set_lw(0.8)
        #trunk_lines[3].set_data([trunkx[3],trunkx[i+1]],[trunky[i],trunky[i+1]])
        return patches+pat_texts+hand_lines+head_lines+trunk_lines

    def update(_):
        global frame,t0,pause,cycind
            
        t=(frame*duration/frames)
        
        if int(t0)<int(t):
            
            #print(t,frame,t0s)
            
            #pause=not pause
            
            for pat_text in pat_texts:
                pat_text.set_color("black")
            pat_texts[cycind].set_color("red")
            for ind,_ in enumerate(heights):
                if t>=t0s[ind]:
                    
                    
                    #print("!",ind)
                    #print(t,t0s[ind])
                    if heights[ind]>0:
                        heights[ind]-=1
                    if heights[ind]==0:
                        t0s[ind]=t
                        
                        nh=pattern[cycind]#(cycpat)
                        #print(nh)
                        heights[ind]=nh
                        durs[ind]=nh
                        p0s[ind]=ps[ind]
                        if nh%2==1:
                            thands[ind]*=-1
                        #print(states[ind],durs[ind],nh)
                    
                    #print(t,durs,heights,t0s,thands)
                    #input()
            cycind=(cycind+1)%len(pattern)
        #input()
        
        lhand=handline(t%2,-hand_x,hand_y,2,delay=delay,shift=hand_shift)
        rhand=handline((t+1)%2,hand_x,hand_y,2,delay=delay,shift=-hand_shift)
        lelbow=trunkx[0]+(-trunkx[0]+lhand[0])/5,trunky[0]/2#elbowline(t%2,-hand_x,trunky[0]/2,2)
        relbow=trunkx[1]+(-trunkx[1]+rhand[0])/5,trunky[1]/2#elbowline(t%2,-hand_x,trunky[0]/2,2)

        #hand_lines[0].set_data([-2*hand_x,lhand[0]],[llim,lhand[1]])
        #hand_lines[1].set_data([2*hand_x,rhand[0]],[llim,rhand[1]])
        hand_lines[0].set_data([trunkx[0],lelbow[0]],[trunky[0],lelbow[1]])
        hand_lines[1].set_data([lelbow[0],lhand[0]],[lelbow[1],lhand[1]])
        hand_lines[2].set_data([trunkx[1],relbow[0]],[trunky[1],relbow[1]])
        hand_lines[3].set_data([relbow[0],rhand[0]],[relbow[1],rhand[1]])
        
        for ind,patch in enumerate(patches):
            #x, y = patch.center
            if t<t0s[ind]:
                x,y=p0s[ind][0],p0s[ind][1]
            else:
                #x,y = parabola(t-t0s[ind],p0s[ind][0]+thands[ind]*2.5,p0s[ind][1],thands[ind]*hand_x,hand_y,durs[ind])
                x,y = delayed_throw(t-t0s[ind],p0s[ind][0],p0s[ind][1],thands[ind]*hand_x,hand_y,durs[ind],delay=delay,shift=(-hand_shift if ps[ind][0]>0 else hand_shift))
        
            ps[ind]=patch.center = (x, y)
        t0=t
        if not pause:
            frame=frame+direction*incr
            if frame>frames:
                init()
                frame=0
        return patches+pat_texts+hand_lines+head_lines+trunk_lines

    def onClick(event):
        global pause,direction
        if event.button==1:
            pause = not pause
        if event.button==3:
            direction=-direction
    def onPress(event):
        global pause,incr
        if event.key in [" "]:
            pause= not pause
        elif event.key=="right":
            incr=incr+1            
        elif event.key=="left":
            incr=max(0,incr-1)
    ax.set_aspect('equal')
    anim = FuncAnimation(fig,update,init_func=init,blit=True,interval=1,repeat=True,save_count=frames,frames=frames)
    fig.canvas.mpl_connect('button_press_event', onClick)
    fig.canvas.mpl_connect('key_press_event', onPress)

    plt.show()
    
    #return fig

def delayed_throw(t,x0,y0,x1,y1,tottime,delay=0.5,shift=0):
    if t>tottime-delay:
        #return x1,y1
        return circle(t-tottime+delay,x1,y1,x1+shift,y1,delay)
    else:
        return parabola(t,x0,y0,x1,y1,tottime-delay)
def circle(t,x0,y0,x1,y1,tottime):
    r=(x0-x1)/2
    ang=np.pi/tottime*t*(1 if x1>x0 else -1)
    return (x0+x1)/2+r*np.cos(ang),(y0+y1)/2+r*np.sin(ang)
def parabola(t,x0,y0,x1,y1,tottime):
    if tottime in [0,2]:
        return x0,y0
    vx=(x1-x0)/tottime
    vy=(y1-y0+1/2*g*tottime**2)/tottime
    return x0+vx*t,y0+vy*t-1/2*g*t**2
def handline(t,x1,y1,tottime,delay=0.5,shift=0):
    if t>tottime-delay:
        return circle(t-tottime+delay,x1,y1,x1+shift,y1,delay)
    elif t<delay:
        return circle(t+delay,x1,y1,x1+shift,y1,delay)
    else:
        return x1,y1

def elbowline(t,x1,y1,tottime,delay=0.5,shift=0):
    return x1+np.sin(t*np.pi),y1
#anim(3,"3",t0s=[0,1,2])#,hands=[1,-1,-1])
#anim(3,"51",t0s=[0,1,2],hands=[1,-1,-1])
#anim(4,"35",delay=0.5,happy_state=1)#,t0s=[0,1,2],hands=[1,-1,-1])