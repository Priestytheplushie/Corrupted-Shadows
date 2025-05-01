---
description: >-
  Small, but chaotic, Goblins were once petty thieves, but something changed
  within their hearts, causing their new, vicious behavior
icon: face-smile-horns
---

# Goblins

**Goblins** are hostile enemies introduced in `v0.1.0-chapter1a`. They are first encountered in `Act 2 - The Forest` and are characterized as vicious and greedy

### Stats

* Level: `1+`
* HP: 45 (+ Level)
* Strength: 5 (+ Level)
* Speed: 10
* Intelligence: 0
* Defense: 0
* Loot Table: "goblin"

### Loot Table

| Item          | Chance |
| ------------- | ------ |
| Health Potion | 30%    |
| Goblin Tooth  | 70%    |
| Goblin Dagger | 15%    |

### In Battle

Goblins in battle typically attack **in a group.** Goblins have a tendency to steal, in which they will take money and coins from the player.&#x20;

#### Enemy Behavior

Goblins have a **30%** chance to attempt to rob the player and a **70%** chance to use the regular attack. Goblins will not attempt to rob if the player's balance is **0**

#### Attacks:

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
{% endtabs %}

### Version History

| Version            | Change                                                                                  |
| ------------------ | --------------------------------------------------------------------------------------- |
| `v0.1.0-chapter1a` | Added `Goblin`                                                                          |
| `v0.2.0-chapter1`  | `Goblins` now steal half as much and have a increased chance of dropping Health Potions |
