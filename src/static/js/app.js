var DOMICS = (function() {
  function get(url, success) {
    $.ajax(url, {
      method: "get",
      success: success
    });
  }

  function post(url, body) {
    $.ajax(url, {
      method: "post",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify(body)
    })
  }

  var rooms = {
    'unknown': {name: 'Unknown', devices: []}
  };

  function render() {
    var template = $('script#devices-template').text();
    template = Handlebars.compile(template);
    var rendered = template({rooms: rooms});
    $('div.main').html(rendered);
  }

  function fetch() {
    get('/api/room', function(result) {
      $.each(result.rooms, function(i, room) {
        rooms[room.id] = room;
        rooms[room.id].devices = [];
      });

      get('/api/device', function(result) {
        $.each(result.devices, function(i, device) {
          var room_id = device.room in rooms ? device.room : 'unknown';
          rooms[room_id].devices.push(device);
        });

        render();
      });
    });
  }

  $(function () {
    fetch();

    $('div.main').on('click', 'div.room .all-on', function() {
      var room_id = $(this).closest('div.room').data('room-id');

      post(sprintf('/api/room/%s/command', room_id), {
          command: "all_on",
        });
    });

    $('div.main').on('click', 'div.room .all-off', function() {
      var room_id = $(this).closest('div.room').data('room-id');

      post(sprintf('/api/room/%s/command', room_id), {
          command: "all_off",
        });
    });

    $('div.main').on('click', 'div.device .device-on', function() {
      var device_id = $(this).closest('div.device').data('device-id');

      post(sprintf('/api/device/%s/command', device_id), {
          command: "turn_on",
        });
    });

    $('div.main').on('click', 'div.device .device-off', function() {
      var device_id = $(this).closest('div.device').data('device-id');

      post(sprintf('/api/device/%s/command', device_id), {
          command: "turn_off",
        });
    });

    $("input#wemo_on").click(function() {
      send_json(sprintf("/api/device/wemo-221412K11013E1/command"),
        {
          command: "turn_on",
        });
    });

  });

  return {
    'rooms': rooms
  }
})();
