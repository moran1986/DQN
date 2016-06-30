#!/usr/bin/python
import sys
import random
import pygame
import re
from PIL import Image
from pygame.locals import *
import os
import datetime
import linecache
def getCards():
    global deck, values, suits
    values = '2 3 4 5 6 7 8 9 10 j q k A'.split()
    suits = 'c d h s'.split()
    deck = ["%s%s" % (v, s) for v in suits for s in values]
def shuffleDeck():
    global deck
    s = 1
    random.seed()
    while s <= 3: 
        random.seed()
        random.shuffle(deck)
        s += 1
def player_order(order):
    global p1,p2,position_flag
    text_temp=order.split('|')
    p1=text_temp[0]
    p2=text_temp[1]
    if p1 == "B":
        position_flag=1;
    else:
        position_flag=0;
    
def action_seq(actions):
    global  total_round,pre_flop,flop,turn,river
    text_temp=actions.split('/')
    total_round = len(text_temp)
    pre_flop=text_temp[0]
    if total_round > 1:
        flop=text_temp[1]
    if total_round > 2:
        turn=text_temp[2]
    if total_round > 3:
        river=text_temp[3]

def get_cards(all_cards):
    global card_p1,card_p2,c3,c4,c5
    text_temp=all_cards.split('/')
    card_temp=text_temp[0].split('|')
    card_p1=card_temp[0][::-1].lower()
    card_p2=card_temp[1][::-1].lower()
    if total_round > 1:
        c3=text_temp[1][::-1].lower()
    if total_round > 2:
        c4=text_temp[2][::-1].lower()
    if total_round > 3:
        c5=text_temp[3][::-1].lower()
    print card_p1+" "+card_p2+" "+c3+" "+c4+" "+c5
def get_results(results):
    text_temp=results.split('|')
    result_1p=text_temp[0]
    result_2p=text_temp[1]

def main():

    HAND_NUM = 2
    PUBLIC_CARD_NUM = 5
    ROUND_NUM = 4

    currentPlay=""


    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800, 512))
    pygame.display.set_caption('2-limited Texas Hold\'em Poker')
    # Fill screen

    screen.fill((39, 119, 20))
    
    def deal(obj, pos, mx, my, obj2):   
        pos = pos.move(mx,  my)
        screen.blit(obj2, pos)
        pygame.display.update()
           

    def retract(obj, pos, mx, my):  
        pos = pos.move(mx,  my)
        screen.blit(obj2, pos)
        pygame.display.update()
    pygame.time.wait(100)

    my_rect=pygame.Rect(100, 50,150,100)
    my_rect2=pygame.Rect(100, 350,150,100)
##################################################    
    #du qu wenjian 
    f=open("wpc.log","rw+")
    #with open('1.log') as f:
    f1 ="wpc.log"
    pre_time=os.path.getmtime(f1)
    #while 1!=0:
        #if pre_time!=os.path.getmtime(f1) :
        #    pre_time=os.path.getmtime(f1)
        #    print "false"
    i_l=1
    while True:
        with open('wpc.log') as f:
            with open('wpc.log') as f:
                j_l=1
                for line in f:
                    if line and len(line)>=3:
                        if j_l>=i_l:
                            print str(i_l)+"^^^^^^FSADA"+line
                            i_l+=1
                        j_l+=1
                        if line[0] == 'S':
                            if line[1] == 'T':
                                ls=line.split(':')
                                currentState=ls[1]
                                actions=ls[2]
                                all_cards=ls[3]
                                results=ls[4]
                                order=ls[5]
                                action_seq(actions)
                                get_cards(all_cards)
                                player_order(order)

             ############################
                                screen.fill((39,119,20))# clear
                                pygame.display.update()
                                finish_state=0 
                                global sb,bb
                                font = pygame.font.Font(None, 36)
                                bb=10
                                sb=5
                                def print_b(sb,bb,d,f):   # da yin tu xiang 
                                    #screen.fill((39, 119, 20))
                                    #pygame.time.delay(200)
                                    pygame.draw.rect(screen,[39, 119, 20],my_rect,0)
                                    pygame.draw.rect(screen,[39, 119, 20],my_rect2,0)
                                    pygame.time.delay(300)
                                    if f==0:
                                        s1=font.render(d+"   "+str(sb), 1, (0, 255, 255))
                                        s2=font.render(str(bb), 1, (0, 255, 200))
                                    else:
                                        s1=font.render(str(sb), 1, (0, 255, 255))
                                        s2=font.render(d+"   "+str(bb), 1, (0, 255, 200))
                                    if position_flag ==1:
                                        numpos1 = s1.get_rect(center=(170, 100))
                                        numpos2 = s2.get_rect(center=(170, 400))
                                    else:
                                        numpos1 = s1.get_rect(center=(170, 400))
                                        numpos2 = s2.get_rect(center=(170, 100))

                                    screen.blit(s1, numpos1)
                                    screen.blit(s2, numpos2)
                                    pygame.display.update()
                                    
                            
                                ################################################# 
                                
                                def pre_action(pre_flop):
                                    sum=0
                                    global sb,bb
                                    for c in pre_flop:
                                        if c =='c':
                                            if sb < bb:
                                                sb=bb
                                            else:
                                                bb=sb
                                            d="Call"
                                            if sum%2==0:
                                                f=0
                                            else :
                                                f=1
                                        elif c == 'r':
                                            if sum%2 ==0 and sb < bb:
                                                sb+=bb-sb+10
                                            elif sum%2==1 and sb>bb :
                                                bb+=sb-bb+10
                                            else:
                                                if sum%2 == 0:
                                                    sb+=bb-sb+10
                                                else:
                                                    bb+=sb-bb+10
                                            d="Raise"
                                            if sum%2==0:
                                                f=0
                                            else :
                                                f=1
                                        else:
                                            finish_state=1
                                            print "finishhhhhhh"
                                            d="Fold"
                                            if sum%2==0:
                                                f=0
                                            else :
                                                f=1
                                        sum+=1
                                        print_b(sb,bb,d,f)

                                def npre_action(flop,add_size):
                                    sum=0
                                    global sb,bb
                                    for c in flop:

                                        if c =='c':
                                            if sb < bb:
                                                sb=bb
                                            else:
                                                bb=sb
                                            d="Call"
                                            if sum%2==0:
                                                f=1
                                            else :
                                                f=0
                                        elif c == 'r':
                                            if sum%2 ==1 and sb < bb:
                                                sb+=bb-sb+add_size
                                            elif sum%2==0 and sb>bb :
                                                bb+=sb-bb+add_size
                                            else:
                                                if sum%2 == 1:
                                                    sb+=bb-sb+add_size
                                                else:
                                                    bb+=sb-bb+add_size
                                            d="Raise"
                                            if sum%2==0:
                                                f=0
                                            else :
                                                f=1
                                        else:
                                            finish_state=1
                                            print "finishhhhhhh"
                                            d="Fold"
                                            if sum%2==0:
                                                f=0
                                            else :
                                                f=1
                                        sum+=1
                                        
                                        print_b(sb,bb,d,f)
                                        
                                        
                                card1 = Image.open("cards/%s.png" % c3[0:2]) ; card1 = card1.convert("RGBA")
                                card2 = Image.open("cards/%s.png" % c3[2:4]); card2 = card2.convert("RGBA")
                                card3 = Image.open("cards/%s.png" % c3[4:6]) ; card3 = card3.convert("RGBA")
                                card4 = Image.open("cards/%s.png" % c4) ; card4 = card4.convert("RGBA")
                                card5 = Image.open("cards/%s.png" % c5) ; card5 = card5.convert("RGBA")
                                card6 = Image.open("cards/%s.png" % card_p1[0:2]) ; card6 = card6.convert("RGBA")
                                card7 = Image.open("cards/%s.png" % card_p1[2:4]) ; card7 = card7.convert("RGBA")
                                card8 = Image.open("cards/%s.png" % card_p2[0:2]) ; card8 = card8.convert("RGBA")
                                card9 = Image.open("cards/%s.png" % card_p2[2:4]) ; card9 = card9.convert("RGBA")
                                back = Image.open("cards/back.png") ; back = back.convert("RGBA")
                                dbb = Image.open("cards/over.png") ; dbb = dbb.convert("RGBA")
                                m = card1.mode
                                s = card1.size
                                data1 = card1.tostring()
                                data2 = card2.tostring()
                                data3 = card3.tostring()
                                data4 = card4.tostring()
                                data5 = card5.tostring()
                                data6 = card6.tostring()
                                data7 = card7.tostring()
                                data8 = card8.tostring()
                                data9 = card9.tostring()
                                card1b = pygame.image.fromstring(data1, s, m)
                                card2b = pygame.image.fromstring(data2, s, m)
                                card3b = pygame.image.fromstring(data3, s, m)
                                card4b = pygame.image.fromstring(data4, s, m)
                                card5b = pygame.image.fromstring(data5, s, m)
                                card6b = pygame.image.fromstring(data6, s, m)
                                card7b = pygame.image.fromstring(data7, s, m)
                                card8b = pygame.image.fromstring(data8, s, m)
                                card9b = pygame.image.fromstring(data9, s, m)

                                bm = back.mode
                                bs = back.size
                                bd = back.tostring()
                                b0=b1=b2=b3=b4=b5= pygame.image.fromstring(bd, bs, bm)
                                db = dbb.tostring()
                                re = pygame.image.fromstring(db, bs, bm)

                                pos1=pos2=pos3=pos4=pos5=b0.get_rect(topleft=(700, 350))
                                pos1=b0.get_rect(topleft=(200, 200))
                                pos2=b0.get_rect(topleft=(300, 200))
                                pos3=b0.get_rect(topleft=(400, 200))
                                pos4=b0.get_rect(topleft=(500, 200))
                                pos5=b0.get_rect(topleft=(600, 200))  
                               
                                #deal(b1, pos1, -55, -15, card1b)# gonggong pai 
                                #deal(b2, pos2, -45, -15, card2b)
                                #deal(b3, pos3, -35, -15, card3b)
                                #deal(b4, pos4, -25, -15, card4b)
                                #deal(b5, pos5, -15, -15, card5b)
                               

                                if position_flag ==1 :

                                    deal(b1, pos5, -290, -170, card6b)#shangmian de pai 
                                    deal(b2, pos5, -180, -170, card7b)

                                    deal(b3, pos5, -290, 150, card8b)# xia mian de  pai 
                                    deal(b4, pos5, -180, 150, card9b)
                                else:
                                    deal(b1, pos5, -290, -170, card8b)#shangmian de pai 
                                    deal(b2, pos5, -180, -170, card9b)
                                    deal(b3, pos5, -290, 150, card6b)# xia mian de  pai 
                                    deal(b4, pos5, -180, 150, card7b)

                               ################################################## 
                                screen.blit(b0, (700, 350)); screen.blit(b0, (700, 350));#you xia jiao de  pai
                                screen.blit(b0, (702, 352)); screen.blit(b0, (702, 352));
                                screen.blit(b0, (704, 354)); screen.blit(b0, (704, 354));
                                screen.blit(b0, (706, 356)); screen.blit(b0, (706, 356));


                                for i in range(0,total_round):
                                    if i == 0:
                                        pre_action(pre_flop)
                                       
                                        #survivedtext = font.render(str((90000-pygame.time.get_ticks())/60000)+":"+str((90000-pygame.time.get_ticks())/1000%60).zfill(2), True, (0,0,0))
                                        #textRect = survivedtext.get_rect()
                                        #textRect.topright=[635,5]
                                        #screen.blit(survivedtext, textRect)
                                        #print str(bb)+"  "+str(sb)
                                    elif i == 1:
                                        deal(b1, pos1, -55, -15, card1b)# gonggong pai 
                                        deal(b2, pos2, -45, -15, card2b)
                                        deal(b3, pos3, -35, -15, card3b)
                                        pygame.time.delay(500)
                                        npre_action(flop,10)
                                        #print str(bb)+"  "+str(sb)
                                        #pygame.time.wait(200) 
                                    elif i == 2:
                                        deal(b4, pos4, -25, -15, card4b)
                                        pygame.time.delay(500)
                                        npre_action(turn,20)
                                        #print str(bb)+"  "+str(sb)
                                    else :
                                        deal(b5, pos5, -15, -15, card5b)
                                        pygame.time.delay(500)
                                        npre_action(river,20)
                                        print str(bb)+"  "+str(sb)
                                        #print_b(sb,bb)




                                
                                handvalues = " " + deck[0][1:] + " " + deck[1][1:] + " " + deck[2][1:] + " " + deck[3][1:] + " " + deck[4][1:] + " "
                                handsuits  = " " + deck[0][:1] + " " + deck[1][:1] + " " + deck[2][:1] + " " + deck[3][:1] + " " + deck[4][:1] + " "

                                rf = font.render("ROYAL FLUSH", 1, (0, 255, 255))
                                sf = font.render("STRAIGHT FLUSH", 1, (0, 255, 200))
                                fk = font.render("FOUR OF A KIND", 1, (0, 255, 150))
                                fh = font.render("FULL HOUSE", 1, (0, 255, 100))
                                fl = font.render("FLUSH", 1, (0, 255, 75))
                                st = font.render("STRAIGHT", 1, (0, 255, 50))
                                tk = font.render("THREE OF A KIND", 1, (0, 255, 0))
                                tp = font.render("TWO PAIR", 1, (12, 255, 0))
                             
                                textpos = rf.get_rect(center=(420, 470))
                                straights=["[k|q|j|10|9]", "[q|j|10|9|8]", "[j|10|9|8|7]", 
                                           "[10|9|8|7|6]", "[9|8|7|6|5]" , "[8|7|6|5|4]" , 
                                           "[7|6|5|4|3]", "[6|5|4|3|2]"]

                                def isRoyal():
                                    global isRoyal
                                    if handvalues == "a k q j 10":
                                        if 5 in {handsuits.count('c'), handsuits.count('d'), handsuits.count('s'), handsuits.count('h')}:
                                            screen.blit(rf, textpos)
                                            isRoyal = (0 == 0)
                                def isStraightFlush():
                                    global isStraightFlush
                                    if isRoyal: return
                                    if 5 in {handsuits.count('c'), handsuits.count('d'), handsuits.count('s'), handsuits.count('h')}:
                                        for x in straights:
                                            reg = re.compile(x)
                                            if reg.match(handvalues):
                                                screen.blit(sf, textpos)
                                                isStraightFlush = (0 == 0)
                                def isFourKind():
                                    for x in values:
                                        if handvalues.count(' ' + x + ' ') == 4:
                                            screen.blit(fk, textpos)
                                def isFullHouse():
                                    for x in values:
                                        if handvalues.count(' ' + x + ' ') == 3:
                                            for y in values:
                                                if handvalues.count(y) == 2:
                                                    screen.blit(fh, textpos)
                                                    return
                                def isFlush():
                                    if isRoyal: return
                                    if isf: return
                                    if 5 in {handsuits.count('c'), handsuits.count('d'), handsuits.count('s'), handsuits.count('h')}:
                                        screen.blit(fl, textpos)
                                        return
                                def isStraight():
                                    if isRoyal: return
                                    if isStraightFlush: return
                                    for x in straights:
                                        reg = re.compile(x)
                                        if reg.match(handvalues):
                                            screen.blit(st, textpos)
                                            return
                                def isThreeKind():
                                    for x in values:
                                        if handvalues.count(' ' + x + ' ') == 3:
                                            screen.blit(tk, textpos)
                                            return
                                def isTwoPair():
                                    global itp
                                    itp = (0 == 1)
                                    for x in values:
                                        if handvalues.count(' ' + x + ' ') == 2:
                                            firstPair = x
                                            itp = (0 == 1)
                                            for y in values:
                                                if y is not firstPair:
                                                    if handvalues.count(y) == 2:
                                                        screen.blit(tp, textpos)
                                                        itp = (0 == 0)
                                                        return
                                def isPair():
                                    global ip
                                    cond = itp
                                    ip = (0 == 1)
                                    if not itp:
                                        for x in values:
                                            if handvalues.count(' ' + x + ' ') == 2:
                                                if x == "k":
                                                    x = "KING"
                                                if x == "q":
                                                    x = "QUEEN"
                                                if x == "j":
                                                    x = "JACK"
                                                if x == "1":
                                                    x = "ACE"
                                                screen.blit(font.render("PAIR OF %sS" % (x), 1, (100, 255, 0)), textpos)
                                                ip = (0 == 0)
                                                if itp:
                                                    ip = (0 == 0)
                                                    return
                                  
                                isRoyal()
                                isStraightFlush()
                                isFourKind()
                                isFullHouse()
                                isFlush()
                                isStraight()
                                isThreeKind()
                                isTwoPair()
                                isPair()
                                if not ip and not itp:
                                        if 'k' in handvalues: screen.blit(font.render("KING HIGH", 1, (255, 255, 0)), textpos)
                                        elif 'q' in handvalues: screen.blit(font.render("QUEEN HIGH", 1, (255, 255, 0)), textpos)
                                        elif 'j' in handvalues: screen.blit(font.render("JACK HIGH", 1, (255, 255, 0)), textpos)
                                        elif '10' in handvalues: screen.blit(font.render("10 HIGH", 1, (255, 200, 0)), textpos)
                                        elif '9' in handvalues: screen.blit(font.render("9 HIGH", 1, (255, 150, 0)), textpos)
                                        elif '8' in handvalues: screen.blit(font.render("8 HIGH", 1, (255, 100, 0)), textpos)
                                        elif '7' in handvalues: screen.blit(font.render("7 HIGH", 1, (255, 50, 0)), textpos)
                                        elif '6' in handvalues: screen.blit(font.render("6 HIGH", 1, (255, 0, 0)), textpos)
                              

                                # Blit everything to the screen
                                #screen.blit(screen, (0, 0))
                                pygame.display.update()

                        else:
                            continue
                else:
                    while True:
                        screen.blit(screen, (0, 0))
                        pygame.display.update()
                        if pre_time!=os.path.getmtime(f1) :
                            pre_time=os.path.getmtime(f1)
                            print "hello"
                            break;
                    continue

    
###################################################


    

	# Event loop
    #while 1:
    	#for event in pygame.event.get():
        #        keys = pygame.key.get_pressed()
    	#	if event.type == QUIT:
    	#		return
                #if event.type == KEYDOWN:
                    #screen.blit(screen2, (0, 0))
                    #if event.key==pygame.K_r:
                        #screen.blit(screen, (0, 0))
                        #pygame.time.wait(100) ; screen.blit(b0, (100, 150)) ; pygame.display.update()
                       # pygame.time.wait(100) ; screen.blit(b0, (200, 150)) ; pygame.display.update()
                       # pygame.time.wait(100) ; screen.blit(b0, (300, 150)) ; pygame.display.update()
                        #pygame.time.wait(100) ; screen.blit(b0, (400, 150)) ; pygame.display.update()
                        #pygame.time.wait(100) ; screen.blit(b0, (500, 150)) ; pygame.display.update()

                        #screen2.blit(re, (100, 150)) ; retract(b1, pos1, 60, 20)
                        #screen2.blit(re, (200, 150)) ; retract(b2, pos2, 50, 20)
                       # screen2.blit(re, (300, 150)) ; retract(b3, pos3, 40, 20)
                       # screen2.blit(re, (400, 150)) ; retract(b4, pos4, 30, 20)
                       # screen2.blit(re, (500, 150)) ; retract(b5, pos5, 20, 20)

                       # getCards()
                      #  shuffleDeck()
                       # main()

getCards()
shuffleDeck()
if __name__ == '__main__': main()

