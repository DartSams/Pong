import pygame
import random

pygame.init()
width,height = 700,500
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Pong")
fps = 60
black = (0,0,0)
white = (255,255,255)
paddle_width,paddle_height = 20,100
ball_radius = 10
ball_amount = 1
min_ball_speed,max_ball_speed = 1,9
winning_score = 2

score_font = pygame.font.SysFont("comicsans",50)

class Paddle:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = white
        self.vel = 4

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))

    def move(self,up=True):
        if up == True: #move paddle up so y value decreases small number
            self.y -= self.vel

        elif up == False: #move paddle down so y value increases big number
            self.y += self.vel

class Ball:
    def __init__(self,x,y,radius):
        self.x = self.original_x = x
        self.y =self.original_y = y
        self.radius = radius
        self.color = white
        self.x_vel = random.randrange(min_ball_speed,max_ball_speed)
        self.y_vel = random.randrange(min_ball_speed,max_ball_speed)

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        self.y_vel = 0

def handle_collision(ball,left_paddle,right_paddle,left_player,right_player):
    if ball.y + ball.radius >= height: #handles collision with bottom border
        ball.y_vel *= -1

    if ball.y + ball.radius <= 0 + ball.radius: #handles collision with top border
        ball.y_vel *= -1

    if ball.x + ball.radius >= width: #handles collision with right border
        ball.x_vel *= -1
        left_player.increase_score()
        ball.reset()

    if ball.x + ball.radius <= 0 + ball.radius: #handles collision with left border
        ball.x_vel *= -1
        right_player.increase_score()
        ball.reset()

    if ball.x_vel < 0: #handles collision with left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.x_vel
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    elif ball.x_vel >0: #handles collision with right paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.x_vel
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

class Player:
    def __init__(self,name,paddle,score):
        self.paddle = paddle
        self.score = score
        self.games_won = 0

    def get_paddle(self):
        return self.paddle

    def increase_score(self):
        if self.score != winning_score:
            self.score += 1
        return self.score

    def decrease_score(self):
        self.score -= 1
        return self.score

def handle_paddle_movement(keys,left_paddle,right_paddle):
    #left paddle movement so cant move of screen
    if keys[pygame.K_w] and left_paddle.y - left_paddle.vel >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.vel + left_paddle.height <= height:
        left_paddle.move(up=False)

    #right paddle movement so cant move of screen
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.vel >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.vel + right_paddle.height <= height:
        right_paddle.move(up=False)

def handle_win(left_score,right_score,ball_bag):
    if left_score == winning_score:
        for i in ball_bag:
            i.reset()
        return "Left wins"
    elif right_score == winning_score:
        for i in ball_bag:
            i.reset()
        return "Right wins"

def draw(win,paddles,ball_bag,left_score,right_score): #main pyagme draw function
    win.fill(black)
    left_score_text = score_font.render(f"{left_score}",1,white)
    right_score_text = score_font.render(f"{right_score}",1,white)
    win.blit(left_score_text,(width//4-left_score_text.get_width()//2,20))
    win.blit(right_score_text,(width*3//4-right_score_text.get_width()//2,20))

    for paddle in paddles:
        paddle.draw(win)

    pygame.draw.rect(win,white,(width/2-5,0,10,height))

    # ball.draw(win)
    for i in ball_bag:
        i.draw(win)

    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    ball_bag=[]

    left_paddle = Paddle(10,height/2-paddle_height/2,paddle_width,paddle_height) #creates left paddle in middle of screen
    right_paddle = Paddle(width-10-paddle_width,height/2-paddle_height/2,paddle_width,paddle_height) #creates right paddle in middle of screen
    left_player = Player("left player",left_paddle,score=0)
    right_player = Player("right player",right_paddle,score=0)

    for i in range(ball_amount): #creates a set amount of balls based on ball_amount variable
        ball = Ball(width/2,height/2,ball_radius)
        ball_bag.append(ball)

    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys,left_paddle,right_paddle)
        for i in ball_bag: #moves all the balls
            i.move()
        for i in ball_bag: #handles collision on each individual ball
            handle_collision(i,left_paddle,right_paddle,left_player,right_player)
        draw(win,[left_paddle,right_paddle],ball_bag,left_player.score,right_player.score)

        # print(left_player.score,right_player.score)
        if handle_win(left_player.score,right_player.score,ball_bag): #displays on screen which player won the game and resets ball and player scores
            winning_text = score_font.render(f"{handle_win(left_player.score,right_player.score,ball_bag)}",1,white)
            win.blit(winning_text,(width/2-winning_text.get_width()/2,height/2-winning_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(3000)
            left_player.score = 0
            right_player.score = 0

    pygame.quit()


if __name__ == "__main__":
    main()