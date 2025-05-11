import random
from colorama import Fore

# Battle Strings

def randomized_intro_messages(player, enemy): # Intro Messages 
    standard_messages = [
        Fore.GREEN + "You and " + Fore.RED + "the enemy" + Fore.GREEN + " stand at the ready, weapons drawn!",
        Fore.RED + "A tense silence fills the air as " + Fore.GREEN + player.name + Fore.RED + " stares down " + Fore.GREEN + enemy.name,
        Fore.YELLOW + "The ground trembles as both combatants prepare for the clash of battle!",
        Fore.BLUE + "A gust of wind swirls around as " + Fore.GREEN + player.name + Fore.WHITE + " faces off against " + Fore.RED + enemy.name,
        Fore.CYAN + "You feel your heart racing as the battle approaches its inevitable start.",
        Fore.MAGENTA + "The battle begins with a sudden charge as " + Fore.GREEN + player.name + Fore.MAGENTA + " squares up against " + Fore.RED + enemy.name,
        Fore.GREEN + "A bright flash of light blinds you for a second as you lock eyes with " + Fore.RED + enemy.name,
        Fore.WHITE + "The atmosphere is charged with tension as both warriors stare each other down.",
        Fore.YELLOW + "Dust kicks up around you as " + Fore.RED + enemy.name + Fore.YELLOW + " takes a step forward.",
        Fore.CYAN + "The wind howls through the battlefield. " + Fore.GREEN + player.name + Fore.WHITE + " grips their weapon tighter.",
        Fore.MAGENTA + "A strange energy fills the air as " + Fore.RED + enemy.name + Fore.MAGENTA + " cracks a wicked grin.",
        Fore.GREEN + "With a deep breath, you ready yourself. This is it.",
        Fore.RED + enemy.name + Fore.WHITE + " snarls, baring their teeth in anticipation.",
        Fore.BLUE + player.name + Fore.WHITE + " and " + Fore.RED + enemy.name + Fore.BLUE + " slowly circle each other.",
        Fore.YELLOW + "The battlefield is quiet... too quiet.",
        Fore.CYAN + player.name + Fore.WHITE + " senses danger in the air. " + Fore.RED + enemy.name + Fore.CYAN + " won’t go down easily.",
        Fore.MAGENTA + "Magic hums in the air. You feel the weight of the coming fight.",
        Fore.WHITE + "You’ve fought many before, but " + Fore.RED + enemy.name + Fore.WHITE + " feels different.",
        Fore.RED + "A bloodlust radiates from " + enemy.name + ". You steady your stance.",
        Fore.GREEN + player.name + Fore.WHITE + " grips their weapon. There’s no turning back now.",
    ]

    rare_epic = [
        Fore.MAGENTA + "The sky darkens unnaturally as " + Fore.RED + enemy.name + Fore.MAGENTA + " steps into the arena.",
        Fore.YELLOW + "Thunder cracks overhead. Even nature is watching this battle unfold.",
        Fore.RED + "You feel a chill crawl up your spine... something about " + enemy.name + " is deeply wrong.",
        Fore.CYAN + "Whispers echo from the shadows. The fight hasn’t started, but the fear has.",
        Fore.BLUE + "Time feels like it’s slowed. Every heartbeat, every breath—sharp and heavy.",
        Fore.MAGENTA + "A distant roar answers your challenge. This is no ordinary fight.",
    ]

    rare_funny = [
        Fore.GREEN + player.name + Fore.WHITE + ": 'This should be easy.'\n" + Fore.RED + enemy.name + Fore.WHITE + " trips, then glares at you.",
        Fore.RED + enemy.name + Fore.WHITE + " yells something incomprehensible. You nod politely.",
        Fore.YELLOW + "A chicken watches from the side, silently judging you.",
        Fore.WHITE + "The music kicks in. You accidentally strike a pose. " + Fore.RED + enemy.name + " is not impressed.",
        Fore.CYAN + "You forgot your battle speech. Just scream and hope it works.",
        Fore.MAGENTA + "You: 'Let's make this quick.'\n" + Fore.RED + enemy.name + Fore.WHITE + ": 'I was about to say that!'",
        Fore.YELLOW + "You feel like you've done this before... Deja vu?",
        Fore.GREEN + player.name + Fore.WHITE + " dramatically points their sword...\nIt squeaks.",
        Fore.RED + enemy.name + Fore.WHITE + " looks confused why you're just standing there. So are you.",
        Fore.BLUE + "Both of you take a deep breath, ready to—wait, is that a cat in the background?",
    ]

    roll = random.random()
    if roll < 0.1:
        return random.choice(rare_epic)
    elif roll < 0.2:
        return random.choice(rare_funny)
    else:
        return random.choice(standard_messages)

def player_attacks_first_message(player, enemy):
    messages = [
        Fore.GREEN + player.name + Fore.WHITE + " surges forward, seizing the opening without hesitation!",
        Fore.BLUE + "You waste no time — instinct takes over as you make the first move.",
        Fore.YELLOW + "Before " + enemy.name + " can even blink, you're already swinging.",
        Fore.MAGENTA + player.name + Fore.WHITE + " doesn't wait around. You strike first and ask questions never.",
        Fore.CYAN + "Speed is your weapon today. " + Fore.RED + enemy.name + Fore.CYAN + " isn't ready.",
        
        # Funny
        Fore.GREEN + player.name + Fore.WHITE + " yells 'Surprise!' and charges like a lunatic.",
        Fore.YELLOW + "Your feet move before your brain does. Hey, it worked.",
        Fore.CYAN + "You dash forward so fast, even YOU are surprised.",
        Fore.WHITE + "Quick thinking? Nope. Just good reflexes (and maybe panic).",
        Fore.BLUE + "You pretend you had a plan all along. " + Fore.RED + enemy.name + " doesn't need to know."
    ]
    return random.choice(messages)

def enemy_attacks_first_message(player, enemy):
    messages = [
        Fore.RED + enemy.name + Fore.WHITE + " lunges first, catching you slightly off guard!",
        Fore.MAGENTA + "You ready your stance, but " + Fore.RED + enemy.name + Fore.MAGENTA + " is already charging.",
        Fore.YELLOW + "Too late to react — the enemy strikes with terrifying speed.",
        Fore.CYAN + "You hesitate for just a moment. That’s all " + Fore.RED + enemy.name + Fore.CYAN + " needed.",
        Fore.BLUE + enemy.name + Fore.WHITE + " took the initiative. You're now on the defensive.",
        
        # Funny
        Fore.RED + enemy.name + Fore.WHITE + " trips and accidentally headbutts you. It still hurts.",
        Fore.YELLOW + "You blink. " + enemy.name + " doesn't. Oops.",
        Fore.CYAN + "You were busy trying to look cool. " + Fore.RED + enemy.name + Fore.CYAN + " was not.",
        Fore.MAGENTA + "A squirrel distracts you. That's when " + enemy.name + " attacks.",
        Fore.BLUE + enemy.name + Fore.WHITE + " used 'Confuse Ray'! It’s not very effective, but it still hit first."
    ]
    return random.choice(messages)

def random_initiative_message(player, enemy):
    messages = [
        Fore.WHITE + "Both " + player.name + " and " + Fore.RED + enemy.name + Fore.WHITE + " dash forward at once!",
        Fore.YELLOW + "A simultaneous clash — who lands the first hit?",
        Fore.CYAN + "Both sides move in perfect sync. Only fate will decide who strikes first.",
        Fore.BLUE + "A chaotic blur of motion erupts as both combatants charge!",
        Fore.MAGENTA + "Neither waits. Neither hesitates. One of you will land the first blow.",
        
        # Funny
        Fore.GREEN + player.name + Fore.WHITE + " and " + Fore.RED + enemy.name + Fore.WHITE + " both yell 'Go!' at the same time. Awkward.",
        Fore.YELLOW + "You both trip. You both recover. This is going to be weird.",
        Fore.CYAN + "You make eye contact and nod — then both of you sprint like lunatics.",
        Fore.BLUE + "A standoff! You both start yelling battle cries over each other.",
        Fore.RED + enemy.name + Fore.WHITE + " blinks. You blink. Nobody wins. Yet."
    ]
    return random.choice(messages)

def multi_battle_intro(player, enemies):
    enemy_count = len(enemies)

    normal_messages = [
        Fore.GREEN + player.name + Fore.WHITE + " faces off against " + str(enemy_count) + " enemies. No backing down now!",
        Fore.YELLOW + "The enemies gather, weapons raised. " + Fore.GREEN + player.name + Fore.YELLOW + " takes a deep breath.",
        Fore.CYAN + "They're surrounding you. It's not just a fight... it's a challenge.",
        Fore.MAGENTA + player.name + Fore.WHITE + " cracks their knuckles. Time to take them all on.",
        Fore.BLUE + "You feel the odds are stacked, but that never stopped you before.",
        Fore.RED + "Multiple foes approach. " + player.name + " stands alone, unshaken."
    ]

    funny_messages = [
        Fore.GREEN + player.name + Fore.WHITE + ": 'Okay, how many of you are there again?'",
        Fore.YELLOW + "One enemy growls. Then another. Then... you lose count.",
        Fore.CYAN + player.name + Fore.WHITE + " dramatically draws their weapon... and immediately trips.",
        Fore.MAGENTA + "You try to intimidate them with a cool pose. It kind of works.",
        Fore.RED + str(enemy_count) + " enemies? You've fought worse. Like that one time... never mind.",
        Fore.BLUE + "You accidentally yell your full battle plan out loud. Oops."
    ]

    serious_messages = [
        Fore.RED + "The battlefield is filled with hostile eyes. " + player.name + " prepares for war.",
        Fore.MAGENTA + "Shadows shift as your enemies encircle you. The tension is unbearable.",
        Fore.YELLOW + "This is no ordinary fight. You're outnumbered — and they know it.",
        Fore.CYAN + player.name + Fore.WHITE + " tightens their grip. There's no room for error.",
        Fore.GREEN + "Steel clashes with resolve. You are the last line of defense.",
        Fore.BLUE + "You feel the weight of the battle ahead. " + str(enemy_count) + " enemies... one you."
    ]

    roll = random.random()
    if roll < 0.1:
        return random.choice(serious_messages)
    elif roll < 0.3:
        return random.choice(funny_messages)
    else:
        return random.choice(normal_messages)

def multi_battle_player_goes_first(player, enemies):
    messages = [
        Fore.GREEN + player.name + Fore.WHITE + " charges ahead, striking before the enemy group can react!",
        Fore.YELLOW + "You rush forward with fierce determination — they weren’t ready for that!",
        Fore.BLUE + "You pick your target from the crowd and dive into battle.",
        Fore.CYAN + "With lightning speed, you disrupt their formation before they can act.",
        
        # Funny
        Fore.MAGENTA + player.name + Fore.WHITE + ": 'Guess I'll go first!'",
        Fore.RED + "You scream a battle cry and barrel toward the enemy mob. Bold move.",
        Fore.WHITE + "You're halfway into the fight before realizing no one followed.",
        Fore.BLUE + "You leap in, accidentally tripping over the first guy — hey, still counts.",
    ]
    return random.choice(messages)

def multi_battle_enemies_go_first(player, enemies):
    messages = [
        Fore.RED + "The enemy group surges forward, catching you slightly off guard!",
        Fore.YELLOW + "They move as one — overwhelming speed and aggression.",
        Fore.MAGENTA + "You raise your guard just in time as they make the first move.",
        Fore.CYAN + "You’re forced on the defensive as the entire group attacks at once.",
        
        # Funny
        Fore.RED + "One yells 'CHARGE!' and the rest just follow. Classic.",
        Fore.YELLOW + "You blink and suddenly they’re all screaming and running at you.",
        Fore.BLUE + "You were still picking targets when they all picked *you*.",
        Fore.RED + "The enemies jump you... You're alone and outnumbered... What a pitty",
        Fore.WHITE + "They bum-rush you with chaotic energy. Not very coordinated... but effective."
    ]
    return random.choice(messages)

def multi_battle_random_initiative(player, enemies):
    messages = [
        Fore.WHITE + "Both sides explode into action at once! It's pure chaos.",
        Fore.YELLOW + "You and your enemies rush in together — there's no clear advantage.",
        Fore.CYAN + "The battlefield erupts as everyone charges. Timing? Luck will decide.",
        Fore.BLUE + "It's a blur of motion as the clash begins all at once.",
        
        # Funny
        Fore.GREEN + "You shout 'GO!' — so do they. It’s awkward.",
        Fore.MAGENTA + "Everyone stumbles forward at the same time. Graceful? Not really.",
        Fore.RED + "You and three enemies try to hit the same guy. It’s confusing.",
        Fore.BLUE + "Someone yells 'WAIT!' but nobody listens. It's on.",
    ]
    return random.choice(messages)

splash_messages = [
    "Now with 100% more corruption!",
    "What do I put here?",
    "Check out my GitHub!",
    "This game is still in development.",
    "What is 1+1?",
    "Made by Priesty!",
    "Launcher by Donut!",
    "I wasted so much time on this.",
    "No art required!",
    "Peak gameplay?",
    "No one can beat Floor 50 of the Tower!",
    "Made by the worst coder in the world.",
    "XP is nerfed!",
    "Who is Priesty anyways?",
    "This game is ass.",
    "I lost my sanity making this",
    '"Python sucks for gamedev" - Donut',
    "Who the hell are you?",
    "Not a virus, Ignore Windows",
    "I ran out of ideas...",
    "Fear the shadows!",
    '"Turn based combat sucks" - Lavar',
    "Think before you act!",
    "Was that intended? Well it was now...",
    "Don't look at the commit history...",
    "Get your Cleansing Flute Today!",
    "Can you even call this a game?",
    "This game is the illusion of choice",
    "What even is this game?",
    "I can't spel",
    "Will this game ever be finished?",
    "10% good code, 90% shitty code",
    "Behave Yourself",
    "99% chance of a crash!",
    "What are you aiming at?",
    "Damage is nerfed by 400%!",
    "Git gud",
    "Play this game if you have free will",
    "Is it a bug? or is it a feature?",
    "New Update!",
    "Was it a bug? or was it the corruption?",
    "A swing and a miss!",
    "You can't escape the shadows!",
    "The shadows are always watching!",
    "That Goblin will remember that...",
    "Do people even read this?",
    "Made with love... and hate.",
    "Made with Python!",
    "No cheating (Janix)",
    "sys.quit(0)",
    "These are pretty random",
    "This isn't creative at all",
    "Read the README!",
    "Some issues will never be resolved.",
    "Running out of ideas...",
    "Share with your friends!",
    "Laugh at my terrible code!",
    "Buy an Iron Sword, it could save your life!",
    "The building is burning!",
    "Choose your side: Legion or Fist",
    "Contribute to the game on GitHub!",
    "Don't look directly at the bugs!",
    "Read the credits!",
    "Use your AP wisely!",
    "The shadows never sleep!",
]



def get_random_splash():
    splash = random.choice(splash_messages)

    # Remove surrounding quotes if any
    if splash.startswith('"') and splash.endswith('"'):
        stripped = splash[1:-1]
    else:
        stripped = splash

    discord_splash = f'"{stripped}"'  # Add clean quotes

    return splash, discord_splash