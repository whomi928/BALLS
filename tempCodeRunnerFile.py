for i in range(10):
                pygame.draw.circle(self.screen, (255, 255, 255), (self.center_x - 40 * i - 100,40), 15, width=2)
                pygame.draw.circle(self.screen, (255, 255, 255), (self.center_x + 40 * i + 100,40), 15, width=2)
                
            for i in range(self.red):
                i = i + 1
                pygame.draw.circle(self.screen, (255, 0, 0), (self.center_x - 40 * i - 100,40), 14, width=0)
                
            for i in range(self.blue):
                i = i + 1
                pygame.draw.circle(self.screen, (0, 0, 255), (self.center_x + 40 * i + 100,40), 14, width=0)