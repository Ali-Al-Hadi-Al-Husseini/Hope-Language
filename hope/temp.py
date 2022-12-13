# import turtle

# # Window
# def generate_windows(name,title,bgcolor,width,height,tracer):
#     # set name as key for windows object in symbol table 
#     windows = turtle.Screen()
#     windows.title(title)
#     windows.bgcolor(bgcolor)
#     windows.setup(width=width, height=height)
#     windows.tracer(tracer)

# def start_windows_listen(name):
#     #get object from symbol table
#     window = 1
#     window.listen()

# def generate_shape(name,shape_,color,wid,len,goto1,goto2,hide,write ):
#     # set name as key for shape object in symbol table 
#     Shape = turtle.Turtle()
#     Shape.shape(shape_)
#     Shape.color(color)
#     Shape.penup()
#     Shape.shapesize(stretch_wid=wid, stretch_len=len)
#     if hide:
#         Shape.hideturtle()
#     Shape.goto(goto1,goto2)
#     if write != '':
#         Shape.write(write, align="center", font=("Courier", 24,'normal'))
        
# def move_on_y(name,movemnet):
#     # get shape object from symbol table and and move on y axis
#     pass
# def add_key_press_event(windows_name,shape_name,func,key):
#     #get windowsand shape  objects form symbol_Table
#     window =1 
#     window.onkeypress(func,key)

# wind = turtle.Screen()
# wind.title('CTXGO')
# wind.bgcolor('black')
# wind.setup(width=800, height=600)
# wind.tracer(0)
# # Bar A
# bar_A = turtle.Turtle()
# bar_A.shape('square')
# bar_A.color('white')
# bar_A.shapesize(stretch_wid=5, stretch_len=1)
# bar_A.penup()
# bar_A.goto(-350,0)

# # Bar B
# bar_B = turtle.Turtle()
# bar_B.shape('square')
# bar_B.color('white')
# bar_B.shapesize(stretch_wid=5, stretch_len=1)
# bar_B.penup()
# bar_B.goto(350,0)

# # Ball
# ball = turtle.Turtle()
# ball.shape('circle')
# ball.color('white')
# ball.penup()
# ball.goto(0,0)
# ball_x = 0.1
# ball_y = 0.1

# #score
# sboard = turtle.Turtle()
# sboard.shape('square')
# sboard.color('white')
# sboard.penup()
# sboard.hideturtle()
# sboard.goto(0, 260)
# sboard.write("Player A: 0 Player B: 0", align="center", font=("Courier", 24,'normal'))

# score_a = 0
# score_b = 0


# # Functions
# def bar_A_up():
#     y = bar_A.ycor()
#     y += 30
#     bar_A.sety(y)
# def bar_A_down():
#     y = bar_A.ycor()
#     y -= 30
#     bar_A.sety(y)
# def bar_B_up():
#     y = get_y('bar_b')
#     y += 30
#     bar_B.sety(y)
# def bar_B_down():
#     y = bar_B.ycor()
#     y -= 30
#     bar_B.sety(y)



# # Keyboard Bindings
# wind.listen()
# wind.onkeypress(bar_A_up, 'w')
# wind.onkeypress(bar_A_down, 's')
# wind.onkeypress(bar_B_up, 'Up')
# wind.onkeypress(bar_B_down, 'Down')

# while True:
#     wind.update()
# while True:
#     wind.update()

    # # BAll movement
    # ball.setx(ball.xcor() + ball_x)
    # ball.sety(ball.ycor() + ball_y)

    # # Border
    # if ball.ycor() > 290:
    #     ball.sety(290)
    #     ball_y *= -1
    # elif ball.ycor() < -290:
    #     ball.sety(-290)
    #     ball_y *= -1

    # #score
    # if ball.xcor() > 350:
    #     score_a += 1
    #     sboard.clear()
    #     sboard.write("Player A: {} Player B {}".format(score_a, score_b), align='center', font=('Courier', 24, 'normal'))
    #     ball.goto(0,0)
    #     ball_x *= -1

    # elif ball.xcor() < -350:
    #     score_b += 1
    #     sboard.clear()
    #     sboard.write("Player A: {} Player B {}".format(score_a, score_b), align='center',
    #                  font=('Courier', 24, 'normal'))
    #     ball.goto(0, 0)
    #     ball_x *= -1


    # # Collision with bars
    # if ball.xcor() < -340 and ball.ycor() < bar_A.ycor() + 50 and ball.ycor() > bar_A.ycor() - 50:
    #     ball_x *= -1
    # elif ball.xcor() > 340 and ball.ycor() < bar_B.ycor() + 50 and ball.ycor() > bar_B.ycor() - 50:
    #     ball_x *= -1

from Interpreter_tools.Interpreter import run


a = run("""
# generateing main window
generate_windows('windows','Pong','black',800,600,0)

# Bar A
generate_shape('bar_a','square','white',5,1,-350,0,false,'')

# Bar B
generate_shape('bar_b','square','white',5,1,350,0,false,'')

# Ball
generate_shape('ball','circle','white',0,0,0,0,false,'')

let ball_x = 0.1
let ball_y = 0.1

#score
generate_shape('sboard','square','white',0,0,0,260,true,"Player A: 0 Player B: 0")

let score_a = 0
let score_b = 0


# Keyboard Bindings
start_windows_listen('windows')
add_key_press_event('windows','bar_a','up', 'w')
add_key_press_event('windows','bar_a','down', 's')
add_key_press_event('windows','bar_b','up', 'Up')
add_key_press_event('windows','bar_b','down', 'Down')




while true >> 
    windows_update('windows') 

    # BAll movement
    set_x('ball',get_x('ball') + ball_x)
    set_y('ball',get_y('ball') + ball_y)

    # Border
    if get_y('ball') > 290 >>
        set_y('ball',290)
        ball_y = ball_y * -1 
        
    elif get_y('ball') < -290 >>

        set_y('ball',-290)
        ball_y = ball_y * -1 
    <<

    #score
    if get_x('ball') > 350 >>
        score_a = score_a + 1
        clear_shape('sboard')
        write_shape(format("Player A: {} Player B {}",[score_a,score_b]))
        shape_goto('ball',0,0)
        ball_x = ball_x * -1 

    elif get_x('ball') < -350 >>
        score_b = score_b +  1
        clear_shape('sboard')
        write_shape(format("Player A: {} Player B {}",[score_a,score_b]) )
        shape_goto('ball',0,0)
        ball_x = ball_x * -1 

    <<

    # Collision with barsbar_A
    if get_x('ball') < -340 and get_y('ball') < get_y('bar_a') + 50 and get_y('ball') > get_y('bar_a') - 50 >>
        ball_x = ball_x * -1 
    elif get_x('ball') > 340 and get_y('ball') < get_y('bar_b') + 50 and get_y('ball') > get_y('bar_b') - 50 >>
        ball_x = ball_x * -1 
    <<
<<

""",'hp.hope')

print(a)

