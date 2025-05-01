---
description: >-
  The first target of the Corruption, Goblins became meaner, faster, and
  stronger, targeting blood rather than bags
icon: diamond-exclamation
---

# Corrupted Goblins

**Corrupted Goblins** are versions of **Goblins** introduced in `v0.1.0-chapter1a`. They are the first encounter in the game, and have slightly different behaviors than regular Goblins

### Stats

* Level: `1+`
* HP: 35 (+ Level)
* Strength: 10 (+ Level)
* Speed: 25
* Intelligence: 0
* Defense: 0
* Loot Table: "goblin"

### In Battle

Corrupted Goblins usually attack in a **group**, with either other Corrupted Monsters, or by themselves. They are known to be very aggressive and to kill on sight

#### Enemy Behavior

Corrupted Goblins have a 2**0%** chance to attempt to rob the player and a 8**0%** chance to use the regular attack. Goblins will not attempt to rob if the player's balance is **0**

#### **Unstable Variant**

**Unstable Goblins have a 20% chance to attempt to rob the player, a 60% chance to attack normally, and a 20% chance to fail attacking and damage themselves**

#### Attacks

{% tabs %}
{% tab title="Basic Attack" %}
## Basic Attack

The goblin attacks the player like any other enemy, dealing damage based on their strength. This attack has a **10%** chance to miss!

### Damage Formula

base\_strength + strength variation = total\_damage

base\_strength: The Goblin's strength stat

strength\_variation: Random strength varation (-2 to +2)

### Special Effects

None
{% endtab %}

{% tab title="Rob" %}
## Rob

The Goblin attempts to pick your pockets, stealing a random amount of money and dealing damage in the process. This attack has a **50%** chance to miss!

### Damage Formula

base\_strength + -2 to +2 = raw\_damage

#### Stolen Money Formula

The goblin steals from 1 to the maximum amount of money the player has, but the total amount stolen is divided by 2

### Special Effects

The player loses the money stolen by the Goblin
{% endtab %}

{% tab title="Fail" %}
## Attack Failure

Corrupted Goblins which are unstable have a **20%** chance to fail attacking, taking damage from the corruption

### Damage Formula

5 = total\_damage

### Special Effects

The Goblin becomes imobolized for that turn
{% endtab %}
{% endtabs %}

### Version History

| Version            | Change                                                                                            |
| ------------------ | ------------------------------------------------------------------------------------------------- |
| `Pre-Development`  | Added `Corrupted Goblin`                                                                          |
| `v0.1.0-chapter1a` | Added Unstable Varient                                                                            |
| `v0.2.0-chapter1`  | `Goblins` (including corrupted variants) now steal half as much, and drop 15% more Health Potions |
