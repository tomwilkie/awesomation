var DOMICS = (function() {

  var net = (function() {
    return {
      get: function(url, success) {
        return $.ajax(url, {
          method: "get",
          success: success
        });
      },
      post: function(url, body) {
        return $.ajax(url, {
          method: "post",
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify(body)
        });
      },
      del: function(url) {
        return $.ajax(url, {
          method: 'delete',
        });
      }
    };
  }());

  var cache = (function() {
    var rooms = {};
    var devices = {};
    var accounts = {};
    var types = {
      account: accounts,
      device: devices,
      room: rooms,
    };

    function fetch() {
      net.get('/api/account', function(result) {
        $.each(result.objects, function(i, account) {
          accounts[account.id] = account;
        });

        $('body').trigger('cache_updated');
      });

      net.get('/api/room', function(result) {
        $.each(result.objects, function(i, room) {
          rooms[room.id] = room;
        });

        $('body').trigger('cache_updated');
      });

      net.get('/api/device', function(result) {
        $.each(result.objects, function(i, device) {
          devices[device.id] = device;
        });

        $('body').trigger('cache_updated');
      });
    }

    function connect_channel() {
      net.get('/api/user/new_channel', function (data) {
        channel = new goog.appengine.Channel(data.token);
        socket = channel.open();
        socket.onmessage = function (m) {
          var message = JSON.parse(m.data);
          console.log(message);
          $.each(message.events, function(i, event) {
            switch (event.event) {
            case 'delete':
              delete types[event.cls][event.id];
              break;
            case 'update':
              types[event.cls][event.id] = event.obj;
              break;
            }
          });
          $('body').trigger('cache_updated');
        };
      });
    }

    $(function () {
      window.setTimeout(function() {
        connect_channel();
        fetch();
      }, 0);
    });

    return {
      rooms: rooms,
      devices: devices,
      accounts: accounts,
    };
  }());

  Handlebars.registerHelper({
    'IfEquals': function(a, b, options) {
      if (a === b) {
        return options.fn(this);
      } else {
        return options.inverse(this);
      }
    },

    'HasCapability': function(capability, options) {
      if (this.capabilities.indexOf(capability) >= 0) {
        return options.fn(this);
      } else {
        return options.inverse(this);
      }
    },

    'HomelessDevices': function(options) {
      var found = false;
      var ret = '';

      $.each(cache.devices, function(id, device) {
        if (!(device.room in cache.rooms)) {
          found = true;
          ret = ret + options.fn(device);
        }
      });

      if (!found) {
        ret = ret + options.inverse(this);
      }

      return ret;
    },

    'DevicesForRoom': function(room_id, options) {
      var found = false;
      var ret = '';

      $.each(cache.devices, function(id, device) {
        if (device.room === room_id) {
          found = true;
          ret = ret + options.fn(device);
        }
      });

      if (!found) {
        ret = ret + options.inverse(this);
      }

      return ret;
    }
  });

  $(function () {
    $('script.handlebars-partial').each(function() {
      var that = $(this);
      Handlebars.registerPartial(this.id, that.html());
    });

    function render() {
      var mode = $.bbq.getState('mode') || 'devices';
      var template = $(sprintf('script#%s-template', mode)).text();
      template = Handlebars.compile(template);
      var rendered = template({rooms: cache.rooms, devices: cache.devices});
      $('div.main').html(rendered);
    }

    $('body').on('cache_updated', render);
    $(window).bind('hashchange', render);

    $('.nav-sidebar li').on('click', function() {
      var mode = $(this).data('mode');
      $('.nav-sidebar li').removeClass('active');
      $(this).addClass('active');
      $.bbq.pushState({mode: mode});
    });

    $('a[href=#]').click(function(event) {
      event.preventDefault();
    });

    $('div.main').on('click', 'div.room .all-on', function() {
      var room_id = $(this).closest('div.room').data('room-id');

      net.post(sprintf('/api/room/%s/command', room_id), {
          command: "all_on",
        });
    });

    $('div.main').on('click', 'div.room .all-off', function() {
      var room_id = $(this).closest('div.room').data('room-id');

      net.post(sprintf('/api/room/%s/command', room_id), {
          command: "all_off",
        });
    });

    $('div.main').on('click', 'div.device .device-command', function() {
      var device_id = $(this).closest('div.device').data('device-id');
      var command = $(this).data('command');

      net.post(sprintf('/api/device/%s/command', device_id), {
          command: command,
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

    $('.modal#main_modal').on('click', '.btn-primary', function(event) {
      $('.modal#main_modal')
        .trigger('success', [event.target])
        .html('')
        .off('success')
        .modal('hide');
    });

    // Dialog: create new room

    function random_id() {
      return ("0000" + (Math.random() * Math.pow(36,4) << 0).toString(36)).slice(-4);
    }

    $('div.main').on('click', 'a.create-new-room', function() {
      dialog('script#create-new-room-dialog-template', {}, function() {
        var room_id = random_id();
        var room_name = $(this).find('input#room-name').val();

        net.post(sprintf('/api/room/%s', room_id), {
            name: room_name,
          });
      });
    });

    // Dialog: add new device

    $('div.main').on('click', 'a.add-new-device', function() {
      dialog('script#new-device-dialog-template', {rooms: cache.rooms}, function(event, target) {
        var that = $(this);
        var type = $(target).data('type');
        switch(type) {

        case 'rfswitch':
          var device_id = random_id();
          var device_name = that.find('input#device-name').val();
          var system_code = that.find('input#system-code').val();
          var device_code = parseInt(that.find('input#device-code').val());
          var room_id = that.find('input#room').val();

          net.post(sprintf('/api/device/%s', device_id), {
            type: 'rfswitch',
            name: device_name,
            system_code: system_code,
            device_code: device_code
          });
          break;

        case 'proxy':
          var proxy_id = that.find('input#proxy-id').val();
          net.get(sprintf('/api/proxy/claim/%s', proxy_id));
          break;
        }
      });
    });

    // Dialog: change room name

    $('div.main').on('click', 'div.room .room-change-name', function() {
      var room_id = $(this).closest('div.room').data('room-id');
      var room = cache.rooms[room_id];

      dialog('script#room-change-name-dialog-template', room, function() {
        var room_name = $(this).find('input#room-name').val();
        net.post(sprintf('/api/room/%s', room_id), {
            name: room_name,
          });
      });
    });

    // Dialog: delete room

    $('div.main').on('click', 'div.room .room-delete', function() {
      var room_id = $(this).closest('div.room').data('room-id');
      var room = cache.rooms[room_id];

      dialog('script#delete-room-dialog-template', room, function() {
        net.del(sprintf('/api/room/%s', room_id));
      });
    });

    // Dialog: device change room

    $('div.main').on('click', 'div.device .device-change-room', function() {
      var device_id = $(this).closest('div.device').data('device-id');
      var state = {rooms: cache.rooms, device: cache.devices[device_id]};

      dialog('script#device-change-room-dialog-template', state, function() {
        var room_id = $(this).find('select#room').val();
        net.post(sprintf('/api/device/%s/command', device_id), {
            command: 'set_room',
            room_id: room_id
          });
      });
    });

    // Dialog: change device name

    $('div.main').on('click', 'div.device .device-change-name', function() {
      var device_id = $(this).closest('div.device').data('device-id');
      var device = cache.devices[device_id];

      dialog('script#device-change-name-dialog-template', device, function() {
        var device_name = $(this).find('input#device-name').val();
        net.post(sprintf('/api/device/%s', device_id), {
            name: device_name,
          });
      });
    });

    // Dialog: delete device

    $('div.main').on('click', 'div.device .device-delete', function() {
      var device_id = $(this).closest('div.device').data('device-id');
      var device = cache.devices[device_id];

      dialog('script#delete-device-dialog-template', device, function() {
        net.del(sprintf('/api/device/%s', device_id));
      });
    });

  });

  return {
    net: net,
    cache: cache
  };
})();
