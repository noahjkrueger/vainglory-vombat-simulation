import matplotlib.pyplot as plt
import heroes, items
from sys import argv
import argparse


# Is there a better way to do this?
def create_item(item):
    if item.upper() == "SORROWBLADE":
        return items.SorrowBlade()
    elif item.upper() == "TYRANTSMONOCLE":
        return items.TyrantsMonocle()
    elif item.upper() == "TORNADOTRIGGER":
        return items.TornadoTrigger()
    elif item.upper() == "POISONEDSHIV":
        return items.PoisonedShiv()
    elif item.upper() == "BONESAW":
        return items.BoneSaw()
    elif item.upper() == "SPELLSWORD":
        return items.Spellsword()
    elif item.upper() == "SIXSINS":
        return items.SixSins()
    elif item.upper() == "SERPENTMASK":
        return items.SerpentMask()
    elif item.upper() == "SWIFTSHOOTER":
        return items.SwiftShooter()
    elif item.upper() == "BLAZINGSALVO":
        return items.BlazingSalvo()
    elif item.upper() == "HEAVYSTEEL":
        return items.HeavySteel()
    elif item.upper() == "LUCKYSTRIKE":
        return items.LuckyStrike()
    elif item.upper() == "PIERCINGSPEAR":
        return items.PiercingSpear()
    elif item.upper() == "BOOKOFEULOGIES":
        return items.BookOfEulogies()
    elif item.upper() == "MINIONSFOOT":
        return items.MinionsFoot()
    elif item.upper() == "TENSIONBOW":
        return items.TensionBow()
    elif item.upper() == "BARBEDNEEDLE":
        return items.BarbedNeedle()
    elif item.upper() == "BREAKINGPOINT":
        return items.BreakingPoint()
    elif item.upper() == "WEAPONBLADE":
        return items.WeaponBlade()
    else:
        print(f"\033[91mERR i-i:\033[0m Invalid item name \033[1m'{item}'\033[0m - misspelling, malformed or not implemented")
        exit(-1)


# Is there a better way to do this?
def create_hero(hero_name, level, stutter):
    if hero_name.upper() == "AMAEL":
        return heroes.Amael(level, stutter)
    elif hero_name.upper() == "ADAGIO":
        return heroes.Adagio(level, stutter)
    elif hero_name.upper() == "ALPHA":
        return heroes.Alpha(level, stutter)
    elif hero_name.upper() == "ANKA":
        return heroes.Anka(level, stutter)
    elif hero_name.upper() == "ARDAN":
        return heroes.Ardan(level, stutter)
    elif hero_name.upper() == "BAPTISTE":
        return heroes.Baptiste(level, stutter)
    elif hero_name.upper() == "BARON":
        return heroes.Baron(level, stutter)
    elif hero_name.upper() == "BLACKFEATHER":
        return heroes.Blackfeather(level, stutter)
    elif hero_name.upper() == "CAINE":
        return heroes.Caine(level, stutter)
    elif hero_name.upper() == "CATHERINE":
        return heroes.Catherine(level, stutter)
    elif hero_name.upper() == "CELESTE":
        return heroes.Celeste(level, stutter)
    elif hero_name.upper() == "CHURNWALKER":
        return heroes.Churnwalker(level, stutter)
    elif hero_name.upper() == "FLICKER":
        return heroes.Flicker(level, stutter)
    elif hero_name.upper() == "FORTRESS":
        return heroes.Fortress(level, stutter)
    elif hero_name.upper() == "GLAIVE":
        return heroes.Glaive(level, stutter)
    elif hero_name.upper() == "GRACE":
        return heroes.Grace(level, stutter)
    elif hero_name.upper() == "MIHO":
        return heroes.Miho(level, stutter)
    else:
        print(f"\033[91mERR h-i:\033[0m Invalid hero name \033[1m'{hero_name}'\033[0m - misspelling, malformed or not implemented")
        exit(-1)


# Create a hero with items and other options
def create_player(hero_name, build, level, stutter):
    if not 1 <= level <= 12:
        print(f"\033[91mERR h-l:\033[0m Invalid level \033[1m'{hero_name}'\033[0m - valid values are in range [1, 12]")
        exit(-1)
    if len(build) > 6:
        print(f"\033[93mWARN i-c:\033[0m \033[1m Too Many Items \033[0m - more than 6 items provided; inaccurate to actual gameplay. May skew results.")
    item_objs = list()
    for item in build:
        item_objs.append(create_item(item))
    hero_obj = create_hero(hero_name, level, stutter)
    hero_obj.init_build(item_objs)
    return hero_obj


def main(args):
    # Define arguments
    parser = argparse.ArgumentParser(
        prog="python3 simulate_combat.py",
        description="Generates a graph representing a 1v1 battle between two heroes",
        prefix_chars="-",
    )
    parser.add_argument(
        "hero_one",
        type=str,
        help="The first hero to engage in combat"
    )
    parser.add_argument(
        "hero_two",
        type=str,
        help="The second hero to engage in combat"
    )
    parser.add_argument(
        "--items_one",
        type=str,
        nargs="+",
        default="",
        help="The items Hero One has equipped"
    )
    parser.add_argument(
        "--items_two",
        type=str,
        nargs="+",
        default="",
        help="The items Hero Two has equipped"
    )
    parser.add_argument(
        "--level_one",
        type=int,
        default=1,
        help="The level of Hero One"
    )
    parser.add_argument(
        "--level_two",
        type=int,
        default=1,
        help="The level of Hero Two"
    )
    parser.add_argument(
        "--stutter_one",
        action='store_true',
        help="Hero One uses stutter stepping"
    )
    parser.add_argument(
        "--stutter_two",
        action='store_true',
        help="Hero Two uses stutter stepping"
    )
    # Parse Args
    args = parser.parse_args(args)
    hero_one = create_player(args.hero_one, args.items_one, args.level_one, args.stutter_one)
    hero_two = create_player(args.hero_two, args.items_two, args.level_two, args.stutter_two)
    # Collect data to form 4 lines
    h1_hp = list()
    h2_hp = list()
    h1_dmg = list()
    h2_dmg = list()
    milliseconds = 0
    while True:
        if hero_one.stats['current_hp'] <= 0:
            h1_hp.append(0)
            h2_hp.append(hero_two.stats['current_hp'])
            break
        if hero_two.stats['current_hp'] <= 0:
            h1_hp.append(hero_one.stats['current_hp'])
            h2_hp.append(0)
            break
        # HP at this ms
        h1_hp.append(hero_one.stats['current_hp'])
        h2_hp.append(hero_two.stats['current_hp'])
        # Attacks (possibly) delivered at this time
        # Maybe make points?
        h1_attack = hero_one.basic_attack()
        h2_attack = hero_two.basic_attack()
        # Get hit by opposing attack
        h1_ack = hero_one.receive_attack(h2_attack)
        h2_ack = hero_two.receive_attack(h1_attack)
        # Do post attack processing
        hero_one.process_attack_ack(h2_ack)
        hero_two.process_attack_ack(h1_ack)
        # Add damage at this ms to graph
        h1_dmg.append(h2_ack["true_dmg"] + h2_ack["cp_dmg"] + h2_ack["wp_dmg"])
        h2_dmg.append(h1_ack["true_dmg"] + h1_ack["cp_dmg"] + h1_ack["wp_dmg"])
        milliseconds += 1
    # Plot lines
    plt.plot([x if h1_dmg[x] > 0 else None for x in range(0, len(h1_dmg))], [h1_dmg[y] if h1_dmg[y] > 0  else None for y in range(0, len(h1_dmg))], 'b.', label=f"Hero 1 DMG", zorder=15)
    plt.plot(h1_hp,  label=f"Hero 1 HP", zorder=5)
    plt.plot([x if h2_dmg[x] > 0 else None for x in range(0, len(h2_dmg))], [h2_dmg[y] if h2_dmg[y] > 0 else None for y in range(0, len(h2_dmg))], 'r.', label=f"Hero 2 DMG", zorder=10)
    plt.plot(h2_hp,  label=f"Hero 2 HP", zorder=0)
    # Legend, labels and grid
    plt.legend()
    plt.title(f"Hero 1: {hero_one.name} vs Hero 2: {hero_two.name}")
    plt.xlabel("Milliseconds")
    plt.ylabel("Points")
    plt.grid()
    plt.margins(0.01)
    plt.tight_layout()
    # Save to file
    plt.savefig(f"{hero_one.name}_vs_{hero_two.name}", dpi=300)


if __name__ == '__main__':
    main(argv[1:])
