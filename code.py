import pgzrun
import random

# 设定窗口
WIDTH = 371
HEIGHT = 677

#菜单制作
guide = Actor('guide')
start = Actor('start')
back = Actor('back')
again = Actor('back_game')
c1 = Actor('c1')
c2 = Actor('c2')
c3 = Actor('c3')
guide.pos = (175 , 400)
start.pos = (175, 550)
back.pos = (175 , 100)
again.pos = (90 , 600)
c1.pos = (185 , 350)
c2.pos = (185 , 450)
c3.pos = (185, 580)
start_flag = [0]
sf = start_flag
again_flag = [0]
again_flag_parameter = again_flag

#设定食物
food = ["orange1","apple1","lemon1"]
animals = ["dinosaur0","butterfly0","frog0"]
#设定列表来存储得出现在画面上的物件
things = []
x = [102,142,183,227,269]
y = [400,450,500,550,600]

#小动物升级所需的水和食物的条件
level_up_target = [5,15,25]

#用来存储actor在游戏区里的位置
a_position = [[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False]]

#用来存储各块在游戏区里的位置
f_position = [[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False]]

#用click来代表玩家是否有进行操作
click = True

#计算游戏区里有多少块，如果=25就游戏结束
cnt = 0

#设置小动物
temp_animal = "0"
the_animal = "dinosaur0"
player = Actor(the_animal)
player.center = (183,225)


#小动物初始的营养值和水值
player.food_val = 0
player.water_val = 0
player.food_ind = 0
player.water_ind = 0

#小动物的等级
level = [True,False,False]
player.level = 1

#时间设置
player.life = 180
cnt_time = 0

#输赢
finish = False
lose = False
win = False

#设置bg & bgm
music.play("main_bgm")
background = ['forest_bg' , 'grass_bg' , 'pond_bg']
bg_parameter = [0]
bg_flag = bg_parameter
#pond_bg (for frog), grass_bg(for butterfly)

def draw():
    if sf[0] == 1:
        # 清除窗口，设置背景
        player.image = the_animal
        screen.blit(bg , (0, 0))
        player.draw()
        #赢了游戏
        if (finish == True and win == True):
            screen.draw.text("YOU WIN !",center = (183,100),fontsize=80,color="black")
            again_flag_parameter[0] = 1
            again.draw()
        #输了游戏
        if (finish == True and lose == True):
            screen.draw.text("GAME ",center = (183,150),fontsize=120)
            screen.draw.text("OVER ",center = (183,270),fontsize=120)
            again_flag_parameter[0] = 1
            again.draw()
        # 画上游戏模块和玩家
        if (finish == False):
            for t in things:
                t.draw()
            screen.draw.text("等级 : " + str(player.level), (15, 10), color="black",fontname = 'stheiti',fontsize=20)
            screen.draw.text("水值 : " + str(player.water_val) +" / " + str(level_up_target[player.water_ind]), (230, 10), color="black",fontname = 'stheiti',fontsize=20)
            screen.draw.text("营养值 : " + str(player.food_val) +" / " + str(level_up_target[player.food_ind]), (230, 33), color="black",fontname = 'stheiti',fontsize=20)
            screen.draw.text("时间 : " + str(player.life) + "s",center = (183,350),fontname = 'stheiti',fontsize=20)
    #主菜单
    elif sf[0] == 0:
        screen.clear()
        screen.blit('start_bg' , (0 , 0))
        guide.draw()
        start.draw()
    #游戏介绍界面
    elif sf[0] == 2:
        screen.clear()
        screen.blit('menu_bg' , (0 , 0))
        back.draw()
        screen.draw.text("这是一个类似2048的小游戏:\n"
                         "你可以通过合成食物和水喂给\n"
                         "小动物让其长大。食物和水可\n"
                         "通过点击消耗等级2以上的食物\n"
                         "和水，或是到等级8，该值就是\n"
                         "自动加入对应的营养值或水值，\n"
                         "还会出现稀有的神秘道具！\n"
                         "时间只有3分钟，看看你能让\n"
                         "它长多大吧!\n",(20 , 200),fontname = 'stheiti',fontsize = 25  , color = 'white' )
    #选择小动物角色
    else:
        screen.clear()
        screen.blit('start_bg' , (0 , 0))
        c1.draw()
        c2.draw()
        c3.draw()



def update():
    #设定倒计时
    if (sf[0] == 1):
        global cnt_time
        if cnt_time == 60:
            player.life -= 1
            cnt_time = 0
        cnt_time += 1
    #判断是否达到指定的水值和食物值
    update_water_nutrient()
    #print(f"update {the_animal}")
    #是否输了游戏
    check_gameover()
    # 如果有移动，添加一个新的游戏块
    global click
    global finish
    if click == True and finish == False:
        temp = random.randint(1,61)
        if temp % 3 == 0:#水出现
            the_food = "water1"
        elif temp % 12 == 0:#时间出现，概率比较小
            the_food = "time1"
        else:#其余的水果
            the_food = random.choice(food)
        #让click=false才不会在并未进行操作时凭空出现水果
        click = False
        t = Actor(the_food)
        #在x,y里随机选取游戏块落子的位置
        xx = random.choice(x)
        yy = random.choice(y)
        n = check_position(xx,yy)
        ind_x = int(n[0])
        ind_y = int(n[1])
        #若选择的位置已经有其他游戏块，需要重新选取适合的位置
        while(a_position[ind_x][ind_y] != False):
            xx = random.choice(x)
            yy = random.choice(y)
            n = check_position(xx,yy)
            ind_x = int(n[0])
            ind_y = int(n[1])
        t.center = (xx,yy)
        things.append(t)
        a_position[ind_x][ind_y] = t
        f_position[ind_x][ind_y] = the_food
        #游戏区里模块总数加1
        global cnt
        cnt += 1

#玩家按键
def on_key_down():
    #按up键
    if (keyboard.up):
        move_up()
        check_collide_up()
    
    #按down键
    elif (keyboard.down):
        move_down()
        check_collide_down()
    
    #按left键
    elif (keyboard.left):
        move_left()
        check_collide_left()
    
    #按right键
    elif (keyboard.right):
        move_right()
        check_collide_right()
    
    check_lvl_8()

#点击消除lvl 2 以上的游戏块, 喂给小动物
def on_mouse_down(pos):
    global player
    if sf[0] == 1 :
        if again_flag[0] == 0:
            for i in range(5):
                for j in range(5):
                    if(a_position[i][j] != False):
                        if a_position[i][j].collidepoint(pos):
                            n = f_position[i][j]
                            num = n[-1]
                            num = int(num)
                            if num >= 2:
                                #喂给小动物水
                                if n[0] == "w":
                                    if (player.water_val < 25):
                                        player.water_val += num
                                #喂给小动物食物
                                else:
                                    if (player.food_val < 25):
                                        player.food_val += num
                                global the_animal
                                global temp_animal
                                temp_animal = the_animal[-1]
                                temp_animal = int(temp_animal)
                                if temp_animal >= 1:
                                    set_animal_eat()
                                things.remove(a_position[i][j])
                                f_position[i][j] = False
                                a_position[i][j] = False
                                global cnt
                                cnt -= 1
        else:
            #输了游戏后玩家选择重新游戏
            if again.collidepoint(pos):
                start_flag[0] = 0
                global level
                level = [True,False,False]
                # 用来存储actor在游戏区里的位置
                for i in range(5):
                    for j in range(5):
                        if (a_position[i][j] != False):
                            things.remove(a_position[i][j])
                            a_position[i][j] = False
                            f_position[i][j] = False

                # 用click来代表玩家是否有进行操作
                global click
                click = True

                # 计算游戏区里有多少块，如果=25就游戏结束
                cnt = 0
                player.food_val = 0
                player.water_val = 0
                player.food_ind = 0
                player.water_ind = 0

                # 小动物的等级
                player.level = 1

                # 时间设置
                player.life = 180
                global cnt_time
                cnt_time = 0

                # 输赢
                global finish
                finish = False
                global lose
                lose = False
                global win
                win = False
                music.play("main_bgm")
                player.pos = (183,225)
                reset()
                again_flag[0] = 0
    #主菜单         
    elif sf[0] == 0:
        #玩家点击游戏指南 
        if guide.collidepoint(pos):
            start_flag[0] = 2
        #玩家点击开始游戏 
        elif start.collidepoint(pos):
            start_flag[0] = 3
    #玩家点击游戏指南后点击返回主菜单
    elif sf[0] == 2:
        if back.collidepoint(pos):
            start_flag[0] = 0
    #玩家选择小动物
    else:
        #选择小恐龙
        if c1.collidepoint(pos):
            start_flag[0] = 1
            bg_flag[0] = 0
            the_animal = "dinosaur0"
        #选择小蝴蝶
        elif c2.collidepoint(pos):
            start_flag[0] = 1
            bg_flag[0] = 1
            the_animal = "butterfly0"
        #选择小青蛙
        elif c3.collidepoint(pos):
            start_flag[0] = 1
            bg_flag[0] = 2
            the_animal = "frog0"
        global bg
        bg = background[bg_parameter[0]]

#喂给小动物食物时的图片切换
def set_animal_eat():
    global the_animal
    temp1 = the_animal[0:-1]
    temp2 = "9"
    the_animal = temp1 + temp2
    player.image = the_animal
    clock.schedule_unique(set_animal_normal,0.3)

#切换回 正常小动物图片
def set_animal_normal():
    global temp_animal
    global the_animal
    temp1 = the_animal[0:-1]
    temp2 = str(temp_animal)
    the_animal = temp1 + temp2
    player.image = the_animal
    
#更新营养值和水值
def update_water_nutrient():
    global the_animal
    global temp_animal
    if(check_wingame() == False):
        if (player.water_val >= level_up_target[player.water_ind]):
            if (player.water_val < 25 and level_up_target[player.water_ind] != 25):
                player.water_val -= level_up_target[player.water_ind]
                if player.water_ind < 2:
                    player.water_ind +=1
                    
        if (player.food_val >= level_up_target[player.food_ind]):
            if (player.food_val < 25 and level_up_target[player.food_ind] != 25):
                player.food_val -= level_up_target[player.food_ind]
                if player.food_ind < 2:
                    player.food_ind += 1                   
                        
        #当营养值和水值都达到指定的标准后，小动物长大
        if (player.food_ind == player.water_ind and player.food_ind >= 1 and player.water_ind >= 1 and level[player.water_ind] == False):
            level[player.water_ind] = True
            player.level = player.water_ind + 1
            temp1 = the_animal[0:-1]
            temp2 = str(player.water_ind)
            temp_animal = temp2
            the_animal = temp1 + temp2
            player.image = the_animal

#判断是否赢了游戏
def check_wingame():
    if (player.water_val >= 25 and level_up_target[player.water_ind] == 25 and player.food_val >= 25 and level_up_target[player.food_ind] == 25):
        global bg
        global the_animal
        temp = the_animal[0]
        if temp == "d":
            bg1 = "1"
            player.center = (185,450)
        elif temp == "b":
            bg1 = "2"
            player.center = (185,350)
        elif temp == "f":
            bg1 = "3"
            player.center = (185,450)
        bg = "finish_bg" + bg1
        sounds.win_game.play()
        global finish
        finish = True
        global win
        win = True
        temp1 = the_animal[0:-1]
        temp2 = "3"
        the_animal = temp1 + temp2
        return True
    return False

#判断是否游戏结束
def check_gameover():
    global cnt
    if (cnt == 25 or player.life <= 0):
        global bg
        bg = "game_over"
        music.stop()
        sounds.game_over.play()
        global finish
        finish = True
        global lose
        lose = True
        player.center = (185,420)
        global the_animal
        temp1 = the_animal[0:-1]
        if temp1 == "dinosaur":
            temp2 = "5"
            the_animal = temp1 + temp2
            

#为了方便存储进list里
def check_position(xx,yy):
    if ((xx//10) == 10):
        ind_x = '0'
    elif ((xx//10) == 14):
        ind_x = '1'
    elif ((xx//10) == 18):
        ind_x = '2'
    elif ((xx//10) == 22):
        ind_x = '3'
    elif ((xx//10) == 26):
        ind_x = '4'
    if ((yy//10) == 40):
        ind_y = '0'
    elif ((yy//10) == 45):
        ind_y = '1'
    elif ((yy//10) == 50):
        ind_y = '2'
    elif ((yy//10) == 55):
        ind_y = '3'
    elif ((yy//10) == 60):
        ind_y = '4'
    return ind_x + ind_y

#把list里的位置转成实际位置
def recover_position(i,j):
    if (i == 0):
        ind_x = '102'
    elif (i == 1):
        ind_x = '142'
    elif (i == 2):
        ind_x = '183'
    elif (i == 3):
        ind_x = '227'
    elif (i == 4):
        ind_x = '269'
    if (j == 0):
        ind_y = '400'
    elif (j == 1):
        ind_y = '450'
    elif (j == 2):
        ind_y = '500'
    elif (j == 3):
        ind_y = '550'
    elif (j == 4):
        ind_y = '600'
    return ind_x + ind_y

#让lvl 8 的游戏块自动加入营养值（或水值）
def check_lvl_8():
    for i in range(5):
        for j in range(5):
            if(f_position[i][j] != False):
                n = f_position[i][j]
                num = n[-1]
                num = int(num)
                if (num == 8):
                    if n[0] == "w":
                        player.water_val += num
                    else:
                        player.food_val += num
                    global the_animal
                    global temp_animal
                    temp_animal = the_animal[-1]
                    temp_animal = int(temp_animal)
                    if temp_animal >= 1:
                        set_animal_eat()
                    things.remove(a_position[i][j])
                    f_position[i][j] = False
                    a_position[i][j] = False
                    global cnt
                    cnt -= 1

#重置游戏
def reset():
    global things, cnt, start_flag,animals
    start_flag[0] = 0
    things = []
    for i in range(5):
        for j in range(5):
            a_position[i][j] = False
            f_position[i][j] = False
    global click
    click = True
    cnt = 0
    animals = ["dinosaur0"]

    the_animal = random.choice(animals)
    player = Actor(the_animal)
    player.center = (183, 225)

    player.food_val = 0
    player.water_val = 0
    player.food_ind = 0
    player.water_ind = 0

    player.level = 1

    player.life = 180
    global cnt_time
    cnt_time = 0
    
    global finish
    finish = False
    global lose
    lose = False
    global win
    win = False
    music.play("main_bgm")
    
###下面四个函数（移动游戏块）都大同小异，能明白其中一个就可以了

#游戏块往上移动
def move_up():
    global click
    click = True
    #从第2排开始查到第5排（不需要找第1排因为已经在最上面了）
    for i in range(5):
        for j in range(1,5):
            #如果该位置有游戏块
            if a_position[i][j] != False:
                k = j - 1
                #如果该位置的上面没有游戏块：
                if a_position[i][k] == False:
                    #持续往上移动如果都没有游戏块
                    while (a_position[i][k] == False and k >= 1):
                        if k - 1 < 0:#超过框了,break
                            break
                        elif a_position[i][k - 1] != False:#上一个位置已经有游戏块,无法继续往上移动了,break
                            break
                        k-=1#继续往上
                    #把游戏块从原来的位置摆放在适合的位置
                    a_position[i][k] = a_position[i][j]
                    things.remove(a_position[i][j])#删除本来的位置的游戏块
                    a_position[i][j] = False
                    n = recover_position(i,k)#获取须摆放的位置的坐标
                    xx = int(n[0:3])
                    yy = int(n[3:6])
                    a_position[i][k].center = (xx,yy)#在存储actor的list里更改游戏块的位置
                    things.append(a_position[i][k])#把新的位置的游戏块加进去
                    f_position[i][k] = f_position[i][j]#在存储各块的list更改游戏块的位置
                    f_position[i][j] = False
                    #print(f"{a_position[i][k]} move from {i},{j} to {i},{k}")
    
#游戏块往下移动
def move_down():
    global click
    click = True
   #从第4排开始查到第1排（不需要找第5排因为已经在最下面了）
    for i in range(5):
        for j in range(3,-1,-1):
            if a_position[i][j] != False:
                k = j + 1
                if a_position[i][k] == False:
                    while (a_position[i][k] == False and k <= 4):
                        if k + 1 > 4:
                            break
                        elif a_position[i][k + 1] != False:
                            break
                        k+=1
                    a_position[i][k] = a_position[i][j]
                    things.remove(a_position[i][j])
                    a_position[i][j] = False
                    n = recover_position(i,k)
                    xx = int(n[0:3])
                    yy = int(n[3:6])
                    a_position[i][k].center = (xx,yy)
                    things.append(a_position[i][k])
                    f_position[i][k] = f_position[i][j]
                    f_position[i][j] = False
                    #print(f"{a_position[i][k]} move from {i},{j} to {i},{k}")
#游戏块往左移动
def move_left():
    global click
    click = True
    #从第2列开始查到第5列（不需要找第1列因为已经在最左边了）
    for i in range(1,5):
        for j in range(5):
            if a_position[i][j] != False:
                k = i - 1
                if a_position[k][j] == False:
                    while (a_position[k][j] == False and k >= 1):
                        if k - 1 < 0:
                            break
                        elif a_position[k-1][j] != False:
                            break
                        k-=1
                    a_position[k][j] = a_position[i][j]
                    things.remove(a_position[i][j])
                    a_position[i][j] = False
                    n = recover_position(k,j)
                    xx = int(n[0:3])
                    yy = int(n[3:6])
                    a_position[k][j].center = (xx,yy)
                    things.append(a_position[k][j])
                    f_position[k][j] = f_position[i][j]
                    f_position[i][j] = False
                    #print(f"{a_position[k][j]} move from {i},{j} to {k},{j}")
#游戏块往右移动                                         
def move_right():
    global click
    click = True
    #从第4列开始查到第1列（不需要找第5列因为已经在最右边了）
    for i in range(3,-1,-1):
        for j in range(5):
            if a_position[i][j] != False:
                k = i + 1
                if a_position[k][j] == False:
                    while (a_position[k][j] == False and k <= 4):
                        if k + 1 > 4:
                            break
                        elif a_position[k+1][j] != False:
                            break
                        k+=1
                    a_position[k][j] = a_position[i][j]
                    things.remove(a_position[i][j])
                    a_position[i][j] = False
                    n = recover_position(k,j)
                    xx = int(n[0:3])
                    yy = int(n[3:6])
                    a_position[k][j].center = (xx,yy)
                    things.append(a_position[k][j])
                    f_position[k][j] = f_position[i][j]
                    f_position[i][j] = False
                   # print(f"{a_position[k][j]} move from {i},{j} to {k},{j}")

###下面四个函数（检查有无相同的游戏块可以碰撞, 如果有, 该游戏块得升一级）都大同小异，能明白其中一个就可以了
                   
#检查往上移动时, 有没有同样的游戏块碰撞在一起
def check_collide_up():
    #从第1排到第4排
    for i in range(5):
        for j in range(4):
            #若该位置和同样位置的下一排都有游戏块
            if(f_position[i][j] != False and f_position[i][j + 1] != False):
                #如果两个都是同样的游戏块, 进行合成
                if(f_position[i][j] == f_position[i][j + 1]):
                    #合成
                    n = f_position[i][j]
                    #print(f"2) At {i},{j} and {i+1},{j} {f_position[i][j]} becomes", end = " ")
                    #找出合成后的等级
                    num = n[-1]
                    num = int(num)
                    num += num
                    temp = n[0:-1]
                    n = temp + str(num)
                    f_position[i][j] = n
                    f_position[i][j + 1] = False
                    #print(f_position[i][j])
                    #删除本来的两个游戏块
                    things.remove(a_position[i][j])
                    things.remove(a_position[i][j + 1])
                    #添加合成后的游戏块
                    t = Actor(n)
                    pp = recover_position(i,j)
                    xx = int(pp[0:3])
                    yy = int(pp[3:6])
                    t.center = (xx,yy)
                    #新的游戏块保留在上面的位置
                    a_position[i][j] = t
                    a_position[i][j + 1] = False
                    things.append(t)
                    global cnt
                    cnt -= 1

#检查往下移动时, 有没有同样的游戏块碰撞在一起
def check_collide_down():
    #从第1排到第4排
    for i in range(5):
        for j in range(4):
            if(f_position[i][j] != False and f_position[i][j + 1] != False):
                if(f_position[i][j] == f_position[i][j + 1]):
                    n = f_position[i][j]
                    #print(f"2) At {i},{j} and {i+1},{j} {f_position[i][j]} becomes", end = " ")
                    num = n[-1]
                    num = int(num)
                    num += num
                    temp = n[0:-1]
                    n = temp + str(num)
                    f_position[i][j + 1] = n
                    f_position[i][j] = False
                    #print(f_position[i][j])
                    things.remove(a_position[i][j])
                    things.remove(a_position[i][j + 1])
                    t = Actor(n)
                    pp = recover_position(i,j + 1)
                    xx = int(pp[0:3])
                    yy = int(pp[3:6])
                    t.center = (xx,yy)
                    #新的游戏块保留在下面的位置
                    a_position[i][j + 1] = t
                    a_position[i][j] = False
                    things.append(t)
                    global cnt
                    cnt -= 1

#检查往左移动时, 有没有同样的游戏块碰撞在一起
def check_collide_left():
    #从第0列到第4列
    for i in range(4):
        for j in range(5):
            if(f_position[i][j] != False and f_position[i+1][j] != False):
                if(f_position[i][j] == f_position[i+1][j]):
                    n = f_position[i][j]
                    #print(f"1) At {i},{j} and {i+1},{j} {f_position[i][j]} becomes", end = " ")
                    num = n[-1]
                    num = int(num)
                    num += num
                    temp = n[0:-1]
                    n = temp + str(num)
                    f_position[i][j] = n
                    f_position[i+1][j] = False
                    #print(f_position[i][j])
                    things.remove(a_position[i+1][j])
                    things.remove(a_position[i][j])
                    t = Actor(n)
                    pp = recover_position(i,j)
                    xx = int(pp[0:3])
                    yy = int(pp[3:6])
                    t.center = (xx,yy)
                    #新的游戏块保留在左边的位置
                    a_position[i][j] = t
                    a_position[i+1][j] = False
                    things.append(t)
                    global cnt
                    cnt -= 1

#检查往右移动时, 有没有同样的游戏块碰撞在一起
def check_collide_right():
    #从第0列到第4列
    for i in range(4):
        for j in range(5):
            if(f_position[i][j] != False and f_position[i+1][j] != False):
                if(f_position[i][j] == f_position[i+1][j]):
                    n = f_position[i][j]
                    #print(f"1) At {i},{j} and {i+1},{j} {f_position[i][j]} becomes", end = " ")
                    num = n[-1]
                    num = int(num)
                    num += num
                    temp = n[0:-1]
                    n = temp + str(num)
                    f_position[i + 1][j] = n
                    f_position[i][j] = False
                    #print(f_position[i][j])
                    things.remove(a_position[i + 1][j])
                    things.remove(a_position[i][j])
                    t = Actor(n)
                    pp = recover_position(i + 1,j)
                    xx = int(pp[0:3])
                    yy = int(pp[3:6])
                    t.center = (xx,yy)
                    #新的游戏块保留在右边的位置
                    a_position[i + 1][j] = t
                    a_position[i][j] = False
                    things.append(t)
                    global cnt
                    cnt -= 1


    
pgzrun.go()








