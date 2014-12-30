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

  function del(url) {
    $.ajax(url, {
      method: 'delete',
    })
  }

  Handlebars.registerHelper('IfEquals', function(a, b, options) {
    if (a === b) {
      return options.fn(this);
    } else {
      return options.inverse(this);
    }
  });

  var rooms = {
    'unknown': {name: 'Unknown', devices: []}
  };

  var devices = {};

  function render() {
    var template = $('script#devices-template').text();
    template = Handlebars.compile(template);
    var rendered = template({rooms: rooms});
    $('div.main').html(rendered);
  }

  function fetch() {
    get('/api/room', function(result) {
      $.each(result.objects, function(i, room) {
        rooms[room.id] = room;
        rooms[room.id].devices = [];
      });

      get('/api/device', function(result) {
        $.each(result.objects, function(i, device) {
          var room_id = device.room in rooms ? device.room : 'unknown';
          rooms[room_id].devices.push(device);
          devices[device.id] = device;
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

    // Dialogs

    $('div.modal#main_modal').modal({show: false});

    function dialog(name, obj, f) {
      var template = Handlebars.compile($(name).text());
      var rendered = template(obj);
      var modal = $('div.modal#main_modal');

      modal.html(rendered);
      modal.modal();
      modal.on('success', f);
      modal.modal('show');
    }

    $('.modal#main_modal').on('click', '.btn-primary', function() {
      $('.modal#main_modal')
        .trigger('success')
        .html('')
        .off('success')
        .modal('hide');
    });

    // Dialog: change room name

    $('div.main').on('click', 'div.room .room-change-name', function() {
      var room_id = $(this).closest('div.room').data('room-id');
      var room = rooms[room_id];

      dialog('script#room-change-name-dialog-template', room, function() {
        var room_name = $(this).find('input#room-name').val();
        post(sprintf('/api/room/%s', room_id), {
            name: room_name,
          });
      });
    });

    // Dialog: create new room

    function random_id() {
      return ("0000" + (Math.random() * Math.pow(36,4) << 0).toString(36)).slice(-4)
    }

    $('div.main').on('click', 'a.create-new-room', function() {
      dialog('script#create-new-room-dialog-template', {}, function() {
        var room_id = random_id();
        var room_name = $(this).find('input#room-name').val();

        post(sprintf('/api/room/%s', room_id), {
            name: room_name,
          });
      });
    });

    // Dialog: delete room

    $('div.main').on('click', 'div.room .room-delete', function() {
      var room_id = $(this).closest('div.room').data('room-id');
      var room = rooms[room_id];

      dialog('script#delete-room-dialog-template', room, function() {
        del(sprintf('/api/room/%s', room_id));
      });
    });

    // Dialog: device change room

    $('div.main').on('click', 'div.device .device-change-room', function() {
      var device_id = $(this).closest('div.device').data('device-id');
      var state = {rooms: rooms, device: devices[device_id]};

      dialog('script#device-change-room-dialog-template', state, function() {
        var room_id = $(this).find('select#room').val();
        post(sprintf('/api/device/%s/command', device_id), {
            command: 'set_room',
            room_id: room_id
          });
      });
    });

  });

  return {
    'rooms': rooms
  }
})();
