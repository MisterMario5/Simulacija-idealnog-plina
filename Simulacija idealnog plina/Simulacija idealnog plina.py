import pygame
import sys
import numpy as np
import os
from matplotlib import pyplot as plt
import math 




#Funkcija Gumb napravljena u prošlom projektu
class Gumb: 
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))

    def update(self,screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self,position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)





class IdealGasSimulation:
    def __init__(self, N, molar_mass, radius, screen_width, screen_height, v0, duration, nsteps, border_rect, hard, admin):
        self.N = N  # Number of particles
        self.M = molar_mass  # Molarna masa u kg/mol
        self.radius = radius  # Radius
        self.screen_width = screen_width   # Duljina ekrana
        self.duration = duration  # Trajanje (s)
        self.nsteps = nsteps  # Broj intervala
        self.dt = duration / nsteps  # Interval (s)
        self.dt_array = np.full((self.N, 1), self.dt)
        self.v0 = v0  # Početna brzina čestica koja zbog preglednosti simulacije služi kao Temperatura
        self.brzina_graf = math.sqrt((3*8.314*self.v0)/self.M) #Prava brzina po računu u m/s 
        self.border_rect = border_rect  # Border rectangle (x, y, širina, visina)
        self.pressure = 1 #Tlak za simulaciju u atm
        self.volume = float(float(border_rect[2]) * float(border_rect[3])) / 1000 #Volumen za simulaciju u L
        
        self.hard = hard #Određuje je li čvrst ili osjetljiv cilindar
        self.admin = admin #Dozvoljava input
        
        #Liste za graf
        self.lista_volume = [self.volume/1000]
        self.lista_pressure = [self.pressure]
        self.lista_temperatura = [self.v0]



        self.k_N = ((self.volume/1000) * (self.pressure*101325) * 6.022 * (10**23)) / (8.314*self.v0 * self.N) #Za realan broj čestica, tj. nalik na mjernu jedinicu.

        # Pokrene pygame sučelje
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width - 10, screen_height - 50), pygame.RESIZABLE)
        pygame.display.set_caption("Ideal Gas Simulation")

        # Stvara nasumična mjesta
        grid_size = int(np.ceil(np.sqrt(N)))  # Koristi za stvaranje čestica unutar granica
        spacing = min((self.screen_width  - border_rect[2]) / grid_size, (self.screen_width  - border_rect[3]) / grid_size)  # Popravlja kako bi stale unutar granica
        x = np.linspace(border_rect[0] + radius + spacing / 2, border_rect[0] + border_rect[2] - radius - spacing / 2, grid_size)
        y = np.linspace(border_rect[1] + radius + spacing / 2, border_rect[1] + border_rect[3] - radius - spacing / 2, grid_size)
        pos = [(xi, yi) for xi in x for yi in y]

        self.position = np.array(pos[:N])  # Uzima stvorene pozicije
        
        #Stvara kuteve pod kojim se kreću i njihove brzine
        Kutevi = np.random.uniform(0, 2 * np.pi, size=self.N)
        vx, vy = self.v0 * np.cos(Kutevi), self.v0 * np.sin(Kutevi)
        self.v = np.stack((vx, vy), axis=1)




    def check_collisions(self):
        """Provjerava kada se sudare čestice ili kada udare o zid"""
        dt_array = np.full((self.N, 1), self.dt)  
        r_next = self.position + self.v * dt_array

        # Gleda kad se sudare sa zidom
        self.v[r_next[:, 0] < self.border_rect[0] + self.radius, 0] *= -1  # S lijevim
        self.v[r_next[:, 0] > self.border_rect[0] + self.border_rect[2] - self.radius, 0] *= -1  # Desnim
        self.v[r_next[:, 1] < self.border_rect[1] + self.radius, 1] *= -1  # Gornjim
        self.v[r_next[:, 1] > self.border_rect[1] + self.border_rect[3] - self.radius, 1] *= -1  # Donjim

        # Gleda kad se međusobno sudare čestice
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if np.linalg.norm(r_next[i] - r_next[j]) < 2 * self.radius:
                    rdiff = self.position[i] - self.position[j]  # Vektor za česticu [i] i česticu [j]
                    vdiff = self.v[i] - self.v[j]
                    self.v[i] = self.v[i] - rdiff.dot(vdiff) / rdiff.dot(rdiff) * rdiff  # Vraća brzinu za česticu [i]
                    self.v[j] = self.v[j] + rdiff.dot(vdiff) / rdiff.dot(rdiff) * rdiff  # Vraća brzinu za česticu [j]








    def step(self):
        """Izračunava položaje u sljedećem intervalu"""
        self.check_collisions()
        self.position += self.v * self.dt

    def draw_particles(self):
        """Crta čestice"""
        self.screen.fill((195, 195, 195))
        

        for particle_pos in self.position:
            if math.isnan(particle_pos[0]) or math.isnan(particle_pos[1]): #Provjerava jesu li sve pozicije brojevi
                next 
            else:
                pygame.draw.circle(self.screen, (0, 0, 0), (int(particle_pos[0]), int(particle_pos[1])), self.radius) #Crta čestice po pozicijama

        pygame.draw.rect(self.screen, (0, 0, 0), self.border_rect, 2)  # Crta granicu

        #Gumbi
        BACK_BUTTON = Gumb(None, (1400, 700), "NAZAD", test_font, "Black", "White")
        RESET_BUTTON = Gumb(None, (1200, 700), "RESET", test_font, "Black", "White")
        GRAPH_BUTTON = Gumb(None, (800, 750), "Graf", test_font, "Black", "White")
        VELOCITY_INPUT = Gumb(None, (1150, 150), "Temperatura: " + str(self.v0)+"K", test_font, "Black", "White")
        VELOCITY_INCREASE = Gumb(pygame.image.load("Increase_button.png"), (1430, 120), "Povećaj +100     ", small_font, "Black", "White")
        VELOCITY_DECREASE = Gumb(pygame.image.load("Decrease_button.png"), (1430, 180), "Smanji -100     ", small_font, "Black", "White")
        PARTICLE_INPUT = Gumb(None, (1150, 300), "Čestice: " + str(self.N), test_font, "Black", "White")
        PARTICLE_INCREASE = Gumb(pygame.image.load("Increase_button.png"), (1430, 270), "Povećaj +10       ", small_font, "Black", "White")
        PARTICLE_DECREASE = Gumb(pygame.image.load("Decrease_button.png"), (1430, 330), "Smanji -10       ", small_font, "Black", "White")
        RADIUS_INPUT = Gumb(None, (150, 100), "Radius: " + str(self.radius), test_font, "Black", "White")
        VELOCITY_PRESENTED = Gumb(None, (800, 100), "Brzina: " + str(round(self.brzina_graf,4)) + "m/s", test_font, "Black", "White")
        VOLUME_INPUT = Gumb(None, (1150, 450), "Volumen: " + str(round(self.volume,3)) +"L", test_font, "Black", "White")
        VOLUME_INCREASE = Gumb(pygame.image.load("Increase_button.png"), (1430, 420), "Povećaj +25      ", small_font, "Black", "White")
        VOLUME_DECREASE = Gumb(pygame.image.load("Decrease_button.png"), (1430, 480), "Smanji -25      ", small_font, "Black", "White")
        PRESSURE_INPUT = Gumb(None, (1150, 600), "Tlak: " + str(round(float(self.pressure),3)) + "atm", test_font, "Black", "White")
        
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()  
        # Updeta promjene na gumbima i mijenja njihovu boju
        for gumb in [BACK_BUTTON, RESET_BUTTON, GRAPH_BUTTON, VELOCITY_INPUT, VELOCITY_INCREASE, VELOCITY_DECREASE, PARTICLE_INPUT, PARTICLE_INCREASE, PARTICLE_DECREASE, RADIUS_INPUT, VELOCITY_PRESENTED, VOLUME_INPUT, VOLUME_INCREASE, VOLUME_DECREASE, PRESSURE_INPUT]:
            gumb.changeColor(MENU_MOUSE_POS)
            gumb.update(self.screen)



        pygame.display.flip() 
        










    def add_particles(self, new_N):
        """Nadodava i miče čestice."""
        if new_N > self.N:
            new_positions = []
            min_distance = 15  # Minimalni razmak čestica pri stvaranju

            while len(new_positions) < new_N - self.N:
                #Generira nasumične položaje za nove čestice
                new_position = np.random.uniform(
                    (self.border_rect[0] + self.radius, self.border_rect[1] + self.radius),
                    (self.border_rect[0] + self.border_rect[2] - self.radius, self.border_rect[1] + self.border_rect[3] - self.radius),
                    size=(1, 2)
                )
                
                #Gleda preklapaju li se čestice s postojećim + minimalni razmak
                if (not any(np.linalg.norm(new_position - p) < 2 * self.radius + min_distance for p in self.position) and
                        all(np.linalg.norm(new_position - p) >= min_distance for p in new_positions)):
                    new_positions.append(new_position[0])

            #Povezuje nove pozicije i brzine
            self.position = np.concatenate([self.position, np.array(new_positions)], axis=0)
            self.v = np.concatenate([self.v, np.random.uniform(-self.v0, self.v0, size=(len(new_positions), 2))], axis=0)
        elif new_N < self.N:
            # Smanji broj čestica
            self.position = self.position[:new_N]
            self.v = self.v[:new_N]
        self.N = new_N
        global Kutevi
        Kutevi = np.random.uniform(0, 2 * np.pi, size=self.N)









    def adjust_particle_positions(self, new_volume):
        """Popravlja poziciju čestica kad se mijenja volumen"""
        
        if float(new_volume) != self.volume:
            if float(new_volume) <= 150:
                new_volume = 150
            if float(new_volume) >= 500:
                new_volume = 500

            #Izračuna novu granicu rectengla po volumenu
            new_border_width = ((((float(new_volume) * 500) * 1000) / 300) ** 0.5) 
            new_border_height = ((((float(new_volume) * 500) * 1000) / 300) ** 0.5) * (300 / 500) 
            new_border_rect = (50, 150, new_border_width, new_border_height)

            # Stvara čestice unutar granice
            new_positions = []
            min_distance = 15  

            while len(new_positions) < len(self.position):
                new_position = np.random.uniform(
                    (new_border_rect[0] + self.radius, new_border_rect[1] + self.radius),
                    (new_border_rect[0] + new_border_rect[2] - self.radius, new_border_rect[1] + new_border_rect[3] - self.radius),
                    size=(1, 2)
                )
                # Gleda minimalni razmak od već postojećih čestica
                if all(np.linalg.norm(new_position - p) >= min_distance for p in new_positions):
                    new_positions.append(new_position[0])

            # Updatea čestice i granice
            self.position = np.array(new_positions)
            self.border_rect = new_border_rect
            self.volume = float(new_volume)











    def crtanje_grafa(self):
        """Appenda vrijednosti listama pri svakoj promijeni"""
        self.lista_volume.append(self.volume / 1000)
        self.lista_pressure.append(self.pressure)
        self.lista_temperatura.append(self.v0)










    
    def run_simulation(self):
        """Pokreće simulaciju"""
        running = True
        clock = pygame.time.Clock()

       

        # Omogućuje interakciju s gumbima
        BACK_BUTTON = Gumb(None, (1400, 700), "NAZAD", test_font, "Black", "White")
        RESET_BUTTON = Gumb(None, (1200, 700), "RESET", test_font, "Black", "White")
        GRAPH_BUTTON = Gumb(None, (800, 750), "Graf", test_font, "Black", "White")
        VELOCITY_INPUT = Gumb(None, (1150, 150), "Temperatura: " + str(self.v0)+"K", test_font, "Black", "White")
        VELOCITY_INCREASE = Gumb(pygame.image.load("Increase_button.png"), (1430, 120), "Povećaj +100     ", small_font, "Black", "White")
        VELOCITY_DECREASE = Gumb(pygame.image.load("Decrease_button.png"), (1430, 180), "Smanji -100     ", small_font, "Black", "White")
        PARTICLE_INPUT = Gumb(None, (1150, 300), "Čestice: " + str(self.N), test_font, "Black", "White")
        PARTICLE_INCREASE = Gumb(pygame.image.load("Increase_button.png"), (1430, 270), "Povećaj +10       ", small_font, "Black", "White")
        PARTICLE_DECREASE = Gumb(pygame.image.load("Decrease_button.png"), (1430, 330), "Smanji -10       ", small_font, "Black", "White")
        RADIUS_INPUT = Gumb(None, (150, 100), "Radius: " + str(self.radius), test_font, "Black", "White")
        VOLUME_INPUT = Gumb(None, (1150, 450), "Volumen: " + str(round(self.volume,3)) +"L", test_font, "Black", "White")
        VOLUME_INCREASE = Gumb(pygame.image.load("Increase_button.png"), (1430, 420), "Povećaj +25      ", small_font, "Black", "White")
        VOLUME_DECREASE = Gumb(pygame.image.load("Decrease_button.png"), (1430, 480), "Smanji -25      ", small_font, "Black", "White")
        PRESSURE_INPUT = Gumb(None, (1150, 600), "Tlak: " + str(round(float(self.pressure),3)) + "atm", test_font, "Black", "White")


        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        simulacija()
                        
                    if RESET_BUTTON.checkForInput(pygame.mouse.get_pos()): #Resetira vrijednosti
                        new_N = 100
                        self.add_particles(new_N)
                        self.radius = 5

                        new_velocity = 100
                        global Kutevi
                        Kutevi = np.random.uniform(0, 2 * np.pi, size=self.N) 
                        self.v0 = float(new_velocity)
                        vx, vy = self.v0 * np.cos(Kutevi), self.v0 * np.sin(Kutevi)
                        self.v = np.stack((vx, vy), axis=1)
                        self.brzina_graf = math.sqrt((3*8.314*self.v0)/self.M)
                        new_volume = 150
                        self.adjust_particle_positions(new_volume)
                        self.pressure = 1

                        self.crtanje_grafa()
                        
                    if GRAPH_BUTTON.checkForInput(pygame.mouse.get_pos()): #Prikazuje grafove
                    
                        plt.subplot(1, 3, 1)
                        plt.plot(self.lista_volume, self.lista_pressure)
                        plt.title('P-V graf')
                        plt.xlabel('Volumen (m^3)')
                        plt.ylabel('Tlak (atm)')

                        plt.subplot(1, 3, 2)
                        plt.plot( self.lista_temperatura, self.lista_volume)
                        plt.title('V-T graf')
                        plt.xlabel('Temperatura (K)')
                        plt.ylabel('Volumen (m^3)')
                        

                        plt.subplot(1, 3, 3)
                        plt.plot(self.lista_temperatura, self.lista_pressure)
                        plt.title('P-T')
                        plt.xlabel('Temperatura (K)')
                        plt.ylabel('Tlak (atm)')

                        plt.tight_layout()
                        plt.show()
            
                        
                        
                if event.type == pygame.MOUSEBUTTONUP:    
                    if PARTICLE_INCREASE.checkForInput(pygame.mouse.get_pos()):
                            new_N = self.N + 10
                            if new_N >= 200:
                                new_N = 200
                            if new_N == 11:
                                new_N = 10
                            self.change(1, new_N, self.volume, self.v0)
                            self.add_particles(new_N)
                            self.crtanje_grafa()
                    if PARTICLE_DECREASE.checkForInput(pygame.mouse.get_pos()):
                            new_N = self.N - 10
                            if new_N <= 0:
                                new_N = 1
                            self.change(1, new_N, self.volume, self.v0)
                            self.add_particles(new_N)
                            self.crtanje_grafa()
                    if VELOCITY_INCREASE.checkForInput(pygame.mouse.get_pos()):
                            new_velocity = self.v0 + 100
                            if new_velocity >= 1000:
                                new_velocity = 1000
                            if new_velocity == 101:
                                new_velocity = 100
                            self.change(2, self.N, self.volume, float(new_velocity))
                            Kutevi = np.random.uniform(0, 2 * np.pi, size=self.N) 
                            self.v0 = float(new_velocity)
                            vx, vy = self.v0 * np.cos(Kutevi), self.v0 * np.sin(Kutevi)
                            self.v = np.stack((vx, vy), axis=1)
                            self.brzina_graf = math.sqrt((3*8.314*self.v0)/self.M)
                            self.crtanje_grafa()
                            
                    if VELOCITY_DECREASE.checkForInput(pygame.mouse.get_pos()):
                            new_velocity = self.v0 - 100
                            if new_velocity <= 1:
                                new_velocity = 1
                            self.change(2, self.N, self.volume, float(new_velocity)) 
                            Kutevi = np.random.uniform(0, 2 * np.pi, size=self.N) 
                            self.v0 = float(new_velocity)
                            vx, vy = self.v0 * np.cos(Kutevi), self.v0 * np.sin(Kutevi)
                            self.v = np.stack((vx, vy), axis=1)
                            self.brzina_graf = math.sqrt((3*8.314*self.v0)/self.M)
                            self.crtanje_grafa()

                    if VOLUME_INCREASE.checkForInput(pygame.mouse.get_pos()):
                            new_volume = self.volume + 25
                            if new_volume >= 500:
                                new_volume = 500
                            self.change(3, self.N, float(new_volume), self.v0)
                            self.adjust_particle_positions(new_volume)
                            self.crtanje_grafa()
                            
                    if VOLUME_DECREASE.checkForInput(pygame.mouse.get_pos()):
                            new_volume = self.volume - 25
                            if new_volume <= 150:
                                new_volume = 150
                            self.change(3, self.N, float(new_volume), self.v0)
                            self.adjust_particle_positions(new_volume)
                            self.crtanje_grafa()

            
            if self.admin == 1: #Ako admin uključen korisnik smije direktno inputati vrijednosti
                if VELOCITY_INPUT.checkForInput(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        new_velocity = input("Upišite novu temperaturu: ")
                        if float(new_velocity) > 1000:
                            new_velocity = 1000
                        self.change(2, self.N, self.volume, float(new_velocity))
                        try:
                            Kutevi = np.random.uniform(0, 2 * np.pi, size=self.N) 
                            self.v0 = float(new_velocity)
                            vx, vy = self.v0 * np.cos(Kutevi), self.v0 * np.sin(Kutevi)
                            self.v = np.stack((vx, vy), axis=1)
                            VELOCITY_INPUT.text_input = "Temperatura: " + str(new_velocity)
                            self.brzina_graf = math.sqrt((3*8.314*self.v0)/self.M)
                            self.crtanje_grafa()
                        except ValueError:
                            print("Krivi unos. Molimo upišite broj.")            

                if PARTICLE_INPUT.checkForInput(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        new_particles = input("Upišite novi broj čestica: ")
                        
                        try:
                            
                            new_N = int(new_particles)
                            if new_N > 200:
                                new_N = 200
                            if new_N <= 0:
                                new_N = 1
                            self.change(1, new_N, self.volume, self.v0)
                            self.add_particles(new_N)  
                            PARTICLE_INPUT.text_input = "Čestice: " + str(self.N)
                        except ValueError:
                            print("Krivi unos. Molimo upišite broj.")
                            self.crtanje_grafa()

                if RADIUS_INPUT.checkForInput(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        new_radius = input("Upišite novi polumjer: ")
                        try:
                            self.radius = float(new_radius)
                            RADIUS_INPUT.text_input = "Polumjer: " + str(self.radius)
                        except ValueError:
                            print("Krivi unos. Molimo upišite broj.")
                if VOLUME_INPUT.checkForInput(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        new_volume = input("Upišite novi volumen:")
                        self.change(3, self.N, float(new_volume), self.v0)
                        try:
                            self.adjust_particle_positions(new_volume)
                            VOLUME_INPUT.text_input = "Volumen: " + str(self.volume)
                        except ValueError:
                            print("Krivi unos. Molimo upišite broj.")
                            self.crtanje_grafa()

                if PRESSURE_INPUT.checkForInput(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        new_pressure = input("Upišite novi tlak: ")
                        try:
                            self.pressure = round(float(new_pressure))
                            PRESSURE_INPUT.text_input = "Tlak: " + str(round(self.pressure))
                            self.crtanje_grafa()
                        except ValueError:
                            print("Krivi unos. Molimo upišite broj.")
            

            if self.pressure >= 19.99:
                print("KABOOOM")
                self.border_rect = (0, 0, 2000, 2000)
                self.volume = 10000
                self.crtanje_grafa()

            self.step()
            self.draw_particles()
            
            clock.tick(60)       












    #Služi za računanje promjene na razini proporcionalnosti po formuli PV = NkT
    def change(self, promjena, new_N, new_volume, new_velocity):
        if self.hard == 0: #Ako je osjetljivi cilindar
            if promjena == 1:
                k = (new_N/ self.N)
                k_volume = k * self.volume
                if k_volume> 500:
                    self.pressure = (k / (500/(k_volume/k))) * self.pressure
                    self.adjust_particle_positions(500)
                if k_volume< 150:
                    self.pressure = (k / (150/(k_volume/k))) * self.pressure
                    self.adjust_particle_positions(150)
                else:
                    self.adjust_particle_positions(k_volume)


            if promjena == 2:
                k = (new_velocity/ self.v0)
                k_volume = k * self.volume
                if k_volume> 500:
                    self.pressure = (k / (500/(k_volume/k))) * self.pressure
                    self.volume = 500
                    self.adjust_particle_positions(500)
                if k_volume< 150:
                    self.pressure = (k / (150/(k_volume/k))) * self.pressure
                    self.volume = 150
                    self.adjust_particle_positions(150)
                else:
                    self.adjust_particle_positions(k_volume)

            if promjena == 3:
                if new_volume < 150:
                    new_volume = 150
                if new_volume > 500:
                    new_volume = 500
                k = (new_volume/ self.volume)
                self.pressure = float(self.pressure) / k
            

        if self.hard == 1: #Ako je čvrsti cilindar
            if promjena == 1:
                if new_N == 0 or self.N == 0:
                    self.pressure = 0
                else:
                    k = (new_N/ self.N)
                    self.pressure = k * self.pressure

            if promjena == 2:
                k = (new_velocity/ self.v0)
                self.pressure = k * self.pressure

            if promjena == 3:
                if new_volume < 150:
                    new_volume = 150
                if new_volume > 500:
                    new_volume = 500
                k = (new_volume/ self.volume)
                self.pressure = float(self.pressure) / k
            



#Općenito
pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h


screen = pygame.display.set_mode((screen_width-10, screen_height-50))

pygame.display.set_caption("Simulacija")
menu_surface = pygame.image.load("Pozadina_menu.png").convert()
test_font = pygame.font.Font(None, 50) 
naslov_font = pygame.font.Font(None, 100)
small_font = pygame.font.Font(None, 25)

admin = 0







def simulacija(): #Stvara početni prikaz
    pygame.display.set_caption("Menu")
    global admin

    while True:
        screen.blit(menu_surface, (0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        menu_tekst = naslov_font.render("SIMULACIJA IDEALNOG PLINA",True, "Black")
        menu_rect = menu_tekst.get_rect(center = (screen_width/2, 50))

        PRVI_BUTTON = Gumb(None, (400, 400), "SIMULACIJA S ČVRSTIM CILINDROM ", test_font, "Black", "White")
        DRUGI_BUTTON = Gumb(None, (1100, 400), "SIMULACIJA S OSJETLJIVIM CILINDROM", test_font, "Black", "White")
        if admin == 0:
            ADMIN_BUTTON = Gumb(None, (1200, 700), "ADMIN: OFF", test_font, "Black", "White")
        else:
            ADMIN_BUTTON = Gumb(None, (1200, 700), "ADMIN: ON", test_font, "Black", "White")
        QUIT_BUTTON = Gumb(None, (1400, 700), "IZAĐI", test_font, "Black", "White")

        screen.blit(menu_tekst,menu_rect)

        for gumb in [PRVI_BUTTON, DRUGI_BUTTON, ADMIN_BUTTON, QUIT_BUTTON]:
            gumb.changeColor(MENU_MOUSE_POS)
            gumb.update(screen)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PRVI_BUTTON.checkForInput(MENU_MOUSE_POS):
                    duljina = 500
                    border_rect = (50, 150, duljina, (duljina/500)*300)  # Border rectangle (x, y, width, height)
                    sim = IdealGasSimulation(N=100, molar_mass=0.032, radius=5, screen_width= screen_width, screen_height=screen_height, v0=100, duration=10, nsteps=1000, border_rect=border_rect, hard= 1, admin=admin)
                    sim.run_simulation()
                if DRUGI_BUTTON.checkForInput(MENU_MOUSE_POS):
                    duljina = 500
                    border_rect = (50, 150, duljina, (duljina/500)*300)  # Border rectangle (x, y, width, height)
                    sim = IdealGasSimulation(N=100, molar_mass=0.032, radius=5, screen_width= screen_width, screen_height=screen_height, v0=100, duration=10, nsteps=1000, border_rect=border_rect, hard= 0, admin=admin)
                    sim.run_simulation()
                if ADMIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if admin == 0:
                        admin = 1
                    else:
                        admin = 0
                        
                           
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()




simulacija()
                


