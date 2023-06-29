import discord
from discord import utils
import config

client = discord.Client(intents=discord.Intents.all())

class MyClient(discord.Client):
# Проверка готовности бота
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
# Добавление роли с помощью реакций
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.POST_ID:
            channel = self.get_channel(payload.channel_id) # получаем объект канала
            message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
            member = payload.member # получаем объект пользователя который поставил реакцию
            print(member)
 
            try:
                emoji = str(payload.emoji) # эмоджик который выбрал юзер
                role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)
            
                if(len([i for i in member.roles if i and i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
                    await member.add_roles(role)
                    print('{0.display_name} Получил роль {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('[ERROR] Too many roles for user {0.display_name}'.format(member))
            
            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))
 
    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id) # получаем id канала
        message = await channel.fetch_message(payload.message_id) # получаем id сообщения
        user_id = payload.user_id # по сути эта херня не нужна, но на всякий случай не трож
        member = await (await client.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)
        print(member, user_id)
 
        try:
            emoji = str(payload.emoji) # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)
    
            await member.remove_roles(role)
            print('{1.name} ушла от {0.display_name}'.format(member, role))
 
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))

# RUN
client = MyClient(intents=discord.Intents.all())
client.run(config.TOKEN);import discord