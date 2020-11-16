import tweepy
import time

input_user  = '@oifrancine'  #Coloque aqui o @ do twitter da pessoa
#  michael2biff
API_KEY = '3pjPmu6UAXvKJ6VYgw73gvmNC' #API KEY
API_SECRET = 'HYeMkP3CArVMQS2jNjiAuDnn8DrVlLrHAZUvvrCUphF0D81WxQ' #API secret key
#Bearer token AAAAAAAAAAAAAAAAAAAAAP2EJgEAAAAAz9MefKMjfjsBjIdzwbsRb6COTUQ%3DlAfdgfUW82S8v0qt8txiOMYcXrSh54imIluzWS1pgbotL5WMiW
API_TOKEN = '1326343100961353729-VNu5AGqslvSKdGQzWVRDk9s3SwvHZi' #acess token
API_TOKEN_SECRET = 'cDe5BBVGHonSQ4bRj5yULHqPm1iEEgzshRWpmrTX4TXr5' #acess token secret


auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(API_TOKEN, API_TOKEN_SECRET)

api = tweepy.API(auth)


#Traduz o texto pra morse
def to_morse(texto):

    morse = {'A': '.- ',     'B': '-... ',   'C': '-.-. ',
        'D': '-.. ',    'E': '. ',      'F': '..-. ',
        'G': '--. ',    'H': '.... ',   'I': '.. ',
        'J': '.--- ',   'K': '-.- ',    'L': '.-.. ',
        'M': '-- ',     'N': '-. ',     'O': '--- ',
        'P': '.--. ',   'Q': '--.- ',   'R': '.-. ',
     	'S': '... ',    'T': '- ',      'U': '..- ',
        'V': '...- ',   'W': '.-- ',    'X': '-..- ',
        'Y': '-.-- ',   'Z': '--.. ',

        '0': '----- ',  '1': '.---- ',  '2': '..--- ',
        '3': '...-- ',  '4': '....- ',  '5': '..... ',
        '6': '-.... ',  '7': '--... ',  '8': '---.. ',
        '9': '----. ', ' ': '/ ', '.': '.-.-.- ',
        ',': '--..-- ', '?': '	..--.. ', '@':'.--.- ',
        '!' : '-.-.-- ', '/': '-..-. ', '(': '-.--. ',
        ')': '-.--.- ', ':': '---...', 'Á': '.- ', 'Â': '.- ',
        'Ã':'.- ', 'É': '. ', 'Ê': '. ', 'Ô': '--- ', 'Ó': '--- '
        }


    tweet_traduzido  = ''

    for letra in texto:
        if letra.upper() in morse.keys():
            nova_letra = morse[letra.upper()]
        else:
            nova_letra = ''
        tweet_traduzido += nova_letra    

    return tweet_traduzido


#Checa por updates no perfil da pessoa
def update_last_tweet():
    t = api.user_timeline(id=user.id, include_rts=False)
    last_tweet_updated = t[0]
    return last_tweet_updated

#Descobre se o tweet possui imagem ou não
def has_media(tweet): 
    try:
        tweet.entities['media']
        return True
    except:
        return False

#Descobre se é retweet ou não
def is_retweet(tweet):
    try:
        tweet.entities['urls'][0]['display_url'] 
        return True
    except:
        return False


#Apaga o https no final do tweet
def https_erase(tweet_text):
    palavras = tweet_text.split()
    palavras.pop(-1)
    texto = ' '.join(palavras)
    return texto


#Restringe o tweet a 280 caracteres
def lenght_fix(tweet_traduzido):
    
    if len(tweet_traduzido) > 280:
        
        while len(tweet_traduzido) > 280:
            words = tweet_traduzido.split()
            words.pop(-1)
            tweet_traduzido = ' '.join(words)

    return tweet_traduzido        


user = api.get_user(input_user)
tweets = api.user_timeline(id=user.id, include_rts=False)
last_tweet = tweets[0]
print('Primeiro Tweet = ' + last_tweet.text)

while True:
    #checa por updates no último tweet
    last_tweet_updated = update_last_tweet()
    
    #começa a agir se houver update
    if last_tweet_updated.id != last_tweet.id:
        last_tweet = last_tweet_updated

        #Checa se o update não foi de uma mention
        if last_tweet.text[0] != '@':
            print('Novo Tweet Detectado = ' + last_tweet.text)
            
            #Se o tweet tiver media, o https dela é deletado
            if has_media(last_tweet) or is_retweet(last_tweet):
                pronto_pra_traduzir = https_erase(last_tweet.text)

            else:
                pronto_pra_traduzir = last_tweet.text 

            if pronto_pra_traduzir != '':      
                
                try:
                    #Transforma o tweet em 280 caracteres
                    tweet_traduzido = lenght_fix(to_morse(pronto_pra_traduzir))
                    
                    #Pega o id do ultimo tweet
                    
                    status = api.get_status(last_tweet.id).id
                    
                    #Publica o tweet traduzido
                    api.update_status(status=  tweet_traduzido, in_reply_to_status_id=last_tweet.id, auto_populate_reply_metadata=True)

                    print('Novo Tweet Postado = Texto : ' + tweet_traduzido)
                
                except:
                    print('-----------------------------------------------------------------ERROR--------------------------------------------------------------------------')
    
    time.sleep(15)
