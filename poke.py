import asyncio

import discord
from discord.ext import commands
from BuildTeam import check_pokemon as checkP
from BuildTeam import add_move as checkM
from StartBattle import health_value as ChangeHP
import pokebase as pb
import csv_writer


class Poke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addpoke', help='Adds a pokemon to your team')
    async def addpoke(self, ctx, pokename):
        player_id = ctx.author.id
        pokes = csv_writer.get_pokes(player_id)
        poke_num = checkP(pokename, self.bot.lists)
        if pokes is None:
            csv_writer.add_player(ctx.author.id)
            pokes = []
        if len(pokes) == 6:
            await ctx.send(f"You already have a full roster! Say `.clearteam` to clear your team.")
        elif poke_num == 0:
            await ctx.send(f"{pokename} is not a valid Pokemon!")
        else:
            def check(m):
                return m.author == ctx.author

            await ctx.send(f"{pokename} has been added to your roster! You now have `{6-len(pokes)}` slots available.")
            await ctx.send(f"Which move do you want to set as {pokename}'s first move? Say exit to leave")
            moves = []
            while len(moves) < 4:
                try:
                    msg = await self.bot.wait_for('message', timeout=30.0, check=check)
                    if msg.content.lower() == 'exit':
                        await ctx.send("Successfully exited the moves adder.")
                        break
                    elif not checkM(poke_num, msg.content):
                        await ctx.send("That move isn't possible for this selected Pokemon!")
                    elif msg.content.lower() in moves:
                        await ctx.send("You already have that move added!")
                    else:
                        moves.append(msg.content.lower())
                        await ctx.send(f"{msg.content} added!")
                except asyncio.TimeoutError:
                    await ctx.send('Time ran out! Run the function again.')
                    break
            if len(moves) == 4:
                csv_writer.add_poke(player_id, poke_num, moves)
                await ctx.send("All your moves have been added!")

    @commands.command(name='clearteam', help='Removes all pokemon from your team')
    async def clearteam(self, ctx):
        try:
            csv_writer.clear_pokes(ctx.author.id)
            await ctx.send("Team Cleared!")
        except csv_writer.PlayerError:
            await ctx.send("You don't even have a team!")

    @commands.command(name='team', help='Lists your team')
    async def team(self, ctx):
        rstr = "```"
        pokelist = csv_writer.get_pokes(ctx.author.id)
        for i, item in enumerate(pokelist):
            rstr += f"\nPokemon #{i+1}"
            rstr += f"\n   {pb.pokemon(item['id'])}: {', '.join(item['moves'])}"
        await ctx.send(rstr+"```")

    @commands.command(name='battle', help='Starts a poke battle')
    async def battle(self, ctx, opponent: discord.User):
        if not csv_writer.validate_player(ctx.author.id):
            await ctx.send("You don't have a valid team! Run `.addpoke`")
        elif not csv_writer.validate_player(opponent.id):
            await ctx.send(f"<@{opponent.id}> doesn't have a valid team!")
        else:
            msg = await ctx.send('Starting battle, please wait for setup.')
            p1_list = csv_writer.get_pokes(ctx.author.id).copy()
            p2_list = csv_writer.get_pokes(opponent.id).copy()
            p_ids, p_dict = [], {}
            for poke in p1_list:
                p_ids.append(poke['id'])
            for poke in p2_list:
                p_ids.append(poke['id'])
            for j in p_ids:
                p_dict[j] = pb.pokemon(j)
            p1_cp = [p1_list[0], p_dict[p1_list[0]['id']].stats[0].base_stat + 60]
            p2_cp = [p2_list[0], p_dict[p2_list[0]['id']].stats[0].base_stat + 60]
            p1_list.pop(0)
            p2_list.pop(0)
            while True:
                # Player 1 Screen (Author)
                p1 = discord.Embed(title=p_dict[p1_cp[0]['id']].name+f": {p1_cp[1]} HP", description=
                                   f"Enemy: {p_dict[p2_cp[0]['id']].name}({p2_cp[1]} HP)")
                p1.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                p1.add_field(name=p1_cp[0]['moves'][0], value='a', inline=False)
                p1.add_field(name=p1_cp[0]['moves'][1], value='b', inline=False)
                p1.add_field(name=p1_cp[0]['moves'][2], value='c', inline=False)
                p1.add_field(name=p1_cp[0]['moves'][3], value='d', inline=False)
                p1.set_footer(text=f"Pokemon Left({len(p1_list)}): {', '.join([p_dict[poke['id']].name for poke in p1_list])}")
                await msg.edit(embed=p1)
                await msg.add_reaction('1️⃣')
                await msg.add_reaction('2️⃣')
                await msg.add_reaction('3️⃣')
                await msg.add_reaction('4️⃣')
                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
                reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
                try:
                    if str(reaction.emoji) == '1️⃣':
                        p2_cp[1] = ChangeHP(p1_cp[1], p1_cp[0]['moves'][0], p1_cp[0]['id'], p2_cp[0]['id'], p_dict)
                        await msg.remove_reaction('1️⃣', ctx.message.author)
                    elif str(reaction.emoji) == '2️⃣':
                        p2_cp[1] = ChangeHP(p1_cp[1], p1_cp[0]['moves'][1], p1_cp[0]['id'], p2_cp[0]['id'], p_dict)
                        await msg.remove_reaction('2️⃣', ctx.message.author)
                    elif str(reaction.emoji) == '3️⃣':
                        p2_cp[1] = ChangeHP(p1_cp[1], p1_cp[0]['moves'][2], p1_cp[0]['id'], p2_cp[0]['id'], p_dict)
                        await msg.remove_reaction('3️⃣', ctx.message.author)
                    else:
                        p2_cp[1] = ChangeHP(p1_cp[1], p1_cp[0]['moves'][3], p1_cp[0]['id'], p2_cp[0]['id'], p_dict)
                        await msg.remove_reaction('4️⃣', ctx.message.author)
                except TimeoutError:
                    await msg.edit('Time ran out. Please run battle again.')
                    break
                await ctx.send(f'Current health of enemy is now {p2_cp[1]}')
                if p2_cp[1] <= 0:
                    p2_list.pop(0)
                    if len(p2_list) > 0:
                        p2_cp = [p2_list[0], p_dict[p2_list[0]['id']].stats[0].base_stat + 60]
                    else:
                        await ctx.send('Player 2 has won!')
                        break
                # Player 2 Screen
                p2 = discord.Embed(title=p_dict[p2_cp[0]['id']].name + f": {p2_cp[1]} HP", description=
                f"Enemy: {p_dict[p1_cp[0]['id']].name}({p1_cp[1]} HP)")
                p2.set_author(name=f"{opponent}", icon_url=f"{opponent.avatar_url}")
                p2.add_field(name=p2_cp[0]['moves'][0], value='a', inline=False)
                p2.add_field(name=p2_cp[0]['moves'][1], value='b', inline=False)
                p2.add_field(name=p2_cp[0]['moves'][2], value='c', inline=False)
                p2.add_field(name=p2_cp[0]['moves'][3], value='d', inline=False)
                p2.set_footer(
                    text=f"Pokemon Left({len(p1_list)}): {', '.join([p_dict[poke['id']].name for poke in p1_list])}")
                await msg.edit(embed=p2)

                def check2(reaction, user):
                    return str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣']

                reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check2)
                try:
                    if str(reaction.emoji) == '1️⃣':
                        p1_cp[1] = ChangeHP(p2_cp[1], p2_cp[0]['moves'][0], p2_cp[0]['id'], p1_cp[0]['id'], p_dict)
                        await msg.remove_reaction('1️⃣', opponent)
                    elif str(reaction.emoji) == '2️⃣':
                        p1_cp[1] = ChangeHP(p2_cp[1], p2_cp[0]['moves'][1], p2_cp[0]['id'], p1_cp[0]['id'], p_dict)
                        await msg.remove_reaction('2️⃣', opponent)
                    elif str(reaction.emoji) == '3️⃣':
                        p2_cp[1] = ChangeHP(p2_cp[1], p2_cp[0]['moves'][2], p2_cp[0]['id'], p1_cp[0]['id'], p_dict)
                        await msg.remove_reaction('3️⃣', opponent)
                    else:
                        p2_cp[1] = ChangeHP(p2_cp[1], p2_cp[0]['moves'][3], p2_cp[0]['id'], p1_cp[0]['id'], p_dict)
                        await msg.remove_reaction('4️⃣', opponent)
                except TimeoutError:
                    await msg.edit('Time ran out. Please run battle again.')
                    break
                if p1_cp[1] <= 0:
                    p1_list.pop(0)
                    if len(p2_list) > 0:
                        p1_cp = [p1_list[0], p_dict[p1_list[0]['id']].stats[0].base_stat + 60]
                    else:
                        await ctx.send('Player 1 has won!')
                        break

def setup(bot):
    bot.add_cog(Poke(bot))
