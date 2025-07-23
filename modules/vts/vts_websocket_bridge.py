import asyncio
import websockets
import json

VTS_WS_URL = "ws://localhost:8001"

async def send_vts_expression(expression_name):
    async with websockets.connect(VTS_WS_URL) as ws:
        message = {
            "apiName": "VTubeStudioPublicAPI",
            "messageType": "TriggerHotkey",
            "data": {
                "hotkeyID": expression_name
            }
        }
        await ws.send(json.dumps(message))
        response = await ws.recv()
        return json.loads(response)

def trigger_expression(expression_name):
    asyncio.run(send_vts_expression(expression_name))
