import path_util
PROJECT_PATH = path_util.get_project_directory()

animations = {
    "knight": {
        "idle":    [
            f"{PROJECT_PATH}/sprites/knight/idle/idle0.png",
            f"{PROJECT_PATH}/sprites/knight/idle/idle1.png",
            f"{PROJECT_PATH}/sprites/knight/idle/idle2.png",
            f"{PROJECT_PATH}/sprites/knight/idle/idle3.png",
            f"{PROJECT_PATH}/sprites/knight/idle/idle4.png",
            f"{PROJECT_PATH}/sprites/knight/idle/idle5.png",
            f"{PROJECT_PATH}/sprites/knight/idle/idle6.png",
            f"{PROJECT_PATH}/sprites/knight/idle/idle7.png",
            f"{PROJECT_PATH}/sprites/knight/idle/idle8.png",
            f"{PROJECT_PATH}/sprites/knight/idle/idle9.png"
        ],
        "run":  [
            f"{PROJECT_PATH}/sprites/knight/run/run0.png",
            f"{PROJECT_PATH}/sprites/knight/run/run1.png",
            f"{PROJECT_PATH}/sprites/knight/run/run2.png",
            f"{PROJECT_PATH}/sprites/knight/run/run3.png",
            f"{PROJECT_PATH}/sprites/knight/run/run4.png",
            f"{PROJECT_PATH}/sprites/knight/run/run5.png",
            f"{PROJECT_PATH}/sprites/knight/run/run6.png",
            f"{PROJECT_PATH}/sprites/knight/run/run7.png",
            f"{PROJECT_PATH}/sprites/knight/run/run8.png",
            f"{PROJECT_PATH}/sprites/knight/run/run9.png"
        ],
        "attackA": [
            f"{PROJECT_PATH}/sprites/knight/attacka/attack0.png",
            f"{PROJECT_PATH}/sprites/knight/attacka/attack1.png",
            f"{PROJECT_PATH}/sprites/knight/attacka/attack2.png",
            f"{PROJECT_PATH}/sprites/knight/attacka/attack3.png"
        ],
        "attackB": [
            f"{PROJECT_PATH}/sprites/knight/attackb/spin0.png",
            f"{PROJECT_PATH}/sprites/knight/attackb/spin1.png",
            f"{PROJECT_PATH}/sprites/knight/attackb/spin2.png",
            f"{PROJECT_PATH}/sprites/knight/attackb/spin3.png"
        ],
        "roll": [
            f"{PROJECT_PATH}/sprites/knight/roll/roll0.png",
            f"{PROJECT_PATH}/sprites/knight/roll/roll1.png",
            f"{PROJECT_PATH}/sprites/knight/roll/roll2.png",
            f"{PROJECT_PATH}/sprites/knight/roll/roll3.png",
            f"{PROJECT_PATH}/sprites/knight/roll/roll4.png",
            f"{PROJECT_PATH}/sprites/knight/roll/roll5.png",
            f"{PROJECT_PATH}/sprites/knight/roll/roll6.png",
            f"{PROJECT_PATH}/sprites/knight/roll/roll7.png",
            f"{PROJECT_PATH}/sprites/knight/roll/roll8.png",
            f"{PROJECT_PATH}/sprites/knight/roll/roll9.png",
            f"{PROJECT_PATH}/sprites/knight/roll/roll10.png",
            f"{PROJECT_PATH}/sprites/knight/roll/roll11.png"
        ],
        "death": [
            f"{PROJECT_PATH}/sprites/knight/death/death0.png",
            f"{PROJECT_PATH}/sprites/knight/death/death1.png",
            f"{PROJECT_PATH}/sprites/knight/death/death2.png",
            f"{PROJECT_PATH}/sprites/knight/death/death3.png",
            f"{PROJECT_PATH}/sprites/knight/death/death4.png",
            f"{PROJECT_PATH}/sprites/knight/death/death5.png",
            f"{PROJECT_PATH}/sprites/knight/death/death6.png",
            f"{PROJECT_PATH}/sprites/knight/death/death7.png",
            f"{PROJECT_PATH}/sprites/knight/death/death8.png",
            f"{PROJECT_PATH}/sprites/knight/death/death9.png"
        ]
    },
    "wizard": {

    },
    "flyingeye": {
        "chasing": [
            f"{PROJECT_PATH}/sprites/flyingeye/chasing0.png",
            f"{PROJECT_PATH}/sprites/flyingeye/chasing1.png",
            f"{PROJECT_PATH}/sprites/flyingeye/chasing2.png",
            f"{PROJECT_PATH}/sprites/flyingeye/chasing3.png",
            f"{PROJECT_PATH}/sprites/flyingeye/chasing4.png",
            f"{PROJECT_PATH}/sprites/flyingeye/chasing5.png"
        ],
        "projectile": [
            f"{PROJECT_PATH}/sprites/eye_projectile/projectile0.png",
            f"{PROJECT_PATH}/sprites/eye_projectile/projectile1.png",
            f"{PROJECT_PATH}/sprites/eye_projectile/projectile2.png",
            f"{PROJECT_PATH}/sprites/eye_projectile/projectile3.png",
            f"{PROJECT_PATH}/sprites/eye_projectile/projectile4.png",
            f"{PROJECT_PATH}/sprites/eye_projectile/projectile5.png",
            f"{PROJECT_PATH}/sprites/eye_projectile/projectile6.png",
            f"{PROJECT_PATH}/sprites/eye_projectile/projectile7.png",
        ]
    },
    "skeleton": {

    },
    "goblin": {

    }
}