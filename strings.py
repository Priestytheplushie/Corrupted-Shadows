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
