---
description: >-
  Feared for their aggression, Orcs have wandered these lands for generations.
  Their hunger is endless, and their brutal maces leave nothing but ruin.
icon: mace
---

# Orc

**Orcs** are hostile enemies introduced in the `v0.1.0-chapter1a` update. They are first encountered in `Act 2 - The Forest` and are characterized as strong and agressive&#x20;

### Stats:

* Level: `4+`
* HP:  100 (+ Level)
* Strength: 15 (+ Level)
* Speed: 5
* Intelligence: 5
* Defense: 10 (+ Level)
* Loot Table "orc"
* AP Bonus: 0-1

### Loot Table

| Item          | Chance |
| ------------- | ------ |
| Orc's Mace    | 5%     |
| Health Potion | 20%    |

### In Battle

Orcs typically attack alone, Orcs have very strong melee attacks, which can stagger the player for a few turns, immobilizing them

#### Enemy Behavior

Orcs have a **50%** chance to smash attack and a **50%** chance to use the basic attack. Orcs will still attempt to smash the player if the player is currently staggered, showing no mercy in combat

#### Attacks

{% tabs %}
{% tab title="Smash Attack" %}
### Smash Attack

The Orc smashes the ground at the player, creating a shockwave which can **stagger** the player. It also deals heavy AOE damage (In Multi-battles). This attack has a **30%** chance to miss

### Damage Formula

base\_strength + strength variation = total\_damage

base\_strength: The Orc's strength stat

strength\_variation: Random strength varation (-2 to 2)

### Special Effects

The player has a **20%** chance to be staggered, preventing actions for 1-2 turns
{% endtab %}

{% tab title="Basic Attack" %}
## Basic Attack

The Orc attacks the player like any other enemy, dealing damage based on their strength. This attack has a **10%** chance to miss!

### Damage Formula

base\_strength + strength variation = total\_damage

base\_strength: The Orc's strength stat

strength\_variation: Random strength varation (-2 to +2)

### Special Effects

None
{% endtab %}
{% endtabs %}

### Version History

| Version            | Change                                                                        |
| ------------------ | ----------------------------------------------------------------------------- |
| `v0.1.0-chapter1a` | Added Orc                                                                     |
| `v0.1.2-chapter1a` | The Orc in Act 2 now drops 3 Health Potions in addition to their regular loot |
