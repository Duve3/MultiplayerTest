import pygame
from network import Network

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, player, playerList):
    win.fill((255, 255, 255))
    player.draw(win)
    print(f"{playerList = }")
    for plr in playerList:
        plr.draw(win)
    pygame.display.update()


def main():
    run = True
    network = Network()
    print("made NETWORK")  # rm
    player = network.getSelfPlayer()
    print("GOT SELF PLR")  # rm
    clock = pygame.time.Clock()
    print("CLOCK MADE")  # rm

    while run:
        clock.tick(60)
        playerList, player = network.sendPlayerData(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        collisionList = [pygame.Rect(plr.rect) for plr in playerList]
        collision = pygame.Rect.collidelist(pygame.Rect(player.rect), collisionList)
        if collision != -1:
            print(f"{collision = }")
            network.playerHit(playerList[collision])

        player.move()
        print(f"{player.health = }")
        redrawWindow(win, player, playerList)

    network.disconnect()


if __name__ == "__main__":
    main()
