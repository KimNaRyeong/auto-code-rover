import asyncio

# Stub for print_stacktrace function (paste here the function you've provided for consistency)
def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Simulated ASGI application
async def simulated_asgi_handler(receive, send):
    """
    A mockup of Django's ASGI handler function to process incoming ASGI messages.
    """
    try:
        while True:
            message = await receive()
            if message['type'] == 'http.request':
                body = message.get('body', b'')
                print(f"Received body: {body}")
                if not message.get('more_body', False):
                    break
            elif message['type'] == 'http.disconnect':
                raise AssertionError("http.disconnect received but not properly handled.")
        # Sending a mock response
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/plain'],
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': b'Hello, world!',
        })
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with an error code for unhandled disconnect
    except Exception as e:
        print_stacktrace(e)
        assert False, "Unexpected error occurred"

# Testing scenario
async def main():
    async def receive():
        """
        This simulates receiving ASGI messages from a client. First, it sends a part of the
        request body, then it simulates a disconnect.
        """
        await asyncio.sleep(0.1)  # Simulate delay
        yield {'type': 'http.request', 'body': b'some body', 'more_body': True}
        await asyncio.sleep(0.1)
        yield {'type': 'http.disconnect'}

    async def send(message):
        """
        A mock send callable to mimic sending responses back to the client in ASGI.
        """
        print(f"Sending message: {message}")

    receiver = receive()
    await simulated_asgi_handler(receiver.__anext__, send)

if __name__ == "__main__":
    asyncio.run(main())
