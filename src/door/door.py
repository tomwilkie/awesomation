import uuid

from common import client


def main():
  device_id = uuid.getnode()

  # ensure the device exists on the server
  client.AddDevice(device_id, name="Doorbell")
  
  # send an event
  client.DeviceEvent(device_id, "Doorbell")
  
  
if __name__ == '__main__':
  main()