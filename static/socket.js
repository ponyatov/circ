
sio = io()

reload = {
    timeout: 111,
    handler: undefined,
    go:      function()        { location.reload() },
    start:   function(timeout) { reload.handler = setTimeout(reload.go,timeout) },
    stop:    function()        { clearTimeout(reload.handler) },
}

sio.on('connect',(msg)=>{
    console.log('sio','connect',msg)
    $('#localtime').addClass('online').removeClass('offline')
})

sio.on('disconnect',(msg)=>{
    console.log('sio','disconnect',msg)
    $('#localtime').addClass('offline').removeClass('online')
    reload.start(reload.timeout)
})

sio.on('reload',(msg)=>{
    console.log('sio','reload',msg)
    reload.go()
})

sio.on('localtime',(msg)=>{
    console.log('sio','localtime',msg)
    $('#localtime').text(msg.date+" | "+msg.time)
})

