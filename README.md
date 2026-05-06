# redes-p3-2.0
Práctica: Sistema Domótico IoT con MQTT Redes de Comunicaciones 2
PRÁCTICA
Sistema Domótico IoT con MQTT
Redes de Comunicaciones 2
1. Introducción
En esta práctica se va a implementar un sistema domótico para el hogar con dispositivos IoT.
Un sistema de domótica de hogar permite conectar distintos tipos de dispositivos como
interruptores, sensores o motores para realizar acciones cotidianas como encender una luz,
medir una temperatura o subir una persiana. Estos sensores y actuadores se usan en conjunto
con reglas que permiten hacer cosas como: "encender la luz de la puerta al anochecer", "cerrar
las persianas al pulsar un botón", "encender la caldera si la temperatura baja de 21 grados",
etc.
Existen múltiples protocolos para comunicación IoT abiertos e incluso algunos fabricantes
implementan el suyo propietario, pero en este caso nos centraremos en MQTT, de los más
usados.
Se proponen dos opciones para que el usuario interactúe con el sistema:
• Opción A — Django: Proyecto de Django que permita gestionar dispositivos, reglas y
eventos generados.
• Opción B — Discord: Desarrollar un bot de Discord que permita, a través de mensajes
publicados en una sala y leyendo acciones sobre el bot, actuar sobre los dispositivos,
reglas y eventos del sistema.
Componentes del sistema
El sistema consta de varios componentes:
• Dispositivos IoT: Sensores, Interruptores y Relojes
Página 1 de 9
Práctica: Sistema Domótico IoT con MQTT Redes de Comunicaciones 2
• Broker MQTT Mosquitto
• Controlador (Controller): Gestión del sistema general — lee mensajes del broker, llama
al Rule Engine y realiza acciones sobre los dispositivos a través del broker.
• Persistencia: Almacena la información de los dispositivos registrados y las reglas.
• Rule Engine: Entidad que, ante un evento, comprueba las reglas y lanza acciones.
• Bridge (solo Opción B): Aplicación puente que comunica la aplicación web con Discord.
• Aplicación de gestión (solo Opción A): Aplicación web basada en Django para gestionar
los dispositivos y su estado.
• Discord (solo Opción B): Plataforma que soporta la creación de salas de chat de texto,
vídeo y audio.
Actores
Dispositivo IoT (device): Publica sus cambios de estado y puede recibir acciones a realizar
usando MQTT.
Controlador (controller): Recibe y envía mensajes a los dispositivos IoT usando MQTT.
Permite gestionar los dispositivos.
Traductor (bridge): Recibe eventos y los traduce a acciones para el bot. Recibe acciones del
bot y las traduce a acciones sobre los dispositivos.
Bot: Publica mensajes en Discord y recibe acciones.
Dispositivos IoT
Se soportan tres tipos: interruptores, sensores y relojes. Para cada funcionalidad que soporta
un dispositivo se define un topic y las cadenas de los distintos estados. Ejemplo para un
interruptor:
topic: home/climate/boiler_switch
state_on: ON | state_off: OFF
command_topic: home/climate/boiler_switch/set
payload_on: ON | payload_off: OFF
Si se quiere consultar el estado del interruptor se publicará un mensaje en topic y el dispositivo
responderá con uno de los estados. Si se quiere cambiar el estado se publicará un mensaje en
el command_topic con el payload correspondiente y el dispositivo responderá con el estado al
que ha cambiado.
Para los sensores, el dispositivo puede publicar cada cierto tiempo (o con cada cambio) el
cambio de estado en su topic. Es posible también preguntar por su estado.
2. Objetivos de aprendizaje
Página 2 de 9
Práctica: Sistema Domótico IoT con MQTT Redes de Comunicaciones 2
1. Conocer uno de los principales protocolos de comunicación IoT: MQTT
2. Aprender a gestionar un sistema con varios componentes definidos y la interacción entre
ellos, sobre todo si algunos de ellos no los hemos desarrollado nosotros
3. Afianzar los conocimientos adquiridos en la asignatura sobre comunicación asíncrona,
aplicaciones distribuidas y lenguaje Python
4. Continuar aprendiendo a probar mientras se desarrolla
5. Usar uno de los frameworks web más populares: Django
6. Crear un bot en una plataforma con un API abierto
6.1. Familiarizarse con OAuth2
3. Funcionalidad
Las funcionalidades principales del sistema son:
• (1) Gestión de dispositivos IoT: se tiene que poder añadir un dispositivo con su
identificador, tipo, editar y borrar. Para añadir un dispositivo, dependiendo de la opción
escogida, se podrá hacer externamente creando el fichero y notificando al sistema que
se ha añadido un nuevo dispositivo.
• (2) Gestión de reglas básicas: dado-cuando-entonces. Para los disparadores se
soportarán los operadores ==, > y <. Bastará con definir un formato textual que el
sistema tratará, p.ej. "si sala mayor que 25 enciende caldera". Configuración del
sistema: conexión MQTT, topics por defecto, persistencia, contraseñas para API.
• (3) Registro de un dispositivo: mediante su id, si está registrado se procesan sus
mensajes y se pueden realizar acciones sobre él. En caso contrario se rechazan.
• (4) Un dispositivo puede comunicar un cambio de estado o recibir una acción si lo
soporta.
El sistema también deberá:
• Conectar con el broker MQTT
• Generar eventos internos
• Comprobar reglas para ver si un evento encaja y se desencadena una acción
• Realizar acciones sobre dispositivos — cambiar el estado de un interruptor
Opción A — Django
1. Consultar, añadir, editar y borrar dispositivos
2. Consultar, añadir, editar y borrar reglas
3. Consultar eventos internos del sistema
Opción B — Discord
• Gestionar credenciales de API Discord
Página 3 de 9
Práctica: Sistema Domótico IoT con MQTT Redes de Comunicaciones 2
• Publicar cambios de estado en una sala a través del bot
• Consultar, añadir, editar y borrar reglas
• Recibir acciones sobre un dispositivo a través del bot
• Enviar eventos como mensajes a una sala
Limitaciones
• Un dispositivo en sí no tiene persistencia; al arrancar elige un estado y lo comunica.
• Los eventos que se comprueban contra las reglas son efímeros; si el rule engine cae y
se recupera, no procesa eventos antiguos.
Requisitos
Traducir a requisitos la funcionalidad a implementar.
TODO: Completar por el alumno
Casos de uso
TODO: Completar por el alumno
Decisiones de diseño
El alumno deberá razonar y responder a las siguientes preguntas:
• ¿Controller y Rule Engine han de ser aplicaciones separadas? ¿Por qué? ¿Qué
ventajas tiene una y otra opción?
• ¿Cómo se comunican Controller y Rule Engine en la opción escogida?
• ¿Tiene sentido que alguno de estos componentes compartan funcionalidad? ¿Qué
relación hay entre ellos?
• ¿Cuántas instancias hay de cada componente?
• ¿Controller y Bridge han de ser aplicaciones separadas? ¿Por qué? ¿Qué ventajas tiene
una y otra opción?
• ¿Cómo se comunican Controller y Bridge en la opción escogida?
TODO: Completar por el alumno
4. Entregables
Documentación
Completar las partes que faltan en este documento, incluyendo:
• Decisiones de diseño razonadas
Página 4 de 9
Práctica: Sistema Domótico IoT con MQTT Redes de Comunicaciones 2
• Especificación de comunicación con cada tipo de sensor
• Esquema de datos usado en la persistencia
• Clases principales y relación entre ellas — herencia (puede ser en formato esquema o
texto)
• Limitaciones de la solución escogida: "Nuestro sistema no es capaz de hacer esto por
esta razón"
Código
dummy-switch.py
Ejecutable que instancia un interruptor. Argumentos:
• --host: Host para conectar al broker (por defecto: redes2.ii.uam.es)
• -p, --port: Puerto (por defecto: 1883)
• -P, --probability: Probabilidad de fallo al recibir una acción (por defecto: 0.3)
• id: Identificador del dispositivo (posicional)
Ejemplo:
dummy-switch.py --host redes2.ii.uam.es --port 1883 --probability
0.4 1
dummy-sensor.py
Aplicación que instancia un sensor y envía cambios de estado cada cierto tiempo entre dos
valores máximo y mínimo. Argumentos:
• -i, --interval: Tiempo en segundos entre envíos (por defecto: 1)
• -m, --min: Valor mínimo a enviar (por defecto: 20)
• -M, --max: Valor máximo a enviar (por defecto: 30)
• --increment: Incremento entre min y max (por defecto: 1)
Ejemplo:
dummy-sensor.py --host redes2.ii.uam.es --port 1883 --min 20 --max
30 --increment 1 --interval 1 2
dummy-clock.py
• --time: Hora de inicio en formato HH:MM:SS (si no se indica, se usa la hora actual del
sistema)
• --increment: Incremento entre envíos en segundos (por defecto: 1)
• --rate: Frecuencia de envío en segundos (por defecto: 1)
Página 5 de 9
Práctica: Sistema Domótico IoT con MQTT Redes de Comunicaciones 2
controller.py
Aplicación que conecta con el broker, recibe mensajes de los dispositivos y les envía mensajes
a través del broker. Instancia un rule engine. Argumentos:
• --host: Host del broker (por defecto: redes2.ii.uam.es)
• -p, --port: Puerto (por defecto: 1883)
• --database: Nombre del fichero de base de datos SQLite
rule-engine.py
(En el caso de optar por aplicación separada de controller.py.) Recibe opciones similares a
éste.
bridge.py
(Solo opción Discord y aplicación separada de controller.py.) Recibe opciones similares a éste.
En caso de usar un proyecto Django, estos ejecutables pueden integrarse en el proyecto en un
directorio auxiliar tipo tools.
Pruebas
Se han de entregar, al menos, los siguientes tests unitarios:
test_device.py
• Conecta correctamente con el broker
• Si no conecta con el broker da error
• Probar que el sistema lee bien los parámetros por línea de comandos
• (switch) Cambia de estado ante una acción
• (sensor) Cambia de estado en intervalos entre min y max
test_controller.py
• Conecta correctamente con el broker
• Si no conecta con el broker da error
• Ante un mensaje de sensor, desencadena el mecanismo para comprobar reglas
• Ante una respuesta de RuleEngine para realizar una acción, realiza la acción sobre el
dispositivo
• Se lee correctamente la información de los dispositivos de la persistencia
Configuración
Todo lo necesario para poder ejecutar el sistema — p.ej. si se opta por Discord: tokens, URLs,
etc. Si se usa SQLite, se puede entregar el fichero con el esquema ya cargado pero sin ninguna
entrada, dispositivo registrado, regla, etc.
Página 6 de 9
Práctica: Sistema Domótico IoT con MQTT Redes de Comunicaciones 2
simulator.sh
Script que lance a todos los actores y simule cambios de estado para comprobar que todo
funciona. Es el equivalente a un tester de pruebas de integración.
Dudas frecuentes
¿Qué persistencia se recomienda usar?
Si se usa Django, lo más sencillo es usar SQLite, que lo soporta de serie. Aunque se opte por la
opción Discord, se podría usar sólo la capa de persistencia de Django con SQLite. Otra opción
es usar directamente ficheros para almacenar la información en un formato a definir por el
alumno: json, yaml, etc.
¿Tiene que haber algún prefijo en los topics a usar?
Sí. Al usar un broker compartido cada dispositivo tendrá un topic con la forma:
redes2/GRUPO/PAREJA/ID
• redes2/ → Es fijo
• GRUPO → 4 dígitos del grupo al que pertenece el alumno, p.ej. 2303
• PAREJA → 2 dígitos de la pareja, p.ej. 01
• ID → Identificador del dispositivo
Recomendaciones de desarrollo
4. Entender bien el alcance del proyecto y escribirlo: requisitos y casos de uso
5. Resolver dudas de diseño
6. Documentar el diseño
7. Pensar en qué se ha de probar para que cumplan con los casos de uso: si el sistema
tiene que hacer A, ¿cómo me aseguro de que es así de manera reproducible?
8. Reutilizar lo más posible código común encapsulado en clases: conexión con el broker,
recepción y envío de mensajes, persistencia
9. Empezar probando desde lo más pequeño e ir ampliando
10. Ante un comportamiento no esperado, volver atrás en las pruebas hasta descubrir qué
cambio ha provocado el error
Página 7 de 9
Práctica: Sistema Domótico IoT con MQTT Redes de Comunicaciones 2
Implementación
TODO: Completar por el alumno
Conclusiones
TODO: Completar por el alumno
5. Referencias
Discord
◦ Página principal
◦ Portal del desarrollador
◦ Crear un bot de Discord
◦ discord.py — librería para interactuar con Discord en Python
MQTT
◦ Página principal de MQTT
◦ Cómo funciona MQTT
◦ Mosquitto
◦ Instancia de test Mosquitto de Eclipse: test.mosquitto.org
◦ Paho, librería Python para MQTT
Django
◦ Django
◦ Tutorial de Django
Unit test Python
◦ Página principal
Mock
◦ Página principal
Página 8 de 9
Práctica: Sistema Domótico IoT con MQTT Redes de Comunicaciones 2
Persistencia
◦ SQLite
◦ SQLAlchemy
Página 9 de 9