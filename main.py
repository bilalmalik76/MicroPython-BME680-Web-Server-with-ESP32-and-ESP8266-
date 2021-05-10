def web_page():
  bme = BME680_I2C(i2c=i2c)
  temp = str(round(bme.temperature, 2)) + ' C'
  hum = str(round(bme.humidity, 2)) + ' %'
  pres = str(round(bme.pressure, 2)) + ' hPa'  
  gas = str(round(bme.gas/1000, 2)) + ' KOhms'
  html = """<html>
<head>
  <title>MicroPython BME680 Web Server</title>
  <meta http-equiv="refresh" content="10">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
  <link rel="icon" href="data:,">
  <style>
    html {font-family: Arial; display: inline-block; text-align: center;}
    p {  font-size: 1.2rem;}
    body {  margin: 0;}
    .topnav { overflow: hidden; background-color: #5c055c; color: white; font-size: 1.7rem; }
    .content { padding: 20px; }
    .card { background-color: white; box-shadow: 2px 2px 12px 1px rgba(140,140,140,.5); }
    .cards { max-width: 700px; margin: 0 auto; display: grid; grid-gap: 2rem; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
    .reading { font-size: 2.8rem; }
    .card.temperature { color: #0e7c7b; }
    .card.humidity { color: #17bebb; }
    .card.pressure { color: hsl(113, 61%, 29%); }
    .card.gas { color: #5c055c; }
  </style>
</head>
<body>
  <div class="topnav">
    <h3>MicroPython BME680 WEB SERVER</h3>
  </div>
  <div class="content">
    <div class="cards">
      <div class="card temperature">
        <h4><i class="fas fa-thermometer-half"></i>Temp. Celsius</h4><p><span class="reading">""" + temp+ """</p>
      </div>
      <div class="card humidity">
        <h4><i class="fas fa-tint"></i> Humidity</h4><p><span class="reading">""" + hum + """</p>
      </div>
      <div class="card pressure">
        <h4><i class="fas fa-angle-double-down"></i> PRESSURE</h4><p><span class="reading">""" + pres +"""</p>
      </div>
      <div class="card gas">
        <h4><i class="fas fa-wind"></i> Gas</h4><p><span class="reading">""" + gas + """</p>
      </div>
    </div>
  </div>
</body>

</html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')
    
   

  

