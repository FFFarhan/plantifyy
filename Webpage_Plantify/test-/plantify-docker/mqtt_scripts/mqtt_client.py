import paho.mqtt.client as mqtt
import mariadb
import time
import os

class MqttClient:
    def __init__(self, broker, client_id, topic, qos, save_to_db_callback=None):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id, clean_session=False)
        self.topic = topic
        self.qos = qos
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.connect(broker, 1883)

        self.to_db = self.write_to_db_wrapper(save_to_db_callback or self.save_to_db)

    def on_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code.is_failure:
            print(f"Verbindung zum Broker fehlgeschlagen: {reason_code}")
        else:
            print("Verbunden – Subscribing...")
            client.subscribe(self.topic, self.qos)
            print("Subscribed!")

    def on_disconnect(self, client, userdata, reason_code, properties=None, reason_string=None):
        print(f"Verbindung verloren - Grund: {reason_code}")
        while True:
            try:
                print("Versuche erneut zu verbinden...")
                client.reconnect()
                break
            except Exception as e:
                print(f"Reconnect fehlgeschlagen: {e}")
                time.sleep(5)

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        topic = msg.topic
        print(f"Nachricht empfangen: {topic} -> {message}")
        try:
            self.to_db(topic, message)
        except Exception as e:
            print(e)

    def write_to_db_wrapper(self, process_function):

        def db_con_wrapper(topic, message):
            conn = None
            cursor = None
            try:
                conn = mariadb.connect(
                    host="192.168.178.53",#os.getenv('DB_HOST'),
                    port=3306,
                    database="smartplantpot",#os.getenv('DB_NAME'),
                    user="admin",#os.getenv('DB_SENSOR_WRITER'),
                    password="thws2025"#os.getenv('DB_SENSOR_PW')
                )
                cursor = conn.cursor()
                process_function(topic, message, cursor)
                conn.commit()
                print(f"Nachricht gespeichert für Topic: {topic}")

            except mariadb.Error as e:
                print(f"Fehler beim Speichern in DB für Topic '{topic}': {e}")

            except Exception as e:
                print(f"Allgemeiner Fehler bei Verarbeitung: {e}")

            finally:
                try:
                    if cursor is not None:
                        cursor.close()
                    if conn is not None:
                        conn.close()
                except Exception as e:
                    print(f"Fehler beim Schließen der DB-Verbindung: {e}")

        return db_con_wrapper

    def save_to_db(self, topic, message, cursor):
        try:
            values = message.split(';')
            pot_mac = values[0]
            pot_name = values[1]

            sql = f"INSERT IGNORE INTO {self.topic} (pot_mac, pot_name) VALUES (?,?)"
            cursor.execute(sql, (pot_mac, pot_name))
        except Exception as e:
            print(e)

    def start(self):
        self.client.loop_forever()