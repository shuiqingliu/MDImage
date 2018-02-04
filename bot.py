# -*- coding: UTF-8 -*-

from uuid import uuid4
from telegram.utils.helpers import escape_markdown
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton,InlineKeyboardMarkup)
from telegram import InlineQueryResultArticle, ParseMode,InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler,\
     InlineQueryHandler,CallbackQueryHandler
import config,logging,DBHelper,OperationStore

#set logging format
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

#store user,ak,sk,host
bucketTemp = ''
#bot start
def start(bot,updater):
    updater.message.reply_text(
        'Hi! I\'m MDImage Bot. I will help you to upload image to qiniu.\n '
        'Send your qiniu ak and sk to me.\n\n'
        'example: /token <xxxxx> <yyyyy> \n'
        'x is you ak,y is you sk',)

def token(bot, updater, args, chat_data):
    user = updater.message.from_user
    logger.info("DBHelper get username result: %s",DBHelper.getData(user.username))
    #check whether user exist in db,if not then insert else update data
    if DBHelper.getData(user.username) == False:
        insetResult = DBHelper.insertData(user.username, args[0], args[1], args[2], ' ')
        if insetResult  == False:
            updater.message.reply_text('Account binding error,try again later.')
    else:
        updateResult = DBHelper.update(user.username, args[0], args[1], args[2], ' ')
        if updateResult == False:
            updater.message.reply_text('Sorry,I can\'t update your info,Please check your input')
    #show inline keyboard let use select bucket that they want to use.
    reply_markup = chooseBucket(args[0],args[1])
    updater.message.reply_text('Please choose your bucket:',reply_markup=reply_markup)
    def storeData(bucket):
        pass

# def

def photo(bot, updater):
    user = updater.message.from_user
    storedUser = DBHelper.getData(user.username)
    #check whether user has been binded,if yes then send image to qiniu else reminder.
    if storedUser == False:
        updater.message.reply_text('You show binding your qiniu account before you send image to store\n'
                                   'like /token ak,sk,host')
    else:
        photo_file = bot.get_file(updater.message.photo[-1].file_id)
        photo_file.download('user_photo.jpg')
        logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    updater.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

def button(bot, update):
    query = update.callback_query
    bucket = query.data
    username = query.message.chat.username
    logger.info("bucket is %s,username is %s",bucket,username)
    # insert user info to db
    updateBucketResult = DBHelper.updateBucket(username,bucket)
    if updateBucketResult:
        bot.send_message(chat_id=query.message.chat_id,text='Your account binding success!')
    else:
        bot.send_message(chat_id=query.message.chat_id, text='Account binding error,try again later.')

def chooseBucket(ak,sk):
    bukcets = OperationStore.getBucketList(ak,sk)
    logger.info("buckets is %s",bukcets)
    #create inlinekeyboard data
    keyboard = []
    for bukcet in bukcets:
        keyboard.append([InlineKeyboardButton(bukcet,callback_data=bukcet)])
    #rely to user
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def getInfo(bot,updater):
    username = updater.message.from_user.username
    result = DBHelper.getData(username)
    print('=======')
    print(result)
    if result != False:
        ak   = result[0][1]
        sk   = result[0][2]
        host = result[0][3]
        bucket  = result[0][4]
        updater.message.reply_text('Your info as follows:\n\nak:{}\n sk:{}\n host:{}\n bucket:{}\n use /token command to change it'.format(ak,sk,host,bucket))
    else:
        updater.message.reply_text('Sorry,Can\'t found your information!')

def cancel(bot, updater):
    user = updater.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    updater.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    updater = Updater(token=config.BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start',start))
    dispatcher.add_handler(CommandHandler('token',token,pass_args=True,pass_chat_data=True))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo))
    dispatcher.add_handler(CommandHandler('getInfo',getInfo))
    dispatcher.add_handler(CommandHandler('cancel',cancel))

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()