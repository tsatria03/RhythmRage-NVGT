# Introduction and commands

Levels must have the .lvl file extension.

Tutorials must have the .tut extension

Note: first line of the .lvl file is always the name of the level.
It does not matter what name your lvl has, only thing is that if you don't specify a *music name=*, the music file **must** have the same name with .ogg extension.

Note that, due to limitations outside of my control, blank lines aren't counted when showing errors. If you really must leave a blank space, try and put two slashes at the beginning (//)

## intro

This is the parser for the rhythm engine. This lets you create sounds and action maps for the game.
It is robust, flexible, and has many additional parameters which are useful and fun.
In order to make the game work properly, you need to provide the time for each sound and action so that the game knows when it should play sounds or you should press a key. But it is not so easy, as you need to know exactly which millisecond in the source music sound you need the sound or action to happen.
For this, I have provided a small program that will help you with that. It will look for a pack folder inside your packs folder letting you choose any sound from there and you'll be able to use many interesting commands to get the timing for the different actions (though you'll still need to write the level file yourself, as this is not a level creator!)

Using the program is very simple. Just select a file and press h to hear the different keyboard shortcuts you can use. Move to a place in the file using the different navigation commands and press enter to copy the milliseconds to your clipboard. :)

Note that you should *never* specify the .ogg extension from within the script, as it is assumed and it is the *only* format that the game will accept, no mp3 or anything.
If you are creating a level and you want to exit the game prematurely to continue making the level, hit escape while the music is playing.

## commands

### music

- volume=number 0 -20 specifies level bgm volume
- name=name of the level's bgm, optional, defaults at levelname.ogg
- jingle= optional, specifies the name of the level start jingle. It defaults to levelnamej and no extension must be specified as with all other sounds.
- perfect= and fail= let you change the music at the end of the level. if the level was a perfect or a fail, this music will play. normal pass and super are the same for every level in your pack (super_jingle and ok_jingle.ogg).

### comments

An important thing of every parser are comments. You can do these just like in bgt by adding a couple slashes (//) at the beginning of every line, and that line will then be ignored.
//Example: play a sound at the beginning of the song and set its pitch to 100
play name=example time=150 pitch=100

### play: play a sound

- name=name of the sound. If multiple sounds, sepparate with commas and no spaces.
- pitch=0-400
- volume=0- minus20
- pan=<-100,100>
- time=milliseconds, when to play the sound
- require= use this parameter to indicate that the sound should only play if you completed an action with the alias= set to the require= for this sound.
You can specify multiple actions to be required by sepparating them with commas, no spaces. Note that the actions are removed once they are checked, so if you complete an action with the same alias and get a successful require, the action will need to be completed again. This is done to prevent cheating.
- fail= use this parameter to play a sound if a require has failed.
- alias=: if you set an alias, you will be able to use this sound in a macro
- ach=: Must be the *last* item of the sound command. If all require aliases (if any) were successful you will hear newach.ogg and an achievement will be added which will save across sessions. The reason why there is an achievement for sounds is because of sounds that require actions to be completed. When typing the achievements it needs to be a sentence as long as you like, but it must be in one line, and must not contain the characters "==" together anywhere in it. If it does, you might start getting errors.


### action: tap a ke

- name=name of the sound or sounds to play upon correct completion of the action. If more than one sound it must be separated by commas with no spaces.
- fail=sound played when you make a wrong press, or you press too early. defaults to fail_generic
- early=sound played when you press a bit too early, defaults to failsound
- late=sound played when you press just a bit too late, as well as when you don't press in time. defaults to failsound
- miss= sound played when you hit the key way too early, or when you press the wrong key. defaults to failsound
- kp: indicates that this action is important and if you fail it, you will not be able to get a perfect or a super.
- pitch=0-100
- volume=0- minus20
- pan=-100,100
- time=milliseconds, when to play the sound. Based on the file position. For tap and hold actions, time= is used to indicate start time.
- end=: For tap and hold actions, the position in milliseconds where the user must release the key.
- ends=: The sound, or sounds to play, sepparated by commas and no spaces, when a tap and hold action is released successfully on time.
- efail=: the sound played when you successfully execute the start of a tap and hold action, but let go at the wrong time. Defaults to failsound
- key=enter,space,up,down,right,left,abcdefghijklmnopqrstuvwxyz1234567890 which key you need to press for the action to work
- alias=: This is used for sound playing (together with require=) and macros. If you want a sound to play only if a certain action was completed, use alias=and a name, then in the sound use require= and the same name
- ach=: Must be the *last* item of the action command. If this action was also completed successfully, you will hear newach.ogg and an achievement will be added which will save across sessions. When typing the achievements it needs to be a sentence as long as you like, but it must be in one line, and must not contain the characters "==" together anywhere in it. If it does, you might start getting errors.

Note: Please keep in mind that, when creating macros, only the first instance of alias= will be used and subsequent alias=definitions will only be used for require and the macro will not be replaced. if you want to create another macro with the same sound, please give it a different alias. This is done to avoid confusion.

### misc

This lets you configure many things in your level. You can currently modify the following values:

- super: The minimum percentage of good actions that you must obtain to get a super (maximum is always 99), default is 94).
- ok: The least percentage to obtain an ok and unlock the next level (max is always 1 less than super, default minimum is 80).
- cooldown: If you want your level to freeze for a bit before being able to do another action when you fail or press a wrong key, set a cooldown value greater than 0 in milliseconds (default is 0).
- reaction: The time that a user has to press actions in this level (default is 150 which means 75ms too early and 75 too late).

### debug

This, for now, lets you seek to a specified point in your level. All actions and sounds before that point will be ignored so you can test:

- seek=number: jump to that millisecond in the music
- mode: sets debug mode on. If you set debug mode on, all actions will be played automatically. This is to test that your actions are timed correctly and that everything is in sync with the music. No additional parameters are necessary. For example, debug mode seek=520 or simply debug mode.

## creating macros

Creating macros is very simple. Once you have defined actions or sounds with different aliases by using the alias keyword, you can put them together to quickly create the same action patterns over and over without worrying too much about the time, because you will only need to specify the time of the first action.
The sintax is simple: The macro line must contain alias tags sepparated by a comma, with no spaces. Then a space and the time of the first action.
Optionally you can give it a name after the time, so that you can refer to it later without having to copy paste all the actions
The time for tap and hold actions is specified with commas:
! tapsound1,tapaction 5000,8000 macroname

This means the time starts at 5000 and at 8000 user must release.

Let me give you an example: we have a sound called warning that plays an alarm one beat before I swing the ball. After I swing the ball, we wait another beat until you have to return that ball.
We could have something like this:
play name=warn_sound alias=warning time=250
play name=swing_sound time=500 alias=swing
action name=return_sound alias=return time=750 fail=hit_net

Now, let's say we have to do the same thing but on beats 4 5 and 6
It is as simple as saying this:
! warn,swing,return 1000 ball
Now we will have warn at 1000, swing at 1250, and return at 1500. Simple isn't it?
This macro has the name ball, so if we wanted that same ball to swing again at 10000, we could just do this:
@ ball 10000

Now it really is simple.

## making the tutorial

the tutorial is easy to make. It should have the same name as the level, but instead of .lvl, the extension is .tut.
It uses the same commands as the main levels, but with the following restrictions:

1. Macros aren't allowed
2. actions aren't allowed, only say. (see below)
3. In the tutorial, commands need to be sorted. (see below)

The tutorial works by playing sounds and making your screen reader or sapi speak. It will play music, which can be paused via the pause command.
You need to make sure that the music file is long enough for the tutorial to be completed, as it will not loop. However, you can use the restart or seek command (without debug!) to seek to the beginning of the file, and old lines will not be processed. You can also stop, show some text, and load the music again (the usual thing to do).
The main difference between the actual game and the tutorial is that it is necessary to sort your commands properly here. This makes the tutorial cleaner. If you don't sort your commands, they will never be read!

But I'm lazy, I don't want to sort my commands!

well, in this case, you have to. The tutorial is read directly from the file and does not load the level, and does each thing as it happens. Besides, by having your commands ordered you can jump to anywhere in the file, at any time, pause, wait a few milliseconds for something to happen, play sounds when there is no music, and other wonderful things. So trust me, sorting your commands is a good idea.

### special tutorial commands

- text: text, a space, and any text after that will speak the given text and wait for user to press enter.
- play: Play a sound just like in the normal game, but no requires are allowed. sintax is play filename time, or play filename to play at that point in the file and not wait for the music or if there is no music.
- music filename [volume] [seek]: plays a music file for the tutorial. volume is optional. Defaults to 0 which is maximum. If you specify seek, volume must also be specified (0 is usually what you want). Example: music my_music 0 500. would set volume to 0 and go to position 500 milliseconds.
- pause time: Typing pause and a position in milliseconds will pause the music and continue with the tutorial.
- stop: stops the music immediately
- fade: fades out the music
- exit: break execution and exit game entirely
- restart: go back to the beginning of the music to make room for new commands.
- seek: jump to a specified place in the file
- stopsounds: stops all playing sounds, though not music, only sounds started via the play command. useful for tap and hold actions, to stop the action sound when the user should have released the key.
- jump: Jumps to that specific point in the tutorial. you can have as many jumps as you like, and the last one will be used. It is effective only when creating a pack (i.e: when users play the pack, the tutorial wll never jump.
- wait: Wait a number of milliseconds before doing something, useful for playing sounds with no music or showing some text
- playwait name: Play a sound file and wait for it to finish, or interrupt if user presses enter, escape or space.
- say: Say something via the tts. If you want it to say something at a specified time, use the play and/or wait functions (useful for indicating when an action should be done)

### tutorial example

text hi, I am a tutorial
text this level is very easy. I will play a sound with some music, then fade out. just for fun
text I will show you how the wait command, the play command, and the music command work
text I'll play a sound and wait, now
play sound1
wait 500
text see? I played, and waited a bit before this text.
text lets try with music

music 1 -5
play warning 500
say warning!
play shoot 1000
say enter!
play shoot_action
wait 2000
stop
fade
text bye!

# command line operation

You can run game.exe from the command line, with a level (i.e., game.exe remix.lvl): This will make the game skip all the menus and run the level directly. it needs to be on the packs folder as usual. The jingle will not be played if the level is run from the command line, to save time.
Don't even try to run a level from the command line if you're not creating a pack... You cheating fool!

## additional information

Your pack can also contain other files. Some of the files that don't error out if they are not present are:

- logo: played when the game starts or when the pack is changed.
- win_pack: played when you beat the last level of the pack.

## still having problems?

Still having problems figuring out how this works? Here is an example.
You can't play this example, this is just for documentation purposes. This is from the remix1 level.

remix 1
debug mode seek=1
music name=mix1 jingle=remixjingle volume=-2
play name=s_taste time=3450 pan=50 alias=r1
play name=s_my time=3565 pan=50 alias=r2
play time=3750 name=s_blade pan=50 alias=r3
action name=s_parryr,s_grunt pan=50 time=4050 fail=s_pfail key=right alias=r4
//heil
play name=1heil time=4620 alias=rh1
play name=1hitler time=4900 alias=rh2
action name=1shoot fail=1early time=5200 alias=rh3 key=enter
! rh1,rh2,rh3 5810 hitler
@ hitler 6100
@ hitler 6980
play name=3num1 time=7850
play name=3smallswing time=8150
play name=3smallswing time=8280
play name=3bigswing time=8400
action name=3smallhit key=space time=8730
action name=3smallhit key=space time=8870
action name=3bighit key=enter time=9015
//factory
play name=4comingshort pan=50 time=9320
play name=4coming time=9880
action name=4short key=right time=10480 ends=4okshort end=11050
//another
play name=4comingshort pan=-50 time=11640
play name=4coming time=12220
action name=4short key=left time=12810 ends=4okshort end=13390
@ hitler 14250
@ hitler 15130
//test
play name=mixt1 time=16300 alias=t1
play name=mixt1 time=16590 alias=t2
play name=mixt1 time=16885 alias=t3
action name=mixt2 key=enter alias=t4 fail=1bad time=17170
! t1,t2,t3,t4 17465 test
! r1,r2,r3,r4 18560 taste
play name=s_taste time=18880 pan=-50 alias=l1
play name=s_my time=19000 pan=-50 alias=l2
play time=19180 name=s_blade pan=-50 alias=l3
action name=s_parryl,grunt3 pan=-50 time=19450 fail=s_pfail key=left alias=l4
@ test 19800
play name=5coming time=20960 alias=f1
action name=5hit key=space alias=f2 time=21250
! f1,f2 21540 ff
play name=5three time=22130
@ ff 22130
@ ff 22420
! f1 22705
action name=5bighit key=space alias=fb time=22990
play name=3up time=23290 alias=d1
action name=3dir key=up alias=d2 fail=3fail time=23580
play name=3down time=23870 alias=d3
action name=3dir key=down alias=d4 fail=3fail time=24160
play name=3right time=24450 alias=d5
action name=3dir key=right alias=d6 fail=3fail time=24750
play name=3left time=25000 alias=d7
action name=3dir key=left alias=d8 fail=3fail time=25330
//three
play name=5three time=25620
@ ff 25620
@ ff 25910
! f1 26210
! fb 26480
@ ff 26780
play name=5contra time=27230 alias=fo1
action name=5hit key=space time=27520 alias=fo2
@ ff 27955
! fo1,fo2 28390 fo
@ fo 28830
@ fo 29260
play name=4comingshort pan=50 time=29700
play name=4coming time=30000
action name=4short key=right time=30285 ends=4okshort end=30870
play name=4comingshort pan=-50 time=30870
play name=4coming time=31160
action name=4short key=left time=31450 ends=4okshort end=32030

@ ff 32030
play name=3tap time=32615
action key=enter fail=3tapfail name=3tapok time=32910
action key=enter fail=3tapfail name=3tapok time=33200
action key=enter fail=3tapfail name=3tapok time=33490
action key=enter fail=3tapfail name=3tapok time=33780
action key=enter fail=3tapfail name=3tapok time=34075
action key=enter fail=3tapfail name=3tapok time=34360
action key=enter fail=3tapfail name=3tapok time=34660
action key=enter fail=3tapfail name=3tapok time=34950
action key=enter fail=3tapfail name=3tapok time=35240
action key=enter fail=3tapfail name=3tapok time=35530
action key=enter fail=3tapfail name=3tapok time=35795
action key=enter fail=3tapfail name=3tapok time=36100
play name=3stop time=36000
play name=6tot time=37250 alias=tot1
play name=6el time=37400 alias=tot2
play name=6camp time=37550 alias=tot3
action name=6campa time=37820 key=space alias=tot4
action name=6campa key=space time=37960 alias=tot5
action name=6campa key=space time=38100 alias=tot6
! tot1,tot2,tot3,tot4,tot5,tot6 38420 totelcamp
@ totelcamp 39590
play name=6chu time=40740 alias=mad1
play name=6tael time=40960 alias=mad2
play name=6ma time=41160 alias=mad3
play name=6drid time=41320 alias=mad4
action name=6paras time=41600 ends=6para fail=6parafail key=enter end=41930 alias=mad5
@ totelcamp 41920
@ totelcamp 43100
! mad1,mad2,mad3,mad4,mad5 44260 mad
@ mad 45420
play name=3num2 time=46280
play name=3smallswing time=46600 alias=sw1
play name=3bigswing time=46870 alias=sw2
play name=3smallswing time=47170 alias=sw3
play name=3bigswing time=47455 alias=sw4
action name=3smallhit key=space time=47750 alias=sw5
action name=3bighit key=enter time=48050 alias=sw6
action name=3smallhit key=space time=48340 alias=sw7
action name=3bighit key=enter time=48630 alias=sw8
! sw1,sw2,sw3,sw4,sw5,sw6,sw7,sw8 48920 twoswings
@ totelcamp 51240
@ totelcamp 52410
! r1,r2,r3,r4 53540
! l1,l2,l3,l4 54700
@ mad 55900
@ mad 57060
play name=4cominglong time=58230
play name=4coming time=58830
action name=4long fail=4faillong time=59390 key=enter ends=4oklong end=60570

Copyright Oriol Gómez & Guilevi Productions 2016