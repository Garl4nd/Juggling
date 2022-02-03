# TODO: initial hands interface
# TODO: 1-1 padá
import itertools as it
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import numpy as np
import juggle_condensemod
from juganim import anim
from circ_arrow import circarrowdraw


def check_seq(seq:str):
    nums=[int(s) for s in seq]
    ln=len(nums)
    tv=[]
    for i,num in enumerate(nums):
        if (new_comp:=(num+i) % ln ) in tv:
            return False,0
        else:
            tv.append(new_comp)
    try:
        return True,sum(nums)//ln
    except ZeroDivisionError:
        return True,0

def swap(seq,i,j):
    nums=[int(s) for s in seq]
    i=i-1
    j=j-1
    if nums[i]+i<j:
        raise ValueError("This swap is impossible")
    d=nums[i]
    nums[i]=nums[j]+j-i
    nums[j]=d+i-j
    return "".join(str(num) for num in nums)

def is_valid_throw(state,height,nonzero=False):
    if len(state)<height:
        return False
    elif height<len(state) and state[height]==1:
        return False
    elif state[0]==0 and height>0:
        return False
    elif nonzero and state[1]==0 and height!=1:
        
        return False
    else:
        return True

def throw(state,height):
    #print("beg,height",state,height)
    ls=len(state)
    new_state=list(state)
    for i in range(ls-1):
        new_state[i]=state[i+1]
    new_state[ls-1]=0
    if height>0:
        new_state[height-1]=1
    #print("end",state)
    return new_state
def box_format(state):
    return state.replace("1","O").replace("0","—")
def gen_states(max_height,balls,nonzero=False):
    states=[]
    for comb in it.combinations(range(max_height),balls):
        if nonzero and 0 not in comb:
            continue
        states.append([1 if i in comb else 0 for i in range(max_height)])
    return states
def state_name(state):
    return "".join(str(num) for num in state)

def transitions(state_dict,max_height,nonzero=False):
    
    tdict={}
    for i,(stname,state) in enumerate(state_dict.items()):
        tdict[stname]=[]
        for height in range(max_height+1):
            if is_valid_throw(state,height,nonzero=nonzero):
                
                new_state=throw(state,height)
                #print("valid:",state,new_state)
                tdict[stname].append((state_name(new_state),height))
    return tdict

def find_height(s1,s2):
    res=0
    matches=0
    s1=[int(h) for h in s1]
    s2=[int(h) for h in s2]
    for i in range(len(s1)-1):
        
            
        if (s2[i]==1 and s1[i+1]==0):
            res=i+1
            matches+=1
    if s2[-1]==1:
        res=len(s1)
        matches+=1
    if matches<2:
        return res
    else:
        return -1
    
    #if (int(s2[-1])==1):
    #    return len(s1)  
    #else:
    #    return 0
def sideswaps(loop):
    
    s=loop+[loop[0]]
    sw=""
    for i in range(len(loop)):
        sw+=str(find_height(s[i],s[i+1]))
    return sw

def draw_diagram(fig,ax,max_height,balls,figname="juggle_state_graph.png",by_loops=False,nonzero=True,save=False,show=False):
    global artists,tdict,hand_shift,happy_state
    #class Box:
    #    def __init__(self,text_obj,annotation):
    #        self.text_obj=text_obj
    #        self.annotation=annotation
    
    boxes={}#[]      
    clicked=[]
    pattern=[]
    artists=[]
    states=gen_states(max_height,balls,nonzero=nonzero)
    #if save:
    #    fig,ax=plt.subplots(figsize=(12,12))
    #else:    
    #    fig,ax=plt.subplots()
    ax.set_xlim(-1.5,1.5)
    ax.set_ylim(-1.5,1.5)
    n=len(states)
    max_height=len(states[0])
    colors=plt.rcParams['axes.prop_cycle'].by_key()['color']
    
    #print(len(colors))
    #print(f"{idict=},{depdict=}")
    angs=[2*3.14/n*i for i in range(n)]
    #stnames=["".join(str(num) for num in state) for state in states]
    state_dict=dict((state_name(state),state) for state in states)
    xposar={key:np.cos(ang) for key,ang in zip(state_dict,angs)}
    yposar={key:np.sin(ang) for key,ang in zip(state_dict,angs)}
    #print(xposar)
    arwidth=0.01
    tdict=transitions(state_dict,max_height,nonzero=nonzero)
    #print(tdict,state_dict)
    uclabels=[]
    if by_loops:
        rdict={key:[l[0] for l in val ] for key,val in tdict.items()}
        #print("rdict",rdict)
        loops=[]
        initials=juggle_condensemod.get_initials(rdict)
        if not initials:
            initials=[next(iter(rdict))]
        for initial in initials:
            res=juggle_condensemod.make_el_loops(initial,rdict)
        sws=[]
        for loop in res:
            sws.append(sideswaps(loop))
            if loop not in loops:
                if nonzero:
                    if "0" in sws[-1]:
                        continue
                loops.append(loop)
        if len(loops)>10:
            colors=[[random.random() for _ in range(3)] for _ in range(100)]
    #print(tdict)
    labboxes={stname:[[],[]] for stname in state_dict.keys()}
    
    for i,(stname,state) in enumerate(state_dict.items()):
        xpos,ypos=xposar[stname],yposar[stname]
        #boxes.append(Box(ax.text(xpos,ypos,state,bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'),ha="center"),stname))
        boxes[stname]=ax.text(xpos,ypos,box_format(stname),bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'),ha="center")
        
        #print(f"{deps=}")
        
        for new_state,height in tdict[stname]:
        #for height in range(max_height+1):
        #    if is_valid_throw(state,height):
                #new_state=throw(state,height)
                
                if new_state==stname:
                    #print(state,new_state,height,"same")
                    radius=0.1+height*0.025
                    circarrowdraw(ax,xpos,ypos,radius=radius,aspect=1,color="black",lw=height*0.5)#color=colors[height%10]
                    ax.text(xpos,ypos-2*radius*0.98,height)
                else:
                    xpos2=xposar[new_state]
                    ypos2=yposar[new_state]
                    if not by_loops:
                    #print(state,new_state,height,"dif")
                        dx=xpos2-xpos
                        dy=ypos2-ypos
                        if xpos2>xpos:
                            shift=-0.02
                        else:
                            shift=0.02

                        xloc,yloc=xpos+shift,ypos+shift
                        
                        ax.arrow(xloc,yloc,0.85*dx,0.85*dy,width=height*0.002,head_width=height*0.02+0.01,color=colors[height%10])    
                        #ax.text(xloc+0.85*dx+0.075*dy,yloc+0.85*dy-0.075*dx,s=height,fontsize=12,color=colors[height%10])
                        ax.text(xloc+0.6*dx,yloc+0.6*dy,s=height,fontsize=12,color=colors[height%10],zorder=10,bbox=dict(facecolor="white", edgecolor='black', boxstyle='circle'),ha="center",va="center")
    if by_loops:
        #print("loopnum:",len(loops))
        targdict={}
        for loopind,loop in enumerate(loops):
            if len(loop)>1:
                ext_loop=loop+[loop[0]]
                for i,_ in enumerate(loop):
                    s1,s2=ext_loop[i:i+2]
                    targdict[(s1,s2)]=targdict.get((s1,s2),-1)+1
                    xpos,ypos=xposar[s1],yposar[s1]
                    xpos2,ypos2=xposar[s2],yposar[s2]
                    height=find_height(s1,s2)
                    dx=xpos2-xpos
                    dy=ypos2-ypos
                    offset=0.0
                    hoffset=0.0
                    if xpos2>xpos:
                        shift=-0.02
                    else:
                        shift=0.02
                    xloc,yloc=xpos+shift,ypos+shift
                    #scaleback=1-0.1*targdict[(s1,s2)] if targdict[(s1,s2)]<9 else 0#0.1-0.01*targdict[(s1,s2)]
                    if targdict[(s1,s2)]<9:
                        scaleback=1-0.1*targdict[(s1,s2)]
                        ax.arrow(xloc+offset*loopind,yloc+offset*loopind,0.85*dx*scaleback,0.85*dy*scaleback,width=height*0.002,head_width=height*0.02+0.01,color=colors[loopind%10])    
                    #ax.text(xpos+0.1*dx+0.1*dx+toffset*3*loopind+offset*height,ypos+0.5*dy+0.1*dy+toffset*loopind+offset*height,s=height*2,color=colors[loopind%10])
                        if targdict[(s1,s2)]==0:
                            #ax.text(xloc+0.85*dx+0.075*dy,yloc+0.85*dy-0.075*dx,s=height,fontsize=12,color=colors[loopind%10],zorder=10)
                            ax.text(xloc+0.6*dx,yloc+0.6*dy,s=height,fontsize=12,color="black",zorder=10,bbox=dict(facecolor="white", edgecolor='black', boxstyle='circle'),ha="center",va="center")
    
    if save:
        fig.savefig(figname)
    if show:
            plt.show()

    def onClick(event):
        global artists,tdict
        if event.button==1:
            x,y=event.x,event.y
            x,y=ax.transData.inverted().transform((x,y))
            
            loop=False
            #found=False
            for annotation,text_obj in boxes.items():
                extent=text_obj.get_window_extent().inverse_transformed(ax.transData)
                #extent=box.text_obj.get_tightbbox(renderer).inverse_transformed(ax.transData)
                w=extent.x1-extent.x0
                h=extent.y1-extent.y0
                if extent.x0-w/2<x<extent.x1+w/2 and extent.y0-h/2<y<extent.y1+h/2:
                
                    #found=True
                    
                    
                    if len(clicked)>0:
                        if annotation==clicked[0]:
                            loop=True
                        height=find_height(clicked[-1],annotation)
                        #print(height)
                        if height==-1:
                            break
                    clicked.append(annotation)
                    
                    
                    text_obj.set_backgroundcolor("yellow")
                    labboxes[annotation][0].append(len(clicked))
                    labboxes[annotation][1].append(ax.text(extent.x0+1.2*w,extent.y0+1.2*h,",".join(str(s) for s in labboxes[annotation][0]),bbox=dict(facecolor='none', edgecolor='red', boxstyle='round,pad=1')))
                    for labbox in labboxes[annotation][1][:-1]:
                        labbox.set_visible(False)
                    labboxes[annotation][1][:-1].clear()
                    for text_obj2 in boxes.values():
                        text_obj2.get_bbox_patch().set_edgecolor("#000000")
                    for target,_ in tdict[annotation]:
                        boxes[target].get_bbox_patch().set_edgecolor("#0000CC")
                            
                    #labboxes[box.annotation][1][:].clear()
            
                    if len(clicked)>1:
                
                
                
                        pattern.append(height)#=[find_height(clicked[i],clicked[i+1]) for i,_ in enumerate(clicked[:-1])]
                        is_seq,nballs=check_seq(pattern)
                        valid=is_seq and balls==nballs
                        uclabels.append(ax.text(-1.4+0.1*len(uclabels),1.4,height))
                        for uclabel in uclabels:
                                        uclabel.set_color("black")
                        if loop:
                            
                            for annotation,text_obj in boxes.items():
                                if annotation in clicked:
                                    #is_seq,nballs=check_seq(pattern)
                                    if valid:
                                        text_obj.set_backgroundcolor("green")
                                        for uclabel in uclabels:
                                            uclabel.set_color("green")
                                    else:
                                        #failed=True
                                        text_obj.set_backgroundcolor("red")
                                        for uclabel in uclabels:
                                            uclabel.set_color("red")
                            for artist in artists:
                                artist.remove()
                            artists.clear()
                            #artists=DrawPattern(pattern,ax,xstart=-1.45,ystart=1,width=0.8,height=0.3,valid=valid)
                            artists=DrawPattern(pattern,ax,xstart=-0.75,ystart=1.1,width=0.8*2,height=0.3,valid=valid,ncirc=20)
                    break    
            fig.canvas.draw()
            fig.canvas.flush_events()
            

        if event.button==3:
            clicked.clear()
            pattern.clear()
            for artist in artists:
                artist.remove()
            artists.clear()
            for labbox in labboxes.values():
                labbox[0].clear()
                for tbox in labbox[1]:
                    tbox.remove()#set_visible(False)
                labbox[1].clear()
                
                        
            for uclabel in uclabels:
                uclabel.remove()
                #uclabel.set_visible(False)
            uclabels.clear()
            for text_obj in boxes.values():
                text_obj.set_backgroundcolor("white")
                text_obj.get_bbox_patch().set_edgecolor("#000000")
                fig.canvas.draw()
                fig.canvas.flush_events()

    def onPress(event):

        if event.key in ["a","enter"] :
            if clicked:
                #eclicked=clicked+[clicked[0]]
                #pattern=[find_height(clicked[i],clicked[i+1]) for i,_ in enumerate(clicked[:-1])]
                #uclabels.append(ax.text(-1.4,1.4,pattern))
                wtimes=[]
                for i,h in enumerate(clicked[0]):
                    
                    if h=="1":
                        wtimes.append(i)
                anim(balls,pattern,delay=0.75,t0s=wtimes,hand_shift=hand_shift,happy_state=happy_state)

    cid=fig.canvas.mpl_connect("button_press_event",onClick)
    pid=fig.canvas.mpl_connect("key_press_event",onPress)
    return uclabels,labboxes,cid,pid

def DrawPattern(pattern,ax=None,xstart=0.0,ystart=0.0,height=1,width=1,ncirc=12,valid=True):
    if ax==None:
        ax=plt.gca()
    pattern=[int(p) for p in pattern]
    cycpat=it.cycle(pattern)
    cyccol=it.cycle(("blue","green") if valid else ("red",))
    cycshape=it.cycle(("circle","square"))#if valid else ("red",))
    maxdur=max(pattern)
    artists=[]
    #circtxt=[]
    #parabolas=[]
    balls=sum(pattern)//len(pattern)
    maxpat=[p for p,_ in zip(it.cycle(pattern),range(ncirc))]
    orbits={}#{i:0 for i in range(ncirc)}
    for bp in range(balls):
        i=bp
        
        while i in orbits:
            i+=1
        if maxpat[i]>0:
            while i<ncirc:
                orbits[i]=bp
                i+=maxpat[i]
        
    

    def parabola(x,x0,x1,dx=1):
        
        
        t=x-x0
        dur=x1-x0
        return x,4*t*(dur-t)/(maxdur*dx)**2
    
    try:
        dx=width/(ncirc-1)
    except ZeroDivisionError:
        dx=0
    throw_cols=[c for c,_ in zip(it.cycle(("red","blue","green","yellow","pink") if valid else ("red",)),range(balls))]
    for i,dur,col,shape in zip(range(ncirc),cycpat,cyccol,cycshape):
        xpos=i*dx
        tcol=col
        
        
        tcol=throw_cols[orbits.get(i,0)]
        txt=ax.text(xstart+xpos,ystart,dur,bbox=dict(facecolor='none', edgecolor="black", boxstyle=shape),ha="center",va="center")
        #circtxt.append(txt)
        artists.append(txt)
        plt.gcf().canvas.draw()
        bb=txt.get_window_extent().inverse_transformed(ax.transData)

        y0=bb.y1
        x0=xstart+xpos
        x1=x0+dur*dx
        xin=np.linspace(x0,x1,50)
        x,y=parabola(xin,x0,x1,dx=dx)
        y=y0+height*y
        if i+dur<ncirc:
            artists.append(ax.plot(x,y,c=tcol)[0])
    
    return artists

def interface(balls=3,max_height=5,save=False):
    global uclabels,labboxes,by_loops,hide_zeros,hand_shift,happy_state,cid,pid
    uclabels=None
    labboxes=None
    by_loops=True
    hide_zeros=True
    cid=None
    pid=None
    hand_shift=3
    happy_state=1
    global ax2
    state={"balls":balls,"max_height":max_height}
    if save:
        fig,ax=plt.subplots(figsize=(12,12))
        fig.canvas.draw()
    else:    
        fig,ax=plt.subplots()
        fig.canvas.draw()
    ax2=ax.twinx()
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    ax.set_xlim(-1.5,1.5)
    ax.set_ylim(-1.5,1.5)
    arrow_x=-0.9
    arrow_y=1.7
    arrow_w=0.1
    arrow_h=0.1
    ax.text(-1.0,1.9,"Number of balls",ha="center")
    ballnum_text=ax.text(-1.0,1.7,state["balls"],fontsize=20,bbox=dict(facecolor='none', edgecolor='black', boxstyle='circle'),ha="center",va="center")
    #ax.scatter(-0.9,1.8,marker="^",color="blue",s=500,clip_on=False)
    #ax.scatter(-0.9,1.6,marker="v",color="blue",s=500,clip_on=False)

    ax.add_patch(mpatches.Polygon([[arrow_x,arrow_y],[arrow_x+arrow_w,arrow_y],[arrow_x+arrow_w/2,arrow_y+arrow_h]],clip_on=False))
    ax.add_patch(mpatches.Polygon([[arrow_x,arrow_y-arrow_h/3],[arrow_x+arrow_w,arrow_y-arrow_h/3],[arrow_x+arrow_w/2,arrow_y-arrow_h-arrow_h/3]],clip_on=False))
    ax.text(-0.4,1.9,"Maximum duration",ha="center")
    height_text=ax.text(-0.4,1.7,state["max_height"],fontsize=20,color="black",bbox=dict(facecolor='none', edgecolor='black', boxstyle='circle'),ha="center",va="center")
    
    
    harrow_x=-0.3
    harrow_y=1.7
    harrow_w=0.1
    harrow_h=0.1
    ax.add_patch(mpatches.Polygon([[harrow_x,harrow_y],[harrow_x+harrow_w,harrow_y],[harrow_x+harrow_w/2,harrow_y+harrow_h]],clip_on=False))
    ax.add_patch(mpatches.Polygon([[harrow_x,harrow_y-harrow_h/3],[harrow_x+harrow_w,harrow_y-harrow_h/3],[harrow_x+harrow_w/2,harrow_y-harrow_h-harrow_h/3]],clip_on=False))

    
    refr_text=ax.text(0.5,1.7,"Generate",fontsize=15,bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'),ha="center",va="center")
    refr_extent=refr_text.get_window_extent().inverse_transformed(ax.transData)
    loop_text=ax.text(-1.5,1.85,"Show loops",fontsize=10,color="red",bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'),ha="center",va="center")
    looptxt_extent=loop_text.get_window_extent().inverse_transformed(ax.transData)
    zero_text=ax.text(-1.5,1.65,"Hide zeros",fontsize=10,color="red",bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'),ha="center",va="center")
    zerotxt_extent=zero_text.get_window_extent().inverse_transformed(ax.transData)
    inout_text=ax.text(-1.25,1.85,"Reverse throws",fontsize=10,color="black",bbox=dict(facecolor='none', edgecolor='black', boxstyle='round'),ha="center",va="center")
    inout_extent=inout_text.get_window_extent().inverse_transformed(ax.transData)
    happy_state_text=ax.text(-1.25,1.65,"happy",fontsize=10,color="black",bbox=dict(facecolor='none', edgecolor='black', boxstyle='round'),ha="center",va="center")
    happy_state_extent=happy_state_text.get_window_extent().inverse_transformed(ax.transData)

    objs={"bup":(arrow_x,arrow_x+arrow_w,arrow_y,arrow_y+arrow_h),"bdown":(arrow_x,arrow_x+arrow_w,arrow_y-arrow_h/3-arrow_h,arrow_y-arrow_h/3),
    "hup":(harrow_x,harrow_x+harrow_w,harrow_y,harrow_y+harrow_h),"hdown":(harrow_x,harrow_x+harrow_w,harrow_y-harrow_h/3-harrow_h,harrow_y-harrow_h/3),
    "refr":(refr_extent.x0,refr_extent.x1,refr_extent.y0,refr_extent.y1),"loops":(looptxt_extent.x0,looptxt_extent.x1,looptxt_extent.y0,looptxt_extent.y1),
    "zeros":(zerotxt_extent.x0,zerotxt_extent.x1,zerotxt_extent.y0,zerotxt_extent.y1),"inout":(inout_extent.x0,inout_extent.x1,inout_extent.y0,inout_extent.y1),
    "happy_state_sad":(happy_state_extent.x0,happy_state_extent.x1,happy_state_extent.y0,happy_state_extent.y1)}

    def handle_signal(event):
        global labboxes,uclabels,by_loops,hide_zeros,hand_shift,cid,pid,happy_state
        
        detected=None
        try:
            if event.button==1:
                x,y=event.x,event.y
                x,y=ax.transData.inverted().transform((x,y))
                
                for name,(x0,x1,y0,y1) in objs.items():
                    if x0<x<x1 and y0<y<y1:
                        detected=name
                        print(x0,x,x1,y0,y,y1)
        except AttributeError:
            if event.key in ["r","g"]:
                detected="refr"
        if detected:
            print(detected)
            if detected=="bup":
                if state["max_height"]>state["balls"]:
                    state["balls"]+=1
            if detected=="bdown":
                if state["balls"]>0:
                    state["balls"]-=1
            if detected=="hup":
                state["max_height"]+=1
            if detected=="hdown":
                if state["max_height"]>state["balls"]:
                    state["max_height"]-=1
            
        #ballnum_text.remove()#=ax.text(-1.0,1.7,state["balls"],fontsize=20,bbox=dict(facecolor='none', edgecolor='black', boxstyle='circle'),ha="center",va="center")
            ballnum_text.set_text(state["balls"])
            height_text.set_text(state["max_height"])
            if detected=="loops":
                if by_loops:
                    loop_text.set_color("black")
                else:
                    loop_text.set_color("red")
                by_loops=not by_loops
            if detected=="zeros":
                if hide_zeros:
                    zero_text.set_color("black")
                else:
                    zero_text.set_color("red")
                hide_zeros=not hide_zeros
            if detected=="inout":
                if hand_shift>0:
                    inout_text.set_color("red")#set_text("Outside throw")
                else:
                    inout_text.set_color("black")
                    #inout_text.set_text("Inside throw")
                hand_shift*=-1
            if detected=="happy_state_sad":
                if happy_state==1:
                    happy_state_text.set_text("  Sad  ")
                    happy_state=0
                elif happy_state==2:
                    happy_state_text.set_text("Happy")
                    happy_state=1
                else:
                    happy_state_text.set_text("  meh  ")
                    happy_state=2
                    #inout_text.set_text("Inside throw")
                
            if detected=="refr":
                #ax.cla()
                ax2.cla()
                refr_text.set_text("Refresh")#generated
                if uclabels:
                    for uclabel in uclabels:
                        uclabel.remove()
                    uclabels.clear()
                if labboxes:
                    for labbox in labboxes.values():
                        #labbox[0].clear()
                        for tbox in labbox[1]:
                            tbox.remove()#set_visible(False)
                        labbox.clear()
                #uclabel.set_visible(False)
                
                if cid:
                    fig.canvas.mpl_disconnect(cid)
                    fig.canvas.mpl_disconnect(pid)

                uclabels,labboxes,cid,pid=draw_diagram(fig,ax2,balls=state["balls"],max_height=state["max_height"],show=False,by_loops=by_loops,nonzero=hide_zeros)
            fig.canvas.draw()
            fig.canvas.flush_events()
    fig.canvas.mpl_connect("button_press_event",handle_signal)
    fig.canvas.mpl_connect("key_press_event",handle_signal)

print(check_seq("4233"))
print(swap("441",1,3))

state=[1,1,1,0,0,0]
print(is_valid_throw(state,2))
print(throw([1,0,1,0,1],1))
#print(gen_states(5,3))


#states=gen_states(max_height=5,balls=3)
#state_dict=dict((state_name(state),state) for state in states)
#tdict=transitions(state_dict)


#for loops,stname in zip(loops_ar,state_dict.keys()):
    #print(loops,stname)
#    print([sideswaps(list(loop)) for loop in loops])

#anim(7,"7865795354",delay=0.5)
#draw_diagram(max_height=5,balls=4,show=False,by_loops=True,nonzero=True)
interface()
#matplotlib.use("TkAgg")
#plt.ion()
#fig,ax=plt.subplots()
#DrawPattern("504")
#anim(3,"52512",hands=[1,1,-1],delay=0.5)
plt.show()