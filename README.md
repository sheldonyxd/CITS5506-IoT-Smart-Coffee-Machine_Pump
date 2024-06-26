# Smart Coffee Machine Pump controlled by Raspberry Pi & Ultrasonic HC-SR04 sensor.

Automatic water pump system for coffee machine using the HC-SR04 sensor, Raspberry Pi and Flask.


## How to use

1. Install dependencies:

   ```sh
   sudo pip3 install hcsr04sensor
   ```

2. Run the [main.py](main.py):

   ```sh
   sudo python3 coffee-pump/main.py
   ```

   or use make:

   ```sh
   make run
   ```

3. Install as a Service:

   ```bash
   chmod +x service_install.sh
   make install
   ```

4. Use as a Service:

   ```bash
   make start|stop|status
   ```

5. Show service output:

   ```bash
   make log
   ```

