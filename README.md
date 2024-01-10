# Souls Switcher
This little python script lets you play several From Software games in random order. Every X seconds, the game will change randomly. For the moment, it only works for Dark Souls Remastered, Dark Souls 2 (Scholar of the First Sin), Dark Souls 3, Sekiro and Elden Ring.<br><br>
![image (1)](https://github.com/bbordere/SoulsSwitcher/assets/45495330/44ede203-95f6-4e82-bb8c-4dde78fa29bf)

## How to use it ?
1) Requirements
   - [Python 3.X](https://www.python.org/downloads/)
   - Python modules listed in requirement.txt
2) Install
   ```shell
   git clone https://github.com/bbordere/SoulsSwitcher.git 
   cd SoulsSwitcher/
   pip install -r requirements.txt
   ```
3) Setup<br>
    The graphical interface lets you select games for the random choice loop and customize game time ranges. You can also choose to make a definite number of loops or leave in infinite mode.
    For this to work, you **MUST** place and pin the games to the taskbar in this **ORDER** (start from the leftmost location on the taskbar).
    - Dark Souls Remastered
    - Dark Souls 2 (Scholar of the First Sin)
    - Dark Souls 3
    - Sekiro
    - Elden Ring
     <br><br>
Without this precise sequence, the program **WILL NOT** run correctly. You must pin the executables to prevent Windows from changing their order.
If you don't have one of the games, you need to replace its location in the taskbar with another executable of your choice (e.g. Google Chrome).
For some reasons, you need to run Elden Ring without anticheat for it to work.

3) Run
   ```shell
   cd SoulsSwitcher/ # Only if you are not already in the directory
   python app.py
   ```
## Next Step
It's simply a dirty little script that lets you switch games in a rather inconvenient way. 
Many things could be improved to make this project more user-friendly, such as the ability to choose games directly via the GUI by selecting a window.As it is, it simply serves as a proof of concept of funny idea.
