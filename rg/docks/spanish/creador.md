# Introducción y comandos

Los niveles deben tener la extensión .lvl

Los tutoriales deben tener la extensión .tut

La primera línea del archivo .lvl se usará siempre como título (nombre) para el nivel, que se muestra en el menú.

Nota sobre la música de los niveles: no importa el nombre del archivo lvl, solo que si no especifícas el comando *music name=*, el archivo de la música debe tener el **mismo nombre** que el archivo lvl pero con la extensión .ogg.

Ten en cuenta que, dada la manera en que está hecho el programa, las líneas vacías no se cuentan a la hora de mostrar errores. si de verdad necesitas tener una línea en blanco, intenta poner 2 barras al principio como si fuera un comentario (//)

## intro

Este es el archivo de ayuda para los creadores de niveles. Esto te permite crear planos de sonidos, acciones y configuración para el juego.
Es robusto pero flexible, y tiene muchos parámetros adicionales para configurar el nivel a tu medida.
Para que el juego funcione bien, debes especificar el tiempo en milisegundos de cada sonido y acción para que el juego sepa cuándo reproducir un sonido o esperar una acción del jugador. Pero tienes que buscar el milisegundo exacto dentro de una canción.
Para esto, he creado un programa que te ayudará, la herramienta de niveles. De momento está en inglés, pero no es difícil de entender (la ayuda está traducida). Te permitirá abrir cualquier sonido dentro de la carpeta del pack y tiene muchos comandos interesantes para que puedas obtener bien el tiempo dentro de la canción (eso sí, tendrás que escribir igual el archivo del nivel, no es un creador de niveles!).

El programa es fácil de usar.  Elije un archivo y pulsa la h para saber los comandos que puedes usar. Muévete a un lugar determinado del archivo y pulsa enter para copiar la posición del cursor al portapapeles. :)

Nota: Nunca especifiques la extensión .ogg porque el juego ya lo tiene asumida. Es el único formato que se acepta, no mp3 ni wav.
Si estás haciendo un nivel y quieres cerrar el juego de golpe, pulsa escape mientras se reproduce la música. Esto saldrá del juego directamente.

## comandos

Son en inglés, pero los explico a continuación.

### music

- volume=número 0 -20 especifica el volumen de la música. 0 máximo -20 mínimo
- name=nombre de la música del juego. por defecto el mismo que el lvl pero .ogg
- jingle= opcional; especifica la música de intro al nivel. por defecto lo mismo que el lvl con una j al final.
- perfect= y fail= te permiten cambiar la música al final del nivel si consigues un fail o un perfect. Los de ok y super siempre son iguales (ok_jingle y super_jingle).

### comentarios

Una parte importante  de cualquier archivo con código. Puedes hacerlos igual que en bgt, poniendo dos barras (//) al principio de la línea.
//Ejemplo de comentario: Reproduce un sonido al inicio de la canción.
play name=example time=150

### play: reproduce un sonido

- name=nombre del sonido. si quieres más de uno, sepáralos por comas, sin espacios.
- pitch=0-400: el tono del sonido
- volume=0- minus20
- pan=<-100,100>: la posición en estéreo del sonido, a veces es útil cambiarla, por si quieres un sonido a la derecha con la flecha derecha etc. -100 a la izquierda del todo, 100 a la derecha.
- time=milisegundos cuándo reproducir el sonido.
- require= usa este parámetro para indicar que se reproduzca solo si se ha completado correctamente una acción determinada que tenga el alias (alias=) especificado en el require.
si necesitas más de una acción sepáralas por comas sin espacios. Una vez se comprueba una acción se elimina, así que si completas una acción correctamente y haces un require bien, tendrás que completarla otra vez para el próximo require. eso elimina la posibilidad de hacer trampas.
- fail=usa este parámetro para reproducir un sonido si el require falla.
- alias=: poniendo un alias a un sonido hace posible usarlo en una macro.
- ach=: Debe ser el último parámetro del sonido! Si todos los alias de require (si los hay) se completan correctamente, oirás el sonido newach.ogg del pack y conseguirás un nuevo logro, que se guarda en todos los juegos. Cuando escribas el logro debe estar en una sola línea y no debe contener los caracteres ==.

### action: pulsa una tecla

- name=nombre del sonido o sonidos separados por comas sin espacios a reproducir cuando la acción se completa correctamente.
- fail=sonido que se reproduce cuando no pulsas a tiempo o pulsas demasiado pronto.
- early=sonido que se reproduce cuando pulsas un poco demasiado pronto. defecto failsound
- late=sonido que se reproduce cuando pulsas tarde. por defecto failsound
- miss=sonido que se reproduce cuando pulsas muy pronto o pulsas la tecla incorrecta.
- kp: indica que esta acción es importante y, si no la haces bien, no podrás conseguir un perfect ni un super.
- pitch=0-100: el tono
- volume=0- minus20
- pan=-100,100: la posición estéreo
- time=milisegundos, basado en la posición del archivo. para acciones de pulsar y mantener, time= indica el tiempo de comienzo (donde pulsas).
- end=: para acciones de pulsar y mantener, posición en la que el jugador tendrá que soltar la tecla.
- ends=:el sonido o sonidos separados por comas que se reproducirán si el jugador deja de pulsar en el momento indicado.
- efail=: el sonido reproducido cuando el jugador pulsa correctamente la acción de mantener, pero suelta en el tiempo equivocado. Por defecto failsound
- key=enter,space,up,down,right,left,abcdefghijklmnopqrstuvwxyz1234567890 tecla a pulsar para que la acción funcione.
- alias=: esto se usa para los require de los sonidos y también para las macros. Deberás especificar lo mismo que en el require= para que se reconozcan uno al otro.
- ach=: Debe ser el último parámetro de la acción! Oirás el sonido newach.ogg del pack y conseguirás un nuevo logro, que se guarda en todos los juegos. Cuando escribas el logro debe estar en una sola línea y no debe contener los caracteres ==.

Por favor: ten en cuenta que cuando crees las macros, solo se usará la primera instancia de un alias y las llamadas siguientes solo se usarán para require y la macro no se reemplazará. si quieres crear otra macro con el mismo sonido, dale otro alias.

### misc

Esto te permite configurar varias opciones del nivel: Por ahora puedes cambiar lo siguiente.

- super: el porcentage mínimo que debes conseguir para obtener un  super (máximo siempre es 99, mínimo por defecto 94).
- ok: el porcentage mínimo a obtener para esbloquear el siguiente nivel y obtener un ok (máximo siempre es uno menos que súper, mínimo por defecto es 80).
- cooldown: Si fallas una acción y quieres que el nivel no te deje continuar por cierto tiempo, configura este valor. No podrás pulsar ninguna tecla por el número de milisegundos que pongas aquí. Por defecto es 0.
- reaction: el tiempo que tiene el jugador para pulsar acciones en ese nivel (por defecto son 150 lo que son 75ms demasiado pronto y 75 tarde).

### debug

Esto te permite activar el modo automático y/o ir a una posición concreta del archivo, saltando los sonidos y accciones  anteriores.

- seek=: salta a ese milisegundo de la música
- mode: activa el modo automático, realizando automáticamente todas las acciones y sonidos de forma automática para que calcules si todos los tiempos están bien.

## creación de macros

Crear macros es muy sencillo. Una vez hayas creado un patrón de sonidos y acciones, puedes encadenarlos sin preocuparte después por los tiempos, ya que solo tienes que especificar el tiempo de la primera acción!
LA sintaxis es muy simple. Primero va un signo de exclamación (!), un espacio, las acciones separadas por comas y sin espacios, otro espacio, y el tiempo de la primera acción. De forma adicional, puedes también poner otro espacio y especificar un alias para esa macro, para no tener que escribir todos los alias todo el rato.
El tiempo para las acciones de pulsar y mantener se especifica entre comas.
! sonidopulsar1,accionpulsar 5000,8000 nombredelamacro

Esto significa que empieza en 5000 y al 8000 el usuario deja de pulsar

Te voy a dar un ejemplo: tenemos un sonido, atencion, que se reproduce un tiempo antes de que yo tire la pelota. Cuando tire la pelota, esperamos un tiempo antes de que tengas que devolver la pelota
Tendríamos algo así. 
play name=atencion alias=atencion time=250
play name=tiro_pelota time=500 alias=yotiro
action name=devuelves_pelota alias=devuelves time=750 fail=pelota_red

Ahora quieres hacer lo mismo pero en los tiempos 4, 5 y 6
Es así de simple
! atencion,yotiro,devuelves 1000 pelotita
Ahora tenemos atención a 1000, yotiro a 1250 y devuelves a 1500. Guay!
Esta macro se llama pelotita, así que si queremos que pase todo esto otra vez a 10000, haríamos esto:
@ pelotita 10000

Ahora sí que es fácil

## hacer el tutorial

El tutorial es muy fácil de hacer. Tiene que tener el mismo nombre que el lvl pero la extensión .tut
Usa más o menos los mismos comandos que el nivel principal pero con las siguientes restricciones

1. no hay macros
2. las acciones no se permiten, solo say (ver más abajo)
3. en el tutorial sí que hay que ordenar los comandos (ver más abajo)

el tutorial funciona reproduciendo sonidos y mostrando texto. Puede reproducir música que también se puede pausar con el comando pause
debes asegurarte de que la música dura lo suficiente para completar el tutorial, pero puedes usar los comandos restart o seek (sin debug) para volver al inicio, o parar, mostrar texto y volver a cargar la música (es lo que hacemos normalmente).
La diferencia principal es que aquí en el tutorial sí que tienes que ordenar tus comandos. Esto lo hace más limpio. Si no los ordenas, nunca se procesarán!

Pero soy muy vago... No quiero ordenarlos!

Bueno, en este caso tienes que hacerlo. El tutorial se lee directamente del archivo, no carga el nivel y lee cada comando cuando lo necesita. Además, si ordenas tus comandos puedes hacer cosas como saltar a cualquier parte del archivo, en cualquier momento, pausar, mostrar algo de texto y esperar, reproducir sonidos cuando no hay música, y otras cosas guays.
Así que confía en mí, ordenar los comandos es buena idea.

### comandos especiales para el tutorial

- text: text, un espacio y cualquier línea de texto verbalizará el texto y esperará a que el usuario pulse enter. si no  lo lee bien, envíame la línea y lo miraré, ya que puede ser que hayas puesto algún caracter no reconocido, algún acento extraño etc.
- play: reproduce un sonido como en el juego normal: reproduce un sonido como en el juego normal, obviamente sin requires. La sintaxis es: play nombredelarchivo tiempo, o play nombredelarchivo para reproducir sin esperar, útil cuando no hay música. 
- music nombredelarchivo [volumen] [posicion]: reproduce un archivo de música para el tutorial. volumen es opcional y por defecto es 0, el máximo. SI especificas posición, el volumen también tienes que especificarlo (0 es lo que se suele poner a no ser que la música esté muy alta). Ejemplo: music mi_musica 0 500. El volumen sería 0 y la posición 500ms.
- pause tiempo: pon pause y una posición en milisegundos para pausar la música y continuar con el tutorial.
- stop: para immediatamente la música y continúa con el tutorial
- fade: para la música bajando el volumen gradualmente
- exit: parar ejecución y salir completamente del juego
- restart: ir al principio de la música para nuevos comandos que deben escribirse después.
- seek: saltar a una posición dentro del archivo de música.
- stopsounds: para todos los sonidos, menos la música.
- jump: Salta a ese punto específico del tutorial. Puedes tener tantos jump como quieras, y se usa siempre el último. Solo hace efecto si estás creando un pack (es decir, cuando la gente lo juegue, los jump no hacen nada).
- wait: espera un número de milisegundos antes de hacer algo, muy útil para reproducir sonidos sin música o simplemente esperar antes de mostrar texto.
- playwait nombre: reproduce un sonido y espera a que termine; puede interrumpirse con escape, enter o espacio.
- say: decir algo con la tts. Si quieres esperar, usa los comandos play o wait (muy útil para indicar cuándo debes pulsar una tecla para la acción).

### tutorial de ejemplo

text hola, soy un tutorial
text este nivel es muy fácil. reproduciré un sonido con música y saldré.
text te voy a mostrar cómo funciona el play, wait y music.
text voy a reproducir un sonido y luego esperaré.
play sonido1
wait 500
text ves? he reproducido el sonido y he esperado antes de este texto.
text vamos a ver con música

music 1 -5
play atencion 500
say atención!
play disparo 1000
say enter!
play accion_disparo
wait 2000
stop
fade
text hasta luego!

@@ operación desde la línea de comandos

puedes ejecutar game.exe con un nivel (e.j., game.exe remix.lvl): Esto hará que el juego abra directamente ese nivel. Tiene que estar en la misma carpeta de packs como siempre. La música de introducción no se reproducirá, para ahorrar tiempo. No intentes abrir un nivel desde la línea de comandos para ver si se abre en el pack por defecto... que no funciona, tramposo!

## información adicional

El pack también puede contener otros archivos. Algunos de estos archivos recomendados son:

- logo: se reproduce cuando el juego comienza o se cambia el pack.

## Pero todavía no lo entiendo!

Todavía no entiendes cómo funciona? aquí tienes un ejemplo.
No puedes jugar a este ejemplo, solo es para documentarte y que entiendas cómo va. Esto es del nivel remix1:

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

Copyright Oriol Gómez & Guilevi Productions 2016