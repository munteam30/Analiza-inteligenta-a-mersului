import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import bluetooth

kivy.require('1.11.1')

class BluetoothReceiverApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Receiving data...")
        self.layout.add_widget(self.label)

        # Deschide un fir de execuție separat pentru a primi datele în mod continuu
        Clock.schedule_interval(self.receive_data, 1)

        return self.layout

    def receive_data(self, dt):
        try:
            server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            server_sock.bind(("", bluetooth.PORT_ANY))
            server_sock.listen(1)

            port = server_sock.getsockname()[1]
            uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
            bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                                        service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                        profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                        # protocols=[bluetooth.OBEX_UUID]
                                        )

            print("Waiting for connection on RFCOMM channel", port)

            client_sock, client_info = server_sock.accept()
            print("Accepted connection from", client_info)

            client_socket, address = server_sock.accept()
            print("Conexiune acceptată de la", address)

            data = b""
            while True:
                received_data = client_socket.recv(1024)
                if not received_data:
                    break
                data += received_data

            client_socket.close()
            server_sock.close()

            # Actualizează eticheta cu datele primite
            self.label.text = data.decode("utf-8")

        except bluetooth.btcommon.BluetoothError as e:
            print("Eroare Bluetooth:", e)

if __name__ == '__main__':
    BluetoothReceiverApp().run()
