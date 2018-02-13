# -*- coding: UTF-8 -*-

from telegram import (InlineKeyboardButton,InlineKeyboardMarkup)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler,\
     CallbackQueryHandler
import config,logging,DBHelper,OperationStore,requests,os

#set logging format
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

#bot start
def start(bot,updater):
    updater.message.reply_text(
        'Hi! I\'m MDImage Bot. I will help you to upload image to qiniu.\n '
        'Send your qiniu ak,sk,host to me.\n\n'
        'example: /token <ak> <sk> <host>\n'
        'eg: /token 1sdfs 2sdfsd qinliu.qiniudn.com')

#start binding user info
def token(bot, updater, args, chat_data):
    user = updater.message.from_user
    logger.info("DBHelper get username result: %s",DBHelper.getData(user.username))
    #check whether user exist in db,if not then insert else update data
    if DBHelper.getData(user.username) == False:
        insetResult = DBHelper.insertData(user.username, args[0], args[1], args[2], ' ')
        if insetResult  == False:
            updater.message.reply_text('Account binding error,try again later.')
    else:
        logger.info('Start update userinfo!')
        updateResult = DBHelper.update(user.username, args[0], args[1], args[2], ' ')
        logger.info(updateResult)
        if updateResult == False:
            updater.message.reply_text('Sorry,I can\'t update your info,Please check your input')
    #show inline keyboard let use select bucket that they want to use.
    reply_markup = chooseBucket(args[0],args[1])
    updater.message.reply_text('Please choose your bucket:',reply_markup=reply_markup)
    def storeData(bucket):
        pass

def photo(bot, updater):
    user = updater.message.from_user
    storedUser = DBHelper.getData(user.username)
    #check whether user has been binded,if yes then send image to qiniu else reminder.
    if storedUser == False:
        updater.message.reply_text('You show binding your qiniu account before you send image to store\n'
                                   'like /token ak,sk,host')
    else:
        photo_id = updater.message.photo[-1].file_id
        photo_file = bot.get_file(updater.message.photo[-1].file_id)
        json_url = ('https://api.telegram.org/bot' + config.BOT_TOKEN +
                    '/getFile?file_id=' + photo_id)
        file_path = (requests.get(json_url).json())['result']['file_path']
        file_name = file_path.split('/')[1]
        print(file_name)
        photo_url = 'https://api.telegram.org/file/bot' + config.BOT_TOKEN + "/" + file_path
        photo_file.download(os.getcwd() + 'image/{}'.format(file_name))
        #get user details
        userDetails = DBHelper.getDetails(user.username)
        logger.info(photo_url)
        if userDetails:
            ak = userDetails[0]
            sk = userDetails[1]
            host = userDetails[2]
            bucket = userDetails[3]
            #upload image to qiniu bucket
            photoUploadResult = OperationStore.sendImageFromLocal(ak,sk,bucket,file_name)
            if photoUploadResult:
                #reply to user MarkDownLink
                updater.message.reply_text(createMD(file_name,host))
            else:
                updater.message.reply_text('Upload to qiniu bucket failed.Try again later.')
        else:
            updater.message.reply_text('Can\'t found your information in database.')

        #delet Download File
        try:
            os.remove('./image/{}'.format(file_name))
        except:
            logger.info('Delete File {} error'.format(file_name))

#inlineKeyboardButton callback deal,to get user select data and other info
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

#create keyboar button from bucket list
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

#get db stored info about current user
def getInfo(bot,updater):
    username = updater.message.from_user.username
    result = DBHelper.getData(username)
    if result != False:
        ak   = result[0][1]
        sk   = result[0][2]
        host = result[0][3]
        bucket  = result[0][4]
        updater.message.reply_text('Your info as follows:\n\n ak:{}\n sk:{}\n host:{}\n bucket:{}\n\n Use /token command to change it'.format(ak,sk,host,bucket))
    else:
        updater.message.reply_text('Sorry,Can\'t found your information!')

#create MarkDown image URL
def createMD(filename,host):
    url = 'http://{}/{}'.format(host,filename)
    MDLink = '![{}]({})'.format(filename,url)
    return MDLink
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
    dispatcher.add_handler(CommandHandler('getinfo',getInfo))
    dispatcher.add_handler(CommandHandler('cancel',cancel))

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()