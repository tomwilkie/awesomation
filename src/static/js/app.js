var AWESOMATION = (function() {

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
    var types = ['room', 'device', 'account'];
    var objects = {};
    var cache = {
      loading: true,
      objects: objects
    };

    function fetch() {
      var loaded = types.length;

      $.each(types, function(i, type) {
        net.get(sprintf('/api/%s', type), function(result) {
          objects[type] = {};
          $.each(result.objects, function(i, object) {
            objects[type][object.id] = object;
          });

          loaded--;
          if (loaded === 0) {
            cache.loading = false;
            $('body').trigger('cache_updated');
          }
        });
      });
    }

    function connect_channel() {
      net.get('/api/user/new_channel', function (data) {
        channel = new goog.appengine.Channel(data.token);
        socket = channel.open();
        socket.onmessage = function (m) {
          var message = JSON.parse(m.data);
          $.each(message.events, function(i, event) {
            switch (event.event) {
            case 'delete':
              delete objects[event.cls][event.id];
              break;
            case 'update':
              objects[event.cls][event.id] = event.obj;
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

    return cache;
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

      $.each(cache.objects.device, function(id, device) {
        if (!(device.room in cache.objects.room)) {
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

      $.each(cache.objects.device, function(id, device) {
        if (device.room === room_id) {
          found = true;
          ret = ret + options.fn(device);
        }
      });

      if (!found) {
        ret = ret + options.inverse(this);
      }

      return ret;
    },

    'HumanTime': function(millis) {
      return moment(millis).format('LLL');
    },

    'DevicesForAccount': function(account_id, options) {
      var found = false;
      var ret = '';

      $.each(cache.objects.device, function(id, device) {
        if (device.account === account_id) {
          found = true;
          ret = ret + options.fn(device);
        }
      });

      if (!found) {
        ret = ret + options.inverse(this);
      }

      return ret;
    },
  });

  $(function () {
    $('script.handlebars-partial').each(function() {
      var that = $(this);
      Handlebars.registerPartial(this.id, that.html());
    });

    function render() {
      var mode = $.bbq.getState('mode') || 'devices';

      // Update the selected status on the left.
      $('.nav-sidebar li').removeClass('active');
      $(sprintf('.nav-sidebar li[data-mode=%s]', mode)).addClass('active');

      // Rendem the main view.
      var template = $(sprintf('script#%s-template', mode)).text();
      template = Handlebars.compile(template);
      var rendered = template(cache);
      $('div.main').html(rendered);
    }

    $('body').on('cache_updated', render);
    $(window).bind('hashchange', render);
    render();

    $('.nav-sidebar li').on('click', function() {
      var mode = $(this).data('mode');
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
    $('div.modal#main_modal').on('shown.bs.modal', function () {
      $(this).find('input').first().focus();
    });

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
      $('.modal#main_modal').trigger('success', [event.target]);
    });

    function hide_modal() {
      $('.modal#main_modal')
        .html('')
        .off('success')
        .modal('hide');
    }

    function render_error(jqXHR, textStatus, errorThrown) {
      var message;
      try {
        var error = $.parseJSON(jqXHR.responseText);
        message = error.message;
      } catch (e) {
        message = errorThrown;
      }

      var template = $('script#error-template').text();
      template = Handlebars.compile(template);
      return template({message: message});
    }

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
        }).always(hide_modal);
      });
    });

    // Dialog: add new device

    $('div.main').on('click', 'a.add-new-device', function() {
      dialog('script#new-device-dialog-template', {rooms: cache.objects.room}, function(event, target) {
        var that = $(this);
        var type = $(target).data('type');
        switch(type) {

        case 'rfswitch':
          (function() {
            var device_id = random_id();
            var device_name = that.find('input#device-name').val();
            var system_code = that.find('input#system-code').val();
            var device_code = parseInt(that.find('input#device-code').val());
            var room_id = that.find('input#room').val();

            net.post(sprintf('/api/device/%s', device_id), {
              type: 'rfswitch',
              name: device_name,
              system_code: system_code,
              device_code: device_code,
              room: room_id
            }).done(function () {
              hide_modal();
            }).fail(function (jqXHR, textStatus, errorThrown) {
              that.find('input#proxy-id')
                .closest('div.form-group')
                .siblings('.error_placeholder')
                  .html(render_error(jqXHR, textStatus, errorThrown));
            });
          }());
          break;

        case 'proxy':
          (function() {
            var proxy_id = that.find('input#proxy-id').val();
            net.post('/api/proxy/claim', {
              proxy_id: proxy_id
            }).done(function () {
              hide_modal();
            }).fail(function (jqXHR, textStatus, errorThrown) {
              that.find('input#proxy-id')
                .closest('div.form-group')
                .addClass('has-error')
                .siblings('.error_placeholder')
                  .html(render_error(jqXHR, textStatus, errorThrown));
            });
          }());
          break;

        case 'network':
          (function() {
            var device_name = that.find('input#network-device-name').val();
            var mac_address = that.find('input#mac-address').val();
            mac_address = mac_address.toLowerCase();

            MAC_REGEX = /^([0-9a-f]{2}[:-]){5}([0-9a-f]{2})$/;
            if (!MAC_REGEX.test(mac_address)) {
              var error_html = render_error(null, null, 'MAC Address should be of the form \'71:50:FF:59:4C:1E\'.');

              that.find('input#mac-address')
                .closest('div.form-group')
                .addClass('has-error')
                .siblings('.error_placeholder')
                  .html(error_html);
              return;
            }

            net.post(sprintf('/api/device/mac-%s', mac_address), {
              type: 'network',
              name: device_name
            }).done(function () {
              hide_modal();
            }).fail(function (jqXHR, textStatus, errorThrown) {
              that.find('input#mac-address')
                .closest('div.form-group')
                .addClass('has-error')
                .siblings('.error_placeholder')
                  .html(render_error(jqXHR, textStatus, errorThrown));
            });
          }());
          break;
        }
      });
    });

    // Dialog: change room name

    $('div.main').on('click', 'div.room .room-change-name', function() {
      var room_id = $(this).closest('div.room').data('room-id');
      var room = cache.objects.room[room_id];

      dialog('script#room-change-name-dialog-template', room, function() {
        var room_name = $(this).find('input#room-name').val();
        net.post(sprintf('/api/room/%s', room_id), {
          name: room_name,
        }).always(hide_modal);
      });
    });

    // Dialog: delete room

    $('div.main').on('click', 'div.room .room-delete', function() {
      var room_id = $(this).closest('div.room').data('room-id');
      var room = cache.objects.room[room_id];

      dialog('script#delete-room-dialog-template', room, function() {
        net.del(sprintf('/api/room/%s', room_id)).always(hide_modal);
      });
    });

    // Dialog: device change room

    $('div.main').on('click', 'div.device .device-change-room', function() {
      var device_id = $(this).closest('div.device').data('device-id');
      var state = {rooms: cache.objects.room, device: cache.objects.device[device_id]};

      dialog('script#device-change-room-dialog-template', state, function() {
        var room_id = $(this).find('select#room').val();
        net.post(sprintf('/api/device/%s', device_id), {
          room: room_id
        }).always(hide_modal);
      });
    });

    // Dialog: change device name

    $('div.main').on('click', 'div.device .device-change-name', function() {
      var device_id = $(this).closest('div.device').data('device-id');
      var device = cache.objects.device[device_id];

      dialog('script#device-change-name-dialog-template', device, function() {
        var device_name = $(this).find('input#device-name').val();
        net.post(sprintf('/api/device/%s', device_id), {
          name: device_name,
        }).always(hide_modal);
      });
    });

    // Dialog: delete device

    $('div.main').on('click', 'div.device .device-delete', function() {
      var device_id = $(this).closest('div.device').data('device-id');
      var device = cache.objects.device[device_id];

      dialog('script#delete-device-dialog-template', device, function() {
        net.del(sprintf('/api/device/%s', device_id)).always(hide_modal);
      });
    });

    // Dialog: delete account

    $('div.main').on('click', 'div.account .delete-account', function() {
      var account_id = $(this).closest('div.account').data('account-id');
      var account = cache.objects.account[account_id];

      dialog('script#delete-account-dialog-template', account, function() {
        net.del(sprintf('/api/account/%s', account_id)).always(hide_modal);
      });
    });
  });

  return {
    net: net,
    cache: cache
  };
})();
