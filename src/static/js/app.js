var DOMICS = (function() {
  return {}
})()

$(function() {
  function send_json(url, body) {
    $.ajax(url, {
      method: "post",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify(body)
    })
  }

  function get(url, done) {
    $.ajax(url, {
      method: "get",
      done: done
    })
  }

  var devices = {};
  get('/api/device', function(result) {
    $.each(result.devices, function(i, device) {
      devices[device.id] = device;
    });
  });

  $("input#new_device").click(function() {
    var device_id = "office_lamp_1";
    send_json(sprintf("/api/device/%s", device_id),
      {
        type: "rfswitch",
        system_code: "01010",
        device_code: 1
      });
  });

  $("input#lamp_on").click(function() {
    var device_id = "office_lamp_1";

    $.ajax(sprintf("/api/device/%s/command", device_id), {
      method: "post",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({
        command: 'turn_on',
      })
    })
  });

  $("input#lamp_off").click(function() {
    var device_id = "office_lamp_1";

    $.ajax(sprintf("/api/device/%s/command", device_id), {
      method: "post",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({
        command: 'turn_off',
      })
    })
  });

  $("input#hue_scan").click(function() {
    $.ajax(sprintf("/api/driver/hue_bridge/command"), {
      method: "post",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({
        command: 'scan',
      })
    })
  });

  $("input#hue_on").click(function() {
    $.ajax(sprintf("/api/device/hue-001788fffe1502d9-1/command"), {
      method: "post",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({
        command: 'turn_on',
      })
    })
  });

  $("input#hue_off").click(function() {
    $.ajax(sprintf("/api/device/hue-001788fffe1502d9-1/command"), {
      method: "post",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({
        command: 'turn_off',
      })
    })
  });

  $("input#new_room1").click(function() {
    send_json(sprintf("/api/room/office"),
      {
        name: "Office",
      });
  });

  $("input#new_room2").click(function() {
    send_json(sprintf("/api/room/cinema"),
      {
        name: "Home Cinema",
      });
  });


  $("input#new_room2").click(function() {
    send_json(sprintf("/api/room/cinema"),
      {
        name: "Home Cinema",
      });
  });

  $("input#zwave_heal").click(function() {
    send_json(sprintf("/api/driver/zwave/command"),
      {
        command: "heal"
      });
  });

  $("input#zwave_lights_on").click(function() {
    send_json(sprintf("/api/device/zwave-3/command"),
      {
        command: "lights",
        state: true
      });
  });

  $("input#zwave_lights_off").click(function() {
    send_json(sprintf("/api/device/zwave-3/command"),
      {
        command: "lights",
        state: false
      });
  });

  $("input#wemo_on").click(function() {
    send_json(sprintf("/api/device/wemo-221412K11013E1/command"),
      {
        command: "turn_on",
      });
  });

  $("input#wemo_off").click(function() {
    send_json(sprintf("/api/device/wemo-221412K11013E1/command"),
      {
        command: "turn_off",
      });
  });
});
