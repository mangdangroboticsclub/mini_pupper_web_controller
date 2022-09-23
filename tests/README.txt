git clone github.com/mangdangroboticsclub/QuadrupedRobot
modify QuadrupedRobot/UDPComms/UDPComms.py:
         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
-        self.des_address = ("192.168.1.34",port_tx)
-        self.sock.bind(("192.168.1.39", port))
+        self.des_address = ("127.0.0.1",port_tx)
+        self.sock.bind(("127.0.0.1", port))
         self.sock.settimeout(0.2)
192.168.1.34 is my mini pupper and 192.168.1.39 is my PC

pip install QuadrupedRobot/UDPComms/

Now you can run test_all.sh or individual tests
