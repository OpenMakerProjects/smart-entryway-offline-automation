"""Optional local BLE GATT adapter; no cloud connection or credentials."""
import json
SERVICE="a0160000-1313-4444-8888-000000000016"
STATUS="a0160001-1313-4444-8888-000000000016"
CONTROL="a0160002-1313-4444-8888-000000000016"
def schema():
    from bless import GATTCharacteristicProperties as C,GATTAttributePermissions as P
    writable=getattr(P,"writable",None) or getattr(P,"writeable")
    return {SERVICE:{STATUS:{"Properties":C.read|C.notify,"Permissions":P.readable,"Value":bytearray(b"{}")},CONTROL:{"Properties":C.write,"Permissions":writable,"Value":bytearray()}}}
async def start(rule,loop):
    from bless import BlessServer
    server=BlessServer(name="Entryway16",loop=loop)
    server.read_request_func=lambda characteristic,**kwargs:characteristic.value
    def write(characteristic,value,**kwargs):
        if characteristic.uuid.lower()==CONTROL:
            if rule.command(bytes(value)):characteristic.value=bytearray(value)
    server.write_request_func=write
    await server.add_gatt(schema());await server.start();return server
def publish(server,record):
    characteristic=server.get_characteristic(STATUS)
    characteristic.value=bytearray(json.dumps(record,separators=(",",":")).encode())
    server.update_value(SERVICE,STATUS)
