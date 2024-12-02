import sys, math, pygame, random, time, os
import pygame

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for PyInstaller bundling. """
    try:
        base_path = sys._MEIPASS
    except Exception: # Check if running as a bundled executable
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data")
    return os.path.join(base_path, relative_path)

# Load all assets from the Data directory
# data_path = res`ource_path("Data")
# data_path = resource_path("")

# Dictionary to store asset paths
# assets = {}
# 
# # Loop through all files in the Data directory
# for root, dirs, files in os.walk(data_path):
#     for file in files:
#         # Build the full path to the asset
#         full_path = os.path.join(root, file)
        
#         # Optionally, store the path relative to the "Data" directory
#         relative_pth = os.path.relpath(full_path, data_path)
#         full_path = resource_path(relative_pth)
        
#         # Add the asset to the dictionary
#         assets[relative_pth] = full_path

# Example: Accessing an asset by its relative path
# for asset_name, asset_path in assets.items():
#     print(f"Asset: {asset_name}, Path: {asset_path}")

################# Some useful functions ##############

def nint(x):           # round off to nearest integer
    return int(round(x))
def scrx(xi):          # convert to screen coordinate x
    return nint(float(maxx)*(xi+xmax)/(2.0*xmax))
def scry(yi):          # convert to screen coordinate y
    return nint(float(maxy)*(ymax-yi)/(2.0*ymax))


# Init pygame modules
pygame.init()


#################### List of control methods###########

speed = 1
accel = 2
daccel = 3
modetxt = ["0. Error",
           "1. Speed control",
           "2. Acceleration control",
           "3.Rate of accel control"]
############### SET DEFAULT CONTROL METHOD HERE ###############

control = accel

############# CHECK FOR ANY CONNECTED JOYSTICKS ###############

pygame.joystick.init()
swjoy = (pygame.joystick.get_count()>0)
if (swjoy):
    ijoy = 0
    stick = pygame.joystick.Joystick(ijoy)
    stick.init()

#########################################################

# General variables initialisation
fturb = 1.0

# Tuples with RGB-values of colours
black = (0,0,0)
white = (255,255,255)
sky = (160,170,255)# 240
green = (0,255,0)

# Change directory to data directory
# os.chdir("Data")

# Load sound file
# & play later with:               pygame.mixer.music.play()
# explosionsound = pygame.mixer.music.load("explosion.wav")
explosionsound = pygame.mixer.music.load(resource_path("explosion.wav"))


# Setup screen & font

pygame.display.init()
pygame.font.init()
tekst = pygame.font.Font(pygame.font.match_font("arial"),18)
tekst.set_bold(True)
screensize = pygame.display.list_modes()[0]
maxx = screensize[1]
maxy = screensize[0]
maxx = 800
maxy = 600

ymax = 1.5
xmax = 1.0

reso = (maxx,maxy)

#screen = pygame.display.set_mode((1024,768),pygame.FULLSCREEN)
screen = pygame.display.set_mode(reso)

# Load menu screen bitmap (splash screen)

# Center menu on black screen
menu = pygame.image.load(resource_path("menu.jpg"))
menurect = menu.get_rect()

menurect.centerx = maxx/2
menurect.centery = maxy/2

screen.fill(black)
screen.blit(menu,menurect)
pygame.display.flip()

# Bitmaps lezen

# F-16 bitmap & dimensions in rect
f16 = pygame.image.load(resource_path("f16.gif"))
f16rect = f16.get_rect()
f16rect.top = 0
f16rect.left = 0

# Cloud bitmaps & dimensions in rect
wolkfiles=[resource_path("wolk1.gif"),resource_path("wolk2.gif"),resource_path("wolk3.gif"),resource_path("wolk4.gif")]

wolk =  [pygame.image.load(resource_path("wolk1.gif"))]
wolkrect = [wolk[0].get_rect()]
for i in range(1,4):
    wolk.append(pygame.image.load(wolkfiles[i]))
    wolkrect.append(wolk[0].get_rect())
    
# Explosion bitmaps & dimensions in rect

explodefiles = [resource_path("ex1.gif"),resource_path("ex2.gif"),resource_path("ex3.gif"),resource_path("ex4.gif")]

expl =  [pygame.image.load(resource_path("ex1.gif"))]
explrect = [expl[0].get_rect()]
for i in range(1,4):
    expl.append(pygame.image.load(explodefiles[i]))
    explrect.append(expl[0].get_rect())

# Starting positions & speed

x = 0.0
y = 0.0

delta = 2.3

vy = 0.0
vturb = 0.0

vvy = 0.0

vvvy = 0.0

vvvvy = 0.0

xwolk = [-1.5,0.0,1.0,1.2]
ywolk = [0.7,0.3,-0.6,0.9]
sxc = [1,1,1,1]
syc = [1,1,1,1]
vwolk = -1.4
plsound = True
vturb = 0.0

# Wait for space bar
running = False

#  while (pygame.event.wait().type != pygame.KEYDOWN): pass

while (not running):
    pygame.event.pump()
    keybd = pygame.key.get_pressed()
    if (keybd[pygame.K_1]):
         running = True
         control = speed
    if (keybd[pygame.K_2]):
         running = True
         control = accel
    if (keybd[pygame.K_3]):
         running = True
         control = daccel
    if (keybd[pygame.K_ESCAPE]):
        pygame.quit()
        sys.exit("Ready.")
         
# Start the clock
t = pygame.time.get_ticks()
t0 = t
tnew = t
running = True
dead = False

# Game loop
while (running):

# Get keys
   pygame.event.pump()
   keybd = pygame.key.get_pressed()

# Get time step
   tnew = pygame.time.get_ticks()-t0
   dt = 0.001*float(tnew - t)

# Do time step
   if dt>0. :
       t  = tnew


# Do maneuvring
       vc =0.0
       if (not swjoy):
           if keybd[pygame.K_q] or keybd[pygame.K_UP]:
              vc = delta
           if keybd[pygame.K_a]or keybd[pygame.K_DOWN]:
              vc= -delta
       else:
           vc = stick.get_axis(1)*delta
           if (abs(vc) < 0.23) :
                vc = 0.0

# CONTROL MODE speed

       if (control == speed):

# Disturbance
           vturb = max(-delta,min(delta,vturb + 8.0*dt*(2.0*float(random.random())-1.0)))

           
# Update positions
           vy = vc + fturb*vturb
           if (not dead): y = y + vy*dt

# CONTROL MODE accelleration
       elif (control == accel):
          
# Disturbance
           vturb = max(-delta,min(delta,vturb + 8.0*dt*(2.0*float(random.random())-1.0)))

           if (not dead):
               vvy = vc
               vy = vy + vvy*dt
               y = y + (vy+fturb*vturb)*dt
          
# CONTROL MODE rate of accelleration
       elif (control == daccel):

# Disturbance
           vturb = max(-delta,min(delta,vturb + 8.0*dt*(2.0*float(random.random())-1.0)))
           
           if (not dead):
               vvvy = 0.5*vc
               vvy = vvy + vvvy*dt
               vy = vy + vvy*dt
               y = y + (vy+0.5*fturb*vturb)*dt
          
#==============================
               
# Position of clouds
       if (not dead):
           for i in range(0,4):
               xwolk[i] = xwolk[i] + vwolk*dt
               
# Wrap-around clouds when off-screen, but change y-coordinate
               if (xwolk[i]>2.0*xmax):
                   xwolk[i]=xwolk[i]-4.0*xmax
                   ywolk[i] = random.random()*1.4-0.7

               if (xwolk[i]<-2.0*xmax):
                   xwolk[i]=xwolk[i]+4.0*xmax
                   ywolk[i] = random.random()*1.4-0.7
         
# Calculate screen coordinates
       sx = scrx(x)
       sy = scry(y)

       for i in range(0,4):
           sxc[i] = scrx(xwolk[i])
           syc[i] = scry(ywolk[i])


# Clear screen
       pygame.draw.rect(screen,sky,(0,0,maxx,maxy))
       pygame.draw.rect(screen,black,(0, scry(1.5), maxx, scry(1.0)-scry(1.5)))
       pygame.draw.rect(screen,black,(0, scry(-1.0), maxx, scry(-1.5)-scry(-1.0)))

# Draw clouds
       for i in range(0,4):
           wolkrect[i].centerx = sxc[i]
           wolkrect[i].centery = syc[i]
           screen.blit(wolk[i], wolkrect[i])


# Put bitmap F-16 on if not dead, else explosion sequence
       if (not dead):
           f16rect.centerx = sx
           f16rect.centery = sy
           screen.blit(f16, f16rect)

       elif(t-tdeatha<500):
           j = int((t-tdeatha)/50)
           if (j>3): j=3
           if (j<0): j=0
           explrect[j].centerx = sx
           explrect[j].centery = sy
           screen.blit(expl[j], explrect[j])

# Show time on screen
       if (not dead):
           tdisp = t*0.001
       else:
           tdisp = tdeatha*0.001
           
       mins = int(tdisp/60)
       sec = int(tdisp)-mins*60

# Leading zeroes

       if sec<10:
           text = repr(mins)+":"+"0"+repr(sec)
       else:
           text = repr(mins)+":"+repr(sec)

       textimg = tekst.render(text,True,white)
       textrect = textimg.get_rect()
       textrect.centerx = 400
       textrect.centery = 550
       screen.blit(textimg,textrect)
           
# Show control mode on screen
       textimg = tekst.render(modetxt[control],True,white)
       textrect = textimg.get_rect()
       textrect.centerx = 400
       textrect.centery = 70
       screen.blit(textimg,textrect)
 

#restart
       if (dead and (t-tdeatha)>5000) :
           y = 0.0
           vy = 0.0
           vc = 0.0
           vturb = 0.0
           vvy = 0.0
           vvvy = 0.0
           t = pygame.time.get_ticks()
           t0 = t
           tnew = t
           running = True
           dead = False
           xwolk = [-1.5,0.0,1.0,1.2]
           ywolk = [0.7,0.3,-0.6,0.9]
           sxc = [1,1,1,1]
           syc = [1,1,1,1]
           vwolk = -1.4
           plsound = True
           
# Check whether F-16 has hit something
       if (abs(y)>1.0 and not dead):
           dead = True
           tdeatha = t
           lasersound = pygame.mixer.music.load(resource_path("explosion.wav"))
           pygame.mixer.music.play()
           plsound = False

# Update display
       pygame.display.flip()


# Check for escape key
   if keybd[pygame.K_ESCAPE]:
          running = False
          pygame.display.quit()
          pygame.quit()
          sys.exit()

# Check voor einde
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False
          pygame.display.quit()
          pygame.quit()
          sys.exit()

# Out of loop

running = False
pygame.display.quit()
pygame.font.quit()
pygame.quit()
sys.exit()
                         


