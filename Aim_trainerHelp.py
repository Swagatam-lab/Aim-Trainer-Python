# Import necessary libraries
import math  # For mathematical calculations (e.g., distance calculation)
import random  # To generate random positions for targets
import time  # To keep track of elapsed time
import pygame  # The game framework used for handling graphics, events, etc.

# Initialize Pygame library
pygame.init()

# Define the dimensions of the game window
WIDTH, HEIGHT = 800, 600  # Screen size
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window with the defined width and height
pygame.display.set_caption("Aim Trainer")  # Set the title of the game window

# Define constants used in the game
TARGET_INCREMENT = 400  # The time interval (milliseconds) after which a new target appears
TARGET_EVENT = pygame.USEREVENT  # A custom event in Pygame triggered when a new target appears
TARGET_PADDING = 30  # The padding to ensure targets don't appear too close to the edge
BG_COLOR = (0, 25, 40)  # Background color of the game window
LIVES = 3  # Number of lives (misses allowed) for the player
TOP_BAR_HEIGHT = 50  # Height of the top bar that displays game stats
LABEL_FONT = pygame.font.SysFont("comicsans", 24)  # Font used for labels like time, hits, etc.

# Class to represent a target (the red circles the player must click)
class Target:
    MAX_SIZE = 30  # Maximum size of a target
    GROWTH_RATE = 0.2  # How fast the target grows
    COLOR = "red"  # Outer color of the target
    SECOND_COLOR = "white"  # Inner color of the target

    # Initialize a target with given x, y coordinates
    def __init__(self, x, y):
        self.x = x  # X coordinate of the target's center
        self.y = y  # Y coordinate of the target's center
        self.size = 0  # Start size (it will grow over time)
        self.grow = True  # Determines whether the target is growing

    # Update the size of the target (grow or shrink)
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:  # If the target reached max size
            self.grow = False  # Start shrinking

        if self.grow:
            self.size += self.GROWTH_RATE  # Increase size if growing
        else:
            self.size -= self.GROWTH_RATE  # Decrease size if shrinking

    # Draw the target on the game window
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)  # Outer red circle
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)  # White inner circle
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)  # Another red circle
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)  # Small white inner circle

    # Check if the mouse click collides with the target
    def collide(self, x, y):
        dis = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)  # Calculate the distance between the mouse and target center
        return dis <= self.size  # Return True if the click is within the target's radius


# Function to draw the background and all targets on the screen
def draw(win, targets):
    win.fill(BG_COLOR)  # Fill the background with the defined color

    # Loop through all targets and draw each one
    for target in targets:
        target.draw(win)  # Call the draw method of each target


# Function to format the time display (mm:ss.ms)
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)  # Milliseconds part of the time
    seconds = int(round(secs % 60, 1))  # Seconds part of the time
    minutes = int(secs // 60)  # Minutes part of the time

    return f"{minutes:02d}:{seconds:02d}.{milli}"  # Return formatted time as mm:ss.ms


# Function to draw the top bar showing elapsed time, speed, hits, and lives left
def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))  # Draw the top bar rectangle
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")  # Display the formatted elapsed time

    speed = round(targets_pressed / elapsed_time, 1)  # Calculate the hit speed (targets per second)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")  # Display the speed

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")  # Display the number of hits

    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")  # Display remaining lives

    # Blit (draw) the labels onto the window
    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))


# Function to display the end screen after the game ends (showing stats and Restart option)
def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)  # Fill the background with the BG_COLOR
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")  # Display the final time

    speed = round(targets_pressed / elapsed_time, 1)  # Calculate final speed (targets/second)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")  # Display final speed

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")  # Display total hits

    accuracy = round(targets_pressed / clicks * 100, 1)  # Calculate accuracy as a percentage
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")  # Display accuracy

    # Display the stats on the screen
    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    # Draw the "Restart" button
    restart_label = LABEL_FONT.render("Restart", 1, "white")  # Display "Restart" text
    restart_rect = pygame.Rect(WIDTH//2 - restart_label.get_width()//2, 500, restart_label.get_width() + 20, restart_label.get_height() + 10)  # Create a rectangle for the button
    pygame.draw.rect(win, "green", restart_rect)  # Draw the green rectangle for the button
    win.blit(restart_label, (get_middle(restart_label), 505))  # Place the "Restart" text on the button

    pygame.display.update()  # Update the display with the new elements

    # Wait for events to handle clicks or quit
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the player clicks the window close button
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # If the player clicks the mouse
                if restart_rect.collidepoint(event.pos):  # Check if the click is on the "Restart" button
                    main()  # Restart the game by calling the main function

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # If the player presses "Q", quit the game
                    pygame.quit()
                    quit()


# Helper function to get the middle position for centering text
def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/2  # Returns the horizontal position to center the given text


# Main game loop
def main():
    run = True  # Control variable for the game loop
    targets = []  # List to store active targets
    clock = pygame.time.Clock()  # Pygame clock object to control FPS

    targets_pressed = 0  # Count of targets successfully clicked
    clicks = 0  # Total clicks by the player
    misses = 0  # Count of missed targets
    start_time = time.time()  # Record the start time of the game

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)  # Set a timer for TARGET_EVENT to trigger new targets

    while run:
        clock.tick(60)  # Limit the frame rate to 60 FPS
        click = False  # Variable to track if a click occurred
        mouse_pos = pygame.mouse.get_pos()  # Get the current position of the mouse
        elapsed_time = time.time() - start_time  # Calculate the elapsed time

        # Handle events (such as quitting, clicking, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the player clicks the close window button
                run = False  # Exit the game loop
                break

            if event.type == TARGET_EVENT:  # If the timer event triggers a new target
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)  # Generate a random X coordinate for the target
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)  # Generate a random Y coordinate
                target = Target(x, y)  # Create a new target at the random coordinates
                targets.append(target)  # Add the new target to the list

            if event.type == pygame.MOUSEBUTTONDOWN:  # If the player clicks the mouse
                click = True  # Register a click
                clicks += 1  # Increment the total click count

        # Update each target and check for clicks on targets
        for target in targets:
            target.update()  # Update the target size (grow or shrink)

            if target.size <= 0:  # If the target has shrunk completely
                targets.remove(target)  # Remove the target
                misses += 1  # Increment the miss count

            if click and target.collide(*mouse_pos):  # If a click occurred and it hits a target
                targets.remove(target)  # Remove the target (hit)
                targets_pressed += 1  # Increment the hit count

        if misses >= LIVES:  # If the player has missed too many targets
            end_screen(WIN, elapsed_time, targets_pressed, clicks)  # Show the end screen

        draw(WIN, targets)  # Draw the targets on the window
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)  # Draw the top bar with stats
        pygame.display.update()  # Update the display

    pygame.quit()  # Quit Pygame when the game loop ends


# Start the game by calling the main function
if __name__ == "__main__":
    main()
