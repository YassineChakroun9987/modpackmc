// A green "server is ready" banner in the server window (start.bat) once startup has finished.
// The console turns § colour codes into real colours; the log files store the text without them.
ServerEvents.loaded(function (event) {
  var server = event.server
  var port = server.getPort()
  var lines = [
    '§a§l==============================================',
    '§a§l   GREEN LANTERNS SERVER IS READY',
    '§a   Join at §f127.0.0.1:' + port + '§a  (friends: your VPN address)',
    '§a   Type §fstop§a here to shut down safely.',
    '§a§l==============================================',
  ]
  lines.forEach(function (l) { console.info(l + '§r') })
})
