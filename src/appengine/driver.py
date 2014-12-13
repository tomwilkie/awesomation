"""List drivers and send them commands."""
import flask

from appengine import device, user


# pylint: disable=invalid-name
blueprint = flask.Blueprint('driver', __name__)


@blueprint.route('/', methods=['GET'])
def list_drivers():
  """Return json list of drivers."""
  devices = [{'name': k} for k in device.DEVICE_TYPES.iterkeys()]
  return flask.jsonify(devices=devices)


@blueprint.route('/<driver>/command', methods=['POST'])
def driver_command(driver):
  """Using json body to send command to driver."""
  user_id = user.get_user()
  body = flask.request.get_json()
  if body is None:
    flask.abort(400, 'JSON body and mime type required.')

  driver = device.DEVICE_TYPES.get(driver, None)

  if not driver:
    flask.abort(404)

  driver.handle_static_command(user_id, body)

  return ('', 204)

