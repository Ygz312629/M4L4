import discord
from discord.ext import commands
from config import TOKEN

#  Botun mesajları alabilmesi için bir intents nesnesi oluştur
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# '!' öneki ile komutlar için bir bot nesnesi oluştur
bot = commands.Bot(command_prefix='!', intents=intents)

# Kullanıcı görevlerini saklamak için bir sözlük. Anahtar: kullanıcı ID'si, değer: görev listesi
tasks = {}

# Bot başarıyla başlatıldığında tetiklenen bir olay
@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı.')

# Görev yönetimi komutu
@bot.command()
async def task(ctx, action=None, *, content=None):
    # Komutu çağıran kullanıcının ID'sini al
    user_id = ctx.author.id
    # Eğer kullanıcının henüz hiç görevi yoksa, kullanıcı için boş bir görev listesi oluştur
    if user_id not in tasks:
        tasks[user_id] = []

    # Görev ekleme komutunu işle
    if action == 'add':
        task_id = len(tasks[user_id]) + 1  # Görev ID'si oluştur
        tasks[user_id].append({'id': task_id, 'content': content})  # Görevi kullanıcının listesine ekle
        await ctx.send(f'Görev eklendi: {content} (ID: {task_id})')  # Onay mesajı gönder

    # Görev kaldırma komutunu işle
    elif action == 'remove':
        if content and content.isdigit():  # Geçerli bir görev ID'si sağlanıp sağlanmadığını kontrol et
            task_id = int(content)  # Görev ID'sini sayıya dönüştür
            task_list = tasks[user_id]  #Kullanıcının görev listesini al
            # Görevi ID'ye göre ara
            task_to_remove = next((task for task in task_list if task['id'] == task_id), None)
            if task_to_remove:
                task_list.remove(task_to_remove)  # Görevi listeden kaldır
                await ctx.send(f'ID {task_id} olan görev kaldırıldı.')  # Onay mesajı gönder
            else:
                await ctx.send(f'ID {task_id} olan görev bulunamadı.')  # Görev bulunamadıysa bilgilendir
        else:
            await ctx.send('Lütfen kaldırmak için geçerli bir görev ID sağlayın.')  # Hata mesajı gönder

    # Görev listesini gösterme komutunu işle
    elif action == 'list':
        task_list = tasks[user_id]  # Kullanıcının görev listesini al
        if task_list:
            # Görev listesiyle bir yanıt oluştur
            response = "Mevcut görevleriniz:\n"
            response += "\n".join([f"ID: {task['id']}, Açıklama: {task['content']}" for task in task_list])
        else:
            response = "Hiç göreviniz bulunmuyor."  # Kullanıcıya görev olmadığını bildir
        await ctx.send(response)  # Görev listesini gönder

    # Bilinmeyen bir komut işleniyorsa
    else:
        await ctx.send('Bilinmeyen eylem. Lütfen add, remove veya list kullanın..')

# Yardım bilgilerini göstermek için ayrı bir komut
@bot.command()
async def info(ctx):
    response = (
        "Mevcut komutlar:\n"
        "!task add [görev açıklaması] - Yeni bir görev ekler.\n"
        "!task remove [görev ID'si] - Belirtilen ID'ye sahip görevi kaldırır.\n"
        "!task list - Mevcut görevlerin listesini gösterir.\n"
        "!info - Bu yardım bilgilerini görüntüler."
    )
    await ctx.send(response)  # Yardım bilgilerini gönder

# Botu token ile çalıştır
bot.run(TOKEN)
