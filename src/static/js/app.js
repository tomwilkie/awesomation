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

    // Dialog: change room name

    $('div.main').on('click', 'div.room .room-change-name', function() {
      var room_id = $(this).closest('div.room').data('room-id');
      var room = rooms[room_id];

      $('.modal#room_change_name input#room-name').val(room.name);
      $('.modal#room_change_name')
          .data('for-room', room_id)
          .modal({show: true});
    });

    $('.modal#room_change_name button.btn-primary').on('click', function() {
      var room_id = $('.modal#room_change_name').data('for-room');
      var room_name = $('.modal#room_change_name input#room-name').val();

      post(sprintf('/api/room/%s', room_id), {
          name: room_name,
        });

      $('.modal#room_change_name').modal('hide');
    });

    // Dialog: create new room

    function random_id() {
      return ("0000" + (Math.random() * Math.pow(36,4) << 0).toString(36)).slice(-4)
    }

    $('div.main').on('click', 'a.create-new-room', function() {
      $('.modal#create-new-room-dialog').modal({show: true});
    });

    $('.modal#create-new-room-dialog button.btn-primary').on('click', function() {
      var room_id = random_id();
      var room_name = $('.modal#create-new-room-dialog input#room-name').val();

      post(sprintf('/api/room/%s', room_id), {
          name: room_name,
        });

      $('.modal#create-new-room-dialog').modal('hide');
    });
  });

  return {
    'rooms': rooms
  }
})();
